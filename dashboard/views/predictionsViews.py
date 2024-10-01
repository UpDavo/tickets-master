
from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from core.services.predictions_service import PredictionsService
from core.utils.dispatch_permissions import custom_dispatch
from ai_models.data.cities import cities
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.services.ai_service import AiService
from core.models.predictions import Predictions

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
        ]

        # Lista de géneros musicales
        context['genres'] = [
            'Pop', 'Rock', 'Hip-Hop', 'Reggaeton', 'Jazz', 'Reggae', 'Blues', 'Country', 'Classical', 'Electronic', 'Folk',
            'Latin', 'Metal', 'R&B', 'Soul', 'Punk', 'Disco', 'Funk', 'Gospel', 'Ska', 'Techno',
        ]

        return context


@csrf_exempt
def process_prediction(request):
    artist_name = request.POST.get('artist_name')
    artist_gender = request.POST.get('artist_gender')
    artist_age = request.POST.get('artist_age')
    artist_country = request.POST.get('artist_country')
    artist_genres = request.POST.getlist('artist_genres')
    artist_followers = request.POST.get('artist_followers')
    event_country = request.POST.get('event_country')
    event_city = request.POST.get('event_city')
    event_venue = request.POST.get('event_venue')

    popularity_data = {
        'Gender': [artist_gender],
        'Age': [int(artist_age)],
        'Country': [artist_country],
        'Followers': [int(artist_followers)],
        'Genres': [artist_genres]
    }

    venue_data = {
        'City': [event_city],
        'Country': [event_country],
        'Venue': [event_venue],
    }

    print(popularity_data)
    print(venue_data)

    ai_service = AiService()

    popularity = ai_service.processPopularity(popularity_data)

    revenue = ai_service.processTickets(venue_data, popularity)

    # print(store_dict)
    return JsonResponse({'artist_popularity': popularity, 'event_tickets': revenue['TicketsSold'],
                         'event_revenue': revenue['Revenue'], 'event_price': revenue['PricePerTicket']})


@csrf_exempt
def save_prediction(request):
    if request.method == 'POST':
        try:
            # Cargar los datos JSON del cuerpo de la solicitud
            data = json.loads(request.body)

            # Datos del Formulario
            artist_name = data.get('artist_name')
            artist_gender = data.get('artist_gender')
            artist_age = data.get('artist_age')
            artist_country = data.get('artist_country')
            artist_genres = data.get('artist_genres', [])
            artist_followers = data.get('artist_followers')
            event_country = data.get('event_country')
            event_city = data.get('event_city')
            event_venue = data.get('event_venue')

            # Predicciones
            artist_popularity = data.get('artist_popularity')
            event_tickets = data.get('event_tickets')
            event_revenue = data.get('event_revenue')
            event_price = data.get('event_price')

            # Convertir artist_genres de lista a cadena
            artist_genres_str = ', '.join(artist_genres)

            # Crear una instancia del modelo Predictions
            prediction = Predictions(
                artist_name=artist_name,
                artist_gender=artist_gender,
                artist_age=int(artist_age) if artist_age else None,
                artist_country=artist_country,
                artist_genres=artist_genres_str,
                artist_followers=int(
                    artist_followers) if artist_followers else None,
                event_country=event_country,
                event_city=event_city,
                event_venue=event_venue,
                # Campos Generados
                artist_popularity=int(
                    artist_popularity) if artist_popularity else None,
                event_tickets=int(event_tickets) if event_tickets else None,
                event_revenue=int(event_revenue) if event_revenue else None,
                event_price=float(event_price) if event_price else None,
            )

            # Guardar la predicción en la base de datos
            prediction.save()

            # Devolver éxito
            return JsonResponse({'result': True})
        except Exception as e:
            # Puedes registrar el error para depuración
            print(f"Error al guardar la predicción: {e}")
            # Devolver fallo
            return JsonResponse({'result': False, 'error': str(e)})
    else:
        # Método HTTP no permitido
        return JsonResponse({'result': False, 'error': 'Método no permitido'})
