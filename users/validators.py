import datetime

from rest_framework.exceptions import ValidationError

from HW27.settings import MIN_AGE_REQUIRED


def check_age(value):
    today = datetime.date.today()
    age = (today.year - value.year - 1) + ((today.month, today.day) >= (value.month, value.day))
    if age < MIN_AGE_REQUIRED:
        raise ValidationError(f"Возраст не может быть менее 9 лет, а Вам {age}")