import typing
from collections import Iterable

from marshmallow import fields
from marshmallow.validate import OneOf


class Enum(fields.Field):

    def __init__(self, *args, allowed: Iterable = None, **kwargs):
        if allowed is None and args:
            allowed = args[0] if len(args) == 1 else args
        self.allowed = allowed
        super().__init__(**kwargs)

    def deserialize(self, value: typing.Any, *args, **kwargs):
        """Deserialize ``value``.

        :param value: The value to deserialize.
        """
        OneOf(self.allowed)(value)
        return super().deserialize(value, *args, **kwargs)
