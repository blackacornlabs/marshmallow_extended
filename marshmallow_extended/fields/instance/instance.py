from .abstract_instance import AbstractInstance


class Instance:

    strategy: AbstractInstance

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
        :param field: Found instances by this field.
        :param allow_deleted Allowed return deleted instances flag
        :param check_deleted_by Filed, by check deleted instances. (If allow_deleted=False)
        :param return_field: Return value field in this instance
        :param many: Many instances. True/False
        :param assert_every: True/False. Raise exception if not found one instances. (Only many=True)
        :param kwargs:
        """
        if self.is_sqlalchemy_model(model):
            from .sqlalchemy_mixins_instance import SQLAlchemyMixinsInstance
            self.strategy = SQLAlchemyMixinsInstance(
                model=model,
                many=many,
                field=field,
                allow_deleted=allow_deleted,
                check_deleted_by=check_deleted_by,
                assert_every=assert_every,
                return_field=return_field,
                **kwargs)
        else:
            from .mongoengine_instance import MongonengineInstance
            self.strategy = MongonengineInstance(
                model=model,
                many=many,
                field=field,
                allow_deleted=allow_deleted,
                check_deleted_by=check_deleted_by,
                assert_every=assert_every,
                return_field=return_field,
                **kwargs)

    def __getattribute__(self, item):
        if item in ['strategy', 'is_sqlalchemy_model', 'set_strategy', '_serialize', '_deserialize']:
            return super(Instance, self).__getattribute__(item)
        return self.strategy.__getattribute__(item)

    @staticmethod
    def is_sqlalchemy_model(model):
        try:
            from sqlalchemy.orm.util import class_mapper
            class_mapper(model)
            return True
        except:
            return False

    def set_strategy(self, strategy: AbstractInstance):
        self.strategy = strategy()

    def _serialize(self, value, attr, obj, **kwargs):
        """For Schema().dump() func"""
        self.strategy._serialize(self, value, attr, obj, **kwargs)

    def _deserialize(self, value, attr, obj, **kwargs):
        """For Schema().load() func"""
        self.strategy._deserialize(self, value, attr, obj, **kwargs)
