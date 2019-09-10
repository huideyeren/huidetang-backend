from django.db import models
from django.utils.text import slugify

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
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


class PortfolioPageTechnology(TaggedItemBase):
    content_object = ParentalKey(
        'PortfolioPage',
        on_delete=models.CASCADE,
        related_name="technology"
    )


class PortfolioPage(GraphQLEnabledModel, Page):
    update_date = models.DateField(u"更新日")
    tech = ClusterTaggableManager(
        verbose_name=u'経験または興味のある技術',
        through=PortfolioPageTechnology,
        blank=True
    )
    github_url = models.URLField(u'GitHubの個人ページ', max_length=200, blank=True)
    author = models.ForeignKey(
        'author.AuthorPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=u'著者',
    )

    content_panels = Page.content_panels + [
        FieldPanel('update_date'),
        FieldPanel('tech'),
        FieldPanel('github_url'),
        InlinePanel('job_career', label=u'職務経歴'),
        InlinePanel('related_links', label=u'関連リンク'),
        PageChooserPanel('author', 'author.AuthorPage'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    graphql_fields = [
        GraphQLField('author'),
        GraphQLField('update_date'),
        GraphQLField('tech'),
        GraphQLField('github_url'),
        GraphQLField('job_career'),
        GraphQLField('related_links'),
        GraphQLField('slug'),
    ]

    def clean(self):
        super().clean()
        new_title = '%s のポートフォリオ' % self.author.name
        new_slug = self.author.slug
        self.title = new_title
        self.slug = slugify(new_slug)

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


class PortfolioPageJobCareer(GraphQLEnabledModel, Orderable):
    portfolio = ParentalKey(
        PortfolioPage,
        on_delete=models.CASCADE,
        related_name='job_career',
        verbose_name=u'職務経歴'
    )
    title = models.CharField(verbose_name=u'タイトル', max_length=50)
    start_date = models.DateField(u'開始日', auto_now=False, auto_now_add=False)
    end_date = models.DateField(u'終了日', auto_now=False, auto_now_add=False, blank=True, null=True)
    job_role = models.CharField(u'役割', max_length=50, blank=True, null=True)
    description = MarkdownField(verbose_name=u'説明', blank=True, null=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        FieldPanel('job_role'),
        MarkdownPanel('description')
    ]

    graphql_fields = [
        GraphQLField('title'),
        GraphQLField('start_date'),
        GraphQLField('end_date'),
        GraphQLField('job_role'),
        GraphQLField('description'),
    ]


class PortfolioPageRelatedLink(GraphQLEnabledModel, Orderable):
    page = ParentalKey(
        PortfolioPage,
        on_delete=models.CASCADE,
        related_name='related_links',
        verbose_name=u'関連ページ'
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


class PortoflioIndexPage(GraphQLEnabledModel, Page):
    intro = MarkdownField(null=True)

    def child_pages(self):
        return PortfolioPage.objects.live().child_of(self)

    content_panels = Page.content_panels + [
        MarkdownPanel('intro', classname='full')
    ]

    graphql_fields = [
        GraphQLField('intro'),
    ]

    subpage_types = ['PortfolioPage']

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
