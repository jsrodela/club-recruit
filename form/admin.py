from django.contrib import admin


# Register your models here.
from form.models import FormModel
from form.models import TimeModel


class FormModelAdmin(admin.ModelAdmin):
    readonly_fields = ('submit_at', )


admin.site.register(FormModel, FormModelAdmin)
admin.site.register(TimeModel)
