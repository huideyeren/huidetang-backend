# Generated by Django 3.0.4 on 2020-06-16 00:19

from django.db import migrations, models
import django.db.models.deletion
import wagtail_graphql.models
import wagtailmarkdown.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0046_auto_20200305_0557'),
        ('wagtailimages', '0001_squashed_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', wagtailmarkdown.fields.MarkdownField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail_graphql.models.GraphQLEnabledModel, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='CharacterPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('nickname', models.CharField(max_length=15, null=True, verbose_name='称号')),
                ('name', models.CharField(max_length=35, null=True, verbose_name='名前')),
                ('character_id', models.CharField(max_length=6, null=True, verbose_name='キャラクターID')),
                ('description', models.CharField(max_length=255, null=True, verbose_name='概要')),
                ('introduction', wagtailmarkdown.fields.MarkdownField(null=True, verbose_name='説明')),
                ('game_name', models.CharField(max_length=20, null=True, verbose_name='登録されているゲーム')),
                ('character_page_url', models.CharField(max_length=255, null=True, verbose_name='キャラクターのページ')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='画像')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail_graphql.models.GraphQLEnabledModel, 'wagtailcore.page'),
        ),
    ]
