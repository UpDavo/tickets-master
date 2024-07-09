from django.db import models
from .timeStampedModel import TimeStampedModel


class Permission(TimeStampedModel):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.name
