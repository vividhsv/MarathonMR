# -*- coding: utf-8 -*-
from MarathonMR.app import create_app
from MarathonMR.config import ProdConfig, DevConfig, TestConfig


def test_production_config():
    app = create_app(ProdConfig)
    assert app.config['ENV'] == 'prod'
    assert app.config['DEBUG'] is False


def test_dev_config():
    app = create_app(DevConfig)
    assert app.config['ENV'] == 'dev'
    assert app.config['DEBUG'] is True


def test_test_config():
    app = create_app(TestConfig)
    assert app.config['ENV'] == 'test'
    assert app.config['DEBUG'] is True
