# -*- coding: utf-8 -*-
from cas.app import create_app
from cas.config import ProdConfig, DevConfig, TestConfig


def test_production_config():
    app = create_app(ProdConfig)
    assert app.config['ENV'] == 'prod'
    assert app.config['DEBUG'] is False
    # assert app.config['DEBUG_TB_ENABLED'] is False
    # assert app.config['ASSETS_DEBUG'] is False


def test_dev_config():
    app = create_app(DevConfig)
    assert app.config['ENV'] == 'dev'
    assert app.config['DEBUG'] is True
    # assert app.config['ASSETS_DEBUG'] is True


def test_test_config():
    app = create_app(TestConfig)
    assert app.config['ENV'] == 'test'
    assert app.config['DEBUG'] is True
    # assert app.config['ASSETS_DEBUG'] is True