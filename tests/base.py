import unittest

import pytest
import requests
from fastapi.testclient import TestClient

from src.main import app
from tests.asserts import APIAssertMixin
from tests.mock_request import RequestInterceptor, MathByBaseUrl


class APITestCase(APIAssertMixin, unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup_request_box(self, monkeypatch):
        self.client = TestClient(app=app)

        _original_send = requests.Session.send

        self.mock_request = RequestInterceptor(
            real_http_send=_original_send,
            ignore_by=[
                MathByBaseUrl(value=self.client.base_url)
            ]
        )

        monkeypatch.setattr(requests.Session, "send", self.mock_request)

    @property
    def request_box(self):
        return self.mock_request.request_box

