from django.contrib import admin

from .models import DetallePedido, Pedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    raw_id_fields = ("producto",)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "fecha", "estado", "tipo_entrega", "metodo_pago", "total")
    list_filter = ("estado", "tipo_entrega", "metodo_pago", "fecha")
    search_fields = ("usuario__username", "usuario__email")
    ordering = ("-fecha",)
    date_hierarchy = "fecha"
    list_select_related = ("usuario",)
    readonly_fields = ("fecha", "actualizado")
    inlines = [DetallePedidoInline]