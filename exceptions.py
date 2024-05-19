class ScaleError(Exception):
    """Exception raised when the value is not in the scale"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)