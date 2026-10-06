"""Tests for the Flask API."""

import pytest

from app.api import create_app


@pytest.fixture
def app_client():
    """Create a Flask test client."""

    application = create_app()
    application.config["TESTING"] = True

    with application.test_client() as test_client:
        yield test_client


def test_health(app_client):
    """Verify the health endpoint."""

    response = app_client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"


def test_migration_api(app_client):
    """Verify the BI migration endpoint."""

    payload = {
        "calculations": [
            {
                "name": "KPI_1",
                "formula": "SUM([Profit]) / SUM([Sales])",
            }
        ],
        "target_calculation": "KPI_1",
        "existing_dax": "SUM(Sales) / SUM(Profit)",
        "visual": {
            "visual_type": "bar",
            "dimensions": ["Region"],
            "measures": ["KPI_1"],
        },
    }

    response = app_client.post(
        "/api/migrate",
        json=payload,
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert "result" in data

    result = data["result"]

    assert result["is_corrected"] is True
    assert "predicted_dax" in result
    assert "confidence_score" in result
    assert "confidence_level" in result