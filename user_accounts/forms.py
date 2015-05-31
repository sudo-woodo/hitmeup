from collections import OrderedDict
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MinLengthValidator
from communications.models import Subscription
from user_accounts.models import UserProfile


MIN_USERNAME_LENGTH = 5


class LoginForm(forms.Form):
    username = forms.CharField(
        validators=[MinLengthValidator(MIN_USERNAME_LENGTH)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))


class SignupForm(forms.ModelForm, LoginForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }))

    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm_password')


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


class EditProfileForm(SignUpExtendedForm):
    FIELD_ORDER = [
        'email',
        'first_name', 'last_name', 'phone', 'bio',
    ]

    email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }))

    # Reorder fields
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields = OrderedDict((k, self.fields[k]) for k in self.FIELD_ORDER
                                  # Remaining fields
                                  + list(set(self.fields) -
                                         set(self.FIELD_ORDER)))

class EditSubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('general', 'friend_notifications')

class EditPasswordForm(forms.Form):
    current_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Current password',
    }))

    new_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New password',
    }))

    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))
