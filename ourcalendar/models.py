from django.utils import timezone
from django.db import models
from django.forms import ModelForm
from django import forms


class User(models.Model):
    name = models.CharField(max_length=50)


class Calendar(models.Model):
    title = models.CharField(max_length=200)
    color = models.CharField(max_length=100)
    privacy = models.IntegerField(default=0)
    user = models.ForeignKey(User)


class Event(models.Model):
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    calendar = models.ForeignKey(Calendar)
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    users = models.ManyToManyField(User)


class EventForm(ModelForm):
    title = forms.CharField(max_length=200, help_text="Event title:")
    start = forms.DateTimeField(help_text="Start time:")
    end = forms.DateTimeField(required=False, help_text="End time:")
    location = forms.CharField(max_length=200, required=False, help_text="Location")
    description = forms.CharField(max_length=600, required=False, help_text="Description")
    # gives it all calendars for now...
    calendar = forms.ModelChoiceField(queryset=Calendar.objects.all(), empty_label="Select Calendar:")
    # not sure if below correct...using queryset=User.objects.all() gave errors.
    users = forms.MultipleChoiceField(choices=User.objects.all(), required=False)

    class Meta:
        model = Event
        fields = '__all__'   # grabs all the fields.


class CalendarForm(ModelForm):

    class Meta:
        model = Calendar
        fields = '__all__'

