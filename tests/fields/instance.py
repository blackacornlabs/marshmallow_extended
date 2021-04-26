from unittest import main

from tests.test_case import CommonTestCase
from tests.model import TestObject
from marshmallow_extended import Schema, fields, ValidationError


class TestToInstance(CommonTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super(TestToInstance, cls).setUpClass()
        cls.test_object = TestObject.objects.create(name='TestName1')
        cls.test_object2 = TestObject.objects.create(name='TestName2')
        cls.deleted_obj = TestObject.objects.create(name='TestName3', state='deleted')
        cls.deleted_obj2 = TestObject.objects.create(name='TestName4', status='deleted')

    def test_convert_to_one_instance(self):
        class LoadSchema(Schema):
            test_object = fields.Instance(TestObject)

        result = LoadSchema().load({"test_object": str(self.test_object.id)})
        self.assertIn("test_object", result)
        self.assertEqual(result["test_object"].id, self.test_object.id)

    def test_convert_to_one_instance_allow_deleted(self):
        class LoadSchemaAllowDeleted(Schema):
            test_object = fields.Instance(TestObject, allow_deleted=True)

        result = LoadSchemaAllowDeleted().load({"test_object": str(self.deleted_obj.id)})
        self.assertIn("test_object", result)
        self.assertEqual(result["test_object"].id, self.deleted_obj.id)

    def test_convert_to_one_instance_check_deleted_by(self):
        class LoadSchemaCheckDeletedBy(Schema):
            test_object = fields.Instance(TestObject, allow_deleted=True, check_deleted_by='status')

        result = LoadSchemaCheckDeletedBy().load({"test_object": str(self.deleted_obj2.id)})
        self.assertIn("test_object", result)
        self.assertEqual(result["test_object"].id, self.deleted_obj2.id)

    def test_convert_to_one_instance_not_allow_deleted(self):
        class LoadSchemaNotAllowDeleted(Schema):
            test_object = fields.Instance(TestObject)
        try:
            LoadSchemaNotAllowDeleted().load({"test_object": str(self.deleted_obj.id)})
        except ValidationError as exc:
            self.assertIn("test_object", exc.messages)
            self.assertIn(f'Could not find document.', exc.messages["test_object"])

    def test_convert_to_one_instance_return_field(self):
        class LoadSchemaReturnField(Schema):
            test_object = fields.Instance(TestObject, return_field='id')

        result = LoadSchemaReturnField().load({"test_object": str(self.test_object.id)})
        self.assertIn("test_object", result)
        self.assertEqual(result["test_object"], self.test_object.id)

    def test_convert_to_one_instance_return_field_not_found_field(self):
        class LoadSchemaReturnFieldNotFound(Schema):
            test_object = fields.Instance(TestObject, return_field='not_found')
        try:
            LoadSchemaReturnFieldNotFound().load({"test_object": str(self.test_object.id)})
        except ValidationError as exc:
            self.assertIn("test_object", exc.messages)
            self.assertIn("Not found in model this field: 'not_found'.", exc.messages["test_object"])

    def test_convert_to_one_instance_search_instance_by_field(self):
        class LoadSchemaField(Schema):
            test_object = fields.Instance(TestObject, field='name')

        result = LoadSchemaField().load({"test_object": str(self.test_object.name)})
        self.assertIn("test_object", result)
        self.assertEqual(result["test_object"].id, self.test_object.id)

    def test_convert_to_one_instance_search_instance_by_field_not_found_field(self):
        class LoadSchemaField(Schema):
            test_object = fields.Instance(TestObject, field='names')
        try:
            LoadSchemaField().load({"test_object": str(self.test_object.name)})
        except ValidationError as exc:
            self.assertIn("test_object", exc.messages)
            self.assertIn("Not found in model this field: 'names'.", exc.messages["test_object"])

    def test_convert_to_one_instance_invalid_id(self):
        class LoadSchemaField(Schema):
            test_object = fields.Instance(TestObject)
        invalid_id = '1a'
        try:
            LoadSchemaField().load({"test_object": invalid_id})
        except ValidationError as exc:
            self.assertIn("test_object", exc.messages)
            self.assertIn(f"Invalid identifier: '{invalid_id}'.", exc.messages["test_object"])

    def test_convert_many_instances(self):
        class LoadSchema(Schema):
            test_objects = fields.Instance(TestObject, many=True)

        result = LoadSchema().load({"test_objects": [str(self.test_object.id), str(self.test_object2.id)]})
        self.assertIn("test_objects", result)
        list_ids = [obj.id for obj in result['test_objects']]
        self.assertIn(self.test_object.id, list_ids)
        self.assertIn(self.test_object2.id, list_ids)

    def test_convert_many_instances_string_in_value(self):
        class LoadSchemaStringInValue(Schema):
            test_objects = fields.Instance(TestObject, many=True)

        result = LoadSchemaStringInValue().load({"test_objects": f"{str(self.test_object.id)}, "
                                                                 f"{str(self.test_object2.id)}"})
        self.assertIn("test_objects", result)
        list_ids = [obj.id for obj in result['test_objects']]
        self.assertIn(self.test_object.id, list_ids)
        self.assertIn(self.test_object2.id, list_ids)

    def test_convert_many_instances_invalid_ids(self):
        invalid_ids = {'1', '2'}

        class LoadSchemaInvalidIds(Schema):
            test_objects = fields.Instance(TestObject, many=True)
        try:
            LoadSchemaInvalidIds().load({"test_objects": invalid_ids})
        except ValidationError as exc:
            self.assertIn("test_objects", exc.messages)
            self.assertIn(f"Invalid identifier: '{invalid_ids}'.", exc.messages["test_objects"])

    def test_convert_many_instances_not_found(self):
        not_found_ids = ['555555555555555555555555']

        class LoadSchemaNotFoundMany(Schema):
            test_objects = fields.Instance(TestObject, many=True)
        try:
            LoadSchemaNotFoundMany().load({"test_objects": not_found_ids})
        except ValidationError as exc:
            self.assertIn("test_objects", exc.messages)
            self.assertIn(f"Could not find document.", exc.messages["test_objects"])

    def test_convert_many_instances_not_all_where_found(self):
        not_found_ids = [str(self.test_object.id), "555555555555555555555555"]

        class LoadSchemaNotAllWhereFound(Schema):
            test_objects = fields.Instance(TestObject, many=True, assert_every=True)

        try:
            LoadSchemaNotAllWhereFound().load({"test_objects": not_found_ids})
        except ValidationError as exc:
            self.assertIn("test_objects", exc.messages)
            self.assertIn(f"Not all documents were found.", exc.messages["test_objects"])

    def test_convert_many_instances_assert_every_empty_list(self):
        not_found_ids = []

        class LoadSchemaAssertEveryEmptyList(Schema):
            test_objects = fields.Instance(TestObject, many=True, assert_every=True)

        result = LoadSchemaAssertEveryEmptyList().load({"test_objects": not_found_ids})
        self.assertIn('test_objects', result)
        self.assertEqual(result['test_objects'], [])


if __name__ == '__main__':
    main()
