from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from catalogo.models import (
    Categoria,
    Especie,
    Etiqueta,
    Familia,
    GuiaCuidado,
    Producto,
    Proveedor,
)

CATEGORIAS = [
    ("Plantas", "Plantas de interior y exterior"),
    ("Árboles", "Árboles para jardín y vereda"),
    ("Macetas", "Macetas y maceteros"),
    ("Sustratos", "Tierras y mezclas para cultivo"),
    ("Abonos", "Fertilizantes y enmiendas orgánicas"),
    ("Herramientas", "Herramientas de jardinería"),
]

ETIQUETAS = [
    ("Interior", "ubicacion"),
    ("Exterior", "ubicacion"),
    ("Resistente a sequía", "clima"),
    ("Resistente al viento", "clima"),
    ("Apta para aire acondicionado", "clima"),
    ("Suculenta", "tipo_planta"),
    ("Aromática", "tipo_planta"),
    ("Huerta", "tipo_planta"),
    ("Decorativa", "uso"),
    ("Regalo", "uso"),
    ("Oficina", "uso"),
]

FAMILIAS = [
    ("Aráceas", "Plantas de hojas grandes, muy usadas en interiores"),
    ("Asparagáceas", "Familia que incluye a las sansevierias"),
    ("Crasuláceas", "Suculentas de hojas carnosas"),
    ("Cactáceas", "Cactus y plantas de zonas áridas"),
    ("Lamiáceas", "Hierbas aromáticas"),
    ("Bignoniáceas", "Árboles y arbustos con flores vistosas"),
]

# (nombre común, nombre científico, familia, origen, propagación, descripción,
#  riego, luz, temp. mín., temp. máx., sustrato, tóxica para mascotas)
ESPECIES = [
    ("Monstera", "Monstera deliciosa", "Aráceas", "América Central", "esqueje",
     "Planta de hojas grandes y perforadas.",
     "1 vez por semana", "media_sombra", 18, 27,
     "Mezcla aireada con perlita y fibra de coco", True),
    ("Potus", "Epipremnum aureum", "Aráceas", "Sudeste asiático", "esqueje",
     "Enredadera de hojas acorazonadas, muy resistente.",
     "Cada 7 a 10 días", "poca_luz", 15, 29,
     "Sustrato universal con buen drenaje", True),
    ("Sansevieria", "Dracaena trifasciata", "Asparagáceas", "África occidental", "division",
     "Hojas erguidas y rígidas, casi indestructible.",
     "Cada 15 días", "poca_luz", 13, 29,
     "Sustrato para cactus y suculentas", True),
    ("Echeveria", "Echeveria elegans", "Crasuláceas", "México", "esqueje",
     "Roseta de hojas carnosas de color gris azulado.",
     "Cada 10 a 14 días", "pleno_sol", 10, 30,
     "Sustrato arenoso y muy drenante", False),
    ("Albahaca", "Ocimum basilicum", "Lamiáceas", "India", "semilla",
     "Hierba aromática de uso culinario.",
     "Cada 2 días", "pleno_sol", 15, 30,
     "Sustrato rico en materia orgánica", False),
    ("Cactus de Navidad", "Schlumbergera truncata", "Cactáceas", "Brasil", "esqueje",
     "Cactus de tallos colgantes que florece en invierno.",
     "Cada 7 días", "media_sombra", 12, 25,
     "Sustrato liviano con perlita", False),
    ("Jacarandá", "Jacaranda mimosifolia", "Bignoniáceas", "Argentina y Bolivia", "semilla",
     "Árbol ornamental de flores lilas en primavera.",
     "Semanal el primer año", "pleno_sol", -2, 35,
     "Suelo profundo y bien drenado", False),
]

PROVEEDORES = [
    ("Viveros del Sur", "30-71234567-8", "351-555-0101", "ventas@viverosdelsur.example"),
    ("Cerámicas Córdoba", "30-70987654-3", "351-555-0102", "info@ceramicascordoba.example"),
    ("Agroinsumos del Centro", "30-71122334-5", "351-555-0103", "pedidos@agrocentro.example"),
]

# (nombre, descripción, precio, stock, tamaño, categoría, proveedor,
#  nombre científico de la especie o None, etiquetas, activo)
PRODUCTOS = [
    ("Monstera deliciosa M15", "Monstera en maceta N°15.", "18500.00", 12, "mediana",
     "Plantas", "Viveros del Sur", "Monstera deliciosa",
     ["Interior", "Decorativa", "Apta para aire acondicionado"], True),
    ("Potus colgante M12", "Potus en maceta colgante N°12.", "6800.00", 25, "chica",
     "Plantas", "Viveros del Sur", "Epipremnum aureum",
     ["Interior", "Oficina", "Decorativa"], True),
    ("Sansevieria M14", "Sansevieria en maceta N°14.", "9200.00", 18, "mediana",
     "Plantas", "Viveros del Sur", "Dracaena trifasciata",
     ["Interior", "Oficina", "Resistente a sequía"], True),
    ("Echeveria M8", "Suculenta en maceta N°8, ideal para regalar.", "3500.00", 40, "chica",
     "Plantas", "Viveros del Sur", "Echeveria elegans",
     ["Interior", "Exterior", "Suculenta", "Resistente a sequía", "Regalo"], True),
    ("Albahaca en maceta", "Albahaca lista para cosechar.", "2800.00", 30, "chica",
     "Plantas", "Viveros del Sur", "Ocimum basilicum",
     ["Exterior", "Aromática", "Huerta"], True),
    ("Cactus de Navidad M14", "Florece en invierno.", "7600.00", 3, "mediana",
     "Plantas", "Viveros del Sur", "Schlumbergera truncata",
     ["Interior", "Decorativa", "Regalo"], True),
    ("Jacarandá 1,5 m", "Ejemplar joven para plantar en vereda o jardín.", "42000.00", 6, "grande",
     "Árboles", "Viveros del Sur", "Jacaranda mimosifolia",
     ["Exterior", "Resistente al viento"], True),
    ("Maceta cerámica blanca N°15", "Maceta de cerámica esmaltada.", "6200.00", 30, "mediana",
     "Macetas", "Cerámicas Córdoba", None,
     ["Interior", "Decorativa"], True),
    ("Maceta de barro N°20", "Maceta de barro cocido con plato.", "4800.00", 4, "grande",
     "Macetas", "Cerámicas Córdoba", None,
     ["Exterior"], True),
    ("Sustrato universal 5 L", "Mezcla lista para usar.", "3900.00", 50, "",
     "Sustratos", "Agroinsumos del Centro", None, [], True),
    ("Humus de lombriz 2 kg", "Abono orgánico.", "4200.00", 2, "",
     "Abonos", "Agroinsumos del Centro", None, [], True),
    ("Tijera de podar", "Hoja de acero con mango antideslizante.", "11500.00", 15, "",
     "Herramientas", "Agroinsumos del Centro", None, [], True),
    ("Kit de jardinería (discontinuado)", "Producto dado de baja.", "9900.00", 0, "",
     "Herramientas", "Agroinsumos del Centro", None, [], False),
]


class Command(BaseCommand):
    help = "Carga datos de ejemplo del vivero. Se puede ejecutar más de una vez."

    @transaction.atomic
    def handle(self, *args, **options):
        categorias = {}
        for nombre, descripcion in CATEGORIAS:
            obj, _ = Categoria.objects.get_or_create(
                nombre=nombre, defaults={"descripcion": descripcion}
            )
            categorias[nombre] = obj

        etiquetas = {}
        for nombre, grupo in ETIQUETAS:
            obj, _ = Etiqueta.objects.get_or_create(nombre=nombre, grupo=grupo)
            etiquetas[nombre] = obj

        familias = {}
        for nombre, descripcion in FAMILIAS:
            obj, _ = Familia.objects.get_or_create(
                nombre=nombre, defaults={"descripcion": descripcion}
            )
            familias[nombre] = obj

        especies = {}
        for (comun, cientifico, familia, origen, propagacion, descripcion,
             riego, luz, tmin, tmax, sustrato, toxica) in ESPECIES:
            especie, _ = Especie.objects.get_or_create(
                nombre_cientifico=cientifico,
                defaults={
                    "nombre_comun": comun,
                    "familia": familias[familia],
                    "origen": origen,
                    "tipo_propagacion": propagacion,
                    "descripcion": descripcion,
                },
            )
            GuiaCuidado.objects.get_or_create(
                especie=especie,
                defaults={
                    "riego": riego,
                    "luz": luz,
                    "temperatura_min": tmin,
                    "temperatura_max": tmax,
                    "sustrato": sustrato,
                    "toxica_mascotas": toxica,
                },
            )
            especies[cientifico] = especie

        proveedores = {}
        for nombre, cuit, telefono, email in PROVEEDORES:
            obj, _ = Proveedor.objects.get_or_create(
                cuit=cuit,
                defaults={"nombre": nombre, "telefono": telefono, "email": email},
            )
            proveedores[nombre] = obj

        for (nombre, descripcion, precio, stock, tamano, categoria, proveedor,
             cientifico, etiquetas_producto, activo) in PRODUCTOS:
            producto, _ = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": descripcion,
                    "precio": Decimal(precio),
                    "stock": stock,
                    "tamano": tamano,
                    "categoria": categorias[categoria],
                    "proveedor": proveedores[proveedor],
                    "especie": especies[cientifico] if cientifico else None,
                    "activo": activo,
                },
            )
            producto.etiquetas.set([etiquetas[e] for e in etiquetas_producto])

        self.stdout.write(self.style.SUCCESS("Datos de ejemplo cargados correctamente."))