from django.conf import settings
from django.db import transaction
from requests_oauthlib import OAuth1, OAuth1Session
from user import models as user_models
from social import models, constants


def generate_twitter_auth_url(user: user_models.User):
    oauth = OAuth1Session(settings.TWITTER_CLIENT_KEY, client_secret=settings.TWITTER_CLIENT_SECRET)
    fetch_response = oauth.fetch_request_token(settings.TWITTER_REQUEST_TOKEN_URL)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    with transaction.atomic():
        auth = {
            "user": user,
            "type": constants.SocialType.twitter,
            "resource_owner_key": resource_owner_key,
            "resource_owner_secret": resource_owner_secret
        }
        models.SocialAuth.objects.create(**auth)
        return settings.TWITTER_AUTHENTICATE_URL.format(resource_owner_key)


def save_twitter_auth_token(*, user: user_models.User, oauth_token_varifier: str):
    social_auth_instance = models.SocialAuth.get_filter_data({"user": user}).order_by('-id').first()
    oauth = OAuth1Session(settings.TWITTER_CLIENT_KEY,
                          client_secret=settings.TWITTER_CLIENT_SECRET,
                          resource_owner_key=social_auth_instance.resource_owner_key,
                          resource_owner_secret=social_auth_instance.resource_owner_secret,
                          verifier=oauth_token_varifier)
    oauth_tokens = oauth.fetch_access_token(settings.TWITTER_ACCESS_TOKEN_URL)
    access_token = oauth_tokens.get('oauth_token')
    access_token_secret = oauth_tokens.get('oauth_token_secret')
    social_auth_instance.access_token = access_token
    social_auth_instance.access_token_secret = access_token_secret
    social_auth_instance.save()
