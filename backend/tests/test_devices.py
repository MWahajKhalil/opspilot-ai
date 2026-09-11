from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

#test the health endpoint

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_devices():
    response = client.get("/devices")
    assert response.status_code == 200
    assert response.json() == [{"id":1, "name":"Device 1", "status":"ok"}, {"id":2, "name":"Device 2", "status":"warning"}]
    
    