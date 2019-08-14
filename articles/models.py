from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField

"""Article Pages"""


class ArticlePage(Page):

    """Posted Date"""
    date = models.DateField(u"投稿日")
    """Article's Body"""
    body = MarkdownField(blank=True)
