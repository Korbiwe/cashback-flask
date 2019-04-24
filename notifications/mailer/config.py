import os

TEMPLATE_PATH = os.getenv('NOTIFIER_MAILER_TEMPLATE_PATH', './templates')

HOSTNAME = os.getenv('NOTIFIER_MAILER_HOST', 'smtp.gmail.com')
PORT = os.getenv('NOTIFIER_MAILER_PORT', '587')
SENDER = os.getenv('NOTIFIER_MAILER_SENDER', 'noreply.getbonus@gmail.com')
PASSWORD = os.getenv('NOTIFIER_MAILER_PASSWORD', 'vybscskggksoehax')
