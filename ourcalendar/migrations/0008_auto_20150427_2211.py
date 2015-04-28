# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ourcalendar', '0007_auto_20150427_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 28, 5, 11, 45, 419319, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 28, 5, 11, 45, 419193, tzinfo=utc)),
        ),
    ]
