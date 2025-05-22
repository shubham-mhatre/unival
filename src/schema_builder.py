import polars as pl
import pandera as pa
from pandera.polars import Column, DataFrameSchema
from pandera import Check
from typing import Dict
from repository import (
    get_template_columns,
    get_column_mappings,
    get_custom_template,
)

# Corrected type map using valid Polars dtypes
TYPE_MAP = {
    "String": pl.Utf8,
    "Integer": pl.Int64,
    "Float": pl.Float64,
    "Boolean": pl.Boolean,
    "Date": pl.Date,
    "Datetime": pl.Datetime,
}

def build_column(dtype: pl.DataType, nullable: bool, regex: str | None = None) -> Column:
    checks = []
    if regex:
        checks.append(Check.str_matches(regex))
    return Column(dtype, nullable=nullable, checks=checks, coerce=True)

def build_default_template_schema(template_id: int) -> DataFrameSchema:
    columns = get_template_columns(template_id)
    if not columns:
        raise ValueError(f"No columns defined for template_id {template_id}")

    schema_dict = {}
    for col in columns:
        dtype = TYPE_MAP.get(col.data_type)
        if dtype is None:
            raise ValueError(f"Unsupported data type: {col.data_type} in column {col.column_name}")
        
        schema_dict[col.column_name] = build_column(
            dtype=dtype,
            nullable=not bool(col.is_required),
            regex=col.regex
        )

    return DataFrameSchema(schema_dict, coerce=True)

def build_custom_template_schema(custom_template_id: int) -> DataFrameSchema:
    mappings = get_column_mappings(custom_template_id)
    if not mappings:
        raise ValueError(f"No column mappings defined for custom_template_id {custom_template_id}")

    custom_template = get_custom_template(custom_template_id)
    base_template_id = custom_template.base_template_id

    base_columns = {col.column_name: col for col in get_template_columns(base_template_id)}
    schema_dict: Dict[str, Column] = {}

    for mapping in mappings:
        default_col = base_columns.get(mapping.default_column_name)
        if not default_col:
            continue

        dtype = TYPE_MAP.get(default_col.data_type)
        if dtype is None:
            raise ValueError(f"Unsupported data type: {default_col.data_type} in column {default_col.column_name}")

        schema_dict[mapping.user_column_name] = build_column(
            dtype=dtype,
            nullable=not bool(default_col.is_required),
            regex=default_col.regex
        )

    return DataFrameSchema(schema_dict, coerce=True)
