__author__ = 'vividhsv'

import pytest

create_user = True

@pytest.mark.usefixtures("testapp_login")
@pytest.mark.usefixtures("testapp")
class TestURLs:
    def test_home(self, testapp):
        rv = testapp.get('/')
        assert rv.status_code == 200

    def test_about(self, testapp):
        rv = testapp.get('/public/about')
        assert rv.status_code == 200

    def test_login(self, testapp):
        rv = testapp.get('/auth/login')
        assert rv.status_code == 200

    def test_logout(self, testapp):
        rv = testapp.get('auth/logout')
        assert rv.status_code == 302

    def test_register(self, testapp):
        rv = testapp.get('/auth/register')
        assert rv.status_code == 200

    def test_user_profile(self, testapp):
        rv = testapp.get('/admin')
        assert rv.status_code == 200

    def test_setting(self, testapp_login):
        rv = testapp_login.get('/user/settings')
        assert rv.status_code == 200

    def test_setting_profile(self, testapp_login):
        rv = testapp_login.get('/user/settings/profile')
        assert rv.status_code == 200

    def test_setting_change_password(self, testapp_login):
        rv = testapp_login.get('/user/settings/changepassword')
        assert rv.status_code == 200

    def test_setting_delete(self, testapp_login):
        rv = testapp_login.get('/user/settings/delete')
        assert rv.status_code == 200
