from unittest import main

from tests.test_case import CommonTestCase
from .model import TestObject
from marshmallow_advanced import Schema, fields


class LoadSchema(Schema):
    test_object = fields.ToInstance(TestObject)


class TestToInstance(CommonTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super(TestToInstance, cls).setUpClass()
        cls.test_object = TestObject.objects.create(name='TestName')

    def test_convert_to_one_instance(self):
        result = LoadSchema().load({"test_object": str(self.test_object.id)})
        self.assertIn("test_object", result)
        self.assertEqual(result["test_object"].id, self.test_object.id)


if __name__ == '__main__':
    main()
