# Generated by Django 4.0.5 on 2022-06-03 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_useractivation'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivation',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]
