# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('group', models.CharField(help_text='Group text under which links will be compiled for display.', max_length=100)),
                ('url', models.CharField(help_text='Url of resource this link points to.', max_length=500, null=True, blank=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(help_text='Title text to be used in url for this post', unique=True, max_length=255)),
                ('content', models.TextField()),
                ('status', models.CharField(default='DR', max_length=2, choices=[('DR', 'Draft'), ('WD', 'Withdrawn'), ('PU', 'Published')])),
                ('tags', models.CharField(help_text='Tags for the published article', max_length=255, null=True, blank=True)),
                ('published', models.DateTimeField(null=True, verbose_name='published date', blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('created_by', models.CharField(max_length=100)),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('updated_by', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('slug',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='link',
            name='page',
            field=models.ForeignKey(blank=True, to='pages.Page', help_text='Page resource this link points to.', null=True),
            preserve_default=True,
        ),
    ]
