from django.shortcuts import render

from rest_framework import views, response, permissions, status
from social import utils, serializers, models
# Create your views here.


class GenerateTwitterAuthUrl(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return response.Response(data={"auth_url": utils.generate_twitter_auth_url(request.user)})


class SubmitTwitterAuthHandlerAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = serializers.SubmitTwitterOauthHandlerSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        utils.save_twitter_auth_token(user=request.user, oauth_token_varifier=serializer.validated_data.get("oauth_token_varifier"))

        return response.Response(data={"detail": "Twitter access token saved"}, status=status.HTTP_200_OK)