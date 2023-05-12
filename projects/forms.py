from django import forms

from . import models


class ProjectForm(forms.ModelForm):
    """Form for creating a new project
    """

    class Meta:
        model = models.Project
        fields = [
            'name',
            'description',
        ]


class TestimonialForm(forms.ModelForm):
    """Form for creating a new testimonial
    """

    class Meta:
        model = models.Testimonial
        fields = [
            'body',
        ]
