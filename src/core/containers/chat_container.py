from dependency_injector import containers, providers


class ChatContainer(containers.DeclarativeContainer):
    parent = providers.DependenciesContainer()
    pass
