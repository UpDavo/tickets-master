from django.core.paginator import Paginator
from core.models import City
# from django.urls import reverse_lazy


class CityService:
    
    @staticmethod
    def getList(request, name):
        # Obtener todos los usuarios
        items = City.objects.order_by('-created_at').all()

        if name:
            items = items.filter(name__icontains=name)

        # Obtener los campos del modelo Usuario como una lista de objetos Field
        fields = City._meta.fields
        fields_to_include = ['id', 'created_at','name']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los usuarios
        paginator = Paginator(items, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        list_url = 'dashboard:cities'
        edit_url = 'dashboard:city_edit'
        delete_url = 'dashboard:city_delete'
        create_url = 'dashboard:city_create'

        # Obtener los valores de los campos para cada usuario
        object_data = []
        for obj in page_obj:
            obj_data = [getattr(obj, field.name) for field in fields]
            object_data.append(obj_data)

        return page_obj, fields, object_data, edit_url, delete_url, create_url, list_url

    @staticmethod
    def checkExists(item):
        exists = City.objects.filter(name=item).exists()
        return exists

    @staticmethod
    def getModel():
        return City

    @staticmethod
    def getAllCities():
        return City.objects.all()
