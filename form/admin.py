from django.contrib import admin


# Register your models here.
from form.models import FormModel


class FormModelAdmin(admin.ModelAdmin):
    fields = ['number', 'club', 'section', 'archive']
    readonly_fields = ['submit_at']


admin.site.register(FormModel, FormModelAdmin)
