from django.db import transaction
from django.utils import timezone
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt import tokens, exceptions
from rest_framework import serializers, status
from user import models, send_email, email_constant
from core import exceptions as custom_exceptions


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

    def create(self, validated_data):
        validated_data["role"] = "customer"
        validated_data["username"] = validated_data["email"]
        validated_data["is_active"] = False
        with transaction.atomic():
            validated_data['is_active'] = False
            user = models.User.objects.create(**validated_data)
            # create account activation information
            user_activation_instance = models.UserActivation.create_activation_instance(user)

            # send email
            full_name = f"{user.first_name} {user.last_name}"
            TO_EMAILS = [{"email": user.email, "name": full_name}]
            auth_email = send_email.AuthEmail(settings.EMAIL_FROM, TO_EMAILS, "Active your account!")
            dynamic_template_data ={
                "name": full_name,
                "link": f"{settings.FRONTEND_URL}/account-activation?token={user_activation_instance.key}"
            }
            auth_email.send_mail(dynamic_template_data=dynamic_template_data, template_id=email_constant.ACCOUNT_ACTIVATION_TEMPLATE_ID)
            return user


class UserActivationSerializer(serializers.Serializer):
    key = serializers.CharField()
    password = serializers.RegexField(regex=r'[A-Za-z0-9*@#$%^&+=]{8,}')

    def validate(self, attrs):
        token = attrs["key"]
        try:
            user = models.UserActivation.get_user_from_token(token)
        except exceptions.TokenError:
            raise custom_exceptions.SerializerValidationError(status.HTTP_422_UNPROCESSABLE_ENTITY, "token", "Activation key invalid.")

        user_activation_instance = models.UserActivation.get_instance({"user": user, "key": token, "is_used": False})
        if user_activation_instance is None or user_activation_instance.valid_till < timezone.now():
            raise custom_exceptions.SerializerValidationError(status.HTTP_422_UNPROCESSABLE_ENTITY, "token",
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
        auth_email = send_email.AuthEmail(settings.EMAIL_FROM, TO_EMAILS, "Congratulation! Your account activated")
        dynamic_template_data = {
            "name": full_name,
            "login_url": f"{settings.FRONTEND_URL}/login",
            "support_email": "support@insight.com"
        }
        auth_email.send_mail(dynamic_template_data=dynamic_template_data,
                             template_id=email_constant.ACCOUNT_ACTIVATION_CONFIRM_TEMPLATE_ID)

        return user_activation_instance
