# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0006_userprofile_did_extended_signup'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='registration_id',
            field=models.CharField(max_length=300, blank=True),
        ),
    ]
