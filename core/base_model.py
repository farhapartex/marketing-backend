from django.db import models


class BaseAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_instance(cls, payload: dict):
        return cls.objects.filter(**payload).first()

    class Meta:
        abstract = True
