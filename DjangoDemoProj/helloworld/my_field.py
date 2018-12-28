# coding : utf-8

from django.db.models import TextField
import ast

class MyListField(TextField):
    def __init__(self, *args, **kwargs):
        super(MyListField, self).__init__(*args, **kwargs)

    # db to pathon
    def to_python(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return ast.literal_eval(value)

    # python to db
    def get_prep_value(self, value):
        if value is None or not isinstance(value, list):
            return str([])
        return str(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return '[]' if value is None else self.get_prep_value(value)