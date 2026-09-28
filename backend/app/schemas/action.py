from enum import Enum
from typing import Literal
from pydantic import BaseModel

class DeviceAction(str, Enum):
    INSPECT = "inspect"
    RESTART = "restart"
    SHUTDOWN = "shutdown"
    

class DeviceActionRequest(BaseModel):
    action: DeviceAction
    

class DeviceActionResponse(BaseModel):
    device_id: int
    action: DeviceAction
    status: Literal["accepted", "approval_required"]





