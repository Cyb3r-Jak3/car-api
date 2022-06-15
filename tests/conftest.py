import base64
import os

import pytest
from flask.testing import FlaskClient
from dotenv import load_dotenv

# Needs to be loaded before app for local testing using an .env file
load_dotenv()
from app import app


class TestClient(FlaskClient):
    def __init__(self):
        # load_dotenv()
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
            headers=self.auth_headers,
        )

    def authed_get(self, URL: str = "/", *args, **kwargs):
        return self.get(URL, headers=self.auth_headers, *args, **kwargs)


@pytest.fixture
def client():
    yield TestClient()
