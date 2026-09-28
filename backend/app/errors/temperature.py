

class TemperatureServiceError(Exception):
    def __init__(self, device_id: int, message: str) -> None:
        self.device_id = device_id
        self.message = message
        super().__init__(self.message)
