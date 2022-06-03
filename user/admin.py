from django.contrib import admin
from user import models
# Register your models here.


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "username", "email", "is_staff", "role", "is_superuser", "is_active")


@admin.register(models.UserActivation)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "key", "valid_till",)
