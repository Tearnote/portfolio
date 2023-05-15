from django import forms


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
        pass  # TODO
