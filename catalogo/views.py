from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comentario
from .permissions import EsAutorOSoloLectura
from .serializers import ComentarioSerializer


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.select_related("usuario")
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, EsAutorOSoloLectura]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["producto"]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)