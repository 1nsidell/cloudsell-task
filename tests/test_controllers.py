import time

from fastapi.testclient import TestClient
import pytest

from app.main.main import make_app


app = make_app()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_returns_plans_successfully(client: TestClient) -> None:

    response = client.get("/api/cloud-sell/v1/pricing-plans?min_storage=50")

    assert response.status_code == 200  # noqa
    data = response.json()
    assert len(data) == 10  # noqa
    assert data[0]["provider"] == "Provider A"
    assert data[0]["storage_gb"] == 100  # noqa
    assert data[0]["price_per_gb"] == 0.02  # noqa


def test_returns_plans_not_found(client: TestClient) -> None:
    response = client.get(
        "/api/cloud-sell/v1/pricing-plans?min_storage=99999999999999999"
    )
    assert response.status_code == 404  # noqa


def test_returns_plans_pagination_error(client: TestClient) -> None:
    response = client.get("/api/cloud-sell/v1/pricing-plans?min_storage=-2")
    assert response.status_code == 422  # noqa


def test_create_and_get_order_successfully(client: TestClient) -> None:
    test_data = {"provider": "A", "storage_gb": 100}
    response = client.post("/api/cloud-sell/v1/orders", json=test_data)
    assert response.status_code == 201  # noqa
    response_data = response.json()
    assert "order_id" in response_data
    assert "status" in response_data
    assert response_data["status"] == "pending"
    time.sleep(1)

    status_response = client.get(
        f"/api/cloud-sell/v1/orders/{response_data['order_id']}"
    )
    assert status_response.status_code == 200  # noqa
    assert status_response.json()["status"] == "complete"
