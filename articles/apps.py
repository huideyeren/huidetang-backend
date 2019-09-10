from django.apps import AppConfig
from wagtail.core.signals import page_published, page_unpublished
from articles.signals import send_published_signal, send_unpublished_signal
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ArticlesConfig(AppConfig):
    name = 'articles'

    def ready(self):
        logger.debug('シグナルヲ トウロクスルヨー')
        page_published.connect(send_published_signal)
        page_unpublished.connect(send_unpublished_signal)
        logger.debug('シグナルヲ トウロクシタヨー')
