from django.utils import formats

def format_datetime(datetime_obj):
    if datetime_obj:
        return datetime_obj.strftime("%d-%b-%Y")
    return None