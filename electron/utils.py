from django.urls import reverse


def get_cache_key(app_name, view_name, object_id='', url_kwargs=None):
    url_path = reverse(view_name, url_kwargs)
    return f'{app_name}{url_path}{object_id}'
