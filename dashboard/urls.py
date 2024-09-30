from django.urls import path
from .views import *
from core.views import NotAllowed

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardIndexView.as_view(), name='index'),


    # Users
    path('users', UsersList.as_view(), name='users'),
    path('users/create', CreateUser.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', EditUser.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', DeleteUser.as_view(), name='user_delete'),

    # Roles
    path('roles', RoleList.as_view(), name='roles'),
    path('roles/create', CreateRole.as_view(), name='role_create'),
    path('roles/<int:pk>/edit/', EditRole.as_view(), name='role_edit'),
    path('roles/<int:pk>/delete/', DeleteRole.as_view(), name='role_delete'),

    # Cities
    path('cities', CityList.as_view(), name='cities'),
    path('cities/create', CreateCity.as_view(), name='city_create'),
    path('cities/<int:pk>/edit/', EditCity.as_view(), name='city_edit'),
    path('cities/<int:pk>/delete/', DeleteCity.as_view(), name='city_delete'),


    # Extras
    path('not_allowed', NotAllowed, name='notAllowed'),
]
