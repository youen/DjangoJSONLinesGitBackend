from django.test import TestCase

from django.db.utils import ProgrammingError

from .models import MyModel


class TestDatabaseBackend(TestCase):
    databases = ['default', 'json-git']

    def test_read_backend(self):
        # Test that the read backend can retrieve the data from the write backend
        try:
            MyModel.objects.using('json-git-read').all()
        except ProgrammingError as e:
            self.fail(e)

    def test_write_backend(self):
        # Test that the write backend can create and retrieve data
        obj = MyModel.objects.using('json-git').create(myCharField="Dave")
        self.assertEqual(obj.myCharField, 'Dave')
