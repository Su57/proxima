from flask import Flask
from httpx import Client

from app import create_app
from container import Container


class AppContextMixin:
    app: Flask
    client: Client
    container: Container

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_app()
        cls.container = getattr(cls.app, "container")
        cls.client: Client = Client(app=cls.app, base_url="http://localhost")

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.client is not None:
            cls.client.close()
        if cls.container is not None:
            cls.container.shutdown_resources()
            cls.container.unwire()

