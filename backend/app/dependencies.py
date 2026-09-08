from app.services.device import DeviceService

_device_service = DeviceService() #this is used for dependency injection in routes 

def get_device_service() -> DeviceService:
    return _device_service


