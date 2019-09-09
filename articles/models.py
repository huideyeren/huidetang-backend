from http.client import responses
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
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


"""Article Tags"""


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        "ArticlePage",
        on_delete=models.CASCADE,
        related_name="tagged_items"
    )


class ArticlePage(GraphQLEnabledModel, Page):
    """Article Pages"""

    date = models.DateTimeField(u"投稿日")
    tags = ClusterTaggableManager(
        verbose_name=u'タグ',
        through=ArticlePageTag,
        blank=True
    )
    body = MarkdownField(verbose_name=u'本文', blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=u'画像',
    )
    author = models.ForeignKey(
        'author.AuthorPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=u'著者',
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('tags'),
        MarkdownPanel("body", classname="full"),
        ImageChooserPanel('feed_image'),
        PageChooserPanel('author', 'author.AuthorPage'),
        InlinePanel('related_links', label=u'関連リンク'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    graphql_fields = [
        GraphQLField('author'),
        GraphQLField('date'),
        GraphQLField('tags'),
        GraphQLField('slug'),
        GraphQLField('body'),
        GraphQLField('feed_image'),
        GraphQLField('related_links')
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


class ArticlePageRelatedLink(GraphQLEnabledModel, Orderable):
    page = ParentalKey(
        ArticlePage,
        on_delete=models.CASCADE,
        related_name='related_links'
    )
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

    graphql_fields = [
        GraphQLField('name'),
        GraphQLField('url')
    ]
