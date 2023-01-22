from django.contrib import admin
from account.models import User


class UserAdmin(admin.ModelAdmin):
    fields = ['name', 'phone']
    readonly_fields = ['id']


admin.site.register(User)
