from dependency_injector import containers, providers

from src.core.container import BaseContainer


class Container(BaseContainer):

    another_service = providers.Singleton(lambda: "Another Service")
