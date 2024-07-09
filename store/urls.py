from django.urls import path
from .views import *
from core.views import NotAllowed

app_name = 'store'

urlpatterns = [
    path('', StoreViewIndex.as_view(), name='index'),
    # Extras
    path('not_allowed', NotAllowed, name='notAllowed'),
]
