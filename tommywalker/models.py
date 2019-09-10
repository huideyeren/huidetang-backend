from wagtail.core.models import Page
from wagtail.admin.edit_handlers import MultiFieldPanel
from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField

from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField
from wagtail.core.signals import page_published, page_unpublished
import urllib
import logging
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create your models here.


class TommywalkerPage(GraphQLEnabledModel, Page):
    body = MarkdownField(verbose_name=u'本文', blank=True)

    content_panels = Page.content_panels + [
        MarkdownPanel("body", classname="full"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    graphql_fields = [
        GraphQLField('body'),
    ]

    def send_published_signal(sender, **kwargs):
        """Sending signal when an article is published."""
        logger.debug('メソッドガ ヨバレタヨー')
        if os.getenv('NETLIFY_HOOKS_URL') is None:
            url = ''
        else:
            url = os.getenv('NETLIFY_HOOKS_URL').__str__()
        logger.debug('URL ハ %s ダヨー' % url)
        values = {
            'trigger_branch': 'published',
            'trigger_title': '%s was published.' % sender.title
        }
        headers = {
            'Content-Type': 'application/json',
        }
        data = urllib.parse.urlencode(values).encode()
        logger.debug('データ デキタヨー')
        req = urllib.request.Request(url, data, headers)
        logger.debug('リクエスト ジュンビ デキタヨー')
        res = urllib.request.urlopen(req).read().decode('utf-8')
        logger.debug('リクエスト ケッカ ハ %s ダヨー' % res)

    def send_unpublished_signal(sender, **kwargs):
        """Sending signal when an article is unpublished."""
        logger.debug('メソッドガ ヨバレタヨー')
        if os.getenv('NETLIFY_HOOKS_URL') is None:
            url = ''
        else:
            url = os.getenv('NETLIFY_HOOKS_URL').__str__()
        logger.debug('URL ハ %s ダヨー' % url)
        values = {
            'trigger_branch': 'published',
            'trigger_title': '%s was published.' % sender.title
        }
        headers = {
            'Content-Type': 'application/json',
        }
        data = urllib.parse.urlencode(values).encode()
        logger.debug('データ デキタヨー')
        req = urllib.request.Request(url, data, headers)
        logger.debug('リクエスト ジュンビ デキタヨー')
        res = urllib.request.urlopen(req).read().decode('utf-8')
        logger.debug('リクエスト ケッカ ハ %s ダヨー' % res)

    logger.debug('シグナルヲ トウロクスルヨー')
    page_published.connect(send_published_signal)
    page_unpublished.connect(send_unpublished_signal)
    logger.debug('シグナルヲ トウロクシタヨー')
