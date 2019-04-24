__all__ = ['send_email', 'send_sms']

from datetime import datetime

from notifications.mailer import Mailer
from notifications.sms import SmsSender


def send_email(receivers: list,
               subject: str,
               template: str = 'empty',
               **template_kwargs):
    Mailer.send_message(receivers, subject, template, **template_kwargs)


def send_sms(receivers: list,
             sender: str = None,
             delay_until: datetime = None,
             template: str = 'empty',
             **template_kwargs) -> None:
    SmsSender.send_message(receivers, sender, delay_until, template, **template_kwargs)
