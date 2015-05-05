# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ourcalendar', '0002_auto_20150504_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=600, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(default=b'New Event', max_length=200),
        ),
    ]
