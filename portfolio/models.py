from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField

from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField

# Create your models here.


class PortfolioPageTechnology(TaggedItemBase):
    technology = ParentalKey(
        "PortfolioPageJobCareer",
        on_delete=models.CASCADE,
        related_name="technology"
    )


class PortfolioPageInterestTechnology(TaggedItemBase):
    technology = ParentalKey(
        "PortfolioPage",
        on_delete=models.CASCADE,
        related_name="interest_technology"
    )


class PortfolioPage(GraphQLEnabledModel, Page):
    update_date = models.DateField(u"更新日")
    using_technology = ClusterTaggableManager(
        verbose_name=u'使用経験のある技術',
        through=PortfolioPageTechnology
    ).all()
    interest_technology = ClusterTaggableManager(
        verbose_name=u'興味ある技術',
        through=PortfolioPageInterestTechnology,
        blank=True
    )
    github_url = models.URLField(u'GitHubの個人ページ', max_length=200)

    content_panels = Page.content_panels + [
        FieldPanel('update_date'),
        FieldPanel('interest_technology'),
        InlinePanel('job_career', label=u'職務経歴'),
        InlinePanel('related_links', label=u'関連リンク'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    graphql_fields = [
        GraphQLField('update_date'),
        GraphQLField('using_technology'),
        GraphQLField('interest_technology'),
        GraphQLField('github_url'),
        GraphQLField('job_career'),
        GraphQLField('related_links')
    ]

class PortfolioPageJobCareer(Orderable):
    portfolio = ParentalKey(
        PortfolioPage,
        on_delete=models.CASCADE,
        related_name='job_career',
        verbose_name=u'職務経歴'
    )
    title = models.CharField(verbose_name=u'タイトル', max_length=50)
    start_date = models.DateField(u'開始日', auto_now=False, auto_now_add=False)
    end_date = models.DateField(u'終了日', auto_now=False, auto_now_add=False, blank=True)
    job_role = models.CharField(u'役割', max_length=50, blank=True)
    technology = ClusterTaggableManager(
        verbose_name=u'使用技術',
        through=PortfolioPageTechnology,
        blank=True
    )
    description = MarkdownField(verbose_name=u'説明', blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        FieldPanel('job_role'),
        FieldPanel('technology'),
        MarkdownPanel('description')
    ]


class PortfolioPageRelatedLink(Orderable):
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
