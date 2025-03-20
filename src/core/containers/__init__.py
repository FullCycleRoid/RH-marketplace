from src.core.containers.auth_container import AuthContainer
from src.core.containers.base_container import BaseContainer
from src.core.containers.catalog_container import CatalogContainer
from src.core.containers.chat_container import ChatContainer
from src.core.containers.company_container import CompanyContainer
from src.core.containers.product_container import ProductContainer

base_container = BaseContainer()
auth_container = AuthContainer(parent=base_container)
catalog_container = CatalogContainer(parent=base_container)
product_container = ProductContainer(parent=base_container)
company_container = CompanyContainer(parent=base_container)
chat_container = ChatContainer(parent=base_container)
