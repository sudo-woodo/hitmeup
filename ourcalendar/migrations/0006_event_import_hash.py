# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ourcalendar', '0005_auto_20150504_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='import_hash',
            field=models.IntegerField(default=0),
        ),
    ]
