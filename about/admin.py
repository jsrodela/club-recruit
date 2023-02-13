from django.contrib import admin

# Register your models here.
from about.models import ClubModel


class ClubModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(ClubModel)
