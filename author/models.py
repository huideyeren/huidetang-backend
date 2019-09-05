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
from wagtail.core.signals import page_published
import urllib
# Create your models here.


class AuthorPageInterest(TaggedItemBase):
    content_object = ParentalKey(
        "AuthorPage",
        on_delete=models.CASCADE,
        related_name="interest_items"
    )


class AuthorPage(GraphQLEnabledModel, Page):
    profile = MarkdownField(verbose_name=u'プロフィール')
    nickname = models.CharField(verbose_name=u'ニックネーム', max_length=25, null=True, blank=True)
    first_name = models.CharField(verbose_name=u'名', max_length=10, null=True, blank=True)
    middle_name = models.CharField(verbose_name=u'ミドルネーム', max_length=10, null=True, blank=True)
    family_name = models.CharField(verbose_name=u'姓', max_length=10, null=True, blank=True)
    name = models.CharField(verbose_name=u'表示名', max_length=80, null=True, blank=True)
    is_surname_first = models.BooleanField(verbose_name=u'姓が先の表記', null=True, blank=True)
    use_nickname = models.BooleanField(verbose_name=u'ニックネームの使用', null=True, blank=True)
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
        FieldPanel('nickname'),
        FieldPanel('first_name'),
        FieldPanel('middle_name'),
        FieldPanel('family_name'),
        FieldPanel('name'),
        FieldPanel('is_surname_first'),
        FieldPanel('use_nickname'),
        InlinePanel('portfolio_links', label=u'ポートフォリオ'),
        InlinePanel('amazon_wish_list_links', label=u'Amazonのほしいものリスト'),
        InlinePanel('sns_links', label=u'SNSなどのリンク'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    graphql_fields = [
        GraphQLField('name'),
        GraphQLField('profile'),
        GraphQLField('portrait'),
        GraphQLField('interest'),
        GraphQLField('portfolio_links'),
        GraphQLField('amazon_wish_list_links'),
        GraphQLField('sns_links'),
    ]

    def clean(self):
        if self.nickname is not None and self.use_nickname is True:
            self.name = self.nickname
        elif self.is_surname_first is True:
            if self.middle_name is None:
                self.name = self.family_name + u' ' + self.first_name
            else:
                self.name = (
                    self.family_name + u' ' +
                    self.middle_name + u' ' +
                    self.first_name
                )
        else:
            if self.middle_name is None:
                self.name = self.first_name + u' ' + self.family_name
            else:
                self.name = (
                    self.first_name + u' ' +
                    self.middle_name + u' ' +
                    self.family_name
                )

        self.title = '%s のプロフィール' % self.name

    def send_signal(sender):
        url = 'https://api.netlify.com/build_hooks/5d7170b7f2df0f019199c810'
        urllib.request.urlopen(url=url)

    page_published.connect(send_signal)


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

    def send_signal(sender):
        url = 'https://api.netlify.com/build_hooks/5d7170b7f2df0f019199c810'
        urllib.request.urlopen(url=url)

    page_published.connect(send_signal)
