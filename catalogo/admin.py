from django.contrib import admin

from .models import (
    Categoria,
    Comentario,
    Especie,
    Etiqueta,
    Familia,
    GuiaCuidado,
    Producto,
    Proveedor,
)


class GuiaCuidadoInline(admin.StackedInline):
    model = GuiaCuidado
    can_delete = False

@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ("nombre_comun", "nombre_cientifico", "familia", "tipo_propagacion")
    list_filter = ("familia", "tipo_propagacion")
    search_fields = ("nombre_comun", "nombre_cientifico")
    ordering = ("nombre_comun",)
    list_select_related = ("familia",)
    inlines = [GuiaCuidadoInline]


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "grupo")
    list_filter = ("grupo",)
    search_fields = ("nombre",)
    ordering = ("grupo", "nombre")


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cuit", "telefono", "email")
    search_fields = ("nombre", "cuit", "email")
    ordering = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "especie", "precio", "stock", "tamano", "activo")
    list_filter = ("categoria", "activo", "tamano", "etiquetas")
    search_fields = ("nombre", "especie__nombre_cientifico")
    ordering = ("nombre",)
    list_select_related = ("categoria", "especie")
    list_editable = ("precio", "stock", "activo")
    filter_horizontal = ("etiquetas",)
    readonly_fields = ("creado", "actualizado")


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("producto", "usuario", "texto", "fecha")
    list_filter = ("fecha",)
    search_fields = ("texto", "usuario__username", "producto__nombre")
    ordering = ("-fecha",)
    list_select_related = ("producto", "usuario")