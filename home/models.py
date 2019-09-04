from django.db import models

from wagtail.core.models import Page

from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField


class HomePage(GraphQLEnabledModel, Page):
    pass
