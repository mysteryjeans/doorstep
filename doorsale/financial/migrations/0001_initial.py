# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(help_text='ISO Currency Code', unique=True, max_length=3)),
                ('exchange_rate', models.FloatField(default=1.0)),
                ('locale', models.CharField(max_length=10, blank=True)),
                ('display_format', models.CharField(help_text='Display format: 1.2 => "${0:,.2f}".format(price) => $1.20 (python format string)', max_length=50)),
                ('is_primary', models.BooleanField(default=False, help_text='Default currency of prices & costs. When you change primary currency, make sure to update exchange rates, prices & costs.')),
                ('is_active', models.BooleanField(default=False)),
                ('updated_by', models.CharField(max_length=100)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name_plural': 'Currencies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('method', models.CharField(help_text='Tax deduction method: fixed tax per product or percentage (in fraction) of price per product', max_length=2, choices=[('PE', 'Percentage'), ('FI', 'Fixed')])),
                ('rate', models.FloatField(default=0.0)),
                ('updated_by', models.CharField(max_length=100)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'financial_tax',
                'verbose_name_plural': 'Taxes',
            },
            bases=(models.Model,),
        ),
    ]
