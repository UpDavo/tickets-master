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

    # predictions
    path('predictions', PredictionsList.as_view(), name='predictions'),
    path('predictions/create', CreatePredictions.as_view(),
         name='predictions_create'),
    path('predictions/<int:pk>/delete/',
         DeletePredictions.as_view(), name='predictions_delete'),

    # Ajax
    path('predictions/process_prediction',
         process_prediction, name='process_prediction'),
    path('predictions/save_prediction',
         save_prediction, name='save_prediction'),


    # Extras
    path('not_allowed', NotAllowed, name='notAllowed'),
]
