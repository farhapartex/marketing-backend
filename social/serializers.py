from rest_framework import serializers, status
from social import models
from core import exceptions, base_serializer


class SubmitTwitterOauthHandlerSerializer(base_serializer.BaseAbstractSerializer):
    oauth_token_varifier = serializers.CharField()

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        user = self.context['request'].user
        social_auth_instance = models.SocialAuth.get_filter_data({"user": user}).order_by(
            '-id').first()
        if social_auth_instance is None:
            raise exceptions.SerializerValidationError(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                                       "oauth_token_varifier",
                                                       "Twitter auth instance not found. Please login again.")
        return True
