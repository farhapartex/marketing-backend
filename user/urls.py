from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from user import views

router = DefaultRouter()

urlpatterns = [
    re_path(r"^api/v1/test-api/", views.TestAPiView.as_view()),
    re_path(r"^api/v1/token/", views.UserAuthTokenView.as_view()),
    re_path(r"^api/v1/registration/", views.UserRegistrationAPIView.as_view()),
    re_path(r"^api/v1/account-activation/", views.UserAccountActivationAPIView.as_view()),
    re_path(r"^api/v1/create-user/", views.UserCreationAPIView.as_view()),
    re_path(r"^api/v1/users/", views.UserListAPIView.as_view()),
]