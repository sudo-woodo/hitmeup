from django.contrib.auth.models import User
from django import forms
from user_accounts.models import UserProfile


class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))


class SignupForm(forms.ModelForm, UserForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class SignUpExtendedForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First name',
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name',
    }))

    phone = forms.CharField(
        required=False,
        max_length=15,
        validators=[UserProfile.phone_regex],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Phone number',
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
            }
        )
    )


class EditSettingsForm(SignupForm, SignUpExtendedForm):
    current_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Current password',
    }))

    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New password',
    }))

    username = password = None

    class Meta(SignupForm.Meta):
        fields = ('email', 'current_password', 'new_password',
                  'first_name', 'last_name', 'phone', 'bio')
