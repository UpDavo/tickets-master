from django.db import models
from .timeStampedModel import TimeStampedModel
from .user import User


class Points(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, unique=True)
    plus_points = models.IntegerField(default=0)
    minus_points = models.IntegerField(default=0)
    old_points = models.IntegerField(default=0)
    new_points = models.IntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.order_id
