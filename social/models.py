from django.db import models
from core import base_model
from user import models as user_models
from social import constants


class SocialAuth(base_model.BaseAbstractModel):
    user = models.ForeignKey(user_models.User, related_name="social_auths", on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=constants.SocialType.choices)
    resource_owner_key = models.CharField(max_length=300, blank=True, null=True)
    resource_owner_secret = models.CharField(max_length=300, blank=True, null=True)
    access_token = models.CharField(max_length=300, blank=True, null=True)
    access_token_secret = models.CharField(max_length=300, blank=True, null=True)
    is_process_complete = models.BooleanField(default=False)

