import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)
_original_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in‑memory activities dict after each test."""
    yield
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))


def test_get_activities():
    # Arrange
    # (no setup needed beyond fixture)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == _original_activities


def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"
    assert existing_email in activities[activity]["participants"]

    # Act
    response = client.post(
        f"/activities/{activity}/signup", params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_remove():
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"
    assert email in activities[activity]["participants"]

    # Act
    response = client.delete(
        f"/activities/{activity}/participants", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"
    assert email not in activities[activity]["participants"]
