from datetime import datetime
from django.db import models

# Create your models here.

class User(models.Model):
    #id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class Calendar(models.Model):
    """

    """
    title = models.CharField(max_length=200)
    #id = models.AutoField(primary_key=True)
    color = models.CharField(max_length=100)
    privacy_level = models.IntegerField(default=0)
    # user dummy until Kavin/Clarence
    user = models.ForeignKey(User)

"""
# Might not need
class Attendee(models.Model):
    event = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
"""

class Event(models.Model):
    """

    """
    #id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    title = models.CharField(max_length=200)
    # repeats
    calendar = models.ForeignKey(Calendar)
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    users = models.ManyToManyField(User)



