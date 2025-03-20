from dependency_injector import containers, providers


class CatalogContainer(containers.DeclarativeContainer):
    parent = providers.DependenciesContainer()
