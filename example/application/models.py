import uuid
import datetime

import django.utils.timezone

from django.db import models


def default_json():
    return dict(a=4)


class MyModel(models.Model):
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
