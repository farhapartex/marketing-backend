from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from user import models


class UserAuthTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {
            "username": self.user.username,
            "role": self.user.role,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }

        return data


class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.RegexField(regex=r"^(?=.{1,40}$)[a-zA-Z]+(?:[-'\s][a-zA-Z]+)*$")
    last_name = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)
    password = serializers.RegexField(regex=r'[A-Za-z0-9*@#$%^&+=]{8,}')

    def create(self, validated_data):
        validated_data["role"] = "customer"
        validated_data["username"] = validated_data["email"]
        validated_data["is_active"] = False
        with transaction.atomic():
            user = models.User.objects.create(**validated_data)
            # create account activation information
            models.UserActivation.create_activation_instance(user)
            return user

