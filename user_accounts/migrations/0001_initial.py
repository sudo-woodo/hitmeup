# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('outgoing_friends', models.ManyToManyField(related_name='incoming_friends', through='user_accounts.Friendship', to='user_accounts.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='friendship',
            name='from_friend',
            field=models.ForeignKey(related_name='outgoing_friendships', to='user_accounts.UserProfile'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='to_friend',
            field=models.ForeignKey(related_name='incoming_friendships', to='user_accounts.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('from_friend', 'to_friend')]),
        ),
    ]
