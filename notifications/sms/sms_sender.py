import requests

from jinja2 import Environment, FileSystemLoader
from phonenumbers import parse
from phonenumbers.phonenumberutil import NumberParseException

from core.exceptions import ApiValidationException
from core.logger import logger
from . import config

env = Environment(
    loader=FileSystemLoader(config.TEMPLATE_PATH)
)


class SmsSender:
    @staticmethod
    def send_message(receivers, delay_until=None, sender=None, template='empty', **template_kwargs):
        for phone_number in receivers:
            try:
                # we have all the info about a number here so that we can block certain regions &c
                info = parse(phone_number)
                logger.info(info)
            except NumberParseException as e:
                raise ApiValidationException(f'{phone_number} is not a valid phone_number.') from e

        text = env.get_template(f'{template}.txt.j2').render(**template_kwargs)
        payload = {
            'api_id': config.SMS_RU_API_ID,
            'to': ', '.join(receivers),
            'msg': text,
            'json': 1,
        }

        if delay_until is not None:
            payload['time'] = delay_until.timestamp()

        if sender is not None:
            payload['from'] = sender

        res = requests.post(url=config.SMS_RU_SEND_URL, data=payload)
        print(res.json())
