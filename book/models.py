from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

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


class BookPage(GraphQLEnabledModel, Page):

    price = models.IntegerField()
    published_date = models.DateField()
    published_event = models.CharField(max_length=50)
    description = MarkdownField(verbose_name=u'説明')
    booth_url = models.URLField(max_length=255, null=True)
    bookwalker_url = models.URLField(max_length=255, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        FieldPanel('price'),
        FieldPanel('published_date'),
        FieldPanel('published_event'),
        MarkdownPanel('description'),
        FieldPanel('booth_url'),
        FieldPanel('bookwalker_url'),
        ImageChooserPanel('image'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    graphql_fields = [
        GraphQLField('price'),
        GraphQLField('published_date'),
        GraphQLField('published_event'),
        GraphQLField('description'),
        GraphQLField('booth_url'),
        GraphQLField('bookwalker_url'),
        GraphQLField('image'),
        GraphQLField('slug')
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


class BookIndexPage(GraphQLEnabledModel, Page):
    intro = MarkdownField(null=True)

    def child_pages(self):
        return BookPage.objects.live().child_of(self)

    content_panels = Page.content_panels + [
        MarkdownPanel('intro', classname='full')
    ]

    graphql_fields = [
        GraphQLField('intro'),
    ]

    subpage_types = ['BookPage']

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
