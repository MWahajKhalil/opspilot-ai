import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_device_service
from app.main import app
from app.services.device import DeviceService


@pytest.fixture
def client():
    service = DeviceService()
    app.dependency_overrides[get_device_service] = lambda: service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_devices(client):
    response = client.get("/devices")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Device 1", "status": "ok"},
        {"id": 2, "name": "Device 2", "status": "warning"},
    ]


def test_list_devices_filtered_by_status(client):
    response = client.get("/devices", params={"status": "warning"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 2, "name": "Device 2", "status": "warning"}
    ]


def test_list_devices_with_unknown_status_returns_empty_list(client):
    response = client.get("/devices", params={"status": "critical"})

    assert response.status_code == 200
    assert response.json() == []


def test_get_device(client):
    response = client.get("/devices/2")

    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "name": "Device 2",
        "status": "warning",
    }


def test_get_missing_device_returns_404(client):
    response = client.get("/devices/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Device not found"}


def test_invalid_device_id_returns_422(client):
    response = client.get("/devices/not-an-integer")

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["path", "device_id"]


def test_create_device_returns_201_and_persists(client):
    create_response = client.post(
        "/devices",
        json={"name": "Pump-17", "status": "ok"},
    )

    assert create_response.status_code == 201
    assert create_response.json() == {
        "id": 3,
        "name": "Pump-17",
        "status": "ok",
    }

    get_response = client.get("/devices/3")
    assert get_response.status_code == 200
    assert get_response.json() == create_response.json()


def test_create_device_missing_status_returns_422(client):
    response = client.post(
        "/devices",
        json={"name": "Incomplete Device"},
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "status"]
