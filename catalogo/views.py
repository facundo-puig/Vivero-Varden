from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import (
    Categoria,
    Comentario,
    Especie,
    Etiqueta,
    Familia,
    GuiaCuidado,
    Proveedor,
)
from .permissions import EsAutorOSoloLectura, EsStaffOSoloLectura
from .serializers import (
    CategoriaSerializer,
    ComentarioSerializer,
    EspecieListSerializer,
    EspecieSerializer,
    EtiquetaSerializer,
    FamiliaSerializer,
    GuiaCuidadoSerializer,
    ProveedorSerializer,
)


class FamiliaViewSet(viewsets.ModelViewSet):
    queryset = Familia.objects.all()
    serializer_class = FamiliaSerializer
    permission_classes = [EsStaffOSoloLectura]


class EspecieViewSet(viewsets.ModelViewSet):
    queryset = Especie.objects.select_related("familia", "guia")
    permission_classes = [EsStaffOSoloLectura]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["familia"]
    search_fields = ["nombre_comun", "nombre_cientifico"]

    def get_serializer_class(self):
        if self.action == "list":
            return EspecieListSerializer
        return EspecieSerializer

    @action(detail=True, methods=["get"])
    def cuidados(self, request, pk=None):
        especie = self.get_object()
        try:
            guia = especie.guia
        except GuiaCuidado.DoesNotExist:
            return Response(
                {"detail": "Esta especie todavía no tiene guía de cuidado."},
                status=404,
            )
        return Response(GuiaCuidadoSerializer(guia).data)


class GuiaCuidadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GuiaCuidado.objects.select_related("especie")
    serializer_class = GuiaCuidadoSerializer
    permission_classes = [EsStaffOSoloLectura]


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [EsStaffOSoloLectura]


class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    permission_classes = [EsStaffOSoloLectura]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["grupo"]


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAdminUser]


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.select_related("usuario")
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, EsAutorOSoloLectura]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["producto"]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)