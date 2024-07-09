from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import Staff
# from django.urls import reverse_lazy


class StaffService:

    @staticmethod
    def getStaffList(request, name):

        staff = []

        fields = ['id', 'name', 'contract_type']

        # Paginar los horarios
        paginator = Paginator(staff, 10)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Obtener los elementos de la página actual
        object_data = page_obj.object_list

        # Definir la URL de edición
        list_url = 'dashboard:staff'
        profile_url = 'dashboard:staff_profile'

        return page_obj, fields, object_data, profile_url, list_url

    @staticmethod
    def checkExists(brand):
        exists = Staff.objects.filter(name=brand).exists()
        return exists

    @staticmethod
    def getModel():
        return Staff

    @staticmethod
    def getAllStaff():
        return Staff.objects.all()

    @staticmethod
    def getAllStaffByC(country):
        return Staff.objects.filter(country=country)
