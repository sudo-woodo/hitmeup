# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ourcalendar', '0006_event_import_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='import_hash',
            field=models.BigIntegerField(default=0),
        ),
    ]
