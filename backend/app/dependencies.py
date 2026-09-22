import httpx
from fastapi import Depends, Request

#from unittest.mock import Mock
from app.clients.temperature import TemperatureClient
from app.repositories.device import DeviceRepository
from app.services.device import DeviceService

_device_repository = DeviceRepository()



def get_device_repository() -> DeviceRepository:
    return _device_repository



def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


def get_temperature_client(
    http_client: httpx.AsyncClient = Depends(get_http_client),
) -> TemperatureClient:
    return TemperatureClient(
        http_client=http_client,
        base_url="http://localhost:9000",
    )


def get_device_service(
    repository: DeviceRepository = Depends(get_device_repository),
    temperature_client: TemperatureClient = Depends(get_temperature_client),
) -> DeviceService:
    return DeviceService(repository, temperature_client)
