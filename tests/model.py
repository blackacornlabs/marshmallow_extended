from mongoengine import Document, StringField


class TestObject(Document):

    name = StringField()
    state = StringField(choices=['active', 'deleted'], default='active')
    status = StringField(choices=['active', 'deleted'], default='active')

    meta = {
        "collection": "test_objects"
    }
