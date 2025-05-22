# template_resolver.py

from repository import get_template_by_name, get_custom_template_by_name

def resolve_template(app_id: int, template_name: str, is_custom: bool):
    """
    Resolve template metadata.
    
    Returns:
        (template_id: int, is_custom: bool)
    Raises:
        ValueError if template is not found.
    """
    if is_custom:
        custom_template = get_custom_template_by_name(app_id, template_name)
        if not custom_template:
            raise ValueError(f"Custom template '{template_name}' not found for app_id {app_id}.")
        return custom_template.id, True
    else:
        template = get_template_by_name(app_id, template_name)
        if not template:
            raise ValueError(f"Default template '{template_name}' not found for app_id {app_id}.")
        return template.id, False
