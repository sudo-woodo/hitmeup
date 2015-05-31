# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ourcalendar', '0006_recurrencetype_singlerecurrence_weeklyrecurrence'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weeklyrecurrence',
            old_name='last_event',
            new_name='last_event_end',
        ),
    ]
