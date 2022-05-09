import base64
import pytest
from app import app

auth_headers = {'Authorization': 'Basic ' + base64.b64encode(b"user:password").decode("utf-8")}
app.testing = True


@pytest.fixture
def client():
    return app.test_client()


def test_no_auth():
    resp = app.test_client().get("/")
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers


def test_index(client):
    resp = client.get("/", headers=auth_headers)
    assert resp.status_code == 200


def test_bad_range(client):
    resp = client.post(
        "/api/submit",
        data={"BatteryPercentage": 100},
        headers=auth_headers
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False

    resp = client.post(
        "/api/submit",
        data={"BatteryRange": 100},
        headers=auth_headers
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False


def test_good_range(client):
    resp = client.post(
        "/api/submit",
        data={"BatteryPercentage": 100, "BatteryRange": 100},
        headers=auth_headers
    )
    assert resp.status_code == 200
    # assert resp.json["success"]


def test_good_trip(client):
    resp = client.post(
        "/api/submit",
        data={"miles": 10, "kwh": 3.5, "time": "0:15", "destination": "Flask Test"},
        headers=auth_headers
    )
    assert resp.status_code == 200
    # assert resp.json["success"]


def test_bad_trip(client):
    resp = client.post(
        "/api/submit",
        data={"kwh": 3.5, "time": "0:15", "destination": "Flask Test"},
        headers=auth_headers
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False

    resp = client.post(
        "/api/submit",
        data={"miles": 10, "time": "0:15", "destination": "Flask Test"},
        headers=auth_headers
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False

    resp = client.post(
        "/api/submit",
        data={"miles": 10, "kwh": 3.5, "destination": "Flask Test"},
        headers=auth_headers
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False

    resp = client.post(
        "/api/submit",
        data={"miles": 10, "kwh": 3.5, "time": "0:15"},
        headers=auth_headers
    )
    assert resp.status_code == 200
    # assert resp.json["success"] is False


def test_good_charge(client):
    resp = client.post(
        "/api/submit",
        data={"ChargeTime": "1:15:00", "ChargeAmount": 11.78},
        headers=auth_headers
    )
    assert resp.status_code == 200
    # assert resp.json["success"]


def test_bad_charge(client):
    resp = client.post(
        "/api/submit",
        data={"ChargeAmount": 11.78},
        headers=auth_headers
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False

    resp = client.post(
        "/api/submit",
        data={"ChargeTime": "1:15:00"},
        headers=auth_headers
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False


def test_range(client):
    resp = client.get("/range", headers=auth_headers)
    assert resp.status_code == 200


def test_range_no_auth():
    resp = app.test_client().get("/range")
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers


def test_trips(client):
    resp = client.get("/trips", headers=auth_headers)
    assert resp.status_code == 200


def test_trips_no_auth():
    resp = app.test_client().get("/trips")
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers
