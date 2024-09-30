from django.core.paginator import Paginator
from core.models import Predictions
# from django.urls import reverse_lazy


class PredictionsService:

    @staticmethod
    def getList(request, name):
        # Obtener todos los usuarios
        items = Predictions.objects.order_by('-created_at').all()

        if name:
            items = items.filter(artist_name__icontains=name)

        # Obtener los campos del modelo Usuario como una lista de objetos Field
        fields = Predictions._meta.fields
        fields_to_include = ['id', 'created_at',
                             'artist_name', 'artist_popularity']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los usuarios
        paginator = Paginator(items, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        list_url = 'dashboard:predictions'
        edit_url = 'dashboard:predictions_delete'
        delete_url = 'dashboard:predictions_delete'
        create_url = 'dashboard:predictions_create'

        # Obtener los valores de los campos para cada usuario
        object_data = []
        for obj in page_obj:
            obj_data = [getattr(obj, field.name) for field in fields]
            object_data.append(obj_data)

        return page_obj, fields, object_data, edit_url, delete_url, create_url, list_url

    @staticmethod
    def checkExists(item):
        exists = Predictions.objects.filter(name=item).exists()
        return exists

    @staticmethod
    def getModel():
        return Predictions

    @staticmethod
    def getAll():
        return Predictions.objects.all()
