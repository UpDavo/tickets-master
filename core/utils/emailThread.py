import threading
import traceback
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailThread(threading.Thread):
    from_address = settings.DEFAULT_FROM_EMAIL

    def __init__(self, subject, email_data, recipient_list, template, attachments=None):
        self.subject = subject
        self.recipient_list = recipient_list
        self.email_data = email_data
        self.template = template
        self.__attachments = []

        if attachments:
            self.__attachments = attachments

        if settings.EMAIL_SUBJECT_PREFIX:
            self.subject = '{} {}'.format(
                settings.EMAIL_SUBJECT_PREFIX, self.subject)

        threading.Thread.__init__(self)

    def run(self):
        try:
            email_html = render_to_string(self.template, {
                'email_data': self.email_data
            })

            email = EmailMultiAlternatives(
                subject=self.subject,
                body=email_html,
                from_email=self.from_address,
                to=self.recipient_list
            )

            email.attach_alternative(email_html, 'text/html')

            if len(self.__attachments) > 0:
                for attachment in self.__attachments:
                    email.attach(attachment['filename'], attachment['file'])

            email.send()

        except Exception as ex:
            print('ERROR ENVIANDO CORREO', str(ex))
            traceback.print_exc()
