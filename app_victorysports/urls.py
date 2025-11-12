# app_victorysports/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Rutas Comunes
    path('', views.inicio_victorysports, name='inicio_victorysports'),
    
    # 1. Rutas CRUD Proveedor
    path('proveedores/', views.ver_proveedor, name='ver_proveedor'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/actualizar/<int:pk>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores/realizar_actualizacion/', views.realizar_actualizacion_proveedor, name='realizar_actualizacion_proveedor'),
    path('proveedores/borrar/<int:pk>/', views.borrar_proveedor, name='borrar_proveedor'),

    # 2. Rutas CRUD Producto
    path('productos/', views.ver_producto, name='ver_producto'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/actualizar/<int:pk>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/realizar_actualizacion/', views.realizar_actualizacion_producto, name='realizar_actualizacion_producto'),
    path('productos/borrar/<int:pk>/', views.borrar_producto, name='borrar_producto'),
    
    # 3. Rutas CRUD ProductoProveedor (Conexión)
    path('conexiones/', views.ver_conexion, name='ver_conexion'),
    path('conexiones/agregar/', views.agregar_conexion, name='agregar_conexion'),
    path('conexiones/actualizar/<int:pk>/', views.actualizar_conexion, name='actualizar_conexion'),
    path('conexiones/realizar_actualizacion/', views.realizar_actualizacion_conexion, name='realizar_actualizacion_conexion'),
    path('conexiones/borrar/<int:pk>/', views.borrar_conexion, name='borrar_conexion'),

    # 4. Rutas CRUD Categoría
    path('categorias/', views.ver_categoria, name='ver_categoria'),
    path('categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categorias/actualizar/<int:pk>/', views.actualizar_categoria, name='actualizar_categoria'),
    path('categorias/realizar_actualizacion/', views.realizar_actualizacion_categoria, name='realizar_actualizacion_categoria'),
    path('categorias/borrar/<int:pk>/', views.borrar_categoria, name='borrar_categoria'),
    
    # 5. Rutas CRUD Rol
    path('roles/', views.ver_rol, name='ver_rol'),
    path('roles/agregar/', views.agregar_rol, name='agregar_rol'),
    path('roles/actualizar/<int:pk>/', views.actualizar_rol, name='actualizar_rol'),
    path('roles/realizar_actualizacion/', views.realizar_actualizacion_rol, name='realizar_actualizacion_rol'),
    path('roles/borrar/<int:pk>/', views.borrar_rol, name='borrar_rol'),
    
    # 6. Rutas CRUD Cliente
    path('clientes/', views.ver_cliente, name='ver_cliente'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/actualizar/<int:pk>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/realizar_actualizacion/', views.realizar_actualizacion_cliente, name='realizar_actualizacion_cliente'),
    path('clientes/borrar/<int:pk>/', views.borrar_cliente, name='borrar_cliente'),
    
    # 7. Rutas CRUD Dirección
    path('direcciones/', views.ver_direccion, name='ver_direccion'),
    path('direcciones/agregar/', views.agregar_direccion, name='agregar_direccion'),
    path('direcciones/actualizar/<int:pk>/', views.actualizar_direccion, name='actualizar_direccion'),
    path('direcciones/realizar_actualizacion/', views.realizar_actualizacion_direccion, name='realizar_actualizacion_direccion'),
    path('direcciones/borrar/<int:pk>/', views.borrar_direccion, name='borrar_direccion'),
    
    # 8. Rutas CRUD Pedido
    path('pedidos/', views.ver_pedido, name='ver_pedido'),
    path('pedidos/agregar/', views.agregar_pedido, name='agregar_pedido'),
    path('pedidos/actualizar/<int:pk>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('pedidos/realizar_actualizacion/', views.realizar_actualizacion_pedido, name='realizar_actualizacion_pedido'),
    path('pedidos/borrar/<int:pk>/', views.borrar_pedido, name='borrar_pedido'),
    
    # 9. Rutas CRUD Envío
    path('envios/', views.ver_envio, name='ver_envio'),
    path('envios/agregar/', views.agregar_envio, name='agregar_envio'),
    path('envios/actualizar/<int:pk>/', views.actualizar_envio, name='actualizar_envio'),
    path('envios/realizar_actualizacion/', views.realizar_actualizacion_envio, name='realizar_actualizacion_envio'),
    path('envios/borrar/<int:pk>/', views.borrar_envio, name='borrar_envio'),

    # 10. Rutas READ DetallePedido
    path('detalles/', views.ver_detallepedido, name='ver_detallepedido'),
]