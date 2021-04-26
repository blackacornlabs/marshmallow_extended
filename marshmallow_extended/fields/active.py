import typing
from collections import Iterable

from marshmallow import fields
from marshmallow.fields import missing_
from marshmallow.validate import OneOf


class Active(fields.Field):

    def __init__(self, *args, attribute: str = 'state', missing: typing.Any = missing_,
                 positives: Iterable = None,
                 negatives: Iterable = None,
                 as_filter: bool = False,
                 positive_filter=None,
                 negative_filter=None,
                 missing_filter=None,
                 **kwargs):
        self.filter_schema = as_filter
        positives = positives if positives else ['active']
        negatives = negatives if negatives else ['inactive']

        state_map = {}
        for positive in positives:
            state_map[positive] = True
        for negative in negatives:
            state_map[negative] = False
        self.string_state_map = state_map

        # for filter_schema
        missing = missing if missing and missing is not missing_ else ('missing' if self.filter_schema else missing_)
        if self.filter_schema:
            if positive_filter is not None:
                positive_filter = positive_filter
            elif len(positives) == 1:
                positive_filter = {attribute: positives[0]}
            else:
                positive_filter = {f'{attribute}__in': positives}

            if negative_filter is not None:
                negative_filter = negative_filter
            elif len(negatives) == 1:
                negative_filter = {attribute: negatives[0]}
            else:
                negative_filter = {f'{attribute}__in': negatives}

            self.filter_map = {
                'missing': {f'{attribute}__ne': 'deleted'} if missing_filter is None else missing_filter,
                'true': positive_filter,
                'false': negative_filter
            }
        else:
            self.bool_state_map = {v: k for k, v in self.string_state_map.items()}

        super().__init__(*args, attribute=attribute, missing=missing, **kwargs)

    def deserialize(self, value: typing.Any, *args, **kwargs):
        """Deserialize ``value``.

        :param value: The value to deserialize.
        """
        if value is missing_ and self.filter_schema and self.missing == 'missing':
            value = 'missing'
        return super().deserialize(value, *args, **kwargs)

    def _deserialize(self, value: typing.Any, *args, **kwargs):
        if self.filter_schema:
            OneOf(self.filter_map.keys())(value)
            if not (result_filter := self.filter_map[value]):
                return missing_
            [[self.attribute, result]] = result_filter.items()
            return result

        OneOf((True, False))(value)
        return self.bool_state_map.get(value, None)

    def _serialize(self, value: typing.Any, attr: str, obj: typing.Any, **kwargs):
        return self.string_state_map.get(value, None)
