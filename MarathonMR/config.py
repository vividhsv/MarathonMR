import os
os_env = os.environ


class Config(object):
     SECRET_KEY = 'This is my secret key for the Flask forms'
     APP_DIR = os.path.abspath(os.path.dirname(__file__))
     PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
     BCRYPT_LOG_ROUNDS = 13
     ALLOWED_EXTENSIONS = set(['csv'])
     UPLOAD_FOLDER = 'uploads/'


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
    WTF_CSRF_ENABLED = True


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    WTF_CSRF_ENABLED = False
