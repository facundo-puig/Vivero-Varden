from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q


class Familia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "familia"
        verbose_name_plural = "familias"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Especie(models.Model):
    PROPAGACION = [
        ("semilla", "Semilla"),
        ("esqueje", "Esqueje"),
        ("gajo", "Gajo"),
        ("division", "División"),
    ]

    nombre_comun = models.CharField(max_length=150)
    nombre_cientifico = models.CharField(max_length=150, unique=True)
    origen = models.CharField(max_length=150, blank=True)
    tipo_propagacion = models.CharField(
        max_length=20, choices=PROPAGACION, blank=True
    )
    descripcion = models.TextField(blank=True)
    familia = models.ForeignKey(
        Familia, on_delete=models.PROTECT, related_name="especies"
    )

    class Meta:
        verbose_name = "especie"
        verbose_name_plural = "especies"
        ordering = ["nombre_comun"]

    def __str__(self):
        return f"{self.nombre_comun} ({self.nombre_cientifico})"


class GuiaCuidado(models.Model):
    LUZ = [
        ("poca_luz", "Poca luz"),
        ("sombra", "Sombra"),
        ("media_sombra", "Media sombra"),
        ("pleno_sol", "Pleno sol"),
    ]

    especie = models.OneToOneField(
        Especie, on_delete=models.CASCADE, related_name="guia"
    )
    riego = models.CharField(max_length=150, blank=True)
    luz = models.CharField(max_length=20, choices=LUZ, blank=True)
    temperatura_min = models.IntegerField(null=True, blank=True)
    temperatura_max = models.IntegerField(null=True, blank=True)
    sustrato = models.TextField(blank=True)
    toxica_mascotas = models.BooleanField(default=False)

    class Meta:
        verbose_name = "guía de cuidado"
        verbose_name_plural = "guías de cuidado"
        constraints = [
            models.CheckConstraint(
                condition=Q(temperatura_min__lte=F("temperatura_max")),
                name="guia_temperatura_min_menor_o_igual_max",
            )
        ]

    def __str__(self):
        return f"Guía de {self.especie.nombre_comun}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    GRUPOS = [
        ("ubicacion", "Ubicación"),
        ("clima", "Clima"),
        ("tipo_planta", "Tipo de planta"),
        ("uso", "Uso"),
    ]

    nombre = models.CharField(max_length=100)
    grupo = models.CharField(max_length=20, choices=GRUPOS)

    class Meta:
        verbose_name = "etiqueta"
        verbose_name_plural = "etiquetas"
        ordering = ["grupo", "nombre"]
        unique_together = ["nombre", "grupo"]

    def __str__(self):
        return f"{self.nombre} ({self.get_grupo_display()})"


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    cuit = models.CharField(max_length=13, unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    TAMANOS = [
        ("chica", "Chica"),
        ("mediana", "Mediana"),
        ("grande", "Grande"),
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    stock = models.PositiveIntegerField(default=0)
    tamano = models.CharField(max_length=10, choices=TAMANOS, blank=True)
    imagen = models.URLField(blank=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="productos"
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.PROTECT, related_name="productos"
    )
    especie = models.ForeignKey(
        Especie,
        on_delete=models.PROTECT,
        related_name="productos",
        null=True,
        blank=True,
    )
    etiquetas = models.ManyToManyField(
        Etiqueta, related_name="productos", blank=True
    )

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Comentario(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="comentarios"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios"
    )
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.usuario} en {self.producto}"