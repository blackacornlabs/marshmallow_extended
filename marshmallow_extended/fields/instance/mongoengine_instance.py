import typing

from .abstract_instance import AbstractInstance
from mongoengine import ValidationError as MongoValidationError, Document, QuerySet, InvalidQueryError, ObjectIdField
from mongoengine.base import TopLevelDocumentMetaclass


class MongonengineInstance(AbstractInstance):
    sql_db = False
    value = None

    #: Default error messages.
    default_error_messages = {
        "doc_not_found": "Could not find document.",
        "invalid_id": "Invalid identifier: '{value}'.",
        "field_not_found": "Not found in model this field: '{field_name}'.",
        "some_docs_not_found": "Not all documents were found.",
    }

    def __init__(self,
                 model: TopLevelDocumentMetaclass,
                 many: bool = False,
                 field: str = 'pk',
                 allow_deleted: bool = False,
                 check_deleted_by: str = 'state',
                 assert_every: bool = False,
                 return_field: str = None, **kwargs):
        """
        Initialization class

        :param model: Model
        :param field: Search field (pk for mongoengine, id for sqlalchemy_mixins).
        :param allow_deleted Allow returning deleted instances.
        :type allow_deleted: bool
        :param check_deleted_by Filed, by check deleted instances (for allow_deleted=False only).
        :param return_field: Return value field in this instance
        :param many: Many instances.
        :type many: bool
        :param assert_every: Raise exception if any instance is not found (for many=True only).
        :type assert_every: bool
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
        self.object_id = ObjectIdField == self.model.id.__class__

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
        if self.many and isinstance(value, list) and not value:
            return value
        self.value = value
        try:
            result = self._convert_to_many() if self.many else self._query_func().first()
        except MongoValidationError as exc:
            raise self.make_error("invalid_id", value=value)
        except InvalidQueryError:
            raise self.make_error("field_not_found", field_name=self.field)
        else:
            if not result:
                raise self.make_error("doc_not_found")
            return self._get_value(result) if self.return_field else result

    def _convert_to_many(self) -> typing.List[Document]:
        """
        Convert to many instances

        :return: QuerySet
        """
        values = self.value
        if isinstance(values, str):
            values = [item.strip() for item in values.split(',')]
        if isinstance(values, list):
            self.value = list(set(values))
            query = self._query_func()
            if self.assert_every and query.count() != len(self.value):
                raise self.make_error("some_docs_not_found")
            return list(query)
        else:
            raise MongoValidationError

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
        return self.model.objects.filter(**filter_data)

    def _get_value(self, instance: typing.Union[Document, typing.List[Document]]):
        """
        Get value from founded instances

        :param instance: Convert result
        :return: value field in this instance
        """

        instances = instance if self.many else [instance]

        fields = self.model.columns if self.sql_db else getattr(self.model, "_fields").keys()
        if self.return_field in fields:
            result = [getattr(doc, self.return_field) for doc in instances]
            return result if self.many else result[0]
        raise self.make_error("field_not_found", field_name=self.return_field)
