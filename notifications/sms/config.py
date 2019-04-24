import os

TEMPLATE_PATH = os.getenv('NOTIFIER_MAILER_TEMPLATE_PATH', os.path.join(os.path.dirname(__file__), "templates"))

PROVIDER = os.getenv('NOTIFIER_SMS_PROVIDER', 'sms_ru')  # unused for now
SMS_RU_API_ID = os.getenv('NOTIFIER_SMS_RU_API_ID', 'F4A66482-5812-A0CF-7101-7B2A645AB3A2')
SMS_RU_SEND_URL = os.getenv('NOTIFIER_SMS_RU_SEND_URL', 'https://sms.ru/sms/send')
