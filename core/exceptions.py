from rest_framework import exceptions, status
from django.utils.encoding import force_str


class SerializerValidationError(exceptions.APIException):

    def __init__(self, status_code, field=None, detail=None):
        self.status_code = status_code
        self.detail = {'detail': force_str("A uncertain error found")} if detail is None else {field: force_str(detail)}