from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from django.db import models
from .timeStampedModel import TimeStampedModel
from .role import Role


class User(AbstractUser, TimeStampedModel):
    names = models.CharField(max_length=45)
    ci = models.IntegerField(default=0)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, null=True, blank=True)
    total_points = models.IntegerField(default=0)

    def has_permission(self, url_name):
        return self.role.permissions.filter(url=reverse_lazy(url_name)).exists()

    def show_permissions(self):
        permissions = self.role.permissions.all()
        array = []
        for permission in permissions:
            array.append(permission.url)
        return array

    def __str__(self):
        return self.names
