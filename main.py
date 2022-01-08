import logging

from covid_data_scraper import Scraper
from datetime import datetime

logging.basicConfig(level=logging.INFO)


def process(request):
    logging.info(
        f"This function was triggered by "
        f"Cloud Scheduler at {datetime.now()}"
    )

    return Scraper().scrape()
