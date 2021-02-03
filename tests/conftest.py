from base64 import b64encode

import pytest
from fastapi.testclient import TestClient

from ..main import app


@pytest.fixture(scope='session')
def app_():
    return app


@pytest.fixture
def client(app_):
    """
    Flask test client
    :return:
    """
    return TestClient(app_)


@pytest.fixture
def basic_auth_header():
    credentials = b64encode(b"admin:admin").decode("utf-8")
    return {"Authorization": "Basic " + credentials}
