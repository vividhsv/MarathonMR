import os

import pytest

from cas.config import TestConfig
from cas.app import create_app
from cas.database import db
from cas.user.models import User


@pytest.fixture()
def testapp(request):
    app = create_app(TestConfig)
    client = app.test_client()

    db.app = app
    db.create_all()

    if getattr(request.module, "create_user", True):
        admin = User('admin', 'Admin', 'Admin', 'admin@admin.com', 'password')
        db.session.add(admin)
        db.session.commit()

        def teardown():
            db.session.remove()
            db.drop_all()

        request.addfinalizer(teardown)

        return client


@pytest.fixture()
def testapp_login(request):
    app = create_app(TestConfig)
    client = app.test_client()

    db.app = app
    db.create_all()

    if getattr(request.module, "create_user", True):
        admin = User('testuser', 'Test', 'User', 'testuser@test.com', 'password')
        db.session.add(admin)
        db.session.commit()

        def teardown():
            db.session.remove()
            db.drop_all()

        request.addfinalizer(teardown)

        rv = client.post('/auth/login', data=dict(username='testuser', password='password'), follow_redirects=True)
        assert rv.status_code == 200

        return client