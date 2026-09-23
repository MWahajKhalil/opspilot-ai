import httpx
import json
import logging

from app.schemas.telemetry import TemperatureReading
from app.errors.temperature import TemperatureServiceError
from pydantic import ValidationError


logger = logging.getLogger(__name__)
class TemperatureClient:
    def __init__(self, http_client: httpx.AsyncClient, base_url: str):
        self._http_client = http_client
        self._base_url = base_url

    

    async def get_temperature(self, device_id: int) -> TemperatureReading:
        
        try:
            response = await self._http_client.get(

                f"{self._base_url}/devices/{device_id}/temperature"
            )

            response.raise_for_status()
            data = response.json()
            return TemperatureReading.model_validate(data)
        
        except httpx.TimeoutException:
            logger.warning(
                "temperature_provider_timeout device_id=%s",
                device_id,
            )            
            raise TemperatureServiceError(device_id, "Temperature service timed out")


        except httpx.HTTPStatusError as error:
            logger.warning(
                "temperature_provider_http_error device_id=%s status_code=%s",
                device_id,
                error.response.status_code,
            )
            raise TemperatureServiceError(device_id, "Temperature service is not available")

        except httpx.RequestError as error:
            logger.warning(
                "temperature_provider_request_error device_id=%s error_type=%s",
                device_id,
                type(error).__name__,
            )
            raise TemperatureServiceError(device_id, "Temperature service is not available")


        except (json.JSONDecodeError, ValidationError) as error:
            logger.warning(
                "temperature_provider_invalid_response device_id=%s error_type=%s",
                device_id,
                type(error).__name__,
            )
            raise TemperatureServiceError(device_id, "Temperature service returned invalid data")
        

        

        

        
