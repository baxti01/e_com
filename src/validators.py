import re
from datetime import datetime

from email_validator import validate_email


async def validate_date_format(date_str):
    formats = ['%Y-%m-%d', '%d.%m.%Y']

    for date_format in formats:
        try:
            datetime.strptime(date_str, date_format).date()
            return 'date'
        except Exception:
            pass

    return False


async def validate_phone_number(phone_number):
    # Шаблон для номера: +7 xxx xxx xx xx или +7xxxxxxxxxx
    phone_pattern = re.compile(r'^\+7\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}$')
    try:
        phone = re.match(phone_pattern, phone_number)
        if phone:
            return 'phone'
    except Exception:
        pass

    return False


async def validate_email_address(value):
    try:
        validate_email(value)
        return 'email'
    except Exception:
        return False


async def run_validators(value):
    date = await validate_date_format(value)
    phone = await validate_phone_number(value)
    email = await validate_email_address(value)

    return date or phone or email or type(value).__name__
