from marshmallow import fields, ValidationError, Schema


class DatetimeFilter(fields.DateTime):
    """Field to filtering by __gte and __lte for mongoDB or __ge and __le for SQLAlchemy"""

    ValidateSuffixError = ValidationError(message={'errors': 'suffix must be _from or _until only'})

    def __init__(self, db_type, *args, **kwargs):
        if db_type not in ['sql', 'no_sql']:
            raise ValidationError(message={'errors': 'db_type must be sql or no_sql only'})

        if db_type == 'sql':
            self.from_value = '__ge'
            self.until_value = '__le'
        else:
            self.from_value = '__gte'
            self.until_value = '__lte'

        super().__init__(*args, **kwargs)

    def deserialize(self, value, attr, obj, **kwargs):
        if not self.attribute:

            if self.name.endswith('_from'):
                self.attribute = self.name[:-5] + self.from_value
            elif self.name.endswith('_until'):
                self.attribute = self.name[:-6] + self.until_value
            else:
                raise self.ValidateSuffixError

        if not self.attribute.endswith(self.until_value) and not self.attribute.endswith(self.from_value):
            raise self.ValidateSuffixError

        return super().deserialize(value, **kwargs)


if __name__ == '__main__':

    class Example(Schema):
        field_until = DatetimeFilter(db_type='sql')

    result = Example().load({'field_until': "2020-12-10T02:33:33Z"})
    print(result)