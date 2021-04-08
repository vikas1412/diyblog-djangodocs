import datetime

from django import forms
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


