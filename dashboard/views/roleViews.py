from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, UpdateView
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from dashboard.forms import CreateRoleForm
from core.services.role_service import RoleService
from django.conf import settings

PERMISSION = 'dashboard:roles'


class RoleList(TemplateView):
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

        roleService = RoleService()

        name = self.request.GET.get('name')

        page_obj, fields, object_data, edit_url, delete_url, create_url, list_url = roleService.getRoleList(
            self.request, name)

       # Pasar los datos de los objetos y los campos al contexto
        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Roles"
        context['busqueda'] = "nombre de rol"
        context['key'] = "roles"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['edit_url'] = edit_url
        context['delete_url'] = delete_url
        context['create_url'] = create_url
        context['list_url'] = list_url

        return context


class DeleteRole(View):

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
        roleService = RoleService()
        model = roleService.getModel()
        # Obtener el país a eliminar
        role = get_object_or_404(model, pk=pk)
        # Eliminar el país
        role.delete()
        # Redirigir a la página de lista de países después de la eliminación
        return redirect('dashboard:roles')


class EditRole(UpdateView):
    template_name = 'components/roles/generic_checkbox_edit.html'
    form_class = CreateRoleForm
    roleService = RoleService()
    model = roleService.getModel()
    success_url = reverse_lazy('dashboard:roles')

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
        context['nombre'] = "Editar Rol"  # Puedes ajustar el nombre aquí
        return context


class CreateRole(TemplateView):
    template_name = 'components/roles/generic_checkbox_create.html'

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
        form = CreateRoleForm()
        return render(request, self.template_name, {'form': form, 'nombre': 'Crear un Rol'})

    def post(self, request, *args, **kwargs):
        form = CreateRoleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('dashboard:roles'))
        else:
            return render(request, self.template_name, {'form': form, 'nombre': 'Crear un Rol'})
