# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ourcalendar', '0004_auto_20150504_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='color',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(regex=b'^#[\\dA-F]{6}', message=b'Color must be in 6-digit hex format.')]),
        ),
    ]
