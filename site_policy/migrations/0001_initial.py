# Generated by Django 3.0.7 on 2020-07-05 22:33

from django.db import migrations, models
import django.db.models.deletion
import wagtail_graphql.models
import wagtailmarkdown.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0046_auto_20200305_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitePolicyPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtailmarkdown.fields.MarkdownField(blank=True, verbose_name='本文')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail_graphql.models.GraphQLEnabledModel, 'wagtailcore.page'),
        ),
    ]
