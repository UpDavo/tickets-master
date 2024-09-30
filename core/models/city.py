from django.db import models
from .timeStampedModel import TimeStampedModel

class City(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
