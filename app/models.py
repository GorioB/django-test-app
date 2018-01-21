from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
# Create your models here.


def integers_validator(value):
    integer_chars = [x for x in value if ord(x) > 47 and ord(x) < 58]

    if len(integer_chars) < 7 or len(integer_chars) > 15:
        raise ValidationError('Phone number must contain 7-15 digits')


class ContactUser(models.Model):
    SINGLE_FAMILY = 'S'
    HIGHRISE_CONDO = 'H'
    TOWNHOUSE = 'T'
    PROPERTY_TYPE_CHOICES = (
        (SINGLE_FAMILY, 'Single Family'),
        (HIGHRISE_CONDO, 'Highrise Condo'),
        (TOWNHOUSE, 'Townhouse')
    )

    phone_regex = RegexValidator(
        regex=r'^[0-9\-\(\) \+]+$',
        message="Only numbers, (, ), -, +, and spaces are allowed."
    )

    email_address = models.EmailField()
    phone_number = models.CharField(max_length=20, validators=[phone_regex, integers_validator])
    my_property_type = models.CharField(max_length=1, choices=PROPERTY_TYPE_CHOICES)
    notes = models.TextField(
        blank=True,
        default='',
        validators=[
            MinLengthValidator(
                10,
                message="Notes must consist of at least 10 characters."
            )
        ]
    )

    def __str__(self):
        return '{} - {}'.format(self.email_address, self.get_my_property_type_display())
