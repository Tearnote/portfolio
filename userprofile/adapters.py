from allauth.account.adapter import DefaultAccountAdapter

from userprofile import models


class ProfileAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """Create a profile for the new user
        """

        # Save user as normal
        super().save_user(request, user, form, commit)

        profile = models.Profile()
        profile.user = user
        profile.business_name = form.cleaned_data['business_name']
        profile.country = form.cleaned_data['country']
        profile.website = form.cleaned_data['website']
        profile.save()
