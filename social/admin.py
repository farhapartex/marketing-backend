from django.contrib import admin
from social import models
# Register your models here.


@admin.register(models.SocialAuth)
class SocialAuthAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type")
