from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField

from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField

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
