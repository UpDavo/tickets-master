from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, UpdateView
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from accounts.forms import CreateUserForm, UpdateUserForm
from core.services.users_service import UsersService
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

PERMISSION = 'dashboard:users'


class UsersList(TemplateView):
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

        page_obj, fields, object_data, edit_url, delete_url, create_url, list_url = UsersService.getUsersList(
            self.request, name)

        context['nombre'] = "Usuarios"
        context['key'] = 'user'
        context['busqueda'] = "nombre de usuario"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['edit_url'] = edit_url
        context['delete_url'] = delete_url
        context['create_url'] = create_url
        context['list_url'] = list_url

        return context


class DeleteUser(View):

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
        userService = UsersService()
        model = userService.getModel()
        # Obtener el país a eliminar
        user = get_object_or_404(model, pk=pk)
        # Eliminar el país
        user.delete()
        # Redirigir a la página de lista de países después de la eliminación
        return redirect('dashboard:users')


class EditUser(UpdateView):
    template_name = 'components/generic/generic_edit.html'
    form_class = UpdateUserForm
    userService = UsersService()
    model = userService.getModel()
    success_url = reverse_lazy('dashboard:users')

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
        context['nombre'] = "Editar Usuario"
        context['key'] = "user"
        return context


class CreateUser(TemplateView):
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
        form = CreateUserForm()
        return render(request, self.template_name, {'form': form, 'nombre': 'Crear un Usuario', 'key': 'user'})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponseRedirect(reverse_lazy('dashboard:users'))
        else:
            return render(request, self.template_name, {'form': form, 'nombre': 'Crear un País'})


@csrf_exempt
def get_filtered_approvers(request):
    country_id = request.GET.get('country_id')
    brand_id = request.GET.get('brand_id')
    users = UsersService.getAllUsersByCBA(country_id, brand_id)
    user_dict = {user.id: str(user) for user in users}
    return JsonResponse({'users': user_dict})
