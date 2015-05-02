# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('out_friends', models.ManyToManyField(related_name='in_friends', through='user_accounts.Friendship', to='user_accounts.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='friendship',
            name='from_friend',
            field=models.ForeignKey(related_name='out_friendships', to='user_accounts.UserProfile'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='to_friend',
            field=models.ForeignKey(related_name='in_friendships', to='user_accounts.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('from_friend', 'to_friend')]),
        ),
    ]
