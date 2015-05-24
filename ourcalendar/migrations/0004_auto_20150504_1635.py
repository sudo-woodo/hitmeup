# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ourcalendar.models


class Migration(migrations.Migration):

    dependencies = [
        ('ourcalendar', '0003_auto_20150504_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(default=ourcalendar.models.hour_from_now),
        ),
    ]
