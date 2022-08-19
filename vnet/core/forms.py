from typing import Dict
from re import search, compile, findall

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as __
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

from .models import CoreUser
from .tasks import create_azure_identity


class CoreUserCreationForm(forms.Form):
    username = forms.CharField(max_length=191, required=True)
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    password_2 = forms.CharField(required=True)

    @property
    def errors(self):
        errors: Dict = super().errors
        term = '@/./+/-/_'

        if errors.get('username'):
            for key, error in enumerate(errors.get('username', [])):
                if term in error:
                    repaired_term = error.replace(f'{term} characters', '_ character')
                    errors['username'][key] = repaired_term

        return errors

    def clean_password(self):
        data: Dict = self.cleaned_data
        password1 = data.get('password')
        password2 = self.data.get('password_2')
        email = data.get('email')
        username = data.get('username')

        # passwords not similar
        if password1 != password2:
            raise ValidationError(__('The passwords do not match'))

        # similar to the email
        t_user = CoreUser(
            username=username,
            email=email
        )
        validate_password(password1, t_user)

        return password1

    def clean_username(self):
        username = self.cleaned_data.get('username')
        CoreUser.username_validator(username)

        # username exists
        if CoreUser.objects.filter(username=username).count() > 0:
            raise ValidationError(__(f'The username \'{username}\' already exists'))

        # weird characters
        pt = compile(r'[^0-9a-zA-Z_]')
        if search(pt, username):
            illegals = findall(pt, username)
            raise ValidationError(__(f'No special characters on username (like: {", ".join(illegals)}), except _'))

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            validate_email(email)

        # email exists
        if CoreUser.objects.filter(email=email).count() > 0:
            raise ValidationError(__(f'The email \'{email}\' already exists'))
        return email

    def save(self) -> CoreUser:
        """
            If form is valid and data changed, returns \n
            {\n
                'new_user': User ->  USER instance,\n
                'token_key': Token.key -> STRING\n
            }\n
        """
        data: Dict = self.cleaned_data
        av_items = data.keys()
        req_items = ['username', 'email', 'password', 'first_name', 'last_name']
        missing_keys = [key for key in req_items if key not in av_items]

        if len(missing_keys) == 0:
            new_user = CoreUser(
                username=data.get('username'),
                email=data.get('email'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                meeting_name=data.get('username')
            )
            new_user.set_password(data.get('password'))
            new_user.save()
            create_azure_identity(new_user.pk)
            return new_user
