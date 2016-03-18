import os

from flask_script import Manager, Shell, Server
from flask_script.commands import ShowUrls

from MarathonMR.app import create_app
from MarathonMR.config import ProdConfig, DevConfig

if os.environ.get("ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    return {'app': app}


@manager.command
def test():
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

manager.add_command('server', Server(port=1234))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('urls', ShowUrls())


@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-p', '--port', dest='port', type=int, default=6969)
@manager.option('-w', '--workers', dest='workers', type=int, default=3)
def gunicorn(host, port, workers):
    """Start the Server with Gunicorn"""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {
                'bind': '{0}:{1}'.format(host, port),
                'workers': workers
            }

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()

if __name__ == '__main__':
    manager.run()

# To run coverage
# py.test --cov=MarathonMR tests/
