from django.shortcuts import render
from django.db import utils as dj_utils
from rest_framework_simplejwt import views as jwt_views
from rest_framework import views as rest_views
from rest_framework import response, status
from user import serializers, tasks
# Create your views here.


class TestAPiView(rest_views.APIView):
    def get(self, request):
        tasks.send_auth_email.delay()
        return response.Response({}, status=status.HTTP_200_OK)


class UserAUthTokenView(jwt_views.TokenObtainPairView):
    serializer_class = serializers.UserAuthTokenSerializer


class UserRegistrationAPIView(rest_views.APIView):
    def post(self, request):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except dj_utils.IntegrityError:
            return response.Response({"detail": "Can't register with the email."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserAccountActivationAPIView(rest_views.APIView):
    def post(self, request):
        serializer = serializers.UserActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return response.Response({}, status=status.HTTP_200_OK)
        except dj_utils.IntegrityError:
            return response.Response({"detail": "Can't register with the email."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)