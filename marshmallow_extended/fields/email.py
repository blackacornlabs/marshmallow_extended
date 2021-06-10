import typing

from marshmallow import fields
from marshmallow.fields import missing_


class Email(fields.Email):

    def deserialize(self, value: typing.Any, *args, **kwargs):
        """Deserialize ``value``.

        :param value: The value to deserialize.
        """
        if value is not missing_ and isinstance(value, str):
            value = value.lower()
        return super().deserialize(value, *args, **kwargs)
