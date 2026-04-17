import pytest
from fastapi.testclient import TestClient

from src import app as app_module
from src.app import app


@pytest.fixture(autouse=True)
def reset_activities():
    original = {
        activity_name: {
            **activity_data,
            "participants": list(activity_data["participants"]),
        }
        for activity_name, activity_data in app_module.activities.items()
    }
    yield
    app_module.activities.clear()
    app_module.activities.update(
        {
            activity_name: {
                **activity_data,
                "participants": list(activity_data["participants"]),
            }
            for activity_name, activity_data in original.items()
        }
    )


@pytest.fixture
def client():
    return TestClient(app)
