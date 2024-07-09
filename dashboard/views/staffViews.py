from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, View
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from dashboard.forms import CreateStaffForm
from core.services.staff_service import StaffService
from django.utils import timezone
import datetime
from django.conf import settings


PERMISSION = 'dashboard:staff'


class StaffList(TemplateView):
    template_name = 'pages/staff/staff_table_page.html'

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

        staffService = StaffService()

        name = self.request.GET.get('name')
        country = self.request.GET.get('country')

        page_obj, fields, object_data, profile_url, list_url, country_list = staffService.getStaffList(
            self.request, name, country)

        # print(object_data)

        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Personal"
        context['key'] = "staff"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['profile_url'] = profile_url
        context['list_url'] = list_url
        context['country_list'] = country_list

        if not name or not country:
            context['loaded_data'] = False
        else:
            context['loaded_data'] = True

        return context


class StaffProfile(TemplateView):
    template_name = 'pages/staff/staff_profile_page.html'

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

        user_pk = self.kwargs.get('pk')

        profile_obj = StaffService.getStaffProfileByPk(user_pk)

        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Perfil de " + profile_obj['name']
        context['key'] = "staff"
        context['profile_obj'] = profile_obj

        return context


# class EditStaff(UpdateView):
#     # template_name = 'country/country/edit_country.html'
#     template_name = 'components/generic/generic_edit.html'
#     form_class = CreateStaffForm
#     staffService = StaffService()
#     model = staffService.getModel()
#     success_url = reverse_lazy('dashboard:staff')

#     def dispatch(self, request, *args, **kwargs):
#         if settings.LOCAL:
#             return super().dispatch(request, *args, **kwargs)
#         else:
#             user = request.user
#             if not user.is_authenticated:
#                 return login_required(login_url=reverse_lazy(settings.LOGIN))(super().dispatch)(request, *args, **kwargs)
#             if user.has_permission(PERMISSION):
#                 return super().dispatch(request, *args, **kwargs)
#             else:
#                 return HttpResponseRedirect(reverse_lazy(settings.NOT_ALLOWED))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['nombre'] = "Editar Personal"
#         context['key'] = "staff"
#         return context


# class DeleteStaff(View):

#     def dispatch(self, request, *args, **kwargs):
#         if settings.LOCAL:
#             return super().dispatch(request, *args, **kwargs)
#         else:
#             user = request.user
#             if not user.is_authenticated:
#                 return login_required(login_url=reverse_lazy(settings.LOGIN))(super().dispatch)(request, *args, **kwargs)
#             if user.has_permission(PERMISSION):
#                 return super().dispatch(request, *args, **kwargs)
#             else:
#                 return HttpResponseRedirect(reverse_lazy(settings.NOT_ALLOWED))

#     def post(self, request, pk):
#         staffService = StaffService()
#         model = staffService.getModel()
#         # Obtener el país a eliminar
#         country = get_object_or_404(model, pk=pk)
#         # Eliminar el país
#         country.delete()
#         # Redirigir a la página de lista de países después de la eliminación
#         return redirect('dashboard:staff')


# class CreateStaff(TemplateView):
#     # template_name = 'country/country/create_country.html'
#     template_name = 'components/generic/generic_create.html'

#     def dispatch(self, request, *args, **kwargs):
#         if settings.LOCAL:
#             return super().dispatch(request, *args, **kwargs)
#         else:
#             user = request.user
#             if not user.is_authenticated:
#                 return login_required(login_url=reverse_lazy(settings.LOGIN))(super().dispatch)(request, *args, **kwargs)
#             if user.has_permission(PERMISSION):
#                 return super().dispatch(request, *args, **kwargs)
#             else:
#                 return HttpResponseRedirect(reverse_lazy(settings.NOT_ALLOWED))

#     def get(self, request, *args, **kwargs):
#         form = CreateStaffForm()
#         return render(request, self.template_name, {'form': form, 'nombre': 'Crear Personal', 'key': 'staff'})

#     def post(self, request, *args, **kwargs):
#         form = CreateStaffForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse_lazy('dashboard:staff'))
#         else:
#             return render(request, self.template_name, {'form': form, 'nombre': 'Crear Personal'})
