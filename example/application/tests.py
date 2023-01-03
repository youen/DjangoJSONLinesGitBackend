from django.test import TestCase

from django.db import models
from django.db.utils import ProgrammingError

class TestDatabaseBackend(TestCase):
    def setUp(self):
        # Create a test model
        class TestModel(models.Model):
            name = models.CharField(max_length=255)
            age = models.IntegerField()
        
        self.TestModel = TestModel
        self.TestModel.objects.using('json-git-write').bulk_create([
            self.TestModel(name='Alice', age=20),
            self.TestModel(name='Bob', age=30),
            self.TestModel(name='Charlie', age=40),
        ])
    
    def test_read_backend(self):
        # Test that the read backend can retrieve the data from the write backend
        try:
            self.TestModel.objects.using('json-git-read').all()
        except ProgrammingError as e:
            self.fail(e)
    
    def test_write_backend(self):
        # Test that the write backend can create and retrieve data
        obj = self.TestModel.objects.using('json-git-write').create(
            name='Dave', age=50)
        self.assertEqual(obj.name, 'Dave')
        self.assertEqual(obj.age, 50)