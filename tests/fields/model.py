from mongoengine import Document, StringField


class TestObject(Document):

    name = StringField()

    meta = {
        "collection": "test_objects"
    }
