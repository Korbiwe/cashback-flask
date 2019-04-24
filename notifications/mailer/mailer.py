from jinja2 import Environment, FileSystemLoader, select_autoescape
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from validate_email import validate_email

from core.exceptions import ApiValidationException
from . import config

jinja_env = Environment(
    loader=FileSystemLoader(config.TEMPLATE_PATH),
    autoescape=select_autoescape(['html', 'xml'])
)


class Mailer:
    @staticmethod
    def send_message(receivers, subject, template='empty', **template_kwargs):
        with SMTP(config.HOSTNAME, config.PORT) as connection:
            connection.starttls()
            connection.login(config.SENDER, config.PASSWORD)
            for receiver in receivers:
                if not validate_email(receiver):
                    raise ApiValidationException(f'{receiver} is not a valid email address.')

            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = config.SENDER
            message['To'] = ', '.join(receivers)

            plain = jinja_env.get_template(f'{template}.txt.j2').render(**template_kwargs)
            rich = jinja_env.get_template(f'{template}.html.j2').render(**template_kwargs)

            message.attach(MIMEText(plain, 'text'))
            message.attach(MIMEText(rich, 'html'))

            connection.send_message(message)
