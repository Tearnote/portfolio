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
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'eg. Redesign the company website'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Please describe in detail what you need to be'
                ' built, and what the scope is. Including as much detail as'
                ' possible will help avoid resubmissions. You can include any'
                ' supplementary material like branding guidelines via email'
                ' after creating the project.'
            }),
        }


class TestimonialForm(forms.ModelForm):
    """Form for creating a new testimonial
    """

    class Meta:
        model = models.Testimonial
        fields = [
            'body',
        ]
