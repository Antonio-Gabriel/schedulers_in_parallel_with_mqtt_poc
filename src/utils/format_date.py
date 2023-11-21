from datetime import datetime

DATE_FORMAT = "%d/%m/%Y"
HOUR_FORMAT = "%H:%M"


def format_date(date: str, hour: str):
    """return new date formated"""
    date_object = datetime.strptime(date, DATE_FORMAT)
    hour_object = datetime.strptime(hour, HOUR_FORMAT)

    new_date_formated = datetime(date_object.year, date_object.month, date_object.day,
                                 hour_object.hour, hour_object.minute)

    return new_date_formated
