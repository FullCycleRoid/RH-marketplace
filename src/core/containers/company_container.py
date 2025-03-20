from dependency_injector import containers, providers


class CompanyContainer(containers.DeclarativeContainer):
    parent = providers.DependenciesContainer()
