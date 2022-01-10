import os

from google.cloud import pubsub_v1
from .publish_timeout_error import PublishTimeoutError


class Publisher:
    """
    Establishes connection with Google Cloud Pub/Sub and is responsible for publishing to a
    topic
    """

    def __init__(
            self,
            project: str = os.environ.get("PROJECT_ID", ""),
            topic: str = os.environ.get("TOPIC", "")
    ):
        self.publisher = pubsub_v1.PublisherClient()

        if not project:
            raise Exception("Project was not provided. Please pass to the constructor or set "
                            "'PROJECT_ID' environment variable")

        if not topic:
            raise Exception("Project was not provided. Please pass to the constructor or set "
                            "'TOPIC' environment variable")

        self.topic = self.publisher.topic_path(project, topic)

    def publish(self, data: str, timeout: int):
        """
        Function to publish data to pubsub topic with provided timeout
        :param data: takes data as plain string
        :param timeout: time to wait for publish result
        :return: nothing
        :raises: PublishTimeoutError
        """
        future = self.publisher.publish(self.topic, data.encode("utf-8"))

        try:
            return future.result(timeout=timeout)
        except TimeoutError as ex:
            raise PublishTimeoutError from ex
