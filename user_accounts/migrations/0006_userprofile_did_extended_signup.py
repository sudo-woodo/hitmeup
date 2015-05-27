# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0005_auto_20150519_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='did_extended_signup',
            field=models.BooleanField(default=False),
        ),
    ]
