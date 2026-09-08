from fastapi import APIRouter, Depends

router =  APIRouter()

@router.get('/')
async def list_devices():
    return device_service.list_devices()

