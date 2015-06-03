from datetimewidget.widgets import DateWidget
from django import forms


class TritonLinkLoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'User ID / PID',
        'id': 'user',
        'name': 'Username'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password / PAC',
        'id': 'password',
        'name': 'Password'
    }))
    start_date_of_quarter = forms.DateField(widget=DateWidget(usel10n=False, bootstrap_version=3, options={
        'clearBtn': False,
        'format': 'mm/dd/yyyy',
    }))