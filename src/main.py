from file_reader import FileReader
import sys
from template_resolver import resolve_template
from validator import validate_custom_template, validate_default_template
import json

def main(csv_path: str, app_id: int, template_name: str, is_custom: bool):
    print("# # # # # # # # # # Starting UNIVAL # # # # # # # # # #")

    print(f"Reading file: {csv_path}")

    try:
        reader = FileReader(csv_path)
        df = reader.read()
        print(df)
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return    
    
    #resolve template : determine template id
    try:
        template_id, is_custom_template = resolve_template(app_id, template_name, is_custom)
    except ValueError as ve:
        print(str(ve))
        return

    print(f"Resolved template ID: {template_id}, is_custom: {is_custom_template}")

    if is_custom_template:
        try:
            validated_df, errors = validate_custom_template(df, template_id)
        except Exception as e:
            print("Unexpected validation error:", str(e))
            return
    else:
        try:
            validated_df, errors = validate_default_template(df, template_id)
        except Exception as e:
            print("Unexpected validation error:", str(e))
            return

    if errors:
        print("Validation Errors:")
        print(json.dumps(errors, indent=2))
    else:
        print("Validation Passed.")
        print(validated_df.head())


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python main.py <csv_path> <app_id> <template_name> [--custom]")
        sys.exit(1)

    csv_path = sys.argv[1]
    app_id = int(sys.argv[2])
    template_name = sys.argv[3]
    is_custom = "--custom" in sys.argv

    main(csv_path, app_id, template_name, is_custom)