import datetime

DEFAULT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def format_datetime_object(datetime_object, date_format=DEFAULT_DATE_FORMAT):
    """Returns the string representation of a datetime object in the format
    specified. Default used if no format specified.
    """
    return datetime_object.strftime(date_format) if datetime_object else ''


def get_datetime_object(datetime_string, date_format=DEFAULT_DATE_FORMAT):
    """Returns the datetime object representation from the given
    `datetime_string` and `date_format`. Default used if no format specified.
    """
    return datetime.datetime.strptime(datetime_string, date_format)
