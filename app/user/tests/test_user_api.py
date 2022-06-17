"""
Test for the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return new user. """
    return get_user_model().objects.create_user(**params)


class PublicAPITests(TestCase):
    """  Test the public feature of the user API """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """ Test creating a user is successful """

        payload = {
            'email': 'lol@example.com',
            'password': 'life_is_fine',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """ Test error returned if user with email exists"""
        payload = {
            'email': 'lol@example.com',
            'password': 'life_is_fine',
            'name': 'Test Name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test an error is returned if password is less than five characters """

        payload = {
            'email': 'lol@example.com',
            'password': 'pe',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test generate token for valid credential """
        user_details = {
            'name': 'Test Name',
            'email': 'lol@sample.com',
            'password': 'admin_admin'
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """ Test return error if credential invalid."""
        create_user(email='random@example', password='good_pass')

        payload = {
            'email': 'random@example',
            'password': 'bad_pass'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """ Test posting a blank password returns an error """

        payload = {
            'email': 'test@example.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
