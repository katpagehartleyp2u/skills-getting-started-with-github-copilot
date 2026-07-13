import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    for activity in app_module.activities.values():
        activity["participants"] = []
    yield
    for activity in app_module.activities.values():
        activity["participants"] = []


@pytest.fixture()
def client():
    return TestClient(app_module.app)


def test_unregister_participant_removes_email(client):
    signup_response = client.post("/activities/Chess Club/signup?email=student@example.com")
    assert signup_response.status_code == 200

    unregister_response = client.delete("/activities/Chess Club/signup?email=student@example.com")
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == "Removed student@example.com from Chess Club"

    activity = app_module.activities["Chess Club"]
    assert "student@example.com" not in activity["participants"]
