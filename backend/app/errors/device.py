
class DeviceNotFoundError(Exception):
    def __init__(self, device_id: int):
        self.device_id = device_id
        self.message = f"Device with id {device_id} not found"
        super().__init__(self.message)






