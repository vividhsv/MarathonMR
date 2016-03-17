__author__ = 'vividhsv'

import pytest

create_user = True


@pytest.mark.usefixture("testapp")
class TestLogin:

    def test_login(self, testapp):
        rv = testapp.post('/auth/login', data=dict(username='admin', password='password'), follow_redirects=True)
        assert rv.status_code == 200 and 'Your Profile' in str(rv.data) and 'logout' in str(rv.data)

    def test_login_without_username_password(self, testapp):
        rv = testapp.post('/auth/login', data=dict(username='', password=''), follow_redirects=True)
        assert rv.status_code == 200 and 'Username - This field is required.' in str(rv.data) and 'Password - This field is required.' in str(rv.data)

    def test_already_loggedin(self, testapp):
        rv = testapp.post('/auth/login', data=dict(username='admin', password='password'), follow_redirects=True)
        assert rv.status_code == 200 and 'profile' in str(rv.data) and 'logout' in str(rv.data)
        rv = testapp.get('/auth/login', follow_redirects=True)
        assert rv.status_code == 200 and 'You have already signed in as' in str(rv.data)

    def test_login_password_fail(self, testapp):
        rv = testapp.post('/auth/login', data=dict(username='admin', password='adm'), follow_redirects=True)
        assert rv.status_code == 200 and 'Invalid password' in str(rv.data)

    def test_login_username_fail(self, testapp):
        rv = testapp.post('/auth/login', data=dict(username='adm', password='password'), follow_redirects=True)
        assert rv.status_code == 200 and 'Uknown username' in str(rv.data)

    def test_logout(self, testapp):
        rv = testapp.post('/auth/login', data=dict(username='admin', password='password'), follow_redirects=True)
        assert rv.status_code == 200

        rv = testapp.get('/auth/logout', follow_redirects=True)
        assert rv.status_code == 200 and 'You have logged out.' in str(rv.data)


@pytest.mark.usefixture("testapp")
class TestSignup:

    def test_signup(self, testapp):
        rv = testapp.post('/auth/register', data=dict(username='test', first_name='test', last_name='test', email='test@test.com', password='password1', confirm='password1'), follow_redirects=True)
        assert rv.status_code == 200 and "Thank you for registering. You can now log in" in str(rv.data)

    def test_signup_password_not_matching(self, testapp):
        rv = testapp.post('/auth/register', data=dict(username='test', first_name='test', last_name='test', email='test@test.com', password='password1', confirm='password'), follow_redirects=True)
        assert rv.status_code == 200 and "Passwords must match" in str(rv.data)

    def test_signup_registered_username(self, testapp):
        rv = testapp.post('/auth/register', data=dict(username='admin', first_name='test', last_name='test', email='test1@test.com', password='password1', confirm='password1'), follow_redirects=True)
        assert rv.status_code == 200 and "Username already registered" in str(rv.data)

    def test_signup_registered_email(self, testapp):
        rv = testapp.post('/auth/register', data=dict(username='test', first_name='test', last_name='test', email='admin@admin.com', password='password1', confirm='password1'), follow_redirects=True)
        assert rv.status_code == 200 and "Email already registered" in str(rv.data)


@pytest.mark.usefixture("testapp")
class TestProfile:

    def test_loggedin_user_profile(self, testapp):
        rv = testapp.post('/auth/login', data=dict(username='admin', password='password'), follow_redirects=True)
        assert rv.status_code == 200 and 'profile' in str(rv.data) and 'logout' in str(rv.data)
        rv = testapp.get('/admin')
        assert rv.status_code == 200 and 'Edit Profile' in str(rv.data) and 'Admin Admin' in str(rv.data)

    def test_public_user_profile(self, testapp):
        rv = testapp.get('/admin')
        assert rv.status_code == 200 and 'Admin Admin' in str(rv.data)
        assert 'Edit Profile' not in str(rv.data)

    def test_nonexsisting_user_profile(self, testapp):
        rv = testapp.get('/notthere')
        assert rv.status_code == 404 and '404 Not Found' in str(rv.data)


@pytest.mark.usefixture("testapp_login")
@pytest.mark.usefixture("testapp")
class TestSettings:

    def test_settings_change_profile(self, testapp_login):
        rv = testapp_login.post('/user/settings', data=dict(username='testuser1', first_name='Test', last_name='User', email='testuser1@test.com'), follow_redirects=True)
        assert rv.status_code == 200
        rv = testapp_login.get('/testuser1')
        assert rv.status_code == 200 and 'Test User' in str(rv.data)

    def test_settings_change_to_existing_password(self, testapp, testapp_login):
        rv = testapp.post('/auth/register', data=dict(username='test', first_name='test', last_name='test', email='test@test.com', password='password', confirm='password'), follow_redirects=True)
        assert rv.status_code == 200 and "Thank you for registering. You can now log in" in str(rv.data)
        rv = testapp_login.post('/user/settings', data=dict(username='test', first_name='Test', last_name='User', email='testuser@test.com'), follow_redirects=True)
        assert rv.status_code == 200 and 'Username already registered' in str(rv.data)

    def test_settings_change_to_existing_email(self, testapp, testapp_login):
        rv = testapp.post('/auth/register', data=dict(username='test', first_name='test', last_name='test', email='test@test.com', password='password', confirm='password'), follow_redirects=True)
        assert rv.status_code == 200 and "Thank you for registering. You can now log in" in str(rv.data)
        rv = testapp_login.post('/user/settings', data=dict(username='testuser', first_name='Test', last_name='User', email='test@test.com'), follow_redirects=True)
        assert rv.status_code == 200 and 'Email already registered' in str(rv.data)

    def test_settings_change_username_validation(self, testapp, testapp_login):
        rv = testapp.post('/auth/register', data=dict(username='test', first_name='test', last_name='test', email='test@test.com', password='password', confirm='password'), follow_redirects=True)
        assert rv.status_code == 200 and "Thank you for registering. You can now log in" in str(rv.data)
        rv = testapp_login.post('/user/settings', data=dict(username='', first_name='Test', last_name='User', email='test@test.com'), follow_redirects=True)
        assert rv.status_code == 200 and 'Username - This field is required.' in str(rv.data)

    def test_settings_change_email_validation(self, testapp, testapp_login):
        rv = testapp.post('/auth/register', data=dict(username='test', first_name='test', last_name='test', email='test@test.com', password='password', confirm='password'), follow_redirects=True)
        assert rv.status_code == 200 and "Thank you for registering. You can now log in" in str(rv.data)
        rv = testapp_login.post('/user/settings', data=dict(username='testuser', first_name='Test', last_name='User', email=''), follow_redirects=True)
        assert rv.status_code == 200 and 'Email - This field is required.' in str(rv.data)

    def test_settings_change_username_and_login(self, testapp_login):
        rv = testapp_login.post('/user/settings', data=dict(username='testuser1', first_name='Test', last_name='User', email='testuser@test.com'), follow_redirects=True)
        assert rv.status_code == 200
        rv = testapp_login.get('/testuser1')
        assert rv.status_code == 200 and 'Test User' in str(rv.data)
        rv = testapp_login.get('/auth/logout', follow_redirects=True)
        assert rv.status_code == 200
        rv = testapp_login.post('/auth/login', data=dict(username='testuser1', password='password'), follow_redirects=True)
        assert rv.status_code == 200 and 'Signed in as <b>testuser1</b>' in str(rv.data)

    def test_settings_change_password(self, testapp_login):
        rv = testapp_login.post('/user/settings/changepassword', data=dict(old_password='password', new_password='password1', confirm='password1'), follow_redirects=True)
        assert rv.status_code == 200 and 'Password successfully changed' in str(rv.data)
        rv = testapp_login.get('/testuser')
        assert rv.status_code == 200 and 'Test User' in str(rv.data)
        rv = testapp_login.get('/auth/logout', follow_redirects=True)
        assert rv.status_code == 200
        rv = testapp_login.post('/auth/login', data=dict(username='testuser', password='password1'), follow_redirects=True)
        assert rv.status_code == 200 and 'Signed in as <b>testuser</b>' in str(rv.data)

    def test_settings_change_password_worng_old_password(self, testapp_login):
        rv = testapp_login.post('/user/settings/changepassword', data=dict(old_password='passwordw', new_password='password1', confirm='password1'), follow_redirects=True)
        assert rv.status_code == 200 and 'Invalid old password' in str(rv.data)

    def test_settings_change_password_not_matching(self, testapp_login):
        rv = testapp_login.post('/user/settings/changepassword', data=dict(old_password='password', new_password='password11', confirm='password1'), follow_redirects=True)
        assert rv.status_code == 200 and 'Passwords must match' in str(rv.data)


    def test_settings_delete(self, testapp_login):
        rv = testapp_login.get('/user/settings/delete')
        assert rv.status_code == 200 and 'Delete Account' in str(rv.data)
        rv = testapp_login.post('/user/settings/delete', follow_redirects=True)
        assert rv.status_code == 200 and 'Account Deleted' in str(rv.data) and 'Log-in' in str(rv.data)
        rv = testapp_login.get('/admin')
        assert rv.status_code == 404 and '404 Not Found' in str(rv.data)

