from pydantic import BaseModel


class TemperatureReading(BaseModel):
    device_id: int
    temperature_celsius: float



