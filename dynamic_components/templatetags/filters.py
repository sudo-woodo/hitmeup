import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from django_jinja import library


@library.filter
def to_json(value):
    return mark_safe(json.dumps(value, cls=DjangoJSONEncoder))