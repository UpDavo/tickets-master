from django.core.paginator import Paginator
from core.models import Product
import openpyxl
from openpyxl import Workbook
from django.http import HttpResponse
from django.db import transaction


class ProductService:

    @staticmethod
    def getProductList(request, name):

        # Obtener todos los horarios del usuario actual
        products = Product.objects.order_by('created_at').all()

        if name:
            products = products.filter(name__icontains=name)

        # Obtener los campos del modelo Pais
        fields = Product._meta.fields
        fields_to_include = ['id', 'created_at',
                             'image', 'name', 'sku', 'active']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los horarios
        paginator = Paginator(products, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Definir la URL de edición
        list_url = 'dashboard:products'
        edit_url = 'dashboard:product_edit'
        delete_url = 'dashboard:product_delete'
        create_url = 'dashboard:product_create'
        upload_url = 'dashboard:product_upload'

        # Obtener los valores de los campos para cada objeto
        object_data = []
        for obj in page_obj:
            obj_data = [getattr(obj, field.name) for field in fields]
            object_data.append(obj_data)

        return page_obj, fields, object_data, edit_url, delete_url, create_url, list_url, upload_url

    @staticmethod
    def checkExists(product):
        exists = Product.objects.filter(name=product).exists()
        return exists

    @staticmethod
    def getModel():
        return Product

    @staticmethod
    def getAllProducts():
        return Product.objects.all()

    @staticmethod
    def getRecentStarredProducts():
        return Product.objects.filter(starred=True, active=True).order_by('-created_at')[:5]

    @staticmethod
    def getProduct(brand):
        return Product.objects.get(id=brand)

    @staticmethod
    def create_excel_template():
        # Crear un libro de trabajo
        wb = Workbook()
        ws = wb.active

        # Definir los títulos de las columnas
        columns = ['Nombre', 'SKU', 'Producto Físico',
                   'Precio', 'Url Imagen', 'Activo']
        ws.append(columns)

        # Guardar el libro en un objeto de respuesta HTTP
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Plantilla_Productos.xlsx"'
        wb.save(response)

        return response

    @staticmethod
    def uploadProductsDataframe(df):
        df.rename(columns={
            'Nombre': 'name',
            'SKU': 'sku',
            'Producto Físico': 'is_fisical',
            'Precio': 'price',
            'Url Imagen': 'image',
            'Activo': 'active'
        }, inplace=True)

        # Convertir datos al tipo correcto, asegurándose que los tipos de datos sean los correctos
        df['name'] = df['name'].astype(str)
        df['image'] = df['image'].astype(str)
        df['price'] = df['price'].astype(int)
        df['sku'] = df['sku'].astype(int)
        df['active'] = df['active'].apply(
            lambda x: True if x.lower() == 'si' else False)
        df['is_fisical'] = df['is_fisical'].apply(
            lambda x: True if x.lower() == 'si' else False)

        # Utilizar update_or_create para actualizar o crear productos
        with transaction.atomic():
            for index, row in df.iterrows():
                obj, created = Product.objects.update_or_create(
                    sku=row['sku'],  # El SKU es el identificador único
                    defaults={
                        'name': row['name'],
                        'active': row['active'],
                        'is_fisical': row['is_fisical']
                    }
                )
                if created:
                    print(f"Created new product: {obj.name}")
                else:
                    print(f"Updated existing product: {obj.name}")
