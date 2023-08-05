"""Logic related to wrapping logic around the pydantic library."""
from __future__ import annotations

import itertools
from collections.abc import Iterable
from datetime import date, datetime
from typing import Any, ClassVar, Dict, List, Optional, Set, Type, TypeVar, Union

import polars as pl
from pydantic import BaseConfig, BaseModel, Field, create_model  # noqa: F401
from pydantic.main import ModelMetaclass as PydanticModelMetaclass
from typing_extensions import Literal, get_args

from patito.polars import DataFrame
from patito.validators import validate

try:
    import pandas as pd

    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False

# The generic type of a single row in given Relation.
# Should be a typed subclass of Model.
ModelType = TypeVar("ModelType", bound="Model")

# A mapping from pydantic types to the equivalent type used in DuckDB
PYDANTIC_TO_DUCKDB_TYPES = {
    "integer": "BIGINT",
    "string": "VARCHAR",
    "number": "DOUBLE",
    "boolean": "BOOLEAN",
}

# A mapping from pydantic types to equivalent dtypes used in polars
PYDANTIC_TO_POLARS_TYPES = {
    "integer": pl.Int64,
    "string": pl.Utf8,
    "number": pl.Float64,
    "boolean": pl.Boolean,
}


class ModelMetaclass(PydanticModelMetaclass):
    """
    Metclass used by patito.Model.

    Responsible for setting any relevant model-dependent class properties.
    """

    def __init__(cls, name: str, bases: tuple, clsdict: dict) -> None:
        """
        Construct new patito model.

        Args:
            name: Name of model class.
            bases: Tuple of superclasses.
            clsdict: Dictionary containing class properties.
        """
        super().__init__(name, bases, clsdict)  # type: ignore
        # Add a custom subclass of patito.DataFrame to the model class,
        # where .set_model() has been implicitly set.
        cls.DataFrame = DataFrame._construct_dataframe_model_class(
            model=cls,  # type: ignore
        )

    # --- Class properties ---
    # These properties will only be available on Model *classes*, not instantiated
    # objects This is backwards compatible to python versions before python 3.9,
    # unlike a combination of @classmethod and @property.
    @property
    def columns(cls: Type[ModelType]) -> List[str]:  # type: ignore
        """
        Return the name of the specified column fields the DataFrame.

        Returns:
            List of column names.
        """
        return list(cls.schema()["properties"].keys())

    @property
    def dtypes(  # type: ignore
        cls: Type[ModelType],
    ) -> dict[str, Type[pl.DataType]]:
        """
        Return the dtypes of the dataframe.

        Unless Field(dtype=...) is specified, the highest signed column dtype
        is chosen for integer and float columns.

        Returns:
            A dictionary mapping string column names to polars dtype classes.
        """
        return {
            column: valid_dtypes[0] for column, valid_dtypes in cls.valid_dtypes.items()
        }

    @property
    def valid_dtypes(  # type: ignore  # noqa: C901
        cls: Type[ModelType],
    ) -> dict[str, List[Type[pl.DataType]]]:
        """
        Return valid polars dtypes as a column name -> dtypes mapping.

        The first item of each list is the default dtype chosen by Patito.

        Returns:
            A dictionary mapping each column string name to a list of valid
            dtypes.

        Raises:
            NotImplementedError: If one or more model fields are annotated with types
                not compatible with polars.
        """
        schema = cls.schema()
        properties = schema["properties"]

        valid_dtypes = {}
        for column, props in properties.items():
            if "dtype" in props:
                valid_dtypes[column] = [
                    props["dtype"],
                ]
            elif "enum" in props:
                if props["type"] != "string":  # pragma: no cover
                    raise NotImplementedError
                valid_dtypes[column] = [pl.Categorical, pl.Utf8]
            elif "type" not in props:
                raise NotImplementedError(
                    f"No valid dtype mapping found for column '{column}'."
                )
            elif props["type"] == "integer":
                valid_dtypes[column] = [
                    pl.Int64,
                    pl.Int32,
                    pl.Int16,
                    pl.Int8,
                    pl.UInt64,
                    pl.UInt32,
                    pl.UInt16,
                    pl.UInt8,
                ]
            elif props["type"] == "number":
                if props.get("format") == "time-delta":
                    valid_dtypes[column] = [
                        pl.Duration,
                    ]  # pyright: reportPrivateImportUsage=false
                else:
                    valid_dtypes[column] = [pl.Float64, pl.Float32]
            elif props["type"] == "boolean":
                valid_dtypes[column] = [
                    pl.Boolean,
                ]
            elif props["type"] == "string":
                string_format = props.get("format")
                if string_format is None:
                    valid_dtypes[column] = [
                        pl.Utf8,
                    ]
                elif string_format == "date":
                    valid_dtypes[column] = [
                        pl.Date,
                    ]
                # TODO: Find out why this branch is not being hit
                elif string_format == "date-time":  # pragma: no cover
                    valid_dtypes[column] = [
                        pl.Datetime,
                    ]
            elif props["type"] == "null":
                valid_dtypes[column] = [
                    pl.Null,
                ]
            else:  # pragma: no cover
                raise NotImplementedError(
                    f"No valid dtype mapping found for column '{column}'"
                )

        return valid_dtypes

    @property
    def defaults(  # type: ignore
        cls: Type[ModelType],
    ) -> dict[str, Any]:
        """
        Return default field values specified on the model.

        Returns:
            Dictionary containing fields with their respective default values.
        """
        return {
            field_name: props["default"]
            for field_name, props in cls.schema()["properties"].items()
            if "default" in props
        }

    @property
    def non_nullable_columns(  # type: ignore
        cls: Type[ModelType],  # pyright: reportGeneralTypeIssues=false
    ) -> set[str]:
        """
        Return names of those columns that are non-nullable in the schema.

        Returns:
            Set of column name strings.
        """
        return set(cls.schema().get("required", {}))

    @property
    def nullable_columns(  # type: ignore
        cls: Type[ModelType],  # pyright: reportGeneralTypeIssues=false
    ) -> set[str]:
        """
        Return names of those columns that are nullable in the schema.

        Returns:
            Set of column name strings.
        """
        return set(cls.columns) - cls.non_nullable_columns

    @property
    def unique_columns(  # type: ignore
        cls: Type[ModelType],
    ) -> set[str]:
        """
        Return columns with uniqueness constraint.

        Returns:
            Set of column name strings.
        """
        props = cls.schema()["properties"]
        return {column for column in cls.columns if props[column].get("unique", False)}

    @property
    def sql_types(  # type: ignore
        cls: Type[ModelType],
    ) -> dict[str, str]:
        """
        Return SQL types as a column name -> sql type dict mapping.

        Returns:
            Dictionary with column name keys and SQL type identifier strings.
        """
        from patito.duckdb import _enum_type_name

        schema = cls.schema()
        props = schema["properties"]
        types = {}
        for column, props in schema["properties"].items():
            if "enum" in props:
                types[column] = _enum_type_name(field_properties=props)
            else:
                types[column] = PYDANTIC_TO_DUCKDB_TYPES[props["type"]]
        return types


class Model(BaseModel, metaclass=ModelMetaclass):
    """Custom pydantic class for representing table schema and constructing rows."""

    # -- Class properties set by model metaclass --
    # This weird combination of a MetaClass + type annotation
    # in order to make the following work simultaneously:
    #     1. Make these dynamically constructed properties of the class.
    #     2. Have the correct type information for type checkers.
    #     3. Allow sphinx-autodoc to construct correct documentation.
    #     4. Be compatible with python 3.7.
    # Once we drop support for python 3.7, we can replace all of this with just a simple
    # combination of @property and @classmethod.
    columns: ClassVar[List[str]]

    unique_columns: ClassVar[Set[str]]
    non_nullable_columns: ClassVar[Set[str]]
    nullable_columns: ClassVar[Set[str]]

    dtypes: ClassVar[Dict[str, Type[pl.DataType]]]
    sql_types: ClassVar[Dict[str, str]]
    valid_dtypes: ClassVar[Dict[str, List[Type[pl.DataType]]]]

    defaults: ClassVar[Dict[str, Any]]

    @classmethod
    @property
    def DataFrame(cls: Type[ModelType]) -> Type[DataFrame[ModelType]]:  # type: ignore
        """Return DataFrame class where DataFrame.set_model() is set to self."""

    @classmethod
    def from_row(
        cls: Type[ModelType],
        row: Union["pd.DataFrame", pl.DataFrame],
        validate: bool = True,
    ) -> ModelType:
        """
        Represent a single data frame row as a patito model.

        Args:
            row: A dataframe, either polars and pandas, consisting of a single row.
            validate: If False, skip pydantic validation of the given row data.

        Returns:
            A patito model representing the given row data.

        Raises:
            TypeError: If the given type is neither a pandas or polars DataFrame.
        """
        if isinstance(row, pl.DataFrame):
            dataframe = row
        elif _PANDAS_AVAILABLE and isinstance(row, pd.DataFrame):
            dataframe = pl.DataFrame._from_pandas(row)
        elif _PANDAS_AVAILABLE and isinstance(row, pd.Series):
            return cls(**dict(row.iteritems()))
        else:
            raise TypeError(f"{cls.__name__}.from_row not implemented for {type(row)}.")
        return cls.from_polars(dataframe=dataframe, validate=validate)

    @classmethod
    def from_polars(
        cls: Type[ModelType],
        dataframe: pl.DataFrame,
        validate: bool = True,
    ) -> ModelType:
        """
        Construct model from a single polars row.

        Args:
            dataframe: A polars dataframe consisting of one single row.
            validate: If True, run the pydantic validators. If False, pydantic will
                not cast any types in the resulting object.

        Returns:
            A pydantic model object representing the given polars row.

        Raises:
            TypeError: If the provided `dataframe` argument is not of type
                polars.DataFrame.
            ValueError: If the given `dataframe` argument does not consist of exactly
                one row.
        """
        if not isinstance(dataframe, pl.DataFrame):
            raise TypeError(
                f"{cls.__name__}.from_polars() must be invoked with polars.DataFrame, "
                f"not {type(dataframe)}!"
            )
        elif len(dataframe) != 1:
            raise ValueError(
                f"{cls.__name__}.from_polars() can only be invoked with exactly "
                f"1 row, while {len(dataframe)} rows were provided."
            )

        # We have been provided with a single polars.DataFrame row
        # Convert to the equivalent keyword invocation of the pydantic model
        if validate:
            return cls(**dataframe.to_dicts()[0])
        else:
            return cls.construct(**dataframe.to_dicts()[0])

    @classmethod
    def validate(  # type: ignore
        cls,
        dataframe: Union["pd.DataFrame", pl.DataFrame],
    ) -> None:
        """
        Validate the given dataframe.

        Args:
            dataframe: Polars DataFrame to be validated.

        Raises:
            patito.exceptions.ValidationError:  # noqa: DAR402
                If the given dataframe does not match the given schema.
        """
        validate(dataframe=dataframe, schema=cls)

    @classmethod
    def example_value(  # noqa: C901
        cls,
        field: str,
    ) -> Union[date, datetime, float, int, str, None]:
        """
        Return an example value for the given field name defined on the model.

        Args:
            field: Field name identifier.

        Returns:
            A single value which is consistent with the given field definition.

        Raises:
            NotImplementedError: If the given field has no example generator.
        """
        schema = cls.schema()
        field_data = schema["properties"]
        non_nullable = schema["required"]
        properties = field_data[field]
        field_type = properties["type"]
        if "const" in properties:
            # The default value is the only valid value, provided as const
            return properties["const"]

        elif "default" in properties:
            # A default value has been specified in the model field definition
            return properties["default"]

        elif field not in non_nullable:
            return None

        elif "enum" in properties:
            return properties["enum"][0]

        elif field_type in {"integer", "number"}:
            # For integer and float types we must check if there are imposed bounds
            lower = properties.get("minimum") or properties.get("exclusiveMinimum")
            upper = properties.get("maximum") or properties.get("exclusiveMaximum")

            # If the dtype is an unsigned integer type, we must return a positive value
            if "dtype" in properties:
                dtype = properties["dtype"]
                if dtype in (pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64):
                    lower = 0 if lower is None else max(lower, 0)

            # First we check the simple case, no upper or lower bound
            if lower is None and upper is None:
                if field_type == "number":
                    return -0.5
                else:
                    return -1

            # If we have a lower and upper bound, we return something in the middle
            elif lower is not None and upper is not None:
                if field_type == "number":
                    return (lower + upper) / 2
                else:
                    return (lower + upper) // 2

            # What remains is a single-sided bound, which we will return a value on the
            # "right side" of.
            number = float if field_type == "number" else int
            if lower is not None:
                return number(lower + 1)
            else:
                return number(upper - 1)

        elif field_type == "string":
            if "pattern" in properties:
                raise NotImplementedError(
                    "Example data generation has not been implemented for regex "
                    "patterns. You must valid data for such columns explicitly!"
                )
            elif "format" in properties and properties["format"] == "date":
                return date(year=1970, month=1, day=1)
            elif "format" in properties and properties["format"] == "date-time":
                return datetime(year=1970, month=1, day=1)
            elif "minLength" in properties:
                return "a" * properties["minLength"]
            elif "maxLength" in properties:
                return "a" * min(properties["maxLength"], 1)
            else:
                return "dummy_string"

        elif field_type == "boolean":
            return False

        else:  # pragma: no cover
            raise NotImplementedError

    @classmethod
    def example(
        cls: Type[ModelType],
        **kwargs: Any,  # noqa: ANN401
    ) -> ModelType:
        """
        Produce model with dummy data for all unspecified fields.

        The type annotation of unspecified field is used to fill in type-correct
        dummy data, e.g. -1 for int, "dummy_string" for str, and so on...
        The first item of Literal annotatations are used for dummy values.

        Args:
            **kwargs: Provide explicit values for any fields which should not be filled
                with dummy data.

        Returns:
            A pydantic model object filled with dummy data for all unspecified model
                fields.

        Raises:
            TypeError: If one or more of the provided keyword arguments do not match any
                fields on the model.
        """
        # Non-iterable values besides strings must be repeated
        wrong_columns = set(kwargs.keys()) - set(cls.columns)
        if wrong_columns:
            raise TypeError(f"{cls.__name__} does not contain fields {wrong_columns}!")

        schema = cls.schema()
        properties = schema["properties"]
        new_kwargs = {}
        for field_name in properties.keys():
            if field_name in kwargs:
                # The value has been explicitly specified
                new_kwargs[field_name] = kwargs[field_name]
            else:
                new_kwargs[field_name] = cls.example_value(field=field_name)
        return cls(**new_kwargs)

    @classmethod
    def pandas_examples(
        cls: Type[ModelType],
        data: Union[dict, Iterable],
        columns: Optional[Iterable[str]] = None,
    ) -> "pd.DataFrame":
        """
        Generate dataframe with dummy data for all unspecified columns.

        Offers the same API as the pandas.DataFrame constructor.
        Non-iterable values, besides strings, are repeated until they become as long as
        the iterable arguments.

        Args:
            data: Data to populate the dummy dataframe with. If
                not a dict, column names must also be provided.
            columns: Ignored if data is a dict. If
                data is an iterable, it will be used as the column names in the
                resulting dataframe. Defaults to None.

        Returns:
            A pandas DataFrame filled with dummy example data.

        Raises:
            ImportError: If pandas has not been installed. You should install
                patito[pandas] in order to integrate patito with pandas.
            TypeError: If column names have not been specified in the input data.
        """
        if not _PANDAS_AVAILABLE:
            # Re-trigger the import error, but this time don't catch it
            raise ImportError("No module named 'pandas'")

        if not isinstance(data, dict):
            if columns is None:
                raise TypeError(
                    f"{cls.__name__}.pandas_examples() must "
                    "be provided with column names!"
                )
            kwargs = dict(zip(columns, zip(*data)))
        else:
            kwargs = data

        kwargs = {
            key: (
                value
                if isinstance(value, Iterable) and not isinstance(value, str)
                else itertools.cycle([value])
            )
            for key, value in kwargs.items()
        }
        dummies = []
        for values in zip(*kwargs.values()):
            dummies.append(cls.example(**dict(zip(kwargs.keys(), values))))
        return pd.DataFrame([dummy.dict() for dummy in dummies])

    @classmethod
    def examples(
        cls: Type[ModelType],
        data: Optional[Union[dict, Iterable]] = None,
        columns: Optional[Iterable[str]] = None,
    ) -> pl.DataFrame:
        """
        Generate polars dataframe with dummy data for all unspecified columns.

        This constructor accepts the same data format as polars.DataFrame.

        Args:
            data: Data to populate the dummy dataframe with. If given as an iterable of
                values then column names must also be provided. If not provided at all,
                an empty dataframe with the correct column dtypes will be generated
                instead.
            columns: Ignored if data is a dict. If data is an iterable, it will be used
                as the column names in the resulting dataframe. Defaults to None.

        Returns:
            A polars dataframe where all unspecified columns have been filled with dummy
                data which should pass model validation.

        Raises:
            TypeError: If one or more of the model fields are not mappable to polars
                column dtype equivalents.
        """
        if data is None:
            # We should create an empty dataframe, but with the correct dtypes
            kwargs = {}
        elif not isinstance(data, dict):
            if columns is None:
                raise TypeError(
                    f"{cls.__name__}.examples() must be provided with column names!"
                )
            kwargs = dict(zip(columns, zip(*data)))
        else:
            kwargs = data

        wrong_columns = set(kwargs.keys()) - set(cls.columns)
        if wrong_columns:
            raise TypeError(f"{cls.__name__} does not contain fields {wrong_columns}!")

        series: List[Union[pl.Series, pl.Expr]] = []
        unique_series = []
        for column_name, dtype in cls.dtypes.items():
            if column_name not in kwargs:
                if column_name in cls.unique_columns:
                    unique_series.append(
                        pl.first().cumcount().cast(dtype).alias(column_name)
                    )
                else:
                    example_value = cls.example_value(field=column_name)
                    series.append(pl.lit(example_value, dtype=dtype).alias(column_name))
                continue

            value = kwargs.get(column_name)
            if isinstance(value, Iterable) and not isinstance(value, str):
                # We make sure that at least one series is inserted first in the list,
                # otherwise polars will not be able to handle the shape mismatch between
                # series and literate values.
                series.insert(0, pl.Series(name=column_name, values=value, dtype=dtype))
            else:
                series.append(pl.lit(value, dtype=dtype).alias(column_name))

        return (
            pl.DataFrame()
            .with_columns(series)  # type: ignore
            .with_columns(unique_series)
        )

    @classmethod
    def join(
        cls: Type["Model"],
        other: Type["Model"],
        how: Literal["inner", "left", "outer", "asof", "cross", "semi", "anti"],
    ) -> Type["Model"]:
        """
        Dynamically create a new model compatible with a SQL Join operation.

        For instance, `ModelA.join(ModelB, how="left")` will create a model containing
        all the fields of `ModelA` and `ModelB`, but where all fields of `ModelB` has
        been made `Optional`, i.e. nullable. This is consistent with the LEFT JOIN
        SQL operation making all the columns of the right table nullable.

        Args:
            other: Another patito Model class.
            how: The type of SQL Join operation.

        Returns:
            A new model type compatible with the resulting schema produced by the given
              join operation.

        Examples:
            >>> class A(Model):
            ...     a: int

            >>> class B(Model):
            ...     b: int

            >>> InnerJoinedModel = A.join(B, how="inner")
            >>> InnerJoinedModel.columns
            ['a', 'b']
            >>> InnerJoinedModel.nullable_columns
            set()

            >>> LeftJoinedModel = A.join(B, how="left")
            >>> LeftJoinedModel.nullable_columns
            {'b'}

            >>> OuterJoinedModel = A.join(B, how="outer")
            >>> sorted(OuterJoinedModel.nullable_columns)
            ['a', 'b']

            >>> A.join(B, how="anti") is A
            True
        """
        if how in {"semi", "anti"}:
            return cls

        kwargs: Dict[str, Any] = {}
        for model, nullable_methods in (
            (cls, {"outer"}),
            (other, {"left", "outer", "asof"}),
        ):
            for field_name, field in model.__fields__.items():
                field_type = field.type_
                field_default = field.default
                if how in nullable_methods and type(None) not in get_args(field.type_):
                    # This originally non-nullable field has become nullable
                    field_type = Optional[field_type]
                elif field.required and field_default is None:
                    # We need to replace Pydantic's None default value with ... in order
                    # to make it clear that the field is still non-nullable and
                    # required.
                    field_default = ...
                kwargs[field_name] = (field_type, field_default)

        return create_model(
            f"{cls.__name__}{how.capitalize()}Join{other.__name__}",
            **kwargs,
            __base__=Model,
        )

    @classmethod
    def select(
        cls: Type[ModelType], fields: Union[str, Iterable[str]]
    ) -> Type["Model"]:
        """
        Create a new model consisting of only a subset of the model fields.

        Args:
            fields: A single field name as a string, or a set of fields as a collection
                of strings.

        Returns:
            A new model containing only the fields specified by `fields`.

        Raises:
            ValueError: If one or more non-existent fields are selected.

        Example:
            >>> class MyModel(Model):
            ...     a: int
            ...     b: int
            ...     c: int

            >>> MyModel.select("a").columns
            ['a']

            >>> sorted(MyModel.select(["b", "c"]).columns)
            ['b', 'c']
        """
        if isinstance(fields, str):
            fields = [fields]

        fields = set(fields)
        non_existent_fields = fields - set(cls.columns)
        if non_existent_fields:
            raise ValueError(
                f"The following selected fields do not exist: {non_existent_fields}"
            )

        mapping = {field_name: field_name for field_name in fields}
        return cls._derive_model(
            model_name=f"Selected{cls.__name__}", field_mapping=mapping
        )

    @classmethod
    def drop(cls: Type[ModelType], name: Union[str, Iterable[str]]) -> Type["Model"]:
        """
        Return a new model where one or more fields are excluded.

        Args:
            name: A single string field name, or a list of such field names,
                which will be dropped.

        Returns:
            New model class where the given fields have been removed.

        Examples:
            >>> class MyModel(Model):
            ...     a: int
            ...     b: int
            ...     c: int

            >>> MyModel.drop("c").columns
            ['a', 'b']

            >>> MyModel.drop(["b", "c"]).columns
            ['a']
        """
        dropped_columns = {name} if isinstance(name, str) else set(name)
        mapping = {
            field_name: field_name
            for field_name in cls.columns
            if field_name not in dropped_columns
        }
        return cls._derive_model(
            model_name=f"Dropped{cls.__name__}",
            field_mapping=mapping,
        )

    @classmethod
    def prefix(cls: Type[ModelType], prefix: str) -> Type["Model"]:
        """
        Return a new model where all field names have been prefixed.

        Args:
            prefix: String prefix to add to all field names.

        Returns:
            New model class with all the same fields only prefixed with the given prefix.

        Example:
            >>> class MyModel(Model):
            ...     a: int
            ...     b: int

            >>> MyModel.prefix("x_").columns
            ['x_a', 'x_b']
        """
        mapping = {f"{prefix}{field_name}": field_name for field_name in cls.columns}
        return cls._derive_model(
            model_name="Prefixed{cls.__name__}",
            field_mapping=mapping,
        )

    @classmethod
    def suffix(cls: Type[ModelType], suffix: str) -> Type["Model"]:
        """
        Return a new model where all field names have been suffixed.

        Args:
            suffix: String suffix to add to all field names.

        Returns:
            New model class with all the same fields only suffixed with the given
                suffix.

        Example:
            >>> class MyModel(Model):
            ...     a: int
            ...     b: int

            >>> MyModel.suffix("_x").columns
            ['a_x', 'b_x']
        """
        mapping = {f"{field_name}{suffix}": field_name for field_name in cls.columns}
        return cls._derive_model(
            model_name="Suffixed{cls.__name__}",
            field_mapping=mapping,
        )

    @classmethod
    def rename(cls: Type[ModelType], mapping: Dict[str, str]) -> Type["Model"]:
        """
        Return a new model class where the specified fields have been renamed.

        Args:
            mapping: A dictionary where the keys are the old field names
                and the values are the new names.

        Returns:
            A new model class where the given fields have been renamed.

        Raises:
            ValueError: If non-existent fields are renamed.

        Example:
            >>> class MyModel(Model):
            ...     a: int
            ...     b: int

            >>> MyModel.rename({"a": "A"}).columns
            ['b', 'A']
        """
        non_existent_fields = set(mapping.keys()) - set(cls.columns)
        if non_existent_fields:
            raise ValueError(
                f"The following fields do not exist for renaming: {non_existent_fields}"
            )
        field_mapping = {
            field_name: field_name
            for field_name in cls.columns
            if field_name not in mapping
        }
        field_mapping.update({value: key for key, value in mapping.items()})
        return cls._derive_model(
            model_name=f"Renamed{cls.__name__}",
            field_mapping=field_mapping,
        )

    @classmethod
    def with_fields(
        cls: Type[ModelType],
        **field_definitions: Any,  # noqa: ANN401
    ) -> Type["Model"]:
        """
        Return a new model class where the given fields have been added.

        Args:
            **field_definitions: the keywords are of the form:
                field_name=(field_type, field_default)
                Specify `...` if no default value is provided.
                For instance, column_name=(int, ...) will create a new non-optional
                integer field named "column_name".

        Returns:
            A new model with all the original fields and the additional field
            definitions.

        Examples:
            >>> class MyModel(Model):
            ...     a: int

            >>> class ExpandedModel(MyModel):
            ...     b: int

            >>> MyModel.with_fields(b=(int, ...)).columns == ExpandedModel.columns
            True
        """
        fields = {field_name: field_name for field_name in cls.columns}
        fields.update(field_definitions)
        return cls._derive_model(
            model_name=f"Expanded{cls.__name__}",
            field_mapping=fields,
        )

    @classmethod
    def _derive_model(
        cls: Type[ModelType],
        model_name: str,
        field_mapping: Dict[str, Any],
    ) -> Type["Model"]:
        """
        Derive a new model with new field definitions.

        Args:
            model_name: Name of new model class.
            field_mapping: A mapping where the keys represent field names and the values
                represent field definitions. String field definitions are used as
                pointers to the original fields by name. Otherwise, specify field
                definitions as (field_type, field_default) as accepted by
                pydantic.create_model.

        Returns:
            A new model class derived from the model type of self.
        """
        new_fields = {}
        for new_field_name, field_definition in field_mapping.items():
            if isinstance(field_definition, str):
                # A single string, interpreted as the name of a field on the existing
                # model.
                old_field = cls.__fields__[field_definition]
                field_type = old_field.type_
                field_default = old_field.default
                if old_field.required and field_default is None:
                    # The default None value needs to be replaced with ... in order to
                    # make the field required in the new model.
                    field_default = ...
                new_fields[new_field_name] = (field_type, field_default)
            else:
                # We have been given a (field_type, field_default) tuple defining the
                # new field directly.
                new_fields[new_field_name] = field_definition
        return create_model(  # type: ignore
            __model_name=model_name,
            __validators__={"__validators__": cls.__validators__},
            __base__=Model,
            **new_fields,
        )
