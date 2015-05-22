from django.contrib.auth.models import User
from django.core.validators import RegexValidator
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
        'name': 'Email'
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class EditForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your First Name',
        'id': 'first_name',
        'name': 'First Name'
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Last Name',
        'id': 'last_name',
        'name': 'Last Name'
    }))

    current_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Current Password',
        'id': 'current_password',
        'name': 'Current Password'
    }))

    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter New Password',
        'id': 'new_password',
        'name': 'New Password'
    }))

    email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Email',
        'id': 'email',
        'name': 'Email'
    }))

    bio = forms.CharField(
        required=False,
        max_length=300,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write about a quick bio about yourself.',
                'id': 'bio',
                'name': 'Bio'
            }
        )
    )

    phone_regex = RegexValidator(
        regex=r'^\+?\d{10,15}$',
        message="Phone number must be between 10-15 digits")

    phone = forms.CharField(
        required=False,
        max_length=15,
        validators=[phone_regex],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Phone Number',
                'id': 'phone',
                'name': 'Phone'
            }
        )
    )


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
                'class': 'form-control',
                'placeholder': 'Write a short bio about yourself.',
                'id': 'bio',
                'name': 'bio'
            }
        )
    )
