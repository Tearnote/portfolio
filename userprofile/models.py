from django.conf import settings
from django.db import models
from django_countries.fields import CountryField


class Profile(models.Model):
    """Extra fields for each user
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    business_name = models.CharField(max_length=256)
    country = CountryField()
    website = models.URLField()

    def __str__(self):
        return self.user
