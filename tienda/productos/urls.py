from django.urls import path
from django.contrib.auth import views as auth_views  # ← Importar las vistas de autenticación
from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.inicio_view, name='inicio'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('carrito/', views.carrito_view, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('eliminar-del-carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('realizar-compra/', views.realizar_compra, name='realizar_compra'),

    
]
