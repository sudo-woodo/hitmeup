# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0006_userprofile_did_extended_signup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('profile', models.OneToOneField(related_name='subscription', primary_key=True, serialize=False, to='user_accounts.UserProfile')),
                ('general', models.BooleanField(default=True)),
                ('friend_notifications', models.BooleanField(default=True)),
            ],
        ),
    ]
