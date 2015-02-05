# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=75)),
                ('company', models.CharField(max_length=100, null=True, blank=True)),
                ('city', models.CharField(max_length=100)),
                ('address1', models.CharField(max_length=250)),
                ('address2', models.CharField(max_length=250, null=True, blank=True)),
                ('zip_or_postal_code', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=20)),
                ('fax_number', models.CharField(max_length=20, null=True, blank=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('allow_billing', models.BooleanField(default=True, help_text='Allow billing from this country')),
                ('allow_shipping', models.BooleanField(default=True, help_text='Allow shipping to this country')),
                ('iso_code2', models.CharField(help_text='Two letter ISO code', unique=True, max_length=2)),
                ('iso_code3', models.CharField(help_text='Three letter ISO code', unique=True, max_length=3)),
                ('iso_numeric', models.IntegerField(help_text='Numeric ISO code')),
                ('subject_to_vat', models.BooleanField(default=False, help_text='Is VAT applicable')),
                ('display_order', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('display_order', 'name'),
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(help_text='Abbrevation', max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('display_order', models.IntegerField(default=0)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('country', models.ForeignKey(to='geo.Country')),
            ],
            options={
                'ordering': ('display_order', 'name'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(verbose_name='your text', to='geo.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.ForeignKey(blank=True, to='geo.State', null=True),
            preserve_default=True,
        ),
    ]
