from django.core.management.base import BaseCommand, CommandError
from user.constants import RoleType
from user.models import User

class Command(BaseCommand):
    help = 'Pull images from server'

    def handle(self, *args, **options):
        admin = {
            'username': 'admin@admin.com',
            'email': 'admin@admin.com',
            'first_name': 'Md Nazmul',
            'last_name': 'Hasan',
            'role': RoleType.admin,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True
        }

        user = User.objects.create(**admin)
        user.set_password('admin')
        user.save()

