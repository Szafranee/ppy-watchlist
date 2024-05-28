class ScaleError(Exception):
    """Exception raised when the value is not in the scale"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MovieNotFound(Exception):
    """Exception raised when the movie is not found in the collection"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
