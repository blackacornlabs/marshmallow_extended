from unittest import main, TestCase

from marshmallow_extended import Schema
from marshmallow_extended.fields import Active


class ActiveFieldTests(TestCase):

    def test_simple_behaviour(self):
        class SimpleSchema(Schema):
            active = Active()

        result = SimpleSchema().dump({'state': 'active'})
        self.assertEqual(result, {'active': True})
        result = SimpleSchema().dump({'state': 'inactive'})
        self.assertEqual(result, {'active': False})
        result = SimpleSchema().dump({})
        self.assertEqual(result, {})

        result = SimpleSchema().load({'active': True})
        self.assertEqual(result, {'state': 'active'})
        result = SimpleSchema().load({'active': False})
        self.assertEqual(result, {'state': 'inactive'})
        result = SimpleSchema().load({})
        self.assertEqual(result, {})

    def test_advanced_behaviour(self):
        class AdvancedSchema(Schema):
            active = Active(positives=['active', 'running'], negatives=['inactive', 'stopped'])

        result = AdvancedSchema().dump({'state': 'active'})
        self.assertEqual(result, {'active': True})
        result = AdvancedSchema().dump({'state': 'running'})
        self.assertEqual(result, {'active': True})
        result = AdvancedSchema().dump({'state': 'inactive'})
        self.assertEqual(result, {'active': False})
        result = AdvancedSchema().dump({'state': 'stopped'})
        self.assertEqual(result, {'active': False})
        result = AdvancedSchema().dump({})
        self.assertEqual(result, {})

    def test_simple_filter_behaviour(self):
        class SimpleFilterSchema(Schema):
            active = Active(as_filter=True)

        result = SimpleFilterSchema().load({'active': 'true'})
        self.assertEqual(result, {'state': 'active'})
        result = SimpleFilterSchema().load({'active': 'false'})
        self.assertEqual(result, {'state': 'inactive'})
        result = SimpleFilterSchema().load({})
        self.assertEqual(result, {'state__ne': 'deleted'})

    def test_advanced_filter_behaviour(self):
        class AdvancedFilterSchema(Schema):
            active = Active(as_filter=True,
                            positives=['active', 'running'],
                            negatives=['inactive', 'stopped'])

        result = AdvancedFilterSchema().load({'active': 'true'})
        self.assertEqual(result, {'state__in': ['active', 'running']})
        result = AdvancedFilterSchema().load({'active': 'false'})
        self.assertEqual(result, {'state__in': ['inactive', 'stopped']})
        result = AdvancedFilterSchema().load({})
        self.assertEqual(result, {'state__ne': 'deleted'})

    def test_empty_extra_filter_fields_behaviour(self):
        class ExtendedFilterSchema(Schema):
            active = Active(as_filter=True, positive_filter={}, negative_filter={}, missing_filter={})

        result = ExtendedFilterSchema().load({'active': 'true'})
        self.assertEqual(result, {})
        result = ExtendedFilterSchema().load({'active': 'false'})
        self.assertEqual(result, {})
        result = ExtendedFilterSchema().load({})
        self.assertEqual(result, {})

    def test_extra_filter_fields_behaviour(self):
        class ExtendedFilterSchema(Schema):
            active = Active(as_filter=True,
                            positive_filter={'state__exists': True},
                            negative_filter={'state__exists': False},
                            missing_filter={'state__in': ['removed', 'deleted']})

        result = ExtendedFilterSchema().load({'active': 'true'})
        self.assertEqual(result, {'state__exists': True})
        result = ExtendedFilterSchema().load({'active': 'false'})
        self.assertEqual(result, {'state__exists': False})
        result = ExtendedFilterSchema().load({})
        self.assertEqual(result, {'state__in': ['removed', 'deleted']})


if __name__ == '__main__':
    main()
