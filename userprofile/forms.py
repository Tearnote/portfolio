from django import forms
from allauth.account.forms import SignupForm
from django_countries.fields import CountryField

from . import models


class ProfileSignupForm(SignupForm):
    """Extended form to capture profile fields on sign-up
    """

    business_name = forms.CharField(max_length=256)
    country = CountryField().formfield()
    website = forms.URLField()


class ProfileForm(forms.ModelForm):
    """Form for modifying the user profile
    """

    class Meta:
        model = models.Profile
        fields = [
            'business_name',
            'country',
            'website',
        ]
