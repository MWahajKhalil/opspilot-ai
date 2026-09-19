import httpx

from app.schemas.telemetry import TemperatureReading


class TemperatureClient:
    def __init__(self, http_client: httpx.Client, base_url: str):
        self._http_client = http_client
        self._base_url = base_url

    def get_temperature(self, device_id: int) -> TemperatureReading:
        response = self._http_client.get(
            f"{self._base_url}/devices/{device_id}/temperature"
        )
        response.raise_for_status()

        data = response.json()

        return TemperatureReading.model_validate(data)
