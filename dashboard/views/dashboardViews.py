from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.conf import settings


class DashboardIndexView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if settings.LOCAL:
            return super().dispatch(request, *args, **kwargs)
        else:
            user = request.user
            if not user.is_authenticated:
                return login_required(login_url=reverse_lazy('accounts:login'))(super().dispatch)(request, *args, **kwargs)
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nombre = "Dashboard"
        context['nombre'] = nombre
        context['key'] = 'dashboard'
        context['user'] = self.request.user

        return context
