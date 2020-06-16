# Generated by Django 3.0.7 on 2020-06-16 11:55

from django.db import migrations, models
import django.db.models.deletion
import wagtail_graphql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0046_auto_20200616_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail_graphql.models.GraphQLEnabledModel, 'wagtailcore.page'),
        ),
    ]
