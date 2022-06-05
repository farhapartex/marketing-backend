from django.db import models
from django.utils import timezone
from django.contrib.auth import models as auth_model
from rest_framework_simplejwt import tokens
from datetime import timedelta
from core import base_model
from user import constants


class User(auth_model.AbstractUser):
    role = models.CharField(max_length=50, choices=constants.RoleType.choices)

    def __str__(self):
        return self.username

    @classmethod
    def get_user(cls, payload:dict):
        return cls.objects.get(**payload)


class UserActivation(base_model.BaseAbstractModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    key = models.CharField(max_length=300)
    valid_till = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.key}"

    @classmethod
    def create_activation_instance(cls, user):
        data = {
            'user': user,
            'key': str(tokens.RefreshToken.for_user(user)),
            'valid_till': timezone.now() + timedelta(days=1)  # Activation key will be valid for 2 days after creation
        }

        return cls.objects.create(**data)

    @classmethod
    def get_user_from_token(cls, token: str):
        token_payload = tokens.UntypedToken(token).payload
        user_id = token_payload["user_id"]
        return User.get_user({"id": user_id})

