from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, UpdateView
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from dashboard.forms import CreateCityForm
from core.services.city_service import CityService
from core.utils.dispatch_permissions import custom_dispatch


PERMISSION = 'dashboard:cities'


class CityList(TemplateView):
    template_name = 'pages/generic/generic_table_page.html'

    def dispatch(self, request, *args, **kwargs):
        return custom_dispatch(super().dispatch, request, PERMISSION, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get('names')

        page_obj, fields, object_data, edit_url, delete_url, create_url, list_url = CityService.getList(
            self.request, name)

       # Pasar los datos de los objetos y los campos al contexto
        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Ciudades"
        context['busqueda'] = "nombre de ciudad"
        context['key'] = "onlycreate"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['edit_url'] = edit_url
        context['delete_url'] = delete_url
        context['create_url'] = create_url
        context['list_url'] = list_url

        return context


class DeleteCity(View):

    def dispatch(self, request, *args, **kwargs):
        return custom_dispatch(super().dispatch, request, PERMISSION, *args, **kwargs)

    def post(self, request, pk):
        model = CityService.getModel()
        item = get_object_or_404(model, pk=pk)
        item.delete()
        return redirect('dashboard:cities')


class EditCity(UpdateView):
    template_name = 'components/generic/generic_edit.html'
    form_class = CreateCityForm
    model = CityService.getModel()
    success_url = reverse_lazy('dashboard:cities')

    def dispatch(self, request, *args, **kwargs):
        return custom_dispatch(super().dispatch, request, PERMISSION, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = "Editar Ciudad"
        # context['key'] = "user"
        return context


class CreateCity(TemplateView):
    template_name = 'components/generic/generic_create.html'

    def dispatch(self, request, *args, **kwargs):
        return custom_dispatch(super().dispatch, request, PERMISSION, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CreateCityForm()
        return render(request, self.template_name, {'form': form, 'nombre': 'Crear una Ciudad', 'key': 'city'})

    def post(self, request, *args, **kwargs):
        form = CreateCityForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponseRedirect(reverse_lazy('dashboard:cities'))
        else:
            return render(request, self.template_name, {'form': form, 'nombre': 'Crear una Ciudad'})
