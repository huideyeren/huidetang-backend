from django.db import models
from django.utils.text import slugify

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField

from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField
from wagtail.core.signals import page_published, page_unpublished
import urllib
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Create your models here.


class CharacterPage(GraphQLEnabledModel, Page):
    """A page of character list."""
    nickname = models.CharField(u"称号", max_length=15, null=True)
    name = models.CharField(u"名前", max_length=35, null=True)
    character_id = models.CharField(u"キャラクターID", max_length=6, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=u'画像',
    )
    description = models.CharField(u'概要', max_length=255, null=True)
    introduction = MarkdownField(verbose_name=u"説明", null=True)
    game_name = models.CharField(u"登録されているゲーム", max_length=20, null=True)
    character_page_url = models.CharField(u"キャラクターのページ", max_length=255, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('nickname'),
        FieldPanel('name'),
        FieldPanel('character_id'),
        ImageChooserPanel('image'),
        FieldPanel('description'),
        MarkdownPanel('introduction'),
        FieldPanel('game_name'),
        FieldPanel('character_page_url'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    graphql_fields = [
        GraphQLField("nickname"),
        GraphQLField("name"),
        GraphQLField("character_id"),
        GraphQLField("image"),
        GraphQLField("description"),
        GraphQLField("introduction"),
        GraphQLField("game_name"),
        GraphQLField("character_page_url"),
    ]

    def clean(self):
        super().clean()
        new_title = '%s' % self.name
        new_slug = '%s' % self.character_id
        self.title = new_title
        self.slug = slugify(new_slug)

    def send_signal(self, **kwargs):
        url = 'https://api.netlify.com/build_hooks/5d7170b7f2df0f019199c810'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            body = res.read()
            logger.debug(body)

    page_published.send(send_signal)
    page_unpublished.send(send_signal)


class CharacterIndexPage(GraphQLEnabledModel, Page):
    intro = MarkdownField(null=True)

    def child_pages(self):
        return CharacterPage.objects.live().child_of(self)

    content_panels = Page.content_panels + [
        MarkdownPanel('intro', classname='full')
    ]

    graphql_fields = [
        GraphQLField('intro'),
    ]

    subpage_types = ['CharacterPage']

    def send_signal(self, **kwargs):
        url = 'https://api.netlify.com/build_hooks/5d7170b7f2df0f019199c810'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            body = res.read()
            logger.debug(body)

    page_published.send(send_signal)
    page_unpublished.send(send_signal)
