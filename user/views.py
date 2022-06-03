from django.shortcuts import render
from rest_framework_simplejwt import views as jwt_views
from user import serializers
# Create your views here.


class UserAUthTokenView(jwt_views.TokenObtainPairView):
    serializer_class = serializers.UserAuthTokenSerializer
