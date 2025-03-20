from dependency_injector import containers, providers


class ProductContainer(containers.DeclarativeContainer):
    parent = providers.DependenciesContainer()
    pass
