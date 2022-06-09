from django.shortcuts import render
from django.db import utils as dj_utils
from rest_framework_simplejwt import views as jwt_views
from rest_framework import generics, views as rest_views
from rest_framework import response, status, permissions as drf_permissions
from user import serializers, tasks, permissions, models, utils


# Create your views here.


class TestAPiView(rest_views.APIView):
    def get(self, request):
        tasks.send_auth_email.delay()
        return response.Response({}, status=status.HTTP_200_OK)


class UserAuthTokenView(jwt_views.TokenObtainPairView):
    serializer_class = serializers.UserAuthTokenSerializer


class UserRegistrationAPIView(rest_views.APIView):
    def post(self, request):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except dj_utils.IntegrityError:
            return response.Response({"detail": "Can't register with the email."},
                                     status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserAccountActivationAPIView(rest_views.APIView):
    def post(self, request):
        serializer = serializers.UserActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return response.Response({}, status=status.HTTP_200_OK)
        except dj_utils.IntegrityError:
            return response.Response({"detail": "Can't register with the email."},
                                     status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserCreationAPIView(rest_views.APIView):
    permission_classes = (drf_permissions.IsAuthenticated, permissions.IsAdmin)
    
    def post(self, request):
        serializer = serializers.UserCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({}, status=status.HTTP_200_OK)


class UserListAPIView(generics.ListAPIView):
    queryset = models.User.objects.all()
    permission_classes = (drf_permissions.IsAuthenticated, permissions.IsAdmin)
    serializer_class = serializers.UserSerializer


class UserAccountActivationEmailAPIView(rest_views.APIView):
    permission_classes = (drf_permissions.IsAuthenticated, permissions.IsAdmin)

    def post(self, request):
        serializer = serializers.UserAccountActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.initial_data['user']
        if user.is_active:
            return response.Response({"detail": "User is active!"}, status=status.HTTP_400_BAD_REQUEST)
        utils.generate_account_activation_token_send_email(user=user)
        return response.Response({"detail": "Activation email sent!"}, status=status.HTTP_200_OK)