# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ourcalendar.models


class Migration(migrations.Migration):

    dependencies = [
        ('ourcalendar', '0005_auto_20150504_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurrenceType',
            fields=[
                ('event', models.OneToOneField(related_name='recurrence_type', primary_key=True, serialize=False, to='ourcalendar.Event')),
            ],
        ),
        migrations.CreateModel(
            name='SingleRecurrence',
            fields=[
                ('recurrencetype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ourcalendar.RecurrenceType')),
            ],
            bases=('ourcalendar.recurrencetype',),
        ),
        migrations.CreateModel(
            name='WeeklyRecurrence',
            fields=[
                ('recurrencetype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ourcalendar.RecurrenceType')),
                ('days_of_week', models.CharField(default=b'1000000', max_length=7)),
                ('frequency', models.IntegerField(default=1)),
                ('last_event', models.DateTimeField(default=ourcalendar.models.hour_from_now)),
            ],
            bases=('ourcalendar.recurrencetype',),
        ),
    ]
