from django.contrib import admin

from .models import Saidas
class SaidasAdmin(admin.ModelAdmin):
    list_display = ['id', 'data',  'produto', 'quantidade']
    list_display_links = ['id', 'produto']
    list_per_page = 5

# # Register your models here.
admin.site.register(Saidas, SaidasAdmin)


