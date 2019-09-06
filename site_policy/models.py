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
from wagtail.core.signals import page_published, page_unpublished
import urllib
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Create your models here.


class SitePolicyPage(GraphQLEnabledModel, Page):
    body = MarkdownField(verbose_name=u'本文', blank=True)

    content_panels = Page.content_panels + [
        MarkdownPanel("body", classname="full"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    graphql_fields = [
        GraphQLField('body'),
    ]

    def send_signal(self, **kwargs):
        url = 'https://api.netlify.com/build_hooks/5d7170b7f2df0f019199c810'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            body = res.read()
            logger.debug(body)

    page_published.send(send_signal)
    page_unpublished.send(send_signal)
