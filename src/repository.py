
from database import SessionLocal
from models import Template, TemplateColumn, CustomTemplate, ColumnMapping

def get_template_columns(template_id: int):
    session = SessionLocal()
    try:
        return session.query(TemplateColumn).filter_by(template_id=template_id).all()
    finally:
        session.close()

def get_custom_template(custom_template_id: int):
    session = SessionLocal()
    try:
        return session.query(CustomTemplate).filter_by(id=custom_template_id).first()
    finally:
        session.close()

def get_column_mappings(custom_template_id: int):
    session = SessionLocal()
    try:
        return session.query(ColumnMapping).filter_by(custom_template_id=custom_template_id).all()
    finally:
        session.close()

def get_template_by_name(app_id: int, template_name: str):
    session = SessionLocal()
    try:
        return session.query(Template).filter_by(application_id=app_id, template_name=template_name).first()
    finally:
        session.close()

def get_custom_template_by_name(app_id: int, template_name: str):
    session = SessionLocal()
    try:
        return session.query(CustomTemplate).filter_by(app_id=app_id, name=template_name).first()
    finally:
        session.close()
