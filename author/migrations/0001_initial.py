# Generated by Django 3.0.4 on 2020-03-17 07:57

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail_graphql.models
import wagtailmarkdown.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('wagtailcore', '0046_auto_20200317_0757'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorIndexPage',
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
            name='AuthorPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('profile', wagtailmarkdown.fields.MarkdownField(verbose_name='プロフィール')),
                ('nickname', models.CharField(blank=True, max_length=25, null=True, verbose_name='ニックネーム')),
                ('first_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='名')),
                ('middle_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='ミドルネーム')),
                ('family_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='姓')),
                ('name', models.CharField(blank=True, max_length=80, null=True, verbose_name='表示名')),
                ('is_surname_first', models.BooleanField(blank=True, null=True, verbose_name='姓が先の表記')),
                ('use_nickname', models.BooleanField(blank=True, null=True, verbose_name='ニックネームの使用')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail_graphql.models.GraphQLEnabledModel, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='AuthorPageSnsLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=255, verbose_name='名前')),
                ('url', models.URLField(verbose_name='URL')),
                ('Author', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='sns_links', to='author.AuthorPage', verbose_name='SNSなどのURL')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(wagtail_graphql.models.GraphQLEnabledModel, models.Model),
        ),
        migrations.CreateModel(
            name='AuthorPagePortfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=255, verbose_name='名前')),
                ('url', models.URLField(verbose_name='URL')),
                ('Author', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_links', to='author.AuthorPage', verbose_name='ポートフォリオURL')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(wagtail_graphql.models.GraphQLEnabledModel, models.Model),
        ),
        migrations.CreateModel(
            name='AuthorPageInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='interest_items', to='author.AuthorPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_authorpageinterest_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AuthorPageAmazonWishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=255, verbose_name='名前')),
                ('url', models.URLField(verbose_name='URL')),
                ('Author', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='amazon_wish_list_links', to='author.AuthorPage', verbose_name='AmazonのほしいものリストのURL')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(wagtail_graphql.models.GraphQLEnabledModel, models.Model),
        ),
        migrations.AddField(
            model_name='authorpage',
            name='interest',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='author.AuthorPageInterest', to='taggit.Tag', verbose_name='興味を持っていること'),
        ),
        migrations.AddField(
            model_name='authorpage',
            name='portrait',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='画像'),
        ),
    ]