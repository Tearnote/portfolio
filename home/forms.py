from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string


class ContactForm(forms.Form):
    """Form for sending a contact email
    """

    name = forms.CharField(label='Your name', max_length=200)
    sender = forms.EmailField(label='Your email address')
    project_uuid = forms.UUIDField(
        label='Project reference number',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Optional. Please include if the query is about a'
            ' specific project you created.'
        }),
    )
    message = forms.CharField(widget=forms.Textarea)

    def save(self):
        """Send an email to website owner
        """

        if not self.is_valid():
            return False

        email_context = {
            'name': self.cleaned_data['name'],
            'sender': self.cleaned_data['sender'],
            'project_uuid': self.cleaned_data['project_uuid'],
            'message': self.cleaned_data['message'],
        }
        send_mail(
            render_to_string(
                'home/email/contact_subject.txt',
                email_context, None
            ).strip(),
            render_to_string(
                'home/email/contact_message.txt',
                email_context, None
            ),
            None, [owner.email for owner in User.objects.filter(is_staff=True)]
        )
