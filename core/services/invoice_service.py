from django.core.paginator import Paginator
from core.models import Invoice

class InvoiceService:

    @staticmethod
    def getInvoiceList(request, order_id):

        # Obtener todos los horarios del usuario actual
        invoices = Invoice.objects.order_by('created_at').all()

        if order_id:
            invoices = invoices.filter(order_id__icontains=order_id)

        # Obtener los campos del modelo Pais
        fields = Invoice._meta.fields
        fields_to_include = ['id', 'created_at',
                             'user', 'order_id', 'product_name']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los horarios
        paginator = Paginator(invoices, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Definir la URL de edición
        list_url = 'dashboard:invoices'
        description_url = 'dashboard:invoice_description'

        # Obtener los valores de los campos para cada objeto
        object_data = []
        for obj in page_obj:
            obj_data = [getattr(obj, field.name) for field in fields]
            object_data.append(obj_data)

        return page_obj, fields, object_data, list_url, description_url

    @staticmethod
    def checkExists(order_id):
        exists = Invoice.objects.filter(order_id=order_id).exists()
        return exists

    @staticmethod
    def getModel():
        return Invoice
