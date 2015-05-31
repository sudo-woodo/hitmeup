from collections import OrderedDict
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MinLengthValidator
from user_accounts.models import UserProfile


MIN_USERNAME_LENGTH = 5


class LoginForm(forms.Form):
    username = forms.CharField(
        validators=[MinLengthValidator(MIN_USERNAME_LENGTH)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'id': 'username',
            'name': 'username',
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'id': 'password',
        'name': 'password',
    }))


class SignupForm(forms.ModelForm, LoginForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'id': 'email',
        'name': 'email',
    }))

    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        'id': 'confirm-password',
        'name': 'confirm-password',
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm_password')


class SignUpExtendedForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First name',
        'id': 'first-name',
        'name': 'first-name',
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name',
        'id': 'last-name',
        'name': 'last-name',
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
                'name': 'phone',
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
                'name': 'bio',
            }
        )
    )


class EditProfileForm(SignUpExtendedForm):
    FIELD_ORDER = [
        'email',
        'first_name', 'last_name', 'phone', 'bio',
    ]

    email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'id': 'email',
        'name': 'email',
    }))

    # Reorder fields
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields = OrderedDict((k, self.fields[k]) for k in self.FIELD_ORDER
                                  # Remaining fields
                                  + list(set(self.fields) -
                                         set(self.FIELD_ORDER)))

class EditPasswordForm(forms.Form):
    current_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Current password',
        'id': 'current-password',
        'name': 'current-password',
    }))

    new_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New password',
        'id': 'new-password',
        'name': 'new-password',
    }))

    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        'id': 'confirm-password',
        'name': 'confirm-password',
    }))
