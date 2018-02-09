# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command


def load_data(apps, schema_editor):
    call_command('loaddata', 'initial_data', app_label='doorstep', verbosity=0)


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SysConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('value', models.CharField(max_length=250, blank=True)),
                ('description', models.CharField(max_length=500)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'doorstep_sys_config',
                'verbose_name': 'System Config',
                'verbose_name_plural': 'System Configs',
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(load_data),
    ]
