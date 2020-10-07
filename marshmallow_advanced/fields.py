import typing
from marshmallow.fields import *

__all__ = [
    "Field",
    "Raw",
    "Nested",
    "Mapping",
    "Dict",
    "List",
    "Tuple",
    "String",
    "UUID",
    "Number",
    "Integer",
    "Decimal",
    "Boolean",
    "Float",
    "DateTime",
    "NaiveDateTime",
    "AwareDateTime",
    "Time",
    "Date",
    "TimeDelta",
    "Url",
    "URL",
    "Email",
    "IP",
    "IPv4",
    "IPv6",
    "Method",
    "Function",
    "Str",
    "Bool",
    "Int",
    "Constant",
    "Pluck",
    "ToInstance"
]


class ToInstance(Field):

    #: Default error messages.
    default_error_messages = {
        "not_found": "Could not find document.",
        "invalid_id": "Invalid identifier",
    }

    def _serialize(self, value, attr, obj, **kwargs) -> typing.Optional[str]:
        """For Schema().dump()"""
        return None

    def _deserialize(self, value, attr, data, many=False, field='pk', return_field=None, **kwargs) -> typing.Any:
        """For Schema().load() func"""
        return None
