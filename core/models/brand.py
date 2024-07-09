from django.db import models
from .timeStampedModel import TimeStampedModel


class Brand(TimeStampedModel):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name
