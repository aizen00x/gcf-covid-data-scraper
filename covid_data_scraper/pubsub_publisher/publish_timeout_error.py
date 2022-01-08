class PublishTimeoutError(TimeoutError):
    def __init__(self):
        self.message = "Publishing data to PubSub timed out"
