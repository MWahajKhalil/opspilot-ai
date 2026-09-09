from fastapi import APIRouter, Depends
from app.dependencies import get_device_service
from app.schemas.device import DeviceResponse
from app.services.device import DeviceService


router =  APIRouter(prefix='/devices', tags=['devices'])

#tags=["devices"]  → endpoints are grouped under “devices” in Swagger UI
#prefix="/devices" → URLs begin with /devices



@router.get("", response_model=list[DeviceResponse],)
def list_devices(
    service: DeviceService = Depends(get_device_service),
    status: Optional[str] = None
    ) -> list[DeviceResponse]:

    return service.list_devices(status)


