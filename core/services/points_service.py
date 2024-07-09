from django.core.paginator import Paginator
from core.models import Points, User
from openpyxl import Workbook
from django.http import HttpResponse
from django.db import transaction

# from django.urls import reverse_lazy


class PointsService:

    @staticmethod
    def getPointsList(request, name):

        # Obtener todos los productos y sumar el stock correspondiente
        points = Points.objects.order_by('created_at').all()

        # Filtrar por nombre si se proporciona
        if name:
            points = points.filter(order_id__icontains=name)

        # Lista de campos a incluir en la respuesta
        fields = Points._meta.fields
        fields_to_include = ['id', 'created_at',
                             'user', 'order_id',  'old_points', 'new_points']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los resultados
        paginator = Paginator(points, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # URLs para acciones en la interfaz
        list_url = 'dashboard:points'
        upload_url = 'dashboard:points_upload'

        # Preparar los datos para cada producto paginado
        object_data = []
        for obj in page_obj:
            obj_data = [getattr(obj, field.name) for field in fields]
            object_data.append(obj_data)

        return page_obj, fields_to_include, object_data, list_url, upload_url

    @staticmethod
    def checkExists(oid):
        exists = Points.objects.filter(order_id=oid).exists()
        return exists

    @staticmethod
    def getModel():
        return Points

    @staticmethod
    def getAllStocks():
        return Points.objects.all()

    @staticmethod
    def getStore(id):
        return Points.objects.get(id=id)

    @staticmethod
    def create_excel_template():
        # Crear un libro de trabajo
        wb = Workbook()
        ws = wb.active

        # Definir los títulos de las columnas
        columns = ['user_ci', 'order_id', 'plus_points',
                   'minus_points']
        ws.append(columns)

        # Guardar el libro en un objeto de respuesta HTTP
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Plantilla_puntos.xlsx"'
        wb.save(response)

        return response

    @staticmethod
    def uploadPointsDataframe(df):
        # Renombrar las columnas según el modelo Points
        df.rename(columns={
            'user_ci': 'user',
            'order_id': 'order_id',
            'plus_points': 'plus_points',
            'minus_points': 'minus_points',
        }, inplace=True)

        df['order_id'] = df['order_id'].astype(str)
        df['plus_points'] = df['plus_points'].astype(int)
        df['minus_points'] = df['minus_points'].astype(int)

        # Utilizar create para insertar cada fila del DataFrame como un nuevo objeto Points
        with transaction.atomic():
            for index, row in df.iterrows():
                # Obtener usuario actualizado de la base de datos
                user = User.objects.get(ci=row['user'])
                user.refresh_from_db()  # Asegurar que tenemos la información más actualizada
                # Puntos antiguos antes de la transacción
                old_points = user.total_points
                # Puntos nuevos después de la transacción
                new_points = old_points + row['plus_points'] - row['minus_points']

                print(f"User CI: {user.ci}, Old Points: {old_points}, New Points: {new_points}")

                Points.objects.create(
                    user=user,
                    order_id=row['order_id'],
                    plus_points=row['plus_points'],
                    minus_points=row['minus_points'],
                    old_points=old_points,
                    new_points=new_points,
                    description='Actualización de puntos'
                )

                # Actualizar el campo total_points del usuario
                user.total_points = new_points
                user.save(update_fields=['total_points'])

        print("Todos los puntos han sido actualizados correctamente.")
