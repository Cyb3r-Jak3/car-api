import base64
import pytest
import os
from app import app
from flask.testing import FlaskClient


class TestClient(FlaskClient):
    def __init__(self):
        self.auth_headers = {
            "Authorization": "Basic "
            + base64.b64encode(
                f"{os.environ['BASIC_AUTH_USER']}:{os.environ['BASIC_AUTH_PASS']}".encode(
                    "utf-8"
                )
            ).decode("utf-8")
        }
        self.api_link = "/api/submit"
        self.form = {
            "BatteryRange": "",
            "BatteryPercentage": "",
            "miles": "",
            "kwh": "",
            "time": "",
            "destination": "",
            "ChargeTime": "",
            "ChargeAmount": "",
        }
        self.application = app
        self.application.testing = True
        super().__init__(application=self.application)

    def submit_form(self, URL: str = "/", form_args: dict = None):
        return self.post(
            URL,
            data={key: form_args.get(key, val) for key, val in self.form.items()},
            headers=self.auth_headers
        )

    def authed_get(self, URL: str = "/", *args, **kwargs):
        return self.get(
            URL,
            headers=self.auth_headers,
            *args,
            **kwargs
        )


@pytest.fixture
def client():
    return TestClient()


def test_no_auth():
    resp = app.test_client().get("/")
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers


def test_index(client):
    resp = client.authed_get()
    assert resp.status_code == 200


def test_bad_range(client):
    resp = client.submit_form(
        "/api/submit",
        form_args={"BatteryPercentage": 100, "BatteryRange": ""},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False

    resp = client.submit_form(
        "/api/submit",
        form_args={"BatteryRange": 100, "BatteryPercentage": ""},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False


def test_good_range(client):
    resp = client.submit_form(
        "/api/submit",
        form_args={"BatteryPercentage": 100, "BatteryRange": 100},
    )
    assert resp.status_code == 200
    assert resp.json["success"]


def test_good_trip(client):
    resp = client.submit_form(
        "/api/submit",
        form_args={"miles": 10, "kwh": 3.5, "time": "0:15", "destination": "Flask Test"},
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

    resp = client.submit_form(
        "/api/submit",
        form_args={"miles": 10, "time": "0:15", "destination": "Flask Test"},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False

    resp = client.submit_form(
        "/api/submit",
        form_args={"miles": 10, "kwh": 3.5, "destination": "Flask Test"},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False

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
        "/api/submit", form_args={"ChargeAmount": 11.78},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False

    resp = client.submit_form(
        "/api/submit", form_args={"ChargeTime": "1:15:00"},
    )
    assert resp.status_code == 400
    assert resp.json["success"] is False


def test_range(client):
    resp = client.authed_get("/range")
    assert resp.status_code == 200


def test_range_no_auth():
    resp = app.test_client().get("/range")
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers


def test_trips(client):
    resp = client.authed_get("/trips",)
    assert resp.status_code == 200


def test_trips_no_auth():
    resp = app.test_client().get("/trips")
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers
