from flask import Flask
from httpx import Client

from app import create_app


class AppContextMixin:
    app: Flask
    client: Client

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_app()
        cls.client: Client = Client(app=cls.app, base_url="http://localhost")

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.client is not None:
            cls.client.close()
