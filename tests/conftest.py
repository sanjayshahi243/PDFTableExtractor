import pytest
from pdfExtractor import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_root_status_code(client):
    response = client.get("/")
    assert response.status_code == 200

def test_root_content_type(client):
    response = client.get("/")
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"

def test_root_not_found(client):
    response = client.get("/dummy")
    assert response.status_code == 404
