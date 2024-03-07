from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

@admin.register(Instrumento)
class InstrumentoAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'marca', 'precio', 'tipo', 'imagen')
    search_fields = ('nombre', 'marca', 'tipo','texto')
    list_filter = ('tipo','marca')

@admin.register(Comprador)
class CompradorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'correo')
    search_fields = ('usuario__username', 'correo')
    



admin.site.register(HistorialCompra)
admin.site.register(ListaHistorial)
admin.site.register(Ratings)
admin.site.register(Lista)
admin.site.register(Carrito)

