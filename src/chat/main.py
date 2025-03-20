from fastapi import FastAPI

from src.core.containers.chat_container import ChatContainer
from src.main import base_container


def create_subapp(container_cls) -> FastAPI:
    subapp = FastAPI()
    subapp.container = container_cls(parent=base_container)
    return subapp


chat_app = create_subapp(ChatContainer)
