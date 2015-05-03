from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.forms import ModelForm
from django import forms


class Calendar(models.Model):
    title = models.CharField(max_length=200)
    color = models.CharField(max_length=100)
    privacy = models.IntegerField(default=0)
    owner = models.ForeignKey(User)


class Event(models.Model):
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    calendar = models.ForeignKey(Calendar)
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=600)