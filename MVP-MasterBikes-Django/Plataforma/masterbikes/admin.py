# masterbikes/admin.py

from django.contrib import admin
from .models import Bicicleta, Reserva, Reparacion, Feedback, Carrito, ItemCarrito, Compra

admin.site.register(Bicicleta)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Reserva)
admin.site.register(Reparacion)
admin.site.register(Feedback)
admin.site.register(Compra)
