from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


def custom_dispatch(view, request, permission, *args, **kwargs):
    if settings.LOCAL:
        return view(request, *args, **kwargs)
    else:
        user = request.user
        if not user.is_authenticated:
            return login_required(login_url=reverse_lazy(settings.LOGIN))(view)(request, *args, **kwargs)
        if user.has_permission(permission):
            return view(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy(settings.NOT_ALLOWED))
