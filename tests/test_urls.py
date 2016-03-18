__author__ = 'vividhsv'

import pytest

create_user = True

@pytest.mark.usefixtures("testapp")
class TestURLs:
    def test_home(self, testapp):
        rv = testapp.get('/')
        assert rv.status_code == 200

    def test_about(self, testapp):
        rv = testapp.get('/about')
        assert rv.status_code == 200


