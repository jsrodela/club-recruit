from django.contrib import admin

from index.models import StatusModel


# Register your models here.


class StatusModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(StatusModel, StatusModelAdmin)

