from django.apps import AppConfig
from wagtail.core.signals import page_published, page_unpublished
from site_policy.signals import send_published_signal, send_unpublished_signal
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class SitePolicyConfig(AppConfig):
    name = 'site_policy'

    def ready(self):
        logger.debug('シグナルヲ トウロクスルヨー')
        page_published.connect(send_published_signal)
        page_unpublished.connect(send_unpublished_signal)
        logger.debug('シグナルヲ トウロクシタヨー')
