# from django.contrib.auth.models import User
from django.core.paginator import Paginator
from core.models import User


class UsersService:

    @staticmethod
    def getUsersList(request, names):
        # Obtener todos los usuarios
        users = User.objects.order_by('created_at').all()

        if names:
            users = users.filter(names__icontains=names)

        # Obtener los campos del modelo Usuario como una lista de objetos Field
        fields = User._meta.fields
        fields_to_include = ['id', 'last_login',
                             'username', 'names', 'role', 'brand']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los usuarios
        paginator = Paginator(users, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Definir la URL de edición
        list_url = 'dashboard:users'
        edit_url = 'dashboard:user_edit'
        delete_url = 'dashboard:user_delete'
        create_url = 'dashboard:user_create'

        # Obtener los valores de los campos para cada usuario
        object_data = []
        for obj in page_obj:
            obj_data = [getattr(obj, field.name) for field in fields]
            object_data.append(obj_data)

        return page_obj, fields, object_data, edit_url, delete_url, create_url, list_url

    @staticmethod
    def checkExists(username):
        exists = User.objects.filter(username=username).exists()
        return exists

    @staticmethod
    def getModel():
        return User

    @staticmethod
    def getAllUsersByCBA(country, brand):
        return User.objects.filter(country=country, brand=brand, is_approver=True)
