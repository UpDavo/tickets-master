from django.db import models
from .timeStampedModel import TimeStampedModel
from .product import Product


class Stock(TimeStampedModel):
    code = models.CharField(max_length=45)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
