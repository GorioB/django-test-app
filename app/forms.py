from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import ContactUser


class ContactUserModelForm(ModelForm):
    class Meta:
        model = ContactUser
        fields = [
            'email_address', 'phone_number',
            'my_property_type', 'notes'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = None
        self.helper.add_input(
            Button(
                'submit',
                'Submit',
                css_class='btn btn-primary',
                data_loading_text="Submitting"
            )
        )
