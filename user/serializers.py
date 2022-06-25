from abc import ABCMeta, abstractmethod, ABC
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt import tokens, exceptions
from rest_framework import serializers, status
from user import models, send_email, email_constant, tasks, utils
from core import base_serializer, exceptions as custom_exceptions


class BaseUserSerializer(base_serializer.BaseAbstractSerializer):
    first_name = serializers.RegexField(regex=r"^(?=.{1,40}$)[a-zA-Z]+(?:[-'\s][a-zA-Z]+)*$")
    last_name = serializers.RegexField(regex=r"^(?=.{1,40}$)[a-zA-Z]+(?:[-'\s][a-zA-Z]+)*$")
    email = serializers.EmailField(required=True, max_length=150)


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


class UserRegistrationSerializer(BaseUserSerializer):

    def create(self, validated_data):
        validated_data["role"] = "customer"
        validated_data["username"] = validated_data["email"]
        validated_data["is_active"] = False
        with transaction.atomic():
            validated_data['is_active'] = False
            user = models.User.objects.create(**validated_data)
            utils.generate_account_activation_token_send_email(user=user)
            return user


class UserActivationSerializer(base_serializer.BaseAbstractSerializer):
    key = serializers.CharField()
    password = serializers.RegexField(regex=r'[A-Za-z0-9*@#$%^&+=]{8,}')

    def validate(self, attrs):
        token = attrs["key"]
        try:
            user = models.UserActivation.get_user_from_token(token)
        except exceptions.TokenError:
            raise custom_exceptions.SerializerValidationError(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                                              "token",
                                                              "Activation key invalid.")

        user_activation_instance = models.UserActivation.get_instance(
            {"user": user, "key": token, "is_used": False})
        if user_activation_instance is None or user_activation_instance.valid_till < timezone.now():
            raise custom_exceptions.SerializerValidationError(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                                              "token",
                                                              "Activation key invalid.")

        if user.is_active is True:
            raise serializers.ValidationError(detail="User is already activated")
        attrs["user_activation_instance"] = user_activation_instance
        attrs["user"] = user

        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        user_activation_instance = validated_data["user_activation_instance"]

        user_activation_instance.is_used = True
        user_activation_instance.save()

        user.set_password(validated_data["password"])
        user.is_active = True
        user.save()

        # send email
        full_name = f"{user.first_name} {user.last_name}"
        TO_EMAILS = [{"email": user.email, "name": full_name}]
        auth_email = send_email.AuthEmail(settings.EMAIL_FROM, TO_EMAILS,
                                          "Congratulation! Your account activated")
        dynamic_template_data = {
            "name": full_name,
            "login_url": f"{settings.FRONTEND_URL}/login",
            "support_email": "support@insight.com"
        }
        auth_email.send_mail(dynamic_template_data=dynamic_template_data,
                             template_id=email_constant.ACCOUNT_ACTIVATION_CONFIRM_TEMPLATE_ID)

        return user_activation_instance


class UserCreationSerializer(BaseUserSerializer):
    role = serializers.ChoiceField(choices=[("admin", "Admin"), ("customer", "Customer")])

    def validate(self, attrs):
        email = attrs["email"]
        user = models.User.get_user({"username": email})
        if user:
            raise custom_exceptions.SerializerValidationError(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                                              "email",
                                                              "Can't create user with the provided email.")
        return attrs

    def create(self, validated_data):
        validated_data["is_active"] = False
        validated_data["username"] = validated_data["email"]
        with transaction.atomic():
            user = models.User.objects.create(**validated_data)
            utils.generate_account_activation_token_send_email(user=user)
            return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
        "id", "first_name", "last_name", "username", "email", "is_active", "role", "date_joined")


class UserAccountActivationSerializer(base_serializer.BaseAbstractSerializer):
    email = serializers.EmailField(required=True, max_length=150)

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        user = models.User.get_user({"username": self.initial_data['email']})
        if not user:
            raise custom_exceptions.SerializerValidationError(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                                              "email",
                                                              "User not found with the provided email")
        self.initial_data['user'] = user
        return True
