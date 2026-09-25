import httpx
import pytest

from fastapi.testclient import TestClient

from app.dependencies import get_device_repository, get_http_client
from app.main import app
from app.repositories.device import DeviceRepository
from app.schemas.device import DeviceCreate




# @pytest.fixture
# def client():
#     repository = DeviceRepository()

#     transport = httpx.MockTransport(fake_temperature_service)
#     http_client = httpx.AsyncClient(transport=transport)

#     app.dependency_overrides[get_device_repository] = lambda: repository
#     app.dependency_overrides[get_http_client] = lambda: http_client

#     with TestClient(app) as test_client:
#         yield test_client
    
#     http_client.close()
#     app.dependency_overrides.clear()

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("OPSPILOT_API_KEY", "test-api-key")

    
    repository = DeviceRepository() 
    transport = httpx.MockTransport(fake_temperature_service)

    async def get_test_http_client():
        async with httpx.AsyncClient(transport=transport) as http_client:
            yield http_client

    app.dependency_overrides[get_device_repository] = lambda: repository
    app.dependency_overrides[get_http_client] = get_test_http_client

    with TestClient(app, headers={"X-API-Key": "test-api-key"}) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


#unauthorired access we are not passing api key here because we are testing the authentication middleware
#which will return 401 if the api key is not present
def test_devices_require_api_key(monkeypatch):
    monkeypatch.setenv("OPSPILOT_API_KEY", "test-api-key")

    with TestClient(app) as unauthenticated_client:
        response = unauthenticated_client.get("/devices")


    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid or missing API key"
    }


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
    assert response.json() == {"detail": "Device with id 999 not found"}


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


def test_create_device_repo():
    repository = DeviceRepository()
    create_response = repository.create_device(
        DeviceCreate(name="Pump-17", status="ok")
    )

    assert create_response.model_dump() == {
        "id": 3,
        "name": "Pump-17",
        "status": "ok",
    }




def fake_temperature_service(
    request: httpx.Request,
    )-> httpx.Response:
    
    url = str(request.url)

    assert url in ("http://localhost:9000/devices/1/temperature", "http://localhost:9000/devices/2/temperature", "http://localhost:9000/devices/3/temperature", "http://localhost:9000/devices/4/temperature","http://localhost:9000/devices/5/temperature" )


    if request.url.path == "/devices/1/temperature":
        return httpx.Response(
            status_code=200,
            json={ 
            "device_id": 1,
            "temperature_celsius": 72.5,
            
        },
    )
    
    if request.url.path == "/devices/4/temperature":
        return httpx.Response(
            status_code=200,
            json={
                "device_id": 4,
                "temperature_celsius": "not-a-temperature",
            },
        )
    if request.url.path == "/devices/2/temperature":
        return httpx.Response(
            status_code=503,
            content="service unavailable",
        )
    
    if request.url.path == "/devices/3/temperature":
        raise httpx.ReadTimeout(
        "Simulated provider timeout",
        request=request,
    )

    if request.url.path == "/devices/5/temperature":
        return httpx.Response(
            status_code=200,
            content=b"{this is not valid JSON",
            headers={"content-type": "application/json"},
        )
    

def test_get_device_temperature(client):
    response = client.get("/devices/1/temperature")

    assert response.status_code == 200
    assert response.json() == {
        "device_id": 1,
        "temperature_celsius": 72.5,
    }

def test_temperature_provider_failure_503(client):  
    response = client.get("/devices/2/temperature")
    assert response.status_code == 503
    assert response.json() == {
        "detail": "Temperature service is not available"
    }


    

def test_temperature_timeout_returns_503(client):
    create_response = client.post(
        "/devices",
        json={"name": "Timeout Device", "status": "ok"},
    )
    assert create_response.status_code == 201
    assert create_response.json()["id"] == 3

    response = client.get("/devices/3/temperature")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Temperature service timed out"
    }

def test_invalid_temperature_schema_returns_503(client):
    client.post(
        "/devices",
        json={"name": "Device 3", "status": "ok"},
    )
    create_response = client.post(
        "/devices",
        json={"name": "Invalid Data Device", "status": "ok"},
    )
    assert create_response.json()["id"] == 4

    response = client.get("/devices/4/temperature")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Temperature service returned invalid data"
    }


def test_malformed_temperature_json_returns_503(client):
    client.post(
        "/devices",
        json={"name": "Device 3", "status": "ok"},
    )
    client.post(
        "/devices",
        json={"name": "Device 4", "status": "ok"},
    )
    create_response = client.post(
        "/devices",
        json={"name": "Malformed JSON Device", "status": "ok"},
    )
    assert create_response.json()["id"] == 5

    response = client.get("/devices/5/temperature")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Temperature service returned invalid data"
    }