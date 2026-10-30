from rest_framework import serializers

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


class FamiliaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Familia
        fields = "__all__"


class GuiaCuidadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuiaCuidado
        fields = "__all__"


class EspecieSerializer(serializers.ModelSerializer):
    """Para detalle, crear y editar: la familia va como id."""

    class Meta:
        model = Especie
        fields = "__all__"


class EspecieListSerializer(serializers.ModelSerializer):
    """Solo para el listado: familia y guía vienen anidadas."""

    familia = FamiliaSerializer(read_only=True)
    guia = GuiaCuidadoSerializer(read_only=True)

    class Meta:
        model = Especie
        fields = [
            "id",
            "nombre_comun",
            "nombre_cientifico",
            "origen",
            "tipo_propagacion",
            "descripcion",
            "familia",
            "guia",
        ]


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = "__all__"


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = "__all__"

class ComentarioSerializer(serializers.ModelSerializer):
    autor = serializers.CharField(source="usuario.username", read_only=True)
    texto = serializers.CharField(max_length=1000)

    class Meta:
        model = Comentario
        fields = ["id", "producto", "autor", "texto", "fecha"]
        read_only_fields = ["id", "fecha"]

    def update(self, instance, validated_data):
        # el comentario no se puede mover a otro producto
        validated_data.pop("producto", None)
        return super().update(instance, validated_data)

class ProductoListSerializer(serializers.ModelSerializer):
    """Listado: categoría, proveedor y etiquetas vienen anidados."""

    categoria = CategoriaSerializer(read_only=True)
    proveedor = ProveedorSerializer(read_only=True)
    etiquetas = EtiquetaSerializer(many=True, read_only=True)  # many=True: muchos a muchos

    class Meta:
        model = Producto
        fields = [
            "id",
            "nombre",
            "descripcion",
            "precio",
            "stock",
            "tamano",
            "imagen",
            "categoria",
            "proveedor",
            "especie",
            "etiquetas",
        ]


class ProductoSerializer(serializers.ModelSerializer):
    """Detalle, crear y editar: las relaciones van como ids."""

    class Meta:
        model = Producto
        fields = "__all__"