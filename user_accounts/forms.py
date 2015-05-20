from django.contrib.auth.models import User
from django import forms
from user_accounts.models import UserProfile


class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'id': 'user',
        'name': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'id': 'password',
        'name': 'Password'
    }))


class SignupForm(forms.ModelForm, UserForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'id': 'email',
        'name': 'email'
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class SignUpExtendedForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First name',
        'id': 'firstname',
        'name': 'firstname'
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name',
        'id': 'lastname',
        'name': 'lastname'
    }))

    phone = forms.CharField(
        required=False,
        max_length=15,
        validators=[UserProfile.phone_regex],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Phone number',
                'id': 'phone',
                'name': 'phone'
            }
        )
    )

    bio = forms.CharField(
        required=False,
        max_length=300,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Write a short bio about yourself.',
                'id': 'bio',
                'name': 'bio'
            }
        )
    )