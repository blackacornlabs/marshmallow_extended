from copy import copy
from functools import partial

from marshmallow import ValidationError


def not_blank(locale='en'):
    def _not_blank(data, locale):
        LOCALES = {
            'en': {'No data provided': 'No data provided.'},
            'ru': {'No data provided': 'Поле не заполнено'},
        }
        _ = copy(LOCALES)
        _.update(LOCALES.get(locale, {}))

        if not data:
            raise ValidationError(_["No data provided"])
        elif isinstance(data, str):
            if not data.strip():
                raise ValidationError(_["No data provided"])
    return partial(_not_blank, locale=locale)
