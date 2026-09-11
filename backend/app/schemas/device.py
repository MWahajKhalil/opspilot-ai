from pydantic import BaseModel


class DeviceResponse(BaseModel):
    id: int
    name: str
    status: str


class DeviceCreate(BaseModel):
    name: str
    status: str
