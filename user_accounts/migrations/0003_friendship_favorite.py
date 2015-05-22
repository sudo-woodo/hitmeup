# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0002_auto_20150503_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendship',
            name='favorite',
            field=models.BooleanField(default=False),
        ),
    ]
