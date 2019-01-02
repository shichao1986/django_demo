# coding : utf-8

from django.db.models import TextField, BinaryField
import ast
import zlib

class MyListField(TextField):
    def __init__(self, *args, **kwargs):
        super(MyListField, self).__init__(*args, **kwargs)

    # db to pathon, django >= 1.8 use this function
    def from_db_value(self, value, expression, connection, context):
        if not value or not isinstance(value, str):
            return []

        return value.split(',')

    # db to pathon, django <= 1.7 use this function
    def to_python(self, value):
        if not value or not isinstance(value, str):
            return []

        return value.split(',')

    # python to db
    def get_prep_value(self, value):
        if not value or not isinstance(value, list):
            return ''
        v_str = ','.join(value)
        return v_str

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return '' if value is None else self.get_prep_value(value)

class MyCompressTextField(BinaryField):
    def __init__(self, *args, **kwargs):
        super(MyCompressTextField, self).__init__(*args, **kwargs)

    # db to python, django > 1.8
    def from_db_value(self, value, expression, connection, context):
        if not value or not isinstance(value, bytes):
            return b''.decode()

        return zlib.decompress(value).decode()

    # python to db
    def get_prep_value(self, value):
        if not value or not isinstance(value, str):
            return ''.encode()

        return zlib.compress(str.encode())

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return b''.decode() if value is None else self.get_prep_value(value)