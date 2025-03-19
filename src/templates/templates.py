import os

from jinja2 import Environment, FileSystemLoader


def get_email_templates() -> Environment:
    local_path = os.path.dirname(__file__)
    templates = Environment(
        loader=FileSystemLoader(f"{local_path}/email_templates"), autoescape=True
    )
    return templates
