import datetime as dt
import pytest
from cas.user.models import User


@pytest.mark.usefixtures('testapp')
class TestUser:

    def test_created_at_defaults_to_datetime(self):
        user = User(username='foo', email='foo@bar.com', first_name='admin', last_name='admin')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self):
        user = User(username='foo', email='foo@bar.com', first_name='admin', last_name='admin')
        user.save()
        assert user.password is None

    def test_set_password(self):
        user = User(username='foo', email='foo@bar.com', first_name='admin', last_name='admin')
        user.set_password('foobarbaz123')
        user.save()
        assert user.password is not None
        assert user.check_password('foobarbaz123') is True
        assert user.check_password("barfoobaz") is False

    def test_check_password(self):
        user = User(username='foo', email='foo@bar.com', first_name='admin', last_name='admin', password='foobarbaz123')
        assert user.check_password('foobarbaz123') is True
        assert user.check_password("barfoobaz") is False

    def test_update(self):
        User.create(username='foo', email='foo@bar.com', first_name='admin', last_name='admin', password='foobarbaz123')
        user = User.query.filter_by(username='foo').first()
        User.update(user, username='hello')
        updated_user = User.query.filter_by(username='hello').first()
        assert updated_user.username == 'hello'
