from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Pedido(models.Model):
    ESTADOS = [
        ("pagado", "Pagado"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]
    TIPOS_ENTREGA = [
        ("retiro", "Retiro en el vivero"),
        ("envio", "Envío a domicilio"),
    ]
    METODOS_PAGO = [
        ("efectivo", "Efectivo"),
        ("transferencia", "Transferencia"),
        ("tarjeta", "Tarjeta"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pedidos"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pagado")
    tipo_entrega = models.CharField(max_length=10, choices=TIPOS_ENTREGA)
    direccion_envio = models.CharField(max_length=200, blank=True)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="detalles"
    )
    producto = models.ForeignKey(
        "catalogo.Producto", on_delete=models.PROTECT, related_name="detalles"
    )
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "detalle de pedido"
        verbose_name_plural = "detalles de pedido"
        unique_together = ["pedido", "producto"]

    def __str__(self):
        return f"{self.cantidad} x {self.producto}"