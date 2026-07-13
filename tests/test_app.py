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
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    unregister_response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"

    activity = app_module.activities[activity_name]
    assert email not in activity["participants"]
