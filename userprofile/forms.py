from django import forms

from . import models


class ProfileForm(forms.ModelForm):
    """Form for creating a new project
    """

    class Meta:
        model = models.Profile
        fields = [
            'business_name',
            'country',
            'website',
        ]
