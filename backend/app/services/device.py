import logging
from typing import Optional

from app.clients.temperature import TemperatureClient
from app.errors.device import DeviceNotFoundError
from app.repositories.device import DeviceRepository
from app.schemas.action import (
    DeviceAction,
    DeviceActionRequest,
    DeviceActionResponse,
)
from app.schemas.device import DeviceCreate, DeviceResponse
from app.schemas.telemetry import TemperatureReading

logger = logging.getLogger(__name__)

APPROVAL_REQUIRED_ACTIONS = {
    DeviceAction.RESTART,
    DeviceAction.SHUTDOWN,
}


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

    async def get_temperature_for_device(self, device_id: int) -> TemperatureReading:
        self.get_device(device_id)
        return await self._temperature_client.get_temperature(device_id)

    def request_action(
        self,
        device_id: int,
        request: DeviceActionRequest,
    ) -> DeviceActionResponse:
        self.get_device(device_id)
        action = request.action

        if action in APPROVAL_REQUIRED_ACTIONS:
            status = "approval_required"
        else:
            status = "accepted"

        logger.info(
            "device_action_decision device_id=%s action=%s status=%s",
            device_id,
            action.value,
            status,
        )

        return DeviceActionResponse(
            device_id=device_id,
            action=action,
            status=status,
        )
