import httpx

from ..schemas.telemetry import TemperatureReading

class TemperatureClient:
    def __init__(self, http_client: httpx.Client, base_url: str):
        self._http_client = http_client
        self._base_url = base_url

    
    def get_temperature(self, device_id: int) -> TemperatureReading:
        pass
        #response = self._http_client.get(f"{self._base_url}/{device_id}/temperature")
        

    
    
    

