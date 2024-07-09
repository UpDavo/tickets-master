from django.db import models
from .timeStampedModel import TimeStampedModel
from .user import User

class Invoice(TimeStampedModel):
    order_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_sku = models.IntegerField()
    redeemed_code = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    brand_name = models.CharField(max_length=100)

    def __str__(self):
        return self.order_id

    
