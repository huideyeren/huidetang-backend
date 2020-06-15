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
        ('wagtailcore', '0046_auto_20200317_0757'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('update_date', models.DateField(verbose_name='更新日')),
                ('github_url', models.URLField(blank=True, verbose_name='GitHubの個人ページ')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='author.AuthorPage', verbose_name='著者')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail_graphql.models.GraphQLEnabledModel, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='PortoflioIndexPage',
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
            name='PortfolioPageTechnology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='technology', to='portfolio.PortfolioPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_portfoliopagetechnology_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PortfolioPageRelatedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_links', to='portfolio.PortfolioPage', verbose_name='関連ページ')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(wagtail_graphql.models.GraphQLEnabledModel, models.Model),
        ),
        migrations.CreateModel(
            name='PortfolioPageJobCareer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title', models.CharField(max_length=50, verbose_name='タイトル')),
                ('start_date', models.DateField(verbose_name='開始日')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='終了日')),
                ('job_role', models.CharField(blank=True, max_length=50, null=True, verbose_name='役割')),
                ('description', wagtailmarkdown.fields.MarkdownField(blank=True, null=True, verbose_name='説明')),
                ('portfolio', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_career', to='portfolio.PortfolioPage', verbose_name='職務経歴')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(wagtail_graphql.models.GraphQLEnabledModel, models.Model),
        ),
        migrations.AddField(
            model_name='portfoliopage',
            name='tech',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='portfolio.PortfolioPageTechnology', to='taggit.Tag', verbose_name='経験または興味のある技術'),
        ),
    ]