

class TemperatureServiceError(Exception):
    def __init__(self, device_id: int, message: str):
        self.device_id = device_id
        self.message = message
        super().__init__(self.message)
