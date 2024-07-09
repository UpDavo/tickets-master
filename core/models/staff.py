from django.db import models
from .timeStampedModel import TimeStampedModel


class Staff(TimeStampedModel):
    name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField()
    id_number = models.CharField(max_length=45, unique=True)
    available = models.BooleanField(default=True)
