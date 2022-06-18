"""
Serializers for the User API View
"""
from django.contrib.auth import (
    get_user_model, authenticate)
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """ Serializers for the user object """

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """ Create and return  a user with encrypted password. """

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Update and return a user with encrypted password """

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={
            "input_type": 'password',
        }, trim_whitespace=True
    )

    def validate(self, attrs):
        """ validate and authenticate the user. """

        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided information')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
