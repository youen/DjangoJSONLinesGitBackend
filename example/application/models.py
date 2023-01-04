import uuid
import datetime

import django.utils.timezone

from django.db import models


def default_json():
    return dict(a=4)


class MyModel(models.Model):
    """
    Model representing a sample model with various field types.

    Attributes:
    id (UUIDField): Primary key for the model, generated automatically.
    myCharField (CharField): A character field with a maximum length of 25.
    myBooleanField (BooleanField): A boolean field with a default value of True.
    myJsonField (JSONField): A JSON field with a default value of a dictionary with key "a" and value 4.
    myDateField (DateField): A date field with a default value of the current date.
    myDateTimeField (DateTimeField): A datetime field with a default value of the current datetime.
    myDecimalField (DecimalField): A decimal field with a default value of 0.2, a maximum of 4 digits, and 2 decimal places.
    myManyToManyField (ManyToManyField): A many-to-many field linking to the 'MyOtherModel' model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    myCharField = models.CharField(max_length=25, null=True, blank=True)
    myBooleanField = models.BooleanField(default=True)
    myJsonField = models.JSONField(default=default_json)
    myDateField = models.DateField(default=django.utils.timezone.now)
    myDateTimeField = models.DateTimeField(default=django.utils.timezone.now)
    myDecimalField = models.DecimalField(
        default=0.2, max_digits=4, decimal_places=2)
    myManyToManyField = models.ManyToManyField('MyOtherModel')


class MyOtherModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
