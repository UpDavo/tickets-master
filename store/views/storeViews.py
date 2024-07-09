from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.conf import settings
from core.services.product_service import ProductService


class StoreViewIndex(TemplateView):
    template_name = 'store_home.html'

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
        
        products = ProductService.getRecentStarredProducts()
        nombre = "Dashboard"
        context['nombre'] = nombre
        context['key'] = 'dashboard'
        context['user'] = self.request.user
        context['products'] = products

        return context
