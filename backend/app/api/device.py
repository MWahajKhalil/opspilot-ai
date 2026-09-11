from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_device_service
from app.schemas.device import DeviceCreate, DeviceResponse
from app.services.device import DeviceService

router = APIRouter(prefix="/devices", tags=["devices"])


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
    device = service.get_device(device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("", response_model=DeviceResponse, status_code=201)
def create_device(
    device: DeviceCreate,
    service: DeviceService = Depends(get_device_service),
) -> DeviceResponse:
    return service.create_device(device)
