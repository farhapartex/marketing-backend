from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from social import views

router = DefaultRouter()

urlpatterns = [
    re_path(r"^api/v1/generate-twitter-auth-url/", views.GenerateTwitterAuthUrl.as_view()),
    re_path(r"^api/v1/submit-twitter-auth-handler/", views.SubmitTwitterAuthHandlerAPIView.as_view()),
    re_path(r"^api/v1/social-apps/", views.SocialAppListAPiView.as_view()),
]