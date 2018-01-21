from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse

from .models import ContactUser

import json

# Create your tests here.


class IndexTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')

        # Test that we get an OK response
        self.assertEquals(response.status_code, 200)

        # Test that the context contains some sort of form
        self.assertTrue(('form' in response.context))


class ApiPostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_data = {
            'email_address': 'correct@email.com',
            'phone_number': '+631234567890',
            'my_property_type': ContactUser.SINGLE_FAMILY,
            'notes': 'Notes must contain at least 10 characters'
        }

    def contactuser_validation_test(self, key, scenarios):
        data = self.test_data

        for [scenario, error_message] in scenarios:
            data[key] = scenario
            response = self.client.post(
                reverse('ajax_submit'),
                data=data
            )

            response_json = json.loads(response.content)
            self.assertIn(error_message, response_json['error'][key])

    def test_validation(self):
        # empty form
        response = self.client.post(
            reverse('ajax_submit'),
            data={
                'email_address': '',
                'phone_number': '',
                'my_property_type': '',
                'notes': ''
            }
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content)['success'], False)

        # invalid email
        scenarios = [
            ['', 'This field is required.'],
            ['wrong_format_email', 'Enter a valid email address.'],
            ['a'*500, 'Ensure this value has at most 254 characters (it has 500).']
        ]

        self.contactuser_validation_test('email_address', scenarios)

        # # invalid phone number
        scenarios = [
            ['', 'This field is required.'],  # no input
            ['bad_phone', 'Only numbers, (, ), -, +, and spaces are allowed.'],
            ['(+63)123456789123456', 'Phone number must contain 7-15 digits'],
            ['123', 'Phone number must contain 7-15 digits'],
            ['12345678901234561234523124123123123123', 'Ensure this value has at most 20 characters (it has 38).']  # field overflow
        ]

        self.contactuser_validation_test('phone_number', scenarios)

        # invalid proerty type
        scenarios = [
            ['', 'This field is required.'],
            ['L', 'Select a valid choice. L is not one of the available choices.'],
            ['ABC', 'Select a valid choice. ABC is not one of the available choices.']
        ]

        self.contactuser_validation_test('my_property_type', scenarios)

        # invalid note
        scenarios = [
            ['abc', 'Notes must consist of at least 10 characters.']
        ]

        self.contactuser_validation_test('notes', scenarios)

    def test_success(self):
        response = self.client.post(
            reverse('ajax_submit'),
            data=self.test_data
        )

        self.assertTrue(json.loads(response.content)['success'])
        self.assertEqual(
            len(ContactUser.objects.filter(**self.test_data)),
            1
        )  # one database entry with test details has been created
        self.assertEqual(len(mail.outbox), 1)  # email has been sent

    def test_csrf(self):
        client = Client(enforce_csrf_checks=True)

        response = client.post(
            reverse('ajax_submit'),
            data=self.test_data
        )

        self.assertEqual(response.status_code, 403)
