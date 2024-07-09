from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, View
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from dashboard.forms import CreateProductForm
from core.services.product_service import ProductService
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

PERMISSION = 'dashboard:products'


class ProductList(TemplateView):
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

        page_obj, fields, object_data, edit_url, delete_url, create_url, list_url, upload_url = ProductService.getProductList(
            self.request, name)

        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Productos"
        context['activos'] = True
        context['busqueda'] = "nombre de producto"
        context['key'] = "upload"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['edit_url'] = edit_url
        context['delete_url'] = delete_url
        context['create_url'] = create_url
        context['list_url'] = list_url
        context['upload_url'] = upload_url

        return context


class EditProduct(UpdateView):
    # template_name = 'country/country/edit_country.html'
    template_name = 'components/generic/generic_edit.html'
    form_class = CreateProductForm
    model = ProductService.getModel()
    success_url = reverse_lazy('dashboard:products')

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
        context['nombre'] = "Editar Producto"  # Puedes ajustar el nombre aquí
        return context


class DeleteProduct(View):
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
        model = ProductService.getModel()
        # Obtener el país a eliminar
        brand = get_object_or_404(model, pk=pk)
        # Eliminar el país
        brand.delete()
        # Redirigir a la página de lista de países después de la eliminación
        return redirect('dashboard:products')


class CreateProduct(TemplateView):
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
        form = CreateProductForm()
        return render(request, self.template_name, {'form': form, 'nombre': 'Crear Producto'})

    def post(self, request, *args, **kwargs):
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return HttpResponseRedirect(reverse_lazy('dashboard:products'))
        else:
            return render(request, self.template_name, {'form': form, 'nombre': 'Crear una Producto'})


class UploadProduct(TemplateView):
    template_name = 'components/product/upload_products.html'

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
            return ProductService.create_excel_template()
        return render(request, self.template_name, {'nombre': 'Crear Productos Masivos', 'upload_form_url': 'dashboard:product_upload'})

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return render(request, self.template_name, {'nombre': 'Cargar Stock', 'upload_form_url': 'dashboard:product_upload', 'error': True})
        expected_cols = ['Nombre', 'SKU', 'Producto Físico',
                         'Precio', 'Url Imagen', 'Activo']
        excel_file = request.FILES['file']
        df = pd.read_excel(excel_file, engine='openpyxl')

        if all(col in df.columns for col in expected_cols):
            # Process
            ProductService.uploadProductsDataframe(df)
            return HttpResponseRedirect(reverse_lazy('dashboard:products'))
        else:
            return render(request, self.template_name, {'nombre': 'Crear Productos Masivo', 'upload_form_url': 'dashboard:product_upload', 'error': True})


@csrf_exempt
def get_filtered_brands(request):
    country_id = request.GET.get('country_id')
    brands = ProductService.getAllBrandsByC(country_id)
    brand_dict = {brand.id: str(brand) for brand in brands}
    return JsonResponse({'brand': brand_dict})
