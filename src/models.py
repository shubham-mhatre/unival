from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()

class Application(Base):
    __tablename__ = 'am_applications'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class Template(Base):
    __tablename__ = 'am_templates'
    id = Column(Integer, primary_key=True)
    template_name = Column(String(50))
    application_id = Column(Integer, ForeignKey('am_applications.id'))

class TemplateColumn(Base):
    __tablename__ = 'am_templates_columns'
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey('am_templates.id'))
    column_name = Column(String(50))
    data_type = Column(Enum('String', 'Integer', 'Float', 'Date', 'Boolean'))
    is_required = Column(Boolean)
    regex = Column(Text)
    field_order = Column(Integer)

class CustomTemplate(Base):
    __tablename__ = 'am_custom_templates'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    base_template_id = Column(Integer, ForeignKey('am_templates.id'))
    app_id = Column(Integer, ForeignKey('am_applications.id'))

class ColumnMapping(Base):
    __tablename__ = 'am_custom_templates_column_mapping'
    id = Column(Integer, primary_key=True)
    custom_template_id = Column(Integer, ForeignKey('am_custom_templates.id'))
    user_column_name = Column(String(50))
    default_column_name = Column(String(50))
