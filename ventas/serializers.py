from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from catalogo.models import Producto

from .models import DetallePedido, Pedido


class ProductoResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["id", "nombre", "imagen"]


class DetallePedidoSerializer(serializers.ModelSerializer):
    producto = ProductoResumenSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = DetallePedido
        fields = ["id", "producto", "cantidad", "precio_unitario", "subtotal"]

    def get_subtotal(self, obj):
        return obj.cantidad * obj.precio_unitario


class PedidoSerializer(serializers.ModelSerializer):
    """Lectura: lista y detalle, con los renglones anidados."""

    usuario = serializers.CharField(source="usuario.username", read_only=True)
    detalles = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            "id",
            "usuario",
            "fecha",
            "estado",
            "tipo_entrega",
            "direccion_envio",
            "metodo_pago",
            "total",
            "detalles",
        ]


class DetalleCrearSerializer(serializers.Serializer):
    producto = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.filter(activo=True)
    )
    cantidad = serializers.IntegerField(min_value=1)


class PedidoCrearSerializer(serializers.ModelSerializer):
    """Escritura: el cliente manda productos y cantidades, el servidor calcula el resto."""

    detalles = DetalleCrearSerializer(many=True, allow_empty=False)

    class Meta:
        model = Pedido
        fields = ["tipo_entrega", "direccion_envio", "metodo_pago", "detalles"]

    def validate_detalles(self, detalles):
        ids = [d["producto"].id for d in detalles]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError(
                "Hay productos repetidos. Sumá las cantidades en un solo renglón."
            )
        return detalles

    def validate(self, data):
        if data["tipo_entrega"] == "envio":
            if not data.get("direccion_envio"):
                direccion = self.context["request"].user.direccion
                if not direccion:
                    raise serializers.ValidationError(
                        {"direccion_envio": "Indicá una dirección para el envío."}
                    )
                data["direccion_envio"] = direccion
        else:
            data["direccion_envio"] = ""
        return data

    def create(self, validated_data):
        detalles_data = validated_data.pop("detalles")
        usuario = self.context["request"].user

        with transaction.atomic():
            # Se bloquean los productos para que dos compras simultáneas no pisen el stock
            ids = [d["producto"].id for d in detalles_data]
            productos = {
                p.id: p
                for p in Producto.objects.select_for_update()
                .filter(id__in=ids)
                .order_by("id")
            }

            pedido = Pedido.objects.create(usuario=usuario, total=0, **validated_data)
            total = Decimal("0")

            for item in detalles_data:
                producto = productos[item["producto"].id]
                cantidad = item["cantidad"]

                if producto.stock < cantidad:
                    raise serializers.ValidationError(
                        {
                            "detalles": f"Stock insuficiente de {producto.nombre} "
                            f"(disponible: {producto.stock})."
                        }
                    )

                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio,
                )
                producto.stock -= cantidad
                producto.save(update_fields=["stock", "actualizado"])
                total += producto.precio * cantidad

            pedido.total = total
            pedido.save(update_fields=["total", "actualizado"])

        return pedido

    def to_representation(self, instance):
        return PedidoSerializer(instance, context=self.context).data