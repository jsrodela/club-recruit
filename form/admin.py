from django.contrib import admin


# Register your models here.
from form.models import FormModel


class FormModelAdmin(admin.ModelAdmin):
    fields = ['number', 'club', 'section']


admin.site.register(FormModel)
