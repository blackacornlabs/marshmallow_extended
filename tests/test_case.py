from os import getenv
from unittest import TestCase
from dotenv import load_dotenv
from mongoengine import connect


load_dotenv()


class CommonTestCase(TestCase):
    db = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.db = connect(host=getenv("MONGODB_HOST"))
        if 'test' in cls.db.list_database_names():
            cls.db.drop_database('test')

    @classmethod
    def tearDownClass(cls) -> None:
        pass
