from django.core.management.base import BaseCommand
from core.models import Permission
from django.urls import reverse_lazy


class Command(BaseCommand):
    help = 'Add all URLs from urlpatterns as permissions'

    def handle(self, *args, **options):
        url_tuples = [
            ('Usuarios', 'dashboard:users'),
            ('Roles', 'dashboard:roles'),
        ]

        for name, url_name in url_tuples:
            url_path = reverse_lazy(url_name)
            permission, created = Permission.objects.get_or_create(
                name=name, url=url_path)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Se creó el permiso {permission.name}'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'El permiso {permission.name} ya existe'))
