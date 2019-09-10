from django.apps import AppConfig
from wagtail.core.signals import page_published, page_unpublished
from portfolio.signals import send_published_signal, send_unpublished_signal
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class PortfolioConfig(AppConfig):
    name = 'portfolio'

    def ready(self):
        logger.debug('シグナルヲ トウロクスルヨー')
        page_published.connect(send_published_signal)
        page_unpublished.connect(send_unpublished_signal)
        logger.debug('シグナルヲ トウロクシタヨー')
