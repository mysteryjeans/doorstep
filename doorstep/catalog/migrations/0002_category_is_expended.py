# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_expended',
            field=models.BooleanField(default=False, help_text='Catergory will always shown expended'),
            preserve_default=True,
        ),
    ]
