# validator.py

import polars as pl
import pandera as pa
from pandera.errors import SchemaError
from schema_builder import build_default_template_schema, build_custom_template_schema

def _extract_check_message(column_name: str, schema: pa.DataFrameSchema) -> str:
    """
    Returns a human-readable error message based on the column checks.
    """
    column_schema = schema.columns.get(column_name)
    if not column_schema:
        return "Validation failed"

    check_msgs = []
    for check in column_schema.checks:
        if check.name == "str_matches":
            # Extract pattern from Check object (usually inside args)
            pattern = check.statistics.get("pattern", "invalid pattern")
            check_msgs.append(f"Value does not match pattern {pattern}")
        elif check.name == "isin":
            allowed = check.statistics.get("allowed_values", [])
            check_msgs.append(f"Value must be one of {allowed}")
        else:
            check_msgs.append(f"Failed check: {check.name}")

    return "; ".join(check_msgs) if check_msgs else "Validation failed"


def _format_error_report(error: SchemaError, schema: pa.DataFrameSchema) -> list[dict]:
    """
    Convert a SchemaError into structured user-friendly messages.
    """
    failure_cases = error.failure_cases

    try:
        df = pl.DataFrame(failure_cases)
        return [
            {
                "row": int(r["index"]),
                "column": r["column"],
                "error": _extract_check_message(r["column"], schema)
            }
            for r in df.iter_rows(named=True)
        ]
    except Exception:
        return [{"row": None, "column": None, "error": str(error)}]


def validate_default_template(df: pl.DataFrame, template_id: int):
    try:
        schema = build_default_template_schema(template_id)
        validated = schema.validate(df, lazy=True)
        return validated, None
    except SchemaError as err:
        return None, _format_error_report(err, schema)


def validate_custom_template(df: pl.DataFrame, custom_template_id: int):
    try:
        schema = build_custom_template_schema(custom_template_id)
        validated = schema.validate(df, lazy=True)
        return validated, None
    except SchemaError as err:
        return None, _format_error_report(err, schema)
