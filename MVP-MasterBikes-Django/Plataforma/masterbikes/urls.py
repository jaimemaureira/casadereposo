# masterbikes/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('buscar/', views.buscar_bicicleta, name='buscar_bicicleta'),

    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:bicicleta_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/realizar/', views.realizar_compra, name='realizar_compra'),  # Nueva URL para realizar la compra
    
    path('bicicletas/', views.bicicletas, name='bicicletas'),
    path('bicicletas/detalle/<int:pk>/', views.bicicleta_detalle, name='bicicleta_detalle'),
    path('reservas/detalle/<int:pk>/', views.bicicleta_detalle_reservas, name='bicicleta_detalle_reservas'),
    path('compras/detalle/<int:pk>/', views.bicicleta_detalle_compras, name='bicicleta_detalle_compras'),

    path('reservas/', views.reservas, name='reservas'),
    path('reservas/nueva/', views.reserva_create, name='reserva_create'),
    path('reservas/cancelar/<int:pk>/', views.reserva_cancel, name='reserva_cancel'),

    path('reparaciones/', views.reparaciones, name='reparaciones'),
    path('reparaciones/nueva/', views.reparacion_create, name='reparacion_create'),
    path('reparaciones/cancelar/<int:pk>/', views.reparacion_cancel, name='reparacion_cancel'),

    path('seguimiento/', views.seguimiento, name='seguimiento'),
    path('verificacion_entrega/', views.verificacion_entrega, name='verificacion_entrega'),
    path('verificacion_entrega/marcar/<int:pk>/', views.marcar_entregada, name='marcar_entregada'),

    path('detalles_compras/', views.detalles_compras, name='detalles_compras'),
    path('historial/', views.historial, name='historial'),

    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/nuevo/', views.feedback_create, name='feedback_create'),

    path('administracion/', views.administracion, name='administracion'),
    path('crud/', views.crud, name='crud'),

    path('crud/editar_bicicleta/<int:pk>/', views.editar_bicicleta, name='editar_bicicleta'),
    path('crud/eliminar_bicicleta/<int:pk>/', views.eliminar_bicicleta, name='eliminar_bicicleta'),

    path('crud/cambiar_estado_reserva/<int:pk>/', views.cambiar_estado_reserva, name='cambiar_estado_reserva'),
    path('crud/eliminar_reserva/<int:pk>/', views.eliminar_reserva, name='eliminar_reserva'),

    path('crud/eliminar_compra/<int:pk>/', views.eliminar_compra, name='eliminar_compra'),

    path('crud/eliminar_reparacion/<int:pk>/', views.eliminar_reparacion, name='eliminar_reparacion'),

    path('crud/marcar_seguimiento/<int:pk>/', views.marcar_seguimiento, name='marcar_seguimiento'),

    path('crud/eliminar_feedback/<int:pk>/', views.eliminar_feedback, name='eliminar_feedback'),

    path('crud/editar_usuario/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('crud/eliminar_usuario/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
