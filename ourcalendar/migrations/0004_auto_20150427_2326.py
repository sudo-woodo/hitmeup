# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ourcalendar', '0003_auto_20150427_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 23, 26, 12, 118245, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 23, 26, 12, 118206, tzinfo=utc)),
        ),
    ]
