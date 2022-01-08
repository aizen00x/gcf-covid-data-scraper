class RetrieveTimeoutError(TimeoutError):
    def __init__(self):
        self.message = "Request to retrieve data timed out"
