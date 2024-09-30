
from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from core.services.predictions_service import PredictionsService
from core.utils.dispatch_permissions import custom_dispatch
from ai_models.data.cities import cities
import json

PERMISSION = 'dashboard:predictions'


class PredictionsList(TemplateView):
    template_name = 'pages/generic/generic_table_page.html'

    def dispatch(self, request, *args, **kwargs):
        return custom_dispatch(super().dispatch, request, PERMISSION, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get('names')

        page_obj, fields, object_data, edit_url, delete_url, create_url, list_url = PredictionsService.getList(
            self.request, name)

       # Pasar los datos de los objetos y los campos al contexto
        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Predicciones"
        context['busqueda'] = "nombre del artista"
        context['key'] = "onlycreate"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['edit_url'] = edit_url
        context['delete_url'] = delete_url
        context['create_url'] = create_url
        context['list_url'] = list_url

        return context


class DeletePredictions(View):

    def dispatch(self, request, *args, **kwargs):
        return custom_dispatch(super().dispatch, request, PERMISSION, *args, **kwargs)

    def post(self, request, pk):
        model = PredictionsService.getModel()
        item = get_object_or_404(model, pk=pk)
        item.delete()
        return redirect('dashboard:predictions')


class CreatePredictions(TemplateView):
    template_name = 'pages/predictions/create_prediction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nombre'] = "Crear una predicción"
        context['ubicacion_json'] = json.dumps(
            cities)  # Convertir a JSON string

        # Lista de países para el select de event_country
        context['countries_ubicacion'] = [country['country']
                                          for country in cities]

        # Lista de países para artist_country
        context['countries'] = [
            {'code': 'EC', 'name': 'Ecuador'},
            {'code': 'CO', 'name': 'Colombia'},
            {'code': 'US', 'name': 'Estados Unidos'},
            # Agrega más países según necesites
        ]

        # Lista de géneros musicales
        context['genres'] = [
            'Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Reggae', 'Blues', 'Country', 'Classical', 'Electronic', 'Folk',
            'Latin', 'Metal', 'R&B', 'Soul', 'Punk', 'Disco', 'Funk', 'Gospel', 'Ska', 'Techno'
        ]

        return context
