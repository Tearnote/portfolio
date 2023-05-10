from django.conf import settings
from django.db import models
import uuid


class Project(models.Model):
    """A project commission throughout its entire lifecycle
    """

    NEW = "HEY"
    PAYABLE = "$$$"
    IN_PROGRESS = "WIP"
    COMPLETED = "GUD"
    REJECTED = "NOP"
    CANCELLED = "NAH"
    STATUS_CHOICES = [
        (NEW, "New"),
        (PAYABLE, "Payable"),
        (IN_PROGRESS, "In progress"),
        (COMPLETED, "Completed"),
        (REJECTED, "Rejected"),
        (CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=NEW,
    )
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=2048)
    quote_amount = models.PositiveIntegerField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    """A user's review of the website owner's services
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=2048)

    def __str__(self):
        return f"{self.user}'s {self.project} testimonial"
