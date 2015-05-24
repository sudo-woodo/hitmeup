# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0005_auto_20150523_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='facebook_id',
            field=models.CharField(default=0, max_length=30),
        ),
    ]
