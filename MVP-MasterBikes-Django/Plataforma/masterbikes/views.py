# masterbikes/views.py
from django.contrib import messages
from django.utils import timezone  
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime, timedelta
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Bicicleta, Reserva, Reparacion, Feedback, Carrito, ItemCarrito, Compra
from .forms import ReservaForm, ReparacionForm, FeedbackForm, BicicletaForm

def index(request):
    bicicletas = Bicicleta.objects.all()
    return render(request, 'masterbikes/index.html', {'bicicletas': bicicletas})

@login_required
def carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    total = sum(item.subtotal() for item in carrito.items.all())
    return render(request, 'masterbikes/Vistas/carrito.html', {'carrito': carrito, 'total': total})

@login_required
def agregar_al_carrito(request, bicicleta_id):
    bicicleta = get_object_or_404(Bicicleta, id=bicicleta_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, bicicleta=bicicleta)
    if not created:
        item.cantidad += 1
        item.save()
    messages.success(request, 'Bicicleta agregada al carrito.')
    return redirect('carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    if item.carrito.usuario == request.user:
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
            messages.success(request, 'Cantidad reducida en el carrito.')
        else:
            item.delete()
            messages.success(request, 'Bicicleta eliminada del carrito.')
    else:
        messages.error(request, 'No tienes permiso para eliminar este ítem.')
    return redirect('carrito')

@login_required
def realizar_compra(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    if not carrito.items.exists():
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('carrito')

    for item in carrito.items.all():
        Compra.objects.create(
            usuario=request.user,
            bicicleta=item.bicicleta,
            precio=item.bicicleta.precio,
            fecha_compra=timezone.now()
        )
        item.delete()  

    messages.success(request, 'Compra realizada exitosamente.')
    return redirect('historial')

def bicicletas(request):
    bicicletas = Bicicleta.objects.all()
    return render(request, 'masterbikes/Vistas/bicicletas.html', {'bicicletas': bicicletas})

@login_required
def bicicleta_detalle_reservas(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    return render(request, 'masterbikes/Crud/bicicleta_detalle_reservas.html', {'reserva': reserva})

@login_required
def bicicleta_detalle_compras(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    return render(request, 'masterbikes/Crud/bicicleta_detalle_compra.html', {'compra': compra})

def bicicleta_detalle(request, pk):
    bicicleta = get_object_or_404(Bicicleta, pk=pk)
    return render(request, 'masterbikes/Crud/bicicleta_detalle.html', {'bicicleta': bicicleta})

@login_required
def reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'masterbikes/Vistas/reservas.html', {'reservas': reservas})

@login_required
def reserva_create(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            return redirect('reservas')
    else:
        form = ReservaForm()
    return render(request, 'masterbikes/Crud/reserva_form.html', {'form': form})

@login_required
def reserva_cancel(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if reserva.usuario == request.user:
        reserva.delete()
        messages.success(request, 'Reserva cancelada exitosamente.')
    else:
        messages.error(request, 'No tienes permiso para cancelar esta reserva.')
    return redirect('reservas')

@login_required
def reparaciones(request):
    reparaciones = Reparacion.objects.filter(usuario=request.user)
    return render(request, 'masterbikes/Vistas/reparaciones.html', {'reparaciones': reparaciones})

@login_required
def reparacion_create(request):
    if request.method == 'POST':
        form = ReparacionForm(request.POST)
        if form.is_valid():
            reparacion = form.save(commit=False)
            reparacion.usuario = request.user
            reparacion.save()
            return redirect('reparaciones')
    else:
        form = ReparacionForm()
    return render(request, 'masterbikes/Crud/reparacion_form.html', {'form': form})

@login_required
def reparacion_cancel(request, pk):
    reparacion = get_object_or_404(Reparacion, pk=pk)
    if reparacion.usuario == request.user and not reparacion.fecha_completada:
        reparacion.delete()
        messages.success(request, 'Reparación cancelada exitosamente.')
    else:
        messages.error(request, 'No tienes permiso para cancelar esta reparación o ya está completada.')
    return redirect('reparaciones')

@login_required
def seguimiento(request):
    reparaciones = Reparacion.objects.filter(usuario=request.user)
    return render(request, 'masterbikes/Vistas/seguimiento.html', {'reparaciones': reparaciones})

@login_required
def verificacion_entrega(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'masterbikes/Vistas/verificacion_entrega.html', {'reservas': reservas})

@user_passes_test(lambda u: u.is_staff)
def marcar_entregada(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.entregada = True
    reserva.estado = "Entregada"
    reserva.save()
    messages.success(request, 'Reserva marcada como entregada.')
    return redirect('verificacion_entrega')

def detalles_compras(request):
    return render(request, 'masterbikes/Vistas/detalles_compras.html')

@login_required
def historial(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    compras = Compra.objects.filter(usuario=request.user) 
    return render(request, 'masterbikes/Vistas/historial.html', {'reservas': reservas, 'compras': compras})

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'masterbikes/Crud/feedback_list.html', {'feedbacks': feedbacks})


def feedback(request):
    context={}
    return render(request, 'masterbikes/Vistas/feedback.html', context)

@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.usuario = request.user
            feedback.save()
            messages.success(request, 'Feedback enviado exitosamente.')
            return redirect('feedback_list')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] = 'is-invalid'
    else:
        form = FeedbackForm()
    calificaciones = range(1, 6)  # Rango de calificaciones de 1 a 5
    return render(request, 'masterbikes/Crud/feedback_form.html', {'form': form, 'calificaciones': calificaciones})

# Cuentas
def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not User.objects.filter(username=nombre).exists():
            user = User.objects.create_user(username=nombre, email=email, password=password)
            user.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('index')  # Redirige a la página de inicio o a donde prefieras
        else:
            messages.error(request, 'El nombre de usuario ya está en uso.')
    return render(request, 'masterbikes/index.html')


@staff_member_required
def administracion(request):
    bicicletas = Bicicleta.objects.all()
    usuarios = User.objects.all()
    reservas = Reserva.objects.all()
    reparaciones = Reparacion.objects.all()
    feedbacks = Feedback.objects.all()
    return render(request, 'masterbikes/Crud/administracion.html', {
        'bicicletas': bicicletas,
        'usuarios': usuarios,
        'reservas': reservas,
        'reparaciones': reparaciones,
        'feedbacks': feedbacks
    })

@staff_member_required
def crud(request):
    reservas = Reserva.objects.all()
    compras = Compra.objects.all()
    reparaciones = Reparacion.objects.all()
    feedbacks = Feedback.objects.all()
    bicicletas = Bicicleta.objects.all()
    return render(request, 'masterbikes/Crud/crud.html', {
        'reservas': reservas,
        'compras': compras,
        'reparaciones': reparaciones,
        'feedbacks': feedbacks,
        'bicicletas': bicicletas,
    })

@staff_member_required
def cambiar_estado_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        estado = request.POST.get('estado')
        reserva.estado = estado
        reserva.save()
        messages.success(request, 'Estado de la reserva actualizado.')
        return redirect('crud')
    return render(request, 'masterbikes/Crud/cambiar_estado_reserva.html', {'reserva': reserva})

@staff_member_required
def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.delete()
    messages.success(request, 'Reserva eliminada.')
    return redirect('crud')

@staff_member_required
def eliminar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    compra.delete()
    messages.success(request, 'Compra eliminada.')
    return redirect('crud')

@staff_member_required
def eliminar_reparacion(request, pk):
    reparacion = get_object_or_404(Reparacion, pk=pk)
    reparacion.delete()
    messages.success(request, 'Reparación eliminada.')
    return redirect('crud')

@staff_member_required
def marcar_seguimiento(request, pk):
    reparacion = get_object_or_404(Reparacion, pk=pk)
    if request.method == 'POST':
        estado = request.POST.get('estado')
        reparacion.estado = estado
        reparacion.save()
        messages.success(request, 'Estado de la reparación actualizado.')
        return redirect('crud')
    return render(request, 'masterbikes/Crud/marcar_seguimiento.html', {'reparacion': reparacion})

@staff_member_required
def eliminar_feedback(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.delete()
    messages.success(request, 'Feedback eliminado.')
    return redirect('crud')

@staff_member_required
def editar_bicicleta(request, pk):
    bicicleta = get_object_or_404(Bicicleta, pk=pk)
    if request.method == 'POST':
        form = BicicletaForm(request.POST, request.FILES, instance=bicicleta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bicicleta actualizada exitosamente.')
            return redirect('administracion')
    else:
        form = BicicletaForm(instance=bicicleta)
    return render(request, 'masterbikes/Crud/editar_bicicleta.html', {'form': form, 'bicicleta': bicicleta})

@staff_member_required
def eliminar_bicicleta(request, pk):
    bicicleta = get_object_or_404(Bicicleta, pk=pk)
    if request.method == 'POST':
        bicicleta.delete()
        messages.success(request, 'Bicicleta eliminada exitosamente.')
        return redirect('administracion')
    return render(request, 'masterbikes/Crud/eliminar_bicicleta.html', {'bicicleta': bicicleta})

@staff_member_required
def editar_usuario(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('administracion')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'masterbikes/Crud/editar_usuario.html', {'form': form, 'user': user})

@staff_member_required
def eliminar_usuario(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('administracion')
    return render(request, 'masterbikes/Crud/eliminar_usuario.html', {'user': user})


def buscar_bicicleta(request):
    query = request.GET.get('query')
    resultados = []
    if query:
        resultados = Bicicleta.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    return render(request, 'masterbikes/Vistas/resultados_busqueda.html', {'resultados': resultados, 'query': query})