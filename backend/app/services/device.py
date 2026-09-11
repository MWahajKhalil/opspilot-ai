from typing import Optional

from app.schemas.device import DeviceCreate, DeviceResponse


class DeviceService:
    def __init__(self):
        self._devices = [
            DeviceResponse(id=1, name="Device 1", status="ok"),
            DeviceResponse(id=2, name="Device 2", status="warning"),
        ]

    def list_devices(
        self,
        status: Optional[str] = None,
    ) -> list[DeviceResponse]:
        if status is None:
            return self._devices

        return [device for device in self._devices if device.status == status]

    def get_device(self, device_id: int) -> Optional[DeviceResponse]:
        for device in self._devices:
            if device.id == device_id:
                return device
        return None

    def create_device(self, device: DeviceCreate) -> DeviceResponse:
        new_id = max([existing.id for existing in self._devices] + [0]) + 1
        new_device = DeviceResponse(
            id=new_id,
            name=device.name,
            status=device.status,
        )

        self._devices.append(new_device)
        return new_device
    
    
