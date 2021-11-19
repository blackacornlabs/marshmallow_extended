import typing

from marshmallow import fields


class IContains(fields.Field):

    def deserialize(self, value: typing.Any, attr: str = None, *args, **kwargs):
        """Deserialize ``value``.

        :param value: The value to deserialize.
        """
        if not value:
            return super().deserialize(value, attr, *args, **kwargs)

        value = (f'%{value}%')
        if not self.attribute:
            self.attribute = f'{attr}__ilike'
        return super().deserialize(value, attr, *args, **kwargs)
