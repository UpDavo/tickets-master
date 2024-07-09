from django.db import models
from .timeStampedModel import TimeStampedModel
from .permission import Permission


class Role(TimeStampedModel):
    name = models.CharField(max_length=45)
    permissions = models.ManyToManyField(Permission)
    all_countries = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name
