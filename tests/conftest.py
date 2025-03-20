import pytest

from src.core.config.config import Config, create_config_adapter
from src.core.containers.base_container import BaseContainer


@pytest.fixture
def test_config():
    return Config(
        POSTGRES_USER="test",
        POSTGRES_PASSWORD="test",
        POSTGRES_HOST="localhost",
        POSTGRES_PORT=5432,
        POSTGRES_DB="test_db"
    )

@pytest.fixture
def container(test_config):
    config = create_config_adapter(test_config)
    return BaseContainer(config=config)