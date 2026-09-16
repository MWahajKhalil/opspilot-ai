from fastapi import Depends

from app.repositories.device import DeviceRepository
from app.services.device import DeviceService

_device_repository = DeviceRepository()


def get_device_repository() -> DeviceRepository:
    return _device_repository


def get_device_service(
    repository: DeviceRepository = Depends(get_device_repository),
) -> DeviceService:
    return DeviceService(repository)
