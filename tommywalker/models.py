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

    def send_published_signal(self, **kwargs):
        """Sending signal when an article is published."""
        url = os.getenv('NETLIFY_HOOKS_URL')
        data = {}
        headers = {
            'Content-Type': 'application/json',
        }
        req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        res = urllib.request.urlopen(req).read()
        logger.debug(res)

        page_published.send(sender=self.__class__)

    def send_unpublished_signal(self, **kwargs):
        """Sending signal when an article is unpublished."""
        url = os.getenv('NETLIFY_HOOKS_URL')
        data = {}
        headers = {
            'Content-Type': 'application/json',
        }
        req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        res = urllib.request.urlopen(req).read()
        logger.debug(res)

        page_unpublished.send(sender=self.__class__)

    page_published.connect(send_published_signal)
    page_unpublished.connect(send_unpublished_signal)
