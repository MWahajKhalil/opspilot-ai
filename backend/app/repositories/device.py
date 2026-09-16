from typing import Optional
from app.schemas.device import DeviceResponse

class DeviceRepository:
    def __init__(self):
        self._devices = [
            DeviceResponse(id=1, name="Device 1", status="ok"),
            DeviceResponse(id=2, name="Device 2", status="warning"),
        ]
        
    def list_devices(self) -> list[DeviceResponse]:
        return self._devices
    
    def get_by_id(self, device_id: int) -> Optional[DeviceResponse]:
        for device in self._devices:
            if device.id == device_id:
                return device
        return None
            
