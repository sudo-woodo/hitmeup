from django.forms import ModelForm
from django import forms
from ourcalendar.models import Calendar, Event
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class EventForm(ModelForm):
    title = forms.CharField(max_length=200, help_text="Event title:")
    start = forms.DateTimeField(widget=DateInput())
    end = forms.DateTimeField(required=False, help_text="End time:")
    location = forms.CharField(max_length=200, required=False, help_text="Location")
    description = forms.CharField(max_length=600, required=False, help_text="Description")
    # gives it all calendars for now...
    calendar = forms.ModelChoiceField(queryset=Calendar.objects.all(), empty_label="Select Calendar:")
    # not sure if below correct...using queryset=User.objects.all() gave errors.
    # users = forms.MultipleChoiceField(choices=User.objects.all(), required=False)

    class Meta:
        model = Event
        fields = ('start',)   # grabs all the fields.


class CalendarForm(ModelForm):

    class Meta:
        model = Calendar
        fields = '__all__'
