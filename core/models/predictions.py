from django.db import models
from .timeStampedModel import TimeStampedModel


class Predictions(TimeStampedModel):
    artist_name = models.CharField(max_length=255)
    artist_gender = models.CharField(max_length=255)
    artist_age = models.IntegerField()  # Si la edad es un número entero
    artist_country = models.CharField(max_length=255)
    artist_followers = models.IntegerField()  # Si los seguidores son numéricos
    artist_genres = models.CharField(max_length=255)
    event_city = models.CharField(max_length=255)
    event_country = models.CharField(max_length=255)
    event_venue = models.CharField(max_length=255)

    # Generated
    artist_popularity = models.IntegerField()
    event_venue = models.IntegerField()
    event_tickets = models.IntegerField()

    def __str__(self):
        return self.artist_name  # Cambiado de `self.name` a `self.artist_name`
