from app.schemas.device import DeviceResponse, DeviceCreate
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

    
    def get_device(self, device_id:int) -> Optional[DeviceResponse]:
        for d in self._devices:
            if d.id == device_id:
                return d
        return None 
    

    def create_device(self, device:DeviceCreate)-> DeviceResponse:
        new_id = max([d.id for d in self._devices] + [0]) + 1
      #  new_device = DeviceResponse(**device.model_dump(), id=new_id)
      
        new_device = DeviceResponse(
            id=new_id,
            name=device.name,
            status=device.status,
        )

        self._devices.append(new_device)
        return new_device

        
    

    
        

    


    
     
    
    
    
