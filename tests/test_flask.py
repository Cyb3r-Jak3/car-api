import os

from app import app


def test_no_auth():
    resp = app.test_client().get("/")
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers


def test_index(client):
    resp = client.authed_get()
    assert resp.status_code == 200


def test_good_range(client):
    resp = client.submit_form(
        "/api/submit",
        form_args={"BatteryPercentage": 100, "BatteryRange": 100},
    )
    assert resp.status_code == 200
    assert resp.json["success"]


def test_bad_range(client):
    resp = client.submit_form(
        "/api/submit",
        form_args={"BatteryPercentage": 100, "BatteryRange": ""},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False
    assert resp.json["error"] == "Need both battery percentage and battery range"

    resp = client.submit_form(
        "/api/submit",
        form_args={"BatteryRange": 100, "BatteryPercentage": ""},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False
    assert resp.json["error"] == "Need both battery percentage and battery range"


def test_good_trip(client):
    resp = client.submit_form(
        "/api/submit",
        form_args={
            "miles": 10,
            "kwh": 3.5,
            "time": "0:15",
            "destination": "Flask Test",
        },
    )
    assert resp.status_code == 200
    assert resp.json["success"]


def test_bad_trip(client):
    resp = client.submit_form(
        "/api/submit",
        form_args={"kwh": 3.5, "time": "0:15", "destination": "Flask Test"},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False
    assert resp.json["error"] == "Need all miles, kwh, and time filled out"

    resp = client.submit_form(
        "/api/submit",
        form_args={"miles": 10, "time": "0:15", "destination": "Flask Test"},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False
    assert resp.json["error"] == "Need all miles, kwh, and time filled out"

    resp = client.submit_form(
        "/api/submit",
        form_args={"miles": 10, "kwh": 3.5, "destination": "Flask Test"},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False
    assert resp.json["error"] == "Need all miles, kwh, and time filled out"

    resp = client.submit_form(
        "/api/submit",
        form_args={"miles": 10, "kwh": 3.5, "time": "0:15"},
    )
    assert resp.status_code == 200
    assert resp.json["success"]


def test_good_charge(client):
    resp = client.submit_form(
        "/api/submit",
        form_args={"ChargeTime": "1:15:00", "ChargeAmount": 11.78},
    )
    assert resp.status_code == 200
    assert resp.json["success"]


def test_bad_charge(client):
    resp = client.submit_form(
        "/api/submit",
        form_args={"ChargeAmount": 11.78},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False
    assert resp.json["error"] == "Need both ChargeTime and ChargeAmount filled out"

    resp = client.submit_form(
        "/api/submit",
        form_args={"ChargeTime": "1:15:00"},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False
    assert resp.json["error"] == "Need both ChargeTime and ChargeAmount filled out"


def test_range(client):
    resp = client.authed_get("/range")
    assert resp.status_code == 200


def test_range_no_auth():
    resp = app.test_client().get("/range")
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers


def test_trips(client):
    resp = client.authed_get(
        "/trips",
    )
    assert resp.status_code == 200


def test_trips_no_auth():
    resp = app.test_client().get("/trips")
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers


def test_good_secret_header(client):
    resp = client.get("/trips", headers={"X-SECRET-HEADER": os.getenv("SECRET_HEADER")})
    assert resp.status_code == 200


def test_bad_secret_header(client):
    resp = client.get("/trips", headers={"X-SECRET-HEADER": "PLEASE FAIL"})
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers


def test_status_endpoint(client):
    resp = client.authed_get("/status")
    assert resp.status_code == 200
    assert resp.json["Alive"]
