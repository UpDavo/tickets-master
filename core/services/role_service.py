from django.core.paginator import Paginator
from core.models import Role
# from django.urls import reverse_lazy


class RoleService:

    @staticmethod
    def getRoleList(request, name):

        # Obtener todos los horarios del usuario actual
        roles = Role.objects.order_by('created_at').all()

        if name:
            roles = roles.filter(name__icontains=name)

        # Obtener los campos del modelo Pais
        fields = Role._meta.fields
        fields_to_include = ['id', 'created_at', 'name',
                             'all_countries']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los horarios
        paginator = Paginator(roles, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Definir la URL de edición
        list_url = 'dashboard:roles'
        edit_url = 'dashboard:role_edit'
        delete_url = 'dashboard:role_delete'
        create_url = 'dashboard:role_create'

        # Obtener los valores de los campos para cada objeto
        object_data = []
        for obj in page_obj:
            obj_data = [getattr(obj, field.name) for field in fields]
            object_data.append(obj_data)

        return page_obj, fields, object_data, edit_url, delete_url, create_url, list_url

    @staticmethod
    def checkExists(brand):
        exists = Role.objects.filter(name=brand).exists()
        return exists

    @staticmethod
    def getModel():
        return Role

    @staticmethod
    def getAllRoles():
        return Role.objects.all()
