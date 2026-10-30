from rest_framework.routers import DefaultRouter

from catalogo.views import (
    CategoriaViewSet,
    ComentarioViewSet,
    EspecieViewSet,
    EtiquetaViewSet,
    FamiliaViewSet,
    GuiaCuidadoViewSet,
    ProveedorViewSet,
    ProductoViewSet,
)

router = DefaultRouter()

router.register("familias", FamiliaViewSet, basename="familias_vs")
router.register("especies", EspecieViewSet, basename="especies_vs")
router.register("guias-cuidado", GuiaCuidadoViewSet, basename="guias_cuidado_vs")
router.register("categorias", CategoriaViewSet, basename="categorias_vs")
router.register("etiquetas", EtiquetaViewSet, basename="etiquetas_vs")
router.register("proveedores", ProveedorViewSet, basename="proveedores_vs")
router.register("comentarios", ComentarioViewSet, basename="comentarios_vs")
router.register("productos", ProductoViewSet, basename="productos_vs")