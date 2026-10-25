from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

Usuario = get_user_model()


class RegistroSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Usuario.objects.all(),
                lookup="iexact",
                message="Ya existe un usuario con ese email.",
            )
        ]
    )
    password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "telefono",
            "direccion",
            "localidad",
        ]

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)


class PerfilSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Usuario.objects.all(),
                lookup="iexact",
                message="Ya existe un usuario con ese email.",
            )
        ]
    )

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "telefono",
            "direccion",
            "localidad",
        ]
        read_only_fields = ["id", "username"]