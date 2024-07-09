from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponseRedirect
from dashboard.forms import CreateStockForm
from core.services.points_service import PointsService
from django.conf import settings
import pandas as pd

PERMISSION = 'dashboard:points'


class PointsList(TemplateView):
    template_name = 'pages/generic/generic_table_page.html'

    def dispatch(self, request, *args, **kwargs):
        if settings.LOCAL:
            return super().dispatch(request, *args, **kwargs)
        else:
            user = request.user
            if not user.is_authenticated:
                return login_required(login_url=reverse_lazy(settings.LOGIN))(super().dispatch)(request, *args, **kwargs)
            if user.has_permission(PERMISSION):
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse_lazy(settings.NOT_ALLOWED))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get('names')

        page_obj, fields, object_data, list_url, upload_url = PointsService.getPointsList(
            self.request, name)

        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Points"
        context['activos'] = True
        context['busqueda'] = "número de orden"
        context['key'] = "nocreate"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['list_url'] = list_url
        context['upload_url'] = upload_url

        return context


class CreatePoints(TemplateView):
    template_name = 'components/generic/generic_create.html'

    def dispatch(self, request, *args, **kwargs):
        if settings.LOCAL:
            return super().dispatch(request, *args, **kwargs)
        else:
            user = request.user
            if not user.is_authenticated:
                return login_required(login_url=reverse_lazy(settings.LOGIN))(super().dispatch)(request, *args, **kwargs)
            if user.has_permission(PERMISSION):
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse_lazy(settings.NOT_ALLOWED))

    def get(self, request, *args, **kwargs):
        form = CreateStockForm()
        return render(request, self.template_name, {'form': form, 'nombre': 'Crear Stock', 'key': 'stock'})

    def post(self, request, *args, **kwargs):
        form = CreateStockForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('dashboard:stocks'))
        else:
            return render(request, self.template_name, {'form': form, 'nombre': 'Crear una Stock', 'key': 'stock'})


class UploadPoints(TemplateView):
    template_name = 'components/points/upload_points.html'

    def dispatch(self, request, *args, **kwargs):
        if settings.LOCAL:
            return super().dispatch(request, *args, **kwargs)
        else:
            user = request.user
            if not user.is_authenticated:
                return login_required(login_url=reverse_lazy(settings.LOGIN))(super().dispatch)(request, *args, **kwargs)
            if user.has_permission(PERMISSION):
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse_lazy(settings.NOT_ALLOWED))

    def get(self, request, *args, **kwargs):
        if 'download' in request.GET:
            return PointsService.create_excel_template()
        return render(request, self.template_name, {'nombre': 'Cargar Puntos'})

    def post(self, request, *args, **kwargs):
        expected_cols = ['user_ci', 'order_id', 'plus_points',
                         'minus_points']
        if 'file' not in request.FILES:
            return render(request, self.template_name, {'nombre': 'Cargar Puntos', 'error': True})

        excel_file = request.FILES['file']

        df = pd.read_excel(excel_file, engine='openpyxl')

        if all(col in df.columns for col in expected_cols):
            PointsService.uploadPointsDataframe(df)
            return HttpResponseRedirect(reverse_lazy('dashboard:points'))
        else:
            return render(request, self.template_name, {'nombre': 'Cargar Puntos', 'error': True})
