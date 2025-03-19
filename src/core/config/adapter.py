from dependency_injector import providers
from pydantic_settings import BaseSettings


class PydanticSettingsAdapter:
    def __init__(self, settings: BaseSettings):
        self._settings = settings

    def get(self, key: str, default=None):
        return getattr(self._settings, key, default)


# Фабрика для создания адаптера
def create_config_adapter(settings: BaseSettings) -> providers.Configuration:
    adapter = PydanticSettingsAdapter(settings)
    config = providers.Configuration()
    for field_name, field_value in settings.model_dump().items():
        config.from_dict({field_name: field_value})
    return config
