import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class AddAuthorForm(forms.Form):
    first_name = forms.CharField(max_length=100, help_text="Enter your first name")
    last_name = forms.CharField(max_length=100, help_text="Enter your last name")
    bio = forms.Textarea()
    date_of_birth = forms.DateField(help_text="Enter date of birth")

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']

        current_date = datetime.date.today()

        if date_of_birth > current_date:
            raise ValidationError(_("Cannot set future date of birth. Please set correct date"))

        return date_of_birth


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=False, help_text="Enter first name")
    last_name = forms.CharField(max_length=50, required=False, help_text="Enter last name")
    email = forms.EmailField(max_length=200, help_text="Required. Inform a valid email address")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

