from django.db import models

from apps.adopcion.models import Persona


class Vacuna(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class  Mascota(models.Model):
    nombre = models.CharField(max_length=50)
    sexo = models.CharField(max_length=10)
    edad = models.IntegerField()
    fecha_rescate = models.DateField()
    imagen = models.ImageField(upload_to='mascotas', null=False, blank=False)

    persona = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)

    vacuna = models.ManyToManyField(Vacuna, blank=True)

# Create your models here.
