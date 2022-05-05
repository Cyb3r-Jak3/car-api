import os

import pytest
from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_bad_range(client):
    resp = client.post(
        "/api/submit",
        data={"BatteryPercentage": 100}
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False

    resp = client.post(
        "/api/submit",
        data={"BatteryRange": 100}
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False


def test_good_range(client):
    resp = client.post(
        "/api/submit",
        data={"BatteryPercentage": 100, "BatteryRange": 100}
    )
    assert resp.status_code == 200
    # assert resp.json["success"]


def test_good_trip(client):
    resp = client.post(
        "/api/submit",
        data={"miles": 10, "kwh": 3.5, "time": "0:15", "destination": "Flask Test"}
    )
    assert resp.status_code == 200
    # assert resp.json["success"]


def test_bad_trip(client):
    resp = client.post(
        "/api/submit",
        data={"kwh": 3.5, "time": "0:15", "destination": "Flask Test"}
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False

    resp = client.post(
        "/api/submit",
        data={"miles": 10, "time": "0:15", "destination": "Flask Test"}
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False

    resp = client.post(
        "/api/submit",
        data={"miles": 10, "kwh": 3.5, "destination": "Flask Test"}
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False

    resp = client.post(
        "/api/submit",
        data={"miles": 10, "kwh": 3.5, "time": "0:15"}
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False


def test_good_charge(client):
    resp = client.post(
        "/api/submit",
        data={"ChargeTime": "1:15:00", "ChargeAmount": 11.78}
    )
    assert resp.status_code == 200
    # assert resp.json["success"]


def test_bad_charge(client):
    resp = client.post(
        "/api/submit",
        data={"ChargeAmount": 11.78}
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False

    resp = client.post(
        "/api/submit",
        data={"ChargeTime": "1:15:00", }
    )
    assert resp.status_code == 400
    # assert resp.json["success"] is False


def test_range(client):
    resp = client.get("/range")
    assert resp.status_code == 200