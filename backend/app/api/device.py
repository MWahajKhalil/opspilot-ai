from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_device_service
from app.errors.device import DeviceNotFoundError
from app.schemas.device import DeviceCreate, DeviceResponse
from app.schemas.telemetry import TemperatureReading
from app.services.device import DeviceService
from app.errors.temperature import TemperatureServiceError
from app.security import require_api_key

router = APIRouter(prefix="/devices", tags=["devices"], dependencies=[Depends(require_api_key)])
#

@router.get("", response_model=list[DeviceResponse])
def list_devices(
    service: DeviceService = Depends(get_device_service),
    status: Optional[str] = None,
) -> list[DeviceResponse]:
    return service.list_devices(status)


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: int,
    service: DeviceService = Depends(get_device_service),
) -> DeviceResponse:
    try:
        return service.get_device(device_id)
    except DeviceNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("", response_model=DeviceResponse, status_code=201)
def create_device(
    device: DeviceCreate,
    service: DeviceService = Depends(get_device_service),
) -> DeviceResponse:
    return service.create_device(device)


@router.get("/{device_id}/temperature", response_model=TemperatureReading)
async def get_temperature_for_device(
    device_id: int,
    service: DeviceService = Depends(get_device_service),
) -> TemperatureReading:
    try:
        return await service.get_temperature_for_device(device_id)
    except DeviceNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except TemperatureServiceError as error:
        raise HTTPException(status_code=503, detail=str(error))
