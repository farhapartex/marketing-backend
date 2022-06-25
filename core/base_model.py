from django.db import models


class BaseAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def _filter_data(cls, payload: dict):
        return cls.objects.filter(**payload)

    @classmethod
    def get_instance(cls, payload: dict):
        return cls._filter_data(payload).first()

    @classmethod
    def get_filter_data(cls, payload: dict):
        return cls._filter_data(payload)

    class Meta:
        abstract = True
