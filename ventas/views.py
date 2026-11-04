from django.db import transaction
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from catalogo.models import Producto

from .models import Pedido
from .serializers import PedidoCrearSerializer, PedidoSerializer


class PedidoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["estado", "tipo_entrega", "metodo_pago", "usuario"]
    ordering_fields = ["fecha", "total"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Pedido.objects.none()
        queryset = (
            Pedido.objects.select_related("usuario")
            .prefetch_related("detalles__producto")
            .order_by("-fecha")
        )
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(usuario=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return PedidoCrearSerializer
        return PedidoSerializer

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        pedido = self.get_object()  # devuelve 404 si el pedido es de otro usuario

        with transaction.atomic():
            pedido = Pedido.objects.select_for_update().get(pk=pedido.pk)
            if pedido.estado != "pagado":
                return Response(
                    {"detail": "Solo se pueden cancelar pedidos en estado 'pagado'."},
                    status=400,
                )
            for detalle in pedido.detalles.all():
                Producto.objects.filter(pk=detalle.producto_id).update(
                    stock=F("stock") + detalle.cantidad
                )
            pedido.estado = "cancelado"
            pedido.save(update_fields=["estado", "actualizado"])

        serializer = PedidoSerializer(self.get_object(), context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def cambiar_estado(self, request, pk=None):
        pedido = self.get_object()
        nuevo = request.data.get("estado")
        permitidos = {"pagado": ["enviado"], "enviado": ["entregado"]}

        if nuevo not in permitidos.get(pedido.estado, []):
            return Response(
                {
                    "detail": f"No se puede pasar de '{pedido.estado}' a '{nuevo}'. "
                    "Los cambios válidos son pagado → enviado y enviado → entregado."
                },
                status=400,
            )

        pedido.estado = nuevo
        pedido.save(update_fields=["estado", "actualizado"])
        serializer = PedidoSerializer(pedido, context=self.get_serializer_context())
        return Response(serializer.data)