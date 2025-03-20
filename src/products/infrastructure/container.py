from dependency_injector import containers, providers

from src.core.containers.base_container import BaseContainer


class Container(BaseContainer):

    another_service = providers.Singleton(lambda: "Another Service")
