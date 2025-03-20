from dependency_injector import providers
from pydantic_settings import BaseSettings


def create_config_adapter(settings: BaseSettings) -> providers.Configuration:
    config = providers.Configuration()
    for field_name, field_value in settings.model_dump().items():
        config.from_dict({field_name: field_value})
    return config
