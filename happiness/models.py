from django.db import models
from django.utils.text import slugify

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField

from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField

# Create your models here.


class HappinessPage(GraphQLEnabledModel, Page):

    date = models.DateField(u"投稿日")
    first = models.CharField(u"一つ目のよいこと", max_length=25)
    second = models.CharField(u"二つ目のよいこと", max_length=25)
    third = models.CharField(u"三つ目のよいこと", max_length=25)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=u'画像'
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
        FieldPanel('first'),
        FieldPanel('second'),
        FieldPanel('third'),
        PageChooserPanel('author', 'author.AuthorPage'),
        ImageChooserPanel('feed_image'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    graphql_fields = [
        GraphQLField('author'),
        GraphQLField('date'),
        GraphQLField('slug'),
        GraphQLField('first'),
        GraphQLField('second'),
        GraphQLField('third'),
        GraphQLField('feed_image')
    ]

    def clean(self):
        super().clean()
        new_title = '%s の3つのよいこと' % self.date
        new_slug = '3 good things in %s' % self.date
        self.title = new_title
        self.slug = slugify(new_slug)


HappinessPage._meta.get_field('slug').default = 'default-blank-slug'


class HappinessIndexPage(GraphQLEnabledModel, Page):
    intro = MarkdownField(null=True)

    def child_pages(self):
        return HappinessPage.objects.live().child_of(self)

    content_panels = Page.content_panels + [
        MarkdownPanel('intro', classname='full')
    ]

    graphql_fields = [
        GraphQLField('intro'),
    ]

    subpage_types = ['HappinessPage']
