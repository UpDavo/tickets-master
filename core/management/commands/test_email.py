from django.core.management.base import BaseCommand
from core.utils.emailThread import EmailThread


class Command(BaseCommand):
    help = 'Send a custom test email using EmailThread'

    def handle(self, *args, **kwargs):
        
        subject = 'Repartidor Realizó el Picking'
        email_data = {
            'nombre': 'Juan',
            'order_id': 'INV-20240906-00001',
            'code': 'KASLKD',
            'value': 2.7,
            'picker_name': 'Felipe',
            'pick_date': '4/12/2024',
            'bottles': ['6 Botellas 330/550/600', '6 Botellas 850/1000']
        }
        recipient_list = ['updavo@gmail.com']
        template = 'emails/picking_complete.html'

        email_thread = EmailThread(
            subject, email_data, recipient_list, template)

        try:
            email_thread.start()  # Inicia el hilo y envía el correo de manera asíncrona
            self.stdout.write(self.style.SUCCESS(
                'Correo enviado exitosamente en un hilo separado.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error enviando correo: {e}'))
            
        subject = 'Código Asignado'
        template = 'emails/assigned_code.html'

        email_thread = EmailThread(
            subject, email_data, recipient_list, template)

        try:
            email_thread.start()  # Inicia el hilo y envía el correo de manera asíncrona
            self.stdout.write(self.style.SUCCESS(
                'Correo enviado exitosamente en un hilo separado.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error enviando correo: {e}'))
