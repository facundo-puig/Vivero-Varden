from rest_framework import serializers

from .models import Comentario


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