from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, \
    MultiFieldPanel, \
    InlinePanel, \
    PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField

from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField
from wagtail.core.signals import page_published, page_unpublished
import urllib
import logging
import os

logger = logging.getLogger(__name__)
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
