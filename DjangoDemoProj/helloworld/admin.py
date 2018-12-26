from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Person)
admin.site.register(models.Book)
admin.site.register(models.School)
admin.site.register(models.PersonBookRelation)
