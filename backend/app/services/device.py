from typing import Optional

from app.clients.temperature import TemperatureClient
from app.errors.device import DeviceNotFoundError
from app.repositories.device import DeviceRepository
from app.schemas.device import DeviceCreate, DeviceResponse


class DeviceService:
    def __init__(
        self,
        device_repository: DeviceRepository,
        temperature_client: TemperatureClient,
    ) -> None:
        self._device_repository = device_repository
        self._temperature_client = temperature_client

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
