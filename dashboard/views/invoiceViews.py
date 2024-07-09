from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import HttpResponseRedirect
from core.services.invoice_service import InvoiceService
from django.conf import settings


PERMISSION = 'dashboard:invoices'


class InvoiceList(TemplateView):
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

        name = self.request.GET.get('name')

        page_obj, fields, object_data, list_url, description_url = InvoiceService.getInvoiceList(
            self.request, name)

        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Facturas"
        context['key'] = "staff"
        context['busqueda'] = "número de orden"
        context['fields'] = fields
        context['delete_url'] = 'dashboard:invoice_description'
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['description_url'] = description_url
        context['list_url'] = list_url

        return context


class InvoiceDescription(TemplateView):
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

        # profile_obj = StaffService.getStaffProfileByPk(user_pk)

        # Pasar los datos de los objetos y los campos al contexto
        # context['nombre'] = "Perfil de " + profile_obj['name']
        context['key'] = "staff"
        # context['profile_obj'] = profile_obj

        return context
