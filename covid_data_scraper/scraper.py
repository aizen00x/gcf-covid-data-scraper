import logging
import os

from .retriever import Retriever
from .retriever import RetrieveTimeoutError
from .pubsub_publisher import Publisher
from .pubsub_publisher import PublishTimeoutError
from requests import HTTPError
from flask import Response


class Scraper:
    """
    Class encapsulates retrieving data from API and writing it to pubsub topic
    """

    def __init__(
            self,
            publish_timeout_in_seconds: int = int(os.environ.get(
                "PUBLISH_TIMEOUT_IN_SECONDS", "60")
            ),
            request_timeout_in_seconds: int = int(os.environ.get(
                "REQUEST_TIMEOUT_IN_SECONDS", "60")
            )
    ):
        self.retriever = Retriever()
        self.publisher = Publisher()
        self.publish_timeout_in_seconds = publish_timeout_in_seconds
        self.request_timeout_in_seconds = request_timeout_in_seconds

    def scrape(self) -> Response:
        try:
            data = self.retriever.retrieve(timeout=self.request_timeout_in_seconds)
            logging.info(f"Successfully retrieved API Data: {data}")

            message_id = self.publisher.publish(data, timeout=self.publish_timeout_in_seconds)
            logging.info(f"Published message {message_id}")

            return Response(status=200)
        except HTTPError as ex:
            logging.exception(f"Request to retrieve data from API failed with status code: "
                              f"{ex.response.status_code}")
            return Response(status=503)
        except RetrieveTimeoutError as ex:
            logging.exception(ex.message)
            return Response(status=503)
        except PublishTimeoutError as ex:
            logging.exception(ex.message)
            return Response(status=503)
