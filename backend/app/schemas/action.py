from enum import Enum
from pydantic import BaseModel

class DeviceAction(str, Enum):
    INSPECT = "inspect"
    RESTART = "restart"
    SHUTDOWN = "shutdown"
    

class DeviceActionRequest(BaseModel):
    action: DeviceAction



