
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from core.views.error404 import Error404


def default_view(request):
    return redirect('store:index')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('store/', include('store.urls')),
    path('accounts/', include('accounts.urls')),
    path('', default_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = Error404
