# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ourcalendar', '0002_auto_20150426_0159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendar',
            old_name='privacy_level',
            new_name='privacy',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='end_time',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='start_time',
            new_name='start',
        ),
    ]
