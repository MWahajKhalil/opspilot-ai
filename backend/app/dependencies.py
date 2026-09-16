from app.services.device import DeviceService
from app.repositories.device import DeviceRepository

_device_repository = DeviceRepository()



def get_device_service() -> DeviceService:
    _device_service = DeviceService(_device_repository)
    return _device_service