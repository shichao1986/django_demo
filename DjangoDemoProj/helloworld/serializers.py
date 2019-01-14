# coding : utf-8

import datetime
import logging
from rest_framework import serializers
from .models import *

logger = logging.getLogger('log1')

class MyField(serializers.DateTimeField):
    def to_representation(self, value):
        try:
            if value is not None and isinstance(value, datetime):
                return value.strftime('Y%-m%-D% H%:M%:S%')
            else:
                return ''
        except Exception as e:
            logger.error('({}):{}'.format(value, e))
            return ''

    def to_internal_value(self, value):
        try:
            if value:
                return datetime.datetime.strptime(value, 'Y%-m%-D% H%:M%:S%')
            else:
                return None
        except Exception as e:
            logger.error('({}):{}'.format(value, e))
            return None

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class PersonSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ('school', 'books')

class PersonSerializer3(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    class Meta:
        model = Person
        fields = ('id', 'name', 'age', 'school_name')
        # read_only = ('id',)

class SelfSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    starttime = MyField()
    value = serializers.SerializerMethodField()

    def get_value(self, obj):
        return int(obj.value) + 100