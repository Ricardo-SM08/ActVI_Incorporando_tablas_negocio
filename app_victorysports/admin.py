# app_victorysports/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import IntegrityError, transaction
from decimal import Decimal

# Importar TODOS los modelos
from .models import (
    Proveedor, Producto, ProductoProveedor, Categoria, Rol,
    Cliente, Direccion, Pedido, DetallePedido, Envio 
)

# Constantes de Pedido y Envío (Para usar en select/combobox)
ESTADOS_PEDIDO = ['Pendiente', 'Procesando', 'Enviado', 'Completado', 'Cancelado']
ESTADOS_ENVIO = ['Preparando', 'En Tránsito', 'Entregado', 'Problema']


# Vista de Inicio
def inicio_victorysports(request):
    return render(request, 'inicio.html') 

# ===================================
# 1. Funciones CRUD Proveedor
# ===================================
def agregar_proveedor(request):
    if request.method == 'POST':
        try:
            Proveedor.objects.create(
                nombre_empresa=request.POST.get('nombre_empresa'),
                telefono_empresa=request.POST.get('telefono_empresa'),
                email_empresa=request.POST.get('email_empresa'),
                pais_origen=request.POST.get('pais_origen'),
                contacto_principal=request.POST.get('contacto_principal'),
                direccion=request.POST.get('direccion')
            )
            return redirect(reverse('ver_proveedor'))
        except IntegrityError:
            context = {'error_message': 'Ya existe un proveedor con ese nombre de empresa.'}
            return render(request, 'proveedor/agregar_proveedor.html', context)
        except Exception as e:
            context = {'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'proveedor/agregar_proveedor.html', context)
    return render(request, 'proveedor/agregar_proveedor.html')

def ver_proveedor(request):
    proveedores = Proveedor.objects.all().order_by('nombre_empresa')
    context = {'proveedores': proveedores}
    return render(request, 'proveedor/ver_proveedor.html', context)

def actualizar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    context = {'proveedor': proveedor}
    return render(request, 'proveedor/actualizar_proveedor.html', context)

def realizar_actualizacion_proveedor(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('id_proveedor')
        proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
        try:
            proveedor.nombre_empresa = request.POST.get('nombre_empresa')
            proveedor.telefono_empresa = request.POST.get('telefono_empresa')
            proveedor.email_empresa = request.POST.get('email_empresa')
            proveedor.pais_origen = request.POST.get('pais_origen')
            proveedor.contacto_principal = request.POST.get('contacto_principal')
            proveedor.direccion = request.POST.get('direccion')
            proveedor.save()
            return redirect(reverse('ver_proveedor'))
        except IntegrityError:
            context = {'proveedor': proveedor, 'error_message': 'Ya existe un proveedor con ese nombre de empresa.'}
            return render(request, 'proveedor/actualizar_proveedor.html', context)
        except Exception as e:
            context = {'proveedor': proveedor, 'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'proveedor/actualizar_proveedor.html', context)
    return redirect(reverse('ver_proveedor'))

def borrar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect(reverse('ver_proveedor'))
    context = {'proveedor': proveedor}
    return render(request, 'proveedor/borrar_proveedor.html', context)


# ===================================
# 2. Funciones CRUD Producto
# ===================================
def agregar_producto(request):
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    
    if request.method == 'POST':
        try:
            categoria_id = request.POST.get('categoria_id')
            categoria_obj = get_object_or_404(Categoria, pk=categoria_id)

            Producto.objects.create(
                nombre=request.POST.get('nombre'),
                precio_unitario=request.POST.get('precio_unitario'),
                stock=request.POST.get('stock'),
                marca=request.POST.get('marca'),
                img_url=request.POST.get('img_url'),
                categoria=categoria_obj,
                color=request.POST.get('color')
            )
            return redirect(reverse('ver_producto'))
        except Exception as e:
            context = {'error_message': f'Ocurrió un error al guardar: {e}', 'categorias': categorias}
            return render(request, 'producto/agregar_producto.html', context)
            
    context = {'categorias': categorias}
    return render(request, 'producto/agregar_producto.html', context)

def ver_producto(request):
    productos = Producto.objects.select_related('categoria').all().order_by('nombre')
    context = {'productos': productos}
    return render(request, 'producto/ver_producto.html', context)

def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    context = {'producto': producto, 'categorias': categorias}
    return render(request, 'producto/actualizar_producto.html', context)

def realizar_actualizacion_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('id_producto')
        producto = get_object_or_404(Producto, pk=producto_id)
        categorias = Categoria.objects.filter(activo=True).order_by('nombre')

        try:
            categoria_id = request.POST.get('categoria_id')
            categoria_obj = get_object_or_404(Categoria, pk=categoria_id)
            
            producto.nombre = request.POST.get('nombre')
            producto.precio_unitario = request.POST.get('precio_unitario')
            producto.stock = request.POST.get('stock')
            producto.marca = request.POST.get('marca')
            producto.img_url = request.POST.get('img_url')
            producto.categoria = categoria_obj
            producto.color = request.POST.get('color')
            
            producto.save()
            return redirect(reverse('ver_producto'))
        except Exception as e:
            context = {'producto': producto, 'categorias': categorias, 'error_message': f'Ocurrió un error al actualizar: {e}'}
            return render(request, 'producto/actualizar_producto.html', context)
    return redirect(reverse('ver_producto'))

def borrar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect(reverse('ver_producto'))
    context = {'producto': producto}
    return render(request, 'producto/borrar_producto.html', context)


# ===================================
# 3. Funciones CRUD ProductoProveedor
# ===================================
def agregar_conexion(request):
    productos = Producto.objects.all().order_by('nombre')
    proveedores = Proveedor.objects.all().order_by('nombre_empresa')

    if request.method == 'POST':
        try:
            producto_id = request.POST.get('producto_id')
            proveedor_id = request.POST.get('proveedor_id')
            
            producto_obj = get_object_or_404(Producto, pk=producto_id)
            proveedor_obj = get_object_or_404(Proveedor, pk=proveedor_id)

            ProductoProveedor.objects.create(
                producto=producto_obj,
                proveedor=proveedor_obj,
                precio_compra=request.POST.get('precio_compra'),
                cantidad_comprada=request.POST.get('cantidad_comprada'),
                fecha_ultima_compra=request.POST.get('fecha_ultima_compra') or None,
                referencia_pedido=request.POST.get('referencia_pedido'),
                es_proveedor_activo=request.POST.get('es_proveedor_activo') == 'on'
            )
            return redirect(reverse('ver_conexion'))
        except IntegrityError:
            context = {
                'productos': productos, 
                'proveedores': proveedores, 
                'error_message': 'Esta conexión entre Producto y Proveedor ya existe.'
            }
            return render(request, 'producto_proveedor/agregar_conexion.html', context)
        except Exception as e:
            context = {
                'productos': productos, 
                'proveedores': proveedores, 
                'error_message': f'Ocurrió un error al guardar: {e}'
            }
            return render(request, 'producto_proveedor/agregar_conexion.html', context)

    context = {'productos': productos, 'proveedores': proveedores}
    return render(request, 'producto_proveedor/agregar_conexion.html', context)

def ver_conexion(request):
    conexiones = ProductoProveedor.objects.all().order_by('producto__nombre', 'proveedor__nombre_empresa')
    context = {'conexiones': conexiones}
    return render(request, 'producto_proveedor/ver_conexion.html', context)

def actualizar_conexion(request, pk):
    conexion = get_object_or_404(ProductoProveedor, pk=pk)
    productos = Producto.objects.all().order_by('nombre')
    proveedores = Proveedor.objects.all().order_by('nombre_empresa')
    
    context = {'conexion': conexion, 'productos': productos, 'proveedores': proveedores}
    return render(request, 'producto_proveedor/actualizar_conexion.html', context)

def realizar_actualizacion_conexion(request):
    if request.method == 'POST':
        conexion_id = request.POST.get('id_conexion')
        conexion = get_object_or_404(ProductoProveedor, pk=conexion_id)
        
        try:
            conexion.precio_compra = request.POST.get('precio_compra')
            conexion.cantidad_comprada = request.POST.get('cantidad_comprada')
            conexion.fecha_ultima_compra = request.POST.get('fecha_ultima_compra') or None
            conexion.referencia_pedido = request.POST.get('referencia_pedido')
            conexion.es_proveedor_activo = request.POST.get('es_proveedor_activo') == 'on' 
            
            conexion.save()
            return redirect(reverse('ver_conexion'))
        except Exception as e:
            # Recargar datos para el contexto en caso de error
            productos = Producto.objects.all().order_by('nombre')
            proveedores = Proveedor.objects.all().order_by('nombre_empresa')
            context = {
                'conexion': conexion, 
                'productos': productos, 
                'proveedores': proveedores, 
                'error_message': f'Ocurrió un error al actualizar: {e}'
            }
            return render(request, 'producto_proveedor/actualizar_conexion.html', context)
    return redirect(reverse('ver_conexion'))

def borrar_conexion(request, pk):
    conexion = get_object_or_404(ProductoProveedor, pk=pk)
    if request.method == 'POST':
        conexion.delete()
        return redirect(reverse('ver_conexion'))
    context = {'conexion': conexion}
    return render(request, 'producto_proveedor/borrar_conexion.html', context)


# ===================================
# 4. Funciones CRUD Categoria
# ===================================
def agregar_categoria(request):
    if request.method == 'POST':
        try:
            Categoria.objects.create(
                nombre=request.POST.get('nombre'),
                activo=request.POST.get('activo') == 'on'
            )
            return redirect(reverse('ver_categoria'))
        except IntegrityError:
            context = {'error_message': 'Ya existe una categoría con ese nombre.'}
            return render(request, 'categoria/agregar_categoria.html', context)
        except Exception as e:
            context = {'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'categoria/agregar_categoria.html', context)
    return render(request, 'categoria/agregar_categoria.html')

def ver_categoria(request):
    categorias = Categoria.objects.all().order_by('nombre')
    context = {'categorias': categorias}
    return render(request, 'categoria/ver_categoria.html', context)

def actualizar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    context = {'categoria': categoria}
    return render(request, 'categoria/actualizar_categoria.html', context)

def realizar_actualizacion_categoria(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('id_categoria')
        categoria = get_object_or_404(Categoria, pk=categoria_id)
        try:
            categoria.nombre = request.POST.get('nombre')
            categoria.activo = request.POST.get('activo') == 'on'
            categoria.save()
            return redirect(reverse('ver_categoria'))
        except IntegrityError:
            context = {'categoria': categoria, 'error_message': 'Ya existe una categoría con ese nombre.'}
            return render(request, 'categoria/actualizar_categoria.html', context)
        except Exception as e:
            context = {'categoria': categoria, 'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'categoria/actualizar_categoria.html', context)
    return redirect(reverse('ver_categoria'))

def borrar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect(reverse('ver_categoria'))
    context = {'categoria': categoria}
    return render(request, 'categoria/borrar_categoria.html', context)


# ===================================
# 5. Funciones CRUD Rol
# ===================================
def agregar_rol(request):
    if request.method == 'POST':
        try:
            Rol.objects.create(
                nombre_rol=request.POST.get('nombre_rol')
            )
            return redirect(reverse('ver_rol'))
        except IntegrityError:
            context = {'error_message': 'Ya existe un rol con ese nombre.'}
            return render(request, 'rol/agregar_rol.html', context)
        except Exception as e:
            context = {'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'rol/agregar_rol.html', context)
    return render(request, 'rol/agregar_rol.html')

def ver_rol(request):
    roles = Rol.objects.all().order_by('nombre_rol')
    context = {'roles': roles}
    return render(request, 'rol/ver_rol.html', context)

def actualizar_rol(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    context = {'rol': rol}
    return render(request, 'rol/actualizar_rol.html', context)

def realizar_actualizacion_rol(request):
    if request.method == 'POST':
        rol_id = request.POST.get('id_rol')
        rol = get_object_or_404(Rol, pk=rol_id)
        try:
            rol.nombre_rol = request.POST.get('nombre_rol')
            rol.save()
            return redirect(reverse('ver_rol'))
        except IntegrityError:
            context = {'rol': rol, 'error_message': 'Ya existe un rol con ese nombre.'}
            return render(request, 'rol/actualizar_rol.html', context)
        except Exception as e:
            context = {'rol': rol, 'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'rol/actualizar_rol.html', context)
    return redirect(reverse('ver_rol'))

def borrar_rol(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    if request.method == 'POST':
        rol.delete()
        return redirect(reverse('ver_rol'))
    context = {'rol': rol}
    return render(request, 'rol/borrar_rol.html', context)


# ===================================
# 6. Funciones CRUD Cliente
# ===================================
def agregar_cliente(request):
    roles = Rol.objects.all().order_by('nombre_rol')
    
    if request.method == 'POST':
        try:
            rol_id = request.POST.get('rol_id')
            rol_obj = get_object_or_404(Rol, pk=rol_id) if rol_id else None

            Cliente.objects.create(
                rol=rol_obj,
                nombre_completo=request.POST.get('nombre_completo'),
                email=request.POST.get('email'),
                password=request.POST.get('password') 
            )
            return redirect(reverse('ver_cliente'))
        except IntegrityError:
            context = {'error_message': 'Ya existe un cliente con ese email.', 'roles': roles}
            return render(request, 'cliente/agregar_cliente.html', context)
        except Exception as e:
            context = {'error_message': f'Ocurrió un error: {e}', 'roles': roles}
            return render(request, 'cliente/agregar_cliente.html', context)
            
    context = {'roles': roles}
    return render(request, 'cliente/agregar_cliente.html', context)

def ver_cliente(request):
    clientes = Cliente.objects.select_related('rol').all().order_by('nombre_completo')
    context = {'clientes': clientes}
    return render(request, 'cliente/ver_cliente.html', context)

def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    roles = Rol.objects.all().order_by('nombre_rol')
    context = {'cliente': cliente, 'roles': roles}
    return render(request, 'cliente/actualizar_cliente.html', context)

def realizar_actualizacion_cliente(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('id_cliente')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        roles = Rol.objects.all().order_by('nombre_rol')
        
        try:
            rol_id = request.POST.get('rol_id')
            rol_obj = get_object_or_404(Rol, pk=rol_id) if rol_id else None

            cliente.rol = rol_obj
            cliente.nombre_completo = request.POST.get('nombre_completo')
            cliente.email = request.POST.get('email')
            cliente.password = request.POST.get('password')

            cliente.save()
            return redirect(reverse('ver_cliente'))
        except IntegrityError:
            context = {'cliente': cliente, 'roles': roles, 'error_message': 'Ya existe un cliente con ese email.'}
            return render(request, 'cliente/actualizar_cliente.html', context)
        except Exception as e:
            context = {'cliente': cliente, 'roles': roles, 'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'cliente/actualizar_cliente.html', context)
    return redirect(reverse('ver_cliente'))

def borrar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect(reverse('ver_cliente'))
    context = {'cliente': cliente}
    return render(request, 'cliente/borrar_cliente.html', context)


# ===================================
# 7. Funciones CRUD Dirección
# ===================================
def agregar_direccion(request):
    clientes = Cliente.objects.all().order_by('nombre_completo')
    if request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente_id')
            cliente_obj = get_object_or_404(Cliente, pk=cliente_id)

            Direccion.objects.create(
                cliente=cliente_obj,
                calle=request.POST.get('calle'),
                codigo_postal=request.POST.get('codigo_postal'),
                ciudad=request.POST.get('ciudad'),
                pais=request.POST.get('pais')
            )
            return redirect(reverse('ver_direccion'))
        except Exception as e:
            context = {'error_message': f'Ocurrió un error: {e}', 'clientes': clientes}
            return render(request, 'direccion/agregar_direccion.html', context)
    context = {'clientes': clientes}
    return render(request, 'direccion/agregar_direccion.html', context)

def ver_direccion(request):
    direcciones = Direccion.objects.select_related('cliente').all().order_by('cliente__nombre_completo')
    context = {'direcciones': direcciones}
    return render(request, 'direccion/ver_direccion.html', context)

def actualizar_direccion(request, pk):
    direccion = get_object_or_404(Direccion, pk=pk)
    clientes = Cliente.objects.all().order_by('nombre_completo')
    context = {'direccion': direccion, 'clientes': clientes}
    return render(request, 'direccion/actualizar_direccion.html', context)

def realizar_actualizacion_direccion(request):
    if request.method == 'POST':
        direccion_id = request.POST.get('id_direccion')
        direccion = get_object_or_404(Direccion, pk=direccion_id)
        clientes = Cliente.objects.all().order_by('nombre_completo')
        
        try:
            cliente_id = request.POST.get('cliente_id')
            cliente_obj = get_object_or_404(Cliente, pk=cliente_id)

            direccion.cliente = cliente_obj
            direccion.calle = request.POST.get('calle')
            direccion.codigo_postal = request.POST.get('codigo_postal')
            direccion.ciudad = request.POST.get('ciudad')
            direccion.pais = request.POST.get('pais')
            direccion.save()
            return redirect(reverse('ver_direccion'))
        except Exception as e:
            context = {'direccion': direccion, 'clientes': clientes, 'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'direccion/actualizar_direccion.html', context)
    return redirect(reverse('ver_direccion'))

def borrar_direccion(request, pk):
    direccion = get_object_or_404(Direccion, pk=pk)
    if request.method == 'POST':
        direccion.delete()
        return redirect(reverse('ver_direccion'))
    context = {'direccion': direccion}
    return render(request, 'direccion/borrar_direccion.html', context)


# ===================================
# 8. Funciones CRUD Pedido
# ===================================
# Nota: La complejidad de DetallePedido se simplifica aquí.
def agregar_pedido(request):
    clientes = Cliente.objects.all().order_by('nombre_completo')
    # Solo se muestran direcciones que YA tienen un cliente asociado
    direcciones = Direccion.objects.select_related('cliente').all().order_by('cliente__nombre_completo')
    
    if request.method == 'POST':
        try:
            cliente_obj = get_object_or_404(Cliente, pk=request.POST.get('cliente_id'))
            direccion_obj = get_object_or_404(Direccion, pk=request.POST.get('direccion_envio_id'))
            
            Pedido.objects.create(
                cliente=cliente_obj,
                direccion_envio=direccion_obj,
                costo_total=request.POST.get('costo_total'),
                estado_pedido=request.POST.get('estado_pedido')
            )
            return redirect(reverse('ver_pedido'))
        except Exception as e:
            context = {'error_message': f'Ocurrió un error: {e}', 'clientes': clientes, 'direcciones': direcciones, 'estados': ESTADOS_PEDIDO}
            return render(request, 'pedido/agregar_pedido.html', context)
            
    context = {'clientes': clientes, 'direcciones': direcciones, 'estados': ESTADOS_PEDIDO}
    return render(request, 'pedido/agregar_pedido.html', context)

def ver_pedido(request):
    pedidos = Pedido.objects.select_related('cliente', 'direccion_envio').all().order_by('-id')
    context = {'pedidos': pedidos}
    return render(request, 'pedido/ver_pedido.html', context)

def actualizar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    clientes = Cliente.objects.all().order_by('nombre_completo')
    direcciones = Direccion.objects.select_related('cliente').all().order_by('cliente__nombre_completo')
    context = {'pedido': pedido, 'clientes': clientes, 'direcciones': direcciones, 'estados': ESTADOS_PEDIDO}
    return render(request, 'pedido/actualizar_pedido.html', context)

def realizar_actualizacion_pedido(request):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, pk=request.POST.get('id_pedido'))
        try:
            cliente_obj = get_object_or_404(Cliente, pk=request.POST.get('cliente_id'))
            direccion_obj = get_object_or_404(Direccion, pk=request.POST.get('direccion_envio_id'))
            
            pedido.cliente = cliente_obj
            pedido.direccion_envio = direccion_obj
            pedido.costo_total = request.POST.get('costo_total')
            pedido.estado_pedido = request.POST.get('estado_pedido')
            pedido.save()
            return redirect(reverse('ver_pedido'))
        except Exception as e:
            # Recargar datos para el contexto en caso de error
            clientes = Cliente.objects.all().order_by('nombre_completo')
            direcciones = Direccion.objects.select_related('cliente').all().order_by('cliente__nombre_completo')
            context = {'pedido': pedido, 'clientes': clientes, 'direcciones': direcciones, 'estados': ESTADOS_PEDIDO, 'error_message': f'Error: {e}'}
            return render(request, 'pedido/actualizar_pedido.html', context)
    return redirect(reverse('ver_pedido'))

def borrar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect(reverse('ver_pedido'))
    context = {'pedido': pedido}
    return render(request, 'pedido/borrar_pedido.html', context)


# ===================================
# 9. Funciones CRUD Envio
# ===================================
def agregar_envio(request):
    # Solo pedidos que NO tienen un envío asociado
    pedidos_sin_envio = Pedido.objects.filter(envio__isnull=True).select_related('cliente').order_by('-id')
    
    if request.method == 'POST':
        try:
            pedido_obj = get_object_or_404(Pedido, pk=request.POST.get('pedido_id'))
            
            Envio.objects.create(
                pedido=pedido_obj,
                numero_rastreo=request.POST.get('numero_rastreo'),
                fecha_envio=request.POST.get('fecha_envio'),
                costo_envio=request.POST.get('costo_envio'),
                estado_envio=request.POST.get('estado_envio')
            )
            return redirect(reverse('ver_envio'))
        except IntegrityError:
            context = {'error_message': 'Ya existe un envío con ese número de rastreo o ese pedido ya tiene un envío.', 'pedidos': pedidos_sin_envio, 'estados': ESTADOS_ENVIO}
            return render(request, 'envio/agregar_envio.html', context)
        except Exception as e:
            context = {'error_message': f'Ocurrió un error: {e}', 'pedidos': pedidos_sin_envio, 'estados': ESTADOS_ENVIO}
            return render(request, 'envio/agregar_envio.html', context)

    context = {'pedidos': pedidos_sin_envio, 'estados': ESTADOS_ENVIO}
    return render(request, 'envio/agregar_envio.html', context)

def ver_envio(request):
    envios = Envio.objects.select_related('pedido', 'pedido__cliente').all().order_by('-id')
    context = {'envios': envios}
    return render(request, 'envio/ver_envio.html', context)

def actualizar_envio(request, pk):
    envio = get_object_or_404(Envio, pk=pk)
    # Permite cambiar el pedido solo si el nuevo pedido no tiene ya un envío
    pedidos_disponibles = Pedido.objects.filter(envio__isnull=True).select_related('cliente') | Pedido.objects.filter(pk=envio.pedido.pk)
    context = {'envio': envio, 'pedidos': pedidos_disponibles.order_by('-id'), 'estados': ESTADOS_ENVIO}
    return render(request, 'envio/actualizar_envio.html', context)

def realizar_actualizacion_envio(request):
    if request.method == 'POST':
        envio = get_object_or_404(Envio, pk=request.POST.get('id_envio'))
        try:
            pedido_obj = get_object_or_404(Pedido, pk=request.POST.get('pedido_id'))
            
            envio.pedido = pedido_obj
            envio.numero_rastreo = request.POST.get('numero_rastreo')
            envio.fecha_envio = request.POST.get('fecha_envio')
            envio.costo_envio = request.POST.get('costo_envio')
            envio.estado_envio = request.POST.get('estado_envio')
            envio.save()
            return redirect(reverse('ver_envio'))
        except IntegrityError:
            # Recargar datos para el contexto en caso de error
            pedidos_disponibles = Pedido.objects.filter(envio__isnull=True).select_related('cliente') | Pedido.objects.filter(pk=envio.pedido.pk)
            context = {'envio': envio, 'pedidos': pedidos_disponibles.order_by('-id'), 'estados': ESTADOS_ENVIO, 'error_message': 'Ya existe un envío con ese número de rastreo o el pedido seleccionado ya tiene un envío.'}
            return render(request, 'envio/actualizar_envio.html', context)
        except Exception as e:
            pedidos_disponibles = Pedido.objects.filter(envio__isnull=True).select_related('cliente') | Pedido.objects.filter(pk=envio.pedido.pk)
            context = {'envio': envio, 'pedidos': pedidos_disponibles.order_by('-id'), 'estados': ESTADOS_ENVIO, 'error_message': f'Error: {e}'}
            return render(request, 'envio/actualizar_envio.html', context)
    return redirect(reverse('ver_envio'))

def borrar_envio(request, pk):
    envio = get_object_or_404(Envio, pk=pk)
    if request.method == 'POST':
        envio.delete()
        return redirect(reverse('ver_envio'))
    context = {'envio': envio}
    return render(request, 'envio/borrar_envio.html', context)


# ===================================
# 10. Funciones READ DetallePedido (Solo Listar)
# ===================================
def ver_detallepedido(request):
    # Usar select_related para traer Pedido y Producto
    detalles = DetallePedido.objects.select_related('pedido', 'producto').all().order_by('pedido__id')
    context = {'detalles': detalles}
    return render(request, 'detallepedido/ver_detallepedido.html', context)
# Las funciones CRUD completas para DetallePedido se manejarían idealmente
# como inlines en la vista de Pedido en el panel de administración.