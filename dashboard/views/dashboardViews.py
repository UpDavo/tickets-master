from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponseForbidden


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
        # context['schedule_id'] = 0

        # sid = ScheduleService.getLatestScheduleId(self.request)
        # if sid != None:
        #     scheduleStattus = ScheduleService.getScheduleStattus(sid)
        #     print(scheduleStattus)

        #     if scheduleStattus == 'APPROVED':

        #         date = ScheduleService.getScheduleDate(sid)
        #         version = self.request.GET.get('version')
        #         scheduleJson = ScheduleService.getScheduleByModels(
        #             sid, version)
        #         variables = ScheduleService.getSchedule(
        #             scheduleJson['horario_test'])

        #         context['horas'] = variables['horas']
        #         context['dias'] = variables['dias']
        #         context['personas'] = variables['personas']
        #         context['dia_pesado'] = variables['dia_con_mas_personal']
        #         context['fecha'] = date
        #         context['calendar'] = variables['calendar']
        #         context['sid'] = sid
        #     else:
        #         context['sid'] = sid
        #         context['no_schedule'] = False
        #         context['status'] = scheduleStattus
        # else:
        #     context['no_schedule'] = True
        #     context['status'] = 'NONE'

        return context
