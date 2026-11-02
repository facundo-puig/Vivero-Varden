from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    localidad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username