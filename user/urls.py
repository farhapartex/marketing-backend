from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from user import views

router = DefaultRouter()

urlpatterns = [
    re_path(r"^api/v1/token/", views.UserAUthTokenView.as_view()),
    re_path(r"^api/v1/registration/", views.UserRegistrationAPIView.as_view()),
    re_path(r"^api/v1/account-activation/", views.UserAccountActivationAPIView.as_view()),
]