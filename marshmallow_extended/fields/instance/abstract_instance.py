from marshmallow.fields import Field
from abc import ABC, abstractmethod


class AbstractInstance(Field, ABC):

    @abstractmethod
    def _serialize(self, value, attr, obj, **kwargs):
        """For Schema().dump() func"""
        pass

    @abstractmethod
    def _deserialize(self, value, attr, data, **kwargs):
        """
        For Schema().load() func
        """
        pass
