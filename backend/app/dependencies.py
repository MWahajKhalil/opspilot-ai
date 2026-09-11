from app.services.device import DeviceService


_device_service = DeviceService()


def get_device_service() -> DeviceService:
    return _device_service
