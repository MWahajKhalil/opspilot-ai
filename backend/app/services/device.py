from app.schemas.device import DeviceResponse
from typing import Optional

class DeviceService: #this class will be used to perform business logic on devices
    def __init__(self):
        self._devices=[
            DeviceResponse(id=1, name='Device 1', status='ok'),
            DeviceResponse(id=2, name='Device 2', status='warning'),
            
        ]
        # _means internal use not private 

    
    def list_devices(self)-> list[DeviceResponse]:
        return self._devices

    
    def find_device(self, device_id:int) -> Optional[DeviceResponse]:
        for d in self._devices:
            if d.id == device_id:
                return d
        return None 
        
    


    
     
    
    
    



