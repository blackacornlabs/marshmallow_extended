import typing

from .abstract_instance import AbstractInstance


class SQLAlchemyMixinsInstance(AbstractInstance):
    sql_db = False
    value = None

    #: Default error messages.
    default_error_messages = {
        "row_not_found": "Could not find document.",
    }

    def __init__(self,
                 model,
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
        self.field = field
        self.allow_deleted = allow_deleted
        self.check_deleted_by = check_deleted_by

    def _serialize(self, value, attr, obj, **kwargs) -> typing.Optional[str]:
        """For Schema().dump() func"""
        return None

    def _deserialize(self, value, attr, data, **kwargs):
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
            result = self._query()
        except Exception as exc:
            raise self.make_error("row_not_found", field_name=self.field)
        else:
            if not result:
                raise self.make_error("row_not_found", field_name=self.field)
        return result

    def _query(self):
        """
        Query with mongoengine

        :return: QuerySet
        """
        # Generate filter data
        filter_data = {self.field: self.value}
        if not self.allow_deleted:
            filter_data.update({f'{self.check_deleted_by}__ne': 'deleted'})
        # Query
        return self.model.where(**filter_data).first()
