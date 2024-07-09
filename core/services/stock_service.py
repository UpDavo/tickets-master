from django.core.paginator import Paginator
from core.models import Stock, Product
from django.conf import settings
from django.db.models import Sum
from django.db.models.functions import Coalesce
import openpyxl
from openpyxl import Workbook
from django.http import HttpResponse
from django.db import transaction

# from django.urls import reverse_lazy


class StockService:

    @staticmethod
    def getStockList(request, name):

        # Obtener todos los productos y sumar el stock correspondiente
        stocks = Product.objects.annotate(
            total_quantity=Coalesce(Sum('stock__quantity'), 0)
        ).order_by('created_at').values(
            'id',
            'created_at',
            'name',
            'sku',
            'active',
            'total_quantity'
        )

        # Filtrar por nombre si se proporciona
        if name:
            stocks = stocks.filter(name__icontains=name)

        # Lista de campos a incluir en la respuesta
        fields_to_include = ['id', 'created_at',
                             'name', 'sku', 'active', 'total_quantity']

        # Paginar los resultados
        paginator = Paginator(stocks, 10)  # Muestra 10 productos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # URLs para acciones en la interfaz
        list_url = 'dashboard:stocks'
        edit_url = 'dashboard:stock_edit'
        upload_url = 'dashboard:stock_upload'
        upload_url_general = 'dashboard:stock_upload_general'
        upload_form_url = 'dashboard:stock_upload'

        # Preparar los datos para cada producto paginado
        object_data = []
        for obj in page_obj:
            # Accede directamente usando la clave del diccionario
            obj_data = [obj[field] for field in fields_to_include]
            object_data.append(obj_data)

        return page_obj, fields_to_include, object_data, edit_url, list_url, upload_url, upload_url_general, upload_form_url

    @staticmethod
    def checkExists(code):
        exists = Stock.objects.filter(code=code).exists()
        return exists

    @staticmethod
    def getModel():
        return Stock

    @staticmethod
    def getAllStocks():
        return Stock.objects.all()

    @staticmethod
    def getStore(id):
        return Stock.objects.get(id=id)

    @staticmethod
    def create_excel_template():
        # Crear un libro de trabajo
        wb = Workbook()
        ws = wb.active

        # Definir los títulos de las columnas
        columns = ['Codigos']
        ws.append(columns)

        # Guardar el libro en un objeto de respuesta HTTP
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Plantilla_codigos.xlsx"'
        wb.save(response)

        return response

    @staticmethod
    def create_excel_template2():
        # Crear un libro de trabajo
        wb = Workbook()
        ws = wb.active

        # Definir los títulos de las columnas
        columns = ['Sku', 'Codigos']
        ws.append(columns)

        # Guardar el libro en un objeto de respuesta HTTP
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Plantilla_codigos_skus.xlsx"'
        wb.save(response)

        return response

    @staticmethod
    def uploadProductsDataframe(df, pk):
        # Renombrar columnas si es necesario
        df.rename(columns={'Codigos': 'code'}, inplace=True)

        # Convertir datos al tipo correcto si es necesario
        df['code'] = df['code'].astype(str)

        # Obtener códigos existentes
        existing_codes = set(Stock.objects.filter(
            product_id=pk).values_list('code', flat=True))

        # Filtrar solo los códigos que no existen previamente
        new_codes = df[~df['code'].isin(existing_codes)]

        # Iterar sobre los códigos nuevos para agregarlos a la base de datos
        with transaction.atomic():
            for index, row in new_codes.iterrows():
                Stock.objects.create(
                    code=row['code'],
                    quantity=1,
                    product_id=pk
                )

    @staticmethod
    def uploadProductsDataframe2(df):
        # Renombrar columnas si es necesario
        df.rename(columns={'Codigos': 'code', 'Sku': 'sku'}, inplace=True)

        # Convertir datos al tipo correcto si es necesario
        df['code'] = df['code'].astype(str)
        df['sku'] = df['sku'].astype(int)

        with transaction.atomic():
            for index, row in df.iterrows():
                product = Product.objects.filter(sku=row['sku']).first()
                if product:
                    # Obtener códigos existentes para el SKU
                    existing_codes = set(Stock.objects.filter(
                        product=product).values_list('code', flat=True))
                    # Filtrar solo los códigos que no existen previamente
                    new_codes = df[(df['sku'] == row['sku']) & (
                        ~df['code'].isin(existing_codes))]
                    # Iterar sobre los códigos nuevos para agregarlos a la base de datos
                    for _, new_row in new_codes.iterrows():
                        Stock.objects.create(
                            code=new_row['code'],
                            quantity=1,
                            product=product
                        )
