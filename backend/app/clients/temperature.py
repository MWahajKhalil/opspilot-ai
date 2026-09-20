import httpx

from app.schemas.telemetry import TemperatureReading
from app.errors.temperature import TemperatureServiceError


class TemperatureClient:
    def __init__(self, http_client: httpx.Client, base_url: str):
        self._http_client = http_client
        self._base_url = base_url

    def get_temperature(self, device_id: int) -> TemperatureReading:
        
        try:
            response = self._http_client.get(
                f"{self._base_url}/devices/{device_id}/temperature"
            )

            response.raise_for_status()

        except httpx.HTTPStatusError:
            raise TemperatureServiceError(device_id, "Temperature service is not available")
        except httpx.RequestError:
            raise TemperatureServiceError(device_id, "Temperature service is not available")

        data = response.json()

        return TemperatureReading.model_validate(data)
