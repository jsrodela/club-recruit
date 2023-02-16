from django.contrib import admin

# Register your models here.
from about.models import ClubModel, ImageModel


class ClubModelAdmin(admin.ModelAdmin):
    readonly_fields = ('form_start', 'form_end')


class ImageModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )


admin.site.register(ClubModel, ClubModelAdmin)
admin.site.register(ImageModel, ImageModelAdmin)
