"""
Tests for models
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """ Test models """

    def test_create_user_with_email_successful(self):
        """ Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'test_pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test email is normalized for new users."""

        sample_emails = [
            ['test1@EXAMple.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TeSt3@ExaMple.com', 'TeSt3@example.com'],
            ['TESt3@ExaMple.com', 'TESt3@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_use_without_email_raises_error(self):
        """" Test that creating a user without an email raise a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_superuser(self):
        """ Test creating Superuser """
        user = get_user_model().objects.create_superuser(
            'test@example.com', 'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful"""

        user = get_user_model().objects.create_user('user@example.com', 'test123')
        recipe = models.Recipe.objects.create(user=user,
            title='sample recipe name',
            time_minutes=5, price=Decimal('5.50'), description="sample recipe description")

        self.assertEqual(str(recipe), recipe)
