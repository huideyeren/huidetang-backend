from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField

from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField
# Create your models here.


class AuthorPageInterest(TaggedItemBase):
    content_object = ParentalKey(
        "AuthorPage",
        on_delete=models.CASCADE,
        related_name="interest_items"
    )


class AuthorPage(GraphQLEnabledModel, Page):
    profile = MarkdownField(verbose_name=u'プロフィール')
    portrait = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=u'画像',
    )
    interest = ClusterTaggableManager(
        verbose_name=u'興味を持っていること',
        through=AuthorPageInterest,
        blank=True
    )

    content_panels = Page.content_panels + [
        MarkdownPanel('profile'),
        ImageChooserPanel('portrait'),
        FieldPanel('interest'),
        InlinePanel('portfolio_links', label=u'ポートフォリオ'),
        InlinePanel('amazon_wish_list_links', label=u'Amazonのほしいものリスト'),
        InlinePanel('sns_links', label=u'SNSなどのリンク'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    graphql_fields = [
        GraphQLField('profile'),
        GraphQLField('portrait'),
        GraphQLField('interest'),
        GraphQLField('portfolio_links'),
        GraphQLField('amazon_wish_list_links'),
        GraphQLField('sns_links'),
    ]


class AuthorPagePortfolio(GraphQLEnabledModel, Orderable):
    Author = ParentalKey(
        AuthorPage,
        on_delete=models.CASCADE,
        related_name='portfolio_links',
        verbose_name=u'ポートフォリオURL'
    )
    name = models.CharField(verbose_name=u'名前', max_length=255)
    url = models.URLField(verbose_name=u'URL',)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

    graphql_fields = [
        GraphQLField('name'),
        GraphQLField('url')
    ]


class AuthorPageAmazonWishList(GraphQLEnabledModel, Orderable):
    Author = ParentalKey(
        AuthorPage,
        on_delete=models.CASCADE,
        related_name='amazon_wish_list_links',
        verbose_name=u'AmazonのほしいものリストのURL'
    )
    name = models.CharField(verbose_name=u'名前', max_length=255)
    url = models.URLField(verbose_name=u'URL',)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

    graphql_fields = [
        GraphQLField('name'),
        GraphQLField('url')
    ]


class AuthorPageSnsLink(GraphQLEnabledModel, Orderable):
    Author = ParentalKey(
        AuthorPage,
        on_delete=models.CASCADE,
        related_name='sns_links',
        verbose_name=u'SNSなどのURL'
    )
    name = models.CharField(verbose_name=u'名前', max_length=255)
    url = models.URLField(verbose_name=u'URL',)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

    graphql_fields = [
        GraphQLField('name'),
        GraphQLField('url')
    ]


class AuthorIndexPage(GraphQLEnabledModel, Page):
    intro = MarkdownField(null=True)

    def child_pages(self):
        return AuthorPage.objects.live().child_of(self)

    content_panels = Page.content_panels + [
        MarkdownPanel('intro', classname='full')
    ]

    graphql_fields = [
        GraphQLField('intro'),
    ]

    subpage_types = ['AuthorPage']
