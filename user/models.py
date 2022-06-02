from django.db import models
from django.contrib.auth import models as auth_model
from core import base_model
from user import constants
# Create your models here.


class User(auth_model.AbstractUser):
    role = models.CharField(max_length=50, choices=constants.RoleType.choices)

    def __str__(self):
        return self.username