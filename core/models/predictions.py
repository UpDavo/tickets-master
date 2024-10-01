from django.db import models
from .timeStampedModel import TimeStampedModel


class Predictions(TimeStampedModel):
    artist_name = models.CharField(max_length=255, default='Unknown Artist')
    artist_gender = models.CharField(max_length=255, default='Unknown')
    artist_age = models.IntegerField(default=0)
    artist_country = models.CharField(
        max_length=255, default='Unknown Country')
    artist_followers = models.IntegerField(default=0)
    artist_genres = models.CharField(max_length=255, default='Unknown Genre')
    event_city = models.CharField(max_length=255, default='Unknown City')
    event_country = models.CharField(max_length=255, default='Unknown Country')
    event_venue = models.CharField(max_length=255, default='Unknown Venue')

    # Campos Generados
    artist_popularity = models.IntegerField(default=0)
    event_tickets = models.IntegerField(default=0)
    event_revenue = models.IntegerField(default=0)
    event_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.artist_name
