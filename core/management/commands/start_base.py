from django.core.management.base import BaseCommand
from core.models import Permission, Role, User
from django.urls import reverse_lazy


class Command(BaseCommand):
    help = 'Add all URLs from urlpatterns as permissions and create super admin role and user'

    def handle(self, *args, **options):
        url_tuples = [
            ('Usuarios', 'dashboard:users'),
            ('Roles', 'dashboard:roles'),
        ]

        permissions = []
        for name, url_name in url_tuples:
            url_path = reverse_lazy(url_name)
            permission, created = Permission.objects.get_or_create(
                name=name, url=url_path)
            permissions.append(permission)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Se creó el permiso {permission.name}'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'El permiso {permission.name} ya existe'))

        # Create super admin role
        superadmin_role, created = Role.objects.get_or_create(
            name='SuperAdmin', all_access=True)
        if created:
            superadmin_role.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS(
                'Se creó el rol SuperAdmin con todos los permisos'))
        else:
            self.stdout.write(self.style.WARNING(
                'El rol SuperAdmin ya existe'))

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin', password='admin')
            admin_user.role = superadmin_role
            admin_user.names = 'Admin User'
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(
                'Se creó el usuario admin con clave admin'))
        else:
            self.stdout.write(self.style.WARNING('El usuario admin ya existe'))
