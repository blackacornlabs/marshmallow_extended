from unittest import TestCase

from marshmallow_extended import Schema
from marshmallow_extended.fields import Email


class EmailFieldTests(TestCase):
    def test_simple_behaviour(self):
        class SimpleSchema(Schema):
            email = Email()

        result = SimpleSchema().load({'email': 'Test@email.com'})
        self.assertEqual(result, {'email': 'test@email.com'})
