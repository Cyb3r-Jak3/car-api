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

    resp = client.post(
        "/api/submit",
        data={"BatteryRange": 100}
    )
    assert resp.status_code == 400


# def test_good_range(client):
#     resp = client.post(
#         "/api/submit",
#         data={"BatteryPercentage": 100, "BatteryRange": 100}
#     )
#     assert resp.status_code == 200
