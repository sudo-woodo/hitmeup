# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0002_auto_20150503_0800'),
        ('ourcalendar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendar',
            name='user',
        ),
        migrations.RemoveField(
            model_name='event',
            name='users',
        ),
        migrations.AddField(
            model_name='calendar',
            name='owner',
            field=models.ForeignKey(related_name='calendars', default=None, to='user_accounts.UserProfile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='calendar',
            name='color',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(regex=b'^[\\dA-F]{6}', message=b'Color must be in 6-digit hex format.')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='calendar',
            field=models.ForeignKey(related_name='events', to='ourcalendar.Calendar'),
        ),
    ]
