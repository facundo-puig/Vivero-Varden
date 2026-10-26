from rest_framework.routers import DefaultRouter

from catalogo.views import ComentarioViewSet

router = DefaultRouter()

router.register("comentarios", ComentarioViewSet, basename="comentarios_vs")