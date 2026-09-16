from typing import Optional
from app.errors.device import DeviceNotFoundError
from app.schemas.device import DeviceCreate, DeviceResponse
from app.repositories.device import DeviceRepository


class DeviceService:
    def __init__(self, device_repository: DeviceRepository):
        self._device_repository = device_repository
    


    def list_devices(
        self,
        status: Optional[str] = None,
    ) -> list[DeviceResponse]:

        if status is None:
            return self._device_repository.list_devices()
        return self._device_repository.list_devices(status)
    

    def get_device(self, device_id: int) -> DeviceResponse:
        device = self._device_repository.get_by_id(device_id)
        if device is None:
            raise DeviceNotFoundError(device_id)
        return device


    def create_device(self, device: DeviceCreate) -> DeviceResponse:
        return self._device_repository.create_device(device)
