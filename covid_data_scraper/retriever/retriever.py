import os
import requests

from .retrieve_timeout_error import RetrieveTimeoutError


class Retriever:
    """
    Class which encapsulates retrieving data from API
    """
    def __init__(
            self,
            link: str = os.environ.get("LINK", "")
    ):
        if not link:
            raise Exception("Project was not provided. Please pass to the constructor or set "
                            "'LINK' environment variable")

        self.link = link

    def retrieve(self, timeout: int = 60) -> str:
        """
        Fetch data from API
        :return: JSON string with data
        :raises: RetrieveTimeoutException
        """
        try:
            response = requests.get(self.link, timeout=timeout)
        except TimeoutError as ex:
            raise RetrieveTimeoutError from ex

        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()
