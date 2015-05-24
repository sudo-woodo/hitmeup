from django.contrib.auth.models import User
from django import forms
from user_accounts.models import UserProfile


class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'id': 'username',
        'name': 'username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'id': 'password',
        'name': 'password',
    }))


class SignupForm(forms.ModelForm, UserForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'id': 'email',
        'name': 'email',
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password')


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


class EditSettingsForm(SignupForm, SignUpExtendedForm):
    current_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Current password',
        'id': 'current-password',
        'name': 'current-password',
    }))

    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New password',
        'id': 'new-password',
        'name': 'new-password',
    }))

    username = password = None

    class Meta(SignupForm.Meta):
        fields = ('email', 'current_password', 'new_password',
                  'first_name', 'last_name', 'phone', 'bio')
