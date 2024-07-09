from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, View
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from dashboard.forms import CreateStockForm
from core.services.stock_service import StockService
from django.conf import settings
import pandas as pd
from django.urls import reverse

PERMISSION = 'dashboard:stocks'


class StockList(TemplateView):
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

        page_obj, fields, object_data, edit_url, list_url, upload_url, upload_url_general, upload_form_url = StockService.getStockList(
            self.request, name)

        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Stock"
        context['activos'] = True
        context['busqueda'] = "nombre de producto"
        context['key'] = "nocreate"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['edit_url'] = edit_url
        context['list_url'] = list_url
        context['upload_url_specific'] = upload_url
        context['upload_url'] = upload_url_general
        context['upload_form_url'] = upload_form_url

        return context


class EditStock(UpdateView):
    template_name = 'components/generic/generic_edit.html'
    form_class = CreateStockForm
    model = StockService.getModel()
    success_url = reverse_lazy('dashboard:stocks')

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
        context['nombre'] = "Editar Stock"  # Puedes ajustar el nombre aquí
        return context


class DeleteStock(View):

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

    def post(self, request, pk):
        model = StockService.getModel()
        # Obtener el país a eliminar
        store = get_object_or_404(model, pk=pk)
        # Eliminar el país
        store.delete()
        # Redirigir a la página de lista de países después de la eliminación
        return redirect('dashboard:stocks')


class CreateStock(TemplateView):
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


class UploadStock(TemplateView):
    template_name = 'components/stock/upload_stock.html'

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
        pk = kwargs.get('pk')
        if 'download' in request.GET:
            return StockService.create_excel_template()
        return render(request, self.template_name, {'nombre': 'Cargar Stock', 'pid': pk})

    def post(self, request, *args, **kwargs):
        expected_cols = ['Codigos']
        pk = kwargs.get('pk')
        if 'file' not in request.FILES:
            return render(request, self.template_name, {'nombre': 'Cargar Stock', 'pid': pk, 'error': True})
        
        excel_file = request.FILES['file']
        
        df = pd.read_excel(excel_file, engine='openpyxl')

        if all(col in df.columns for col in expected_cols):
            StockService.uploadProductsDataframe(df, pk)
            return HttpResponseRedirect(reverse_lazy('dashboard:stocks'))
        else:
            return render(request, self.template_name, {'nombre': 'Cargar Stock', 'pid': pk, 'error': True})


class UploadStockGeneral(TemplateView):
    template_name = 'components/stock/upload_stock_general.html'

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
            return StockService.create_excel_template2()
        return render(request, self.template_name, {'nombre': 'Cargar Stock Masivo'})

    def post(self, request, *args, **kwargs):
        expected_cols = ['Codigos']
        if 'file' not in request.FILES:
            return render(request, self.template_name, {'nombre': 'Cargar Stock Masivo', 'error': True})
        
        excel_file = request.FILES['file']
        df = pd.read_excel(excel_file, engine='openpyxl')

        if all(col in df.columns for col in expected_cols):
            StockService.uploadProductsDataframe2(df)
            return HttpResponseRedirect(reverse_lazy('dashboard:stocks'))
        else:
            return render(request, self.template_name, {'nombre': 'Cargar Stock Masivo', 'error': True})
