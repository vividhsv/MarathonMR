import os

import pytest

from MarathonMR.config import TestConfig
from MarathonMR.app import create_app


@pytest.fixture()
def testapp(request):
    app = create_app(TestConfig)
    client = app.test_client()
    return client