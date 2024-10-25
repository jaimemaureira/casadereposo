# masterbikes/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Bicicleta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=3)
    imagen = models.ImageField(upload_to='bicicletas/')

    def __str__(self):
        return self.nombre
    
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.bicicleta.nombre}"

    def subtotal(self):
        return self.cantidad * self.bicicleta.precio

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField()
    entregada = models.BooleanField(default=False)
    estado = models.CharField(max_length=50, default='En camino')

    def __str__(self):
        return f"{self.usuario.username} - {self.bicicleta.nombre}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.fecha_solicitud = timezone.now()
            self.fecha_entrega = self.fecha_solicitud + timedelta(days=7)
        super(Reserva, self).save(*args, **kwargs)

class Reparacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_completada = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.bicicleta.nombre}"

class Feedback(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.calificacion}"

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"{self.usuario.username} - {self.bicicleta.nombre}"