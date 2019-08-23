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

"""Article Tags"""


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        "ArticlePage",
        on_delete=models.CASCADE,
        related_name="tagged_items"
    )


"""Article Pages"""


class ArticlePage(GraphQLEnabledModel, Page):

    """Posted Date"""
    date = models.DateField(u"投稿日")
    """Page Tag"""
    tags = ClusterTaggableManager(verbose_name=u'タグ',through=ArticlePageTag, blank=True)
    """Article's Body"""
    body = MarkdownField(verbose_name=u'本文', blank=True)
    """Image File"""
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=u'画像',
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('tags'),
        MarkdownPanel("body", classname="full"),
        ImageChooserPanel('feed_image'),
        InlinePanel('related_links', label=u'関連リンク'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    graphql_fields = [
        GraphQLField('date'),
        GraphQLField('tags'),
        GraphQLField('slug'),
        GraphQLField('body'),
        GraphQLField('feed_image'),
        GraphQLField('author_name'),
    ]


class ArticlePageRelatedLink(Orderable):
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
