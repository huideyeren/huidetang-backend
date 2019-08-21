# Generated by Django 2.1.7 on 2019-08-21 03:52

from django.db import migrations, models
import django.db.models.deletion
import wagtail_graphql.models
import wagtailmarkdown.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('wagtailcore', '0042_auto_20190820_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('nickname', models.CharField(max_length=15, null=True, verbose_name='称号')),
                ('name', models.CharField(max_length=35, null=True, verbose_name='名前')),
                ('character_id', models.CharField(max_length=6, null=True, verbose_name='キャラクターID')),
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
