import typing
from marshmallow.fields import *
from mongoengine import ValidationError as MongoValidationError, Document, QuerySet
from mongoengine.base import TopLevelDocumentMetaclass


__all__ = ["Field", "Raw", "Nested", "Mapping", "Dict", "List", "Tuple", "String", "UUID", "Number", "Integer",
           "Decimal", "Boolean", "Float", "DateTime", "NaiveDateTime", "AwareDateTime", "Time", "Date", "TimeDelta",
           "Url", "URL", "Email", "IP", "IPv4", "IPv6", "Method", "Function", "Str", "Bool", "Int", "Constant",
           "Pluck", "Instance"]


class Instance(Field):
    sql_db = False
    value = None

    #: Default error messages.
    default_error_messages = {
        "not_found_doc": "Could not find document.",
        "not_found_field": "Field not found in model",
        "invalid_id": "Invalid identifier",
        "not_found_all_doc": "Not all documents were found",
    }

    def __init__(self,
                 model: TopLevelDocumentMetaclass,
                 many: bool = False,
                 field: str = 'pk',
                 allow_deleted: bool = True,
                 check_deleted_by: str = 'state',
                 assert_every: bool = True,
                 return_field: str = None, **kwargs):
        """
        Initialisation class

        :param model: Model
        :param field: Found instances by this field.
        :param allow_deleted Allowed return deleted instances flag
        :param check_deleted_by Filed, by check deleted instances. (If allow_deleted=False)
        :param return_field: Return value field in this instance
        :param many: Many instances. True/False
        :param assert_every: True/False. Raise exception if not found one instances. (Only many=True)
        :param kwargs:
        """
        super().__init__(**kwargs)

        self.model = model
        self.many = many
        self.field = field
        self.allow_deleted = allow_deleted
        self.check_deleted_by = check_deleted_by
        self.assert_every = assert_every
        self.return_field = return_field
        self.sql_db = self.__check_sql_db()

    @classmethod
    def __check_sql_db(cls) -> bool:
        # TODO Добавить поверку модели
        cls._query_func = cls._query_nosql
        return False

    def _serialize(self, value, attr, obj, **kwargs) -> typing.Optional[str]:
        """For Schema().dump() func"""
        return None

    def _deserialize(self, value, attr, data, **kwargs) -> typing.Union[Document, typing.List[Document]]:
        """
        For Schema().load() func

        :param value: Value
        :param attr: Attribute name
        :param data:
        :param kwargs: Other params
        :return: One instance or list instances

        Example:
            data = {"attribute_name": 123456}
            ...
            class ClassName(Schema):
                attribute_name = fields.ToInstance(User)
            ...
            result = ClassName().load(data)     # {"attribute_name": UserInstance}
        """
        self.value = value
        try:
            result = self._convert_to_many() if self.many else self._query_func().first()
        except MongoValidationError:
            self.make_error("invalid_id")
        else:
            if not result:
                self.make_error("not_found_doc")
            return self._get_value(result) if self.return_field else result

    def _convert_to_many(self) -> QuerySet:
        """
        Convert to many instances

        :return: QuerySet
        """
        values = []
        if self.value.startswith('[') and self.value.endswith(']'):
            values = self.value[2:-2].replace("'", "").split(',')
        elif isinstance(self.value, str):
            values = self.value.split(',')
        else:
            self.make_error("invalid_id")
        values = list(set(values))
        query = self._query_func()
        if self.assert_every and len(query.count()) != len(values):
            self.make_error("not_found_all_doc")
        return query.all()

    def _query_sql(self, *args, **kwargs):
        pass

    def _query_nosql(self) -> QuerySet:
        """
        Query with mongoengine

        :return: QuerySet
        """
        # Generate filter data
        query_field = f"{self.field}__in" if self.many else self.field
        filter_data = {query_field: self.value}
        if not self.allow_deleted:
            filter_data.update({f'{self.check_deleted_by}__ne': 'deleted'})
        # Query
        return self.model.objects.filter(**{query_field: self.value})

    def _get_value(self, instance: typing.Union[Document, QuerySet]):
        """
        Get value from founded instances

        :param instance: Convert result
        :return: value field in this instance
        """

        instances = instance.all() if self.many else [instance]

        fields = self.model.columns if self.sql_db else getattr(self.model, "_fields").keys()
        if self.return_field in fields:
            result = [getattr(doc, self.return_field) for doc in instances]
            return result if self.many else result[0]
        self.make_error("not_found_field")
