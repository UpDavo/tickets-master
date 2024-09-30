import pandas as pd
import re
from django.core.management.base import BaseCommand
from core.models import User, Role
from core.services.users_service import UsersService
from django.contrib.auth.hashers import make_password


def normalize_store_name(store_name):
    # Convierte el nombre a minúsculas y elimina caracteres especiales
    return re.sub(r'[^a-z0-9]+', '', store_name.lower())


class Command(BaseCommand):
    help = 'Carga usuarios en masa desde un archivo Excel, creando o actualizando tiendas y ciudades, con tiendas normalizadas'

    def add_arguments(self, parser):
        parser.add_argument(
            'excel_file', type=str, help='Ruta del archivo Excel con la información de usuarios')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            try:
                # Extrae la información de cada columna del Excel
                username = row['username']
                password = row['password'] if 'password' in row else 'default_password'
                email = row['email']
                names = row['names']
                ci = row['ci']
                role_name = row['role']

                # Busca el rol
                role, _ = Role.objects.get_or_create(name=role_name)

                # Verifica si el usuario ya existe
                userService = UsersService()
                if userService.checkExists(username):
                    self.stdout.write(self.style.WARNING(
                        f'El usuario {username} ya existe.'))
                    continue

                # Crea el nuevo usuario
                user = User(
                    username=username,
                    password=make_password(password),  # Cifra la contraseña
                    email=email,
                    names=names,
                    ci=ci,
                    role=role,
                )
                user.save()

                self.stdout.write(self.style.SUCCESS(
                    f'Usuario {username} creado con éxito.'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Error al crear el usuario en la fila {index + 1}: {str(e)}'))
