import pytest
from mara_app.app import MaraApp


@pytest.fixture()
def app():
    app = MaraApp()

    # configure app here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()



def test_navigation_bar(client: MaraApp):
    """A simple test checking if the /mara-app/navigation-bar call returns status code 200"""
    response = client.get('/mara-app/navigation-bar')
    assert response.status_code == 200


def test_configuration(client: MaraApp):
    """A simple test checking if the /mara-app/configuration call returns status code 200"""
    response = client.get('/mara-app/configuration')
    assert response.status_code == 200
