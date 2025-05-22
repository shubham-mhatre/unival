# validator.py
import polars as pl
from schema_builder import build_default_template_schema, build_custom_template_schema
import re

def _extract_error_details(raw_error: dict) -> list[dict]:
    """
    Converts Pandera's SchemaErrors args[0] into a clean list of error dictionaries.
    """
    error_list = []

    failure_groups = raw_error.get("DATA", {}).get("DATAFRAME_CHECK", [])

    for group in failure_groups:
        column = group.get("column")
        check = group.get("check")
        err_msg = group.get("error", "")
        
        # Extract failing row indices from message using regex (fragile, but helps)
        match = re.findall(r"\{.*?\}", err_msg)
        for item in match:
            try:
                # Example: {'supplier_gstin': 'AAA'} -> get row value
                val = eval(item)  # safe-ish for simple dict
                error_list.append({
                    "column": column,
                    "check": check,
                    "error": f"Value '{val[column]}' failed validation: {check}"
                })
            except:
                continue

        # If pattern not matched, fallback to full error
        if not match:
            error_list.append({
                "column": column,
                "check": check,
                "error": err_msg
            })

    return error_list


def validate_default_template(df: pl.DataFrame, template_id: int):
    schema = build_default_template_schema(template_id)
    try:
        validated = schema.validate(df, lazy=True)
        return validated, None
    except Exception as err:
        return None, _extract_error_details(err.args[0])


def validate_custom_template(df: pl.DataFrame, custom_template_id: int):
    schema = build_custom_template_schema(custom_template_id)
    try:
        validated = schema.validate(df, lazy=True)
        return validated, None
    except Exception as err:
        return None, _extract_error_details(err.args[0])
