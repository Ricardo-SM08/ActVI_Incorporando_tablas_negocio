# app_victorysports/models.py

from django.db import models

# -----------------
# Modelos de Soporte (ya creados)
# -----------------

# Modelo para Rol (Necesario para Cliente)
class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)
    class Meta:
        verbose_name = "Rol de Usuario"
        verbose_name_plural = "Roles de Usuario"
    def __str__(self):
        return self.nombre_rol

# Modelo para Categoría (Necesario para Producto)
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
    def __str__(self):
        return self.nombre
        
# Modelo para Proveedor (Necesario para ProductoProveedor)
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=150, unique=True)
    telefono_empresa = models.CharField(max_length=15)
    email_empresa = models.EmailField(max_length=100)
    pais_origen = models.CharField(max_length=50)
    contacto_principal = models.CharField(max_length=100)
    fecha_registro = models.DateField(auto_now_add=True)
    direccion = models.TextField()
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
    def __str__(self):
        return self.nombre_empresa

# Modelo para Producto (Necesario para DetallePedido)
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    marca = models.CharField(max_length=100)
    img_url = models.URLField(max_length=255, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    color = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    def __str__(self):
        return f"{self.nombre} ({self.marca})"

# Modelo para Producto Proveedor
class ProductoProveedor(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,
                                 related_name='relaciones_proveedor')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE,
                                  related_name='relaciones_producto')
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ultima_compra = models.DateField(null=True, blank=True)
    cantidad_comprada = models.IntegerField(default=1)
    referencia_pedido = models.CharField(max_length=50, blank=True, null=True)
    es_proveedor_activo = models.BooleanField(default=True)
    class Meta:
        unique_together = (('producto', 'proveedor'),)
        verbose_name = "Producto por Proveedor"
        verbose_name_plural = "Productos por Proveedores"
    def __str__(self):
        return f"Relación: {self.producto.nombre} - {self.proveedor.nombre_empresa}"


# -----------------
# NUEVOS Modelos de Clientes y Pedidos
# -----------------

class Cliente(models.Model):
    # id_cliente (PK) implícito por Django
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)  # id_rol
    nombre_completo = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nombre_completo

class Direccion(models.Model):
    # id_direccion (PK) implícito por Django
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # id_cliente
    calle = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"

    def __str__(self):
        return f"{self.calle}, {self.ciudad} ({self.cliente.nombre_completo})"

class Pedido(models.Model):
    # id_pedido (PK) implícito por Django
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)  # id_cliente
    direccion_envio = models.ForeignKey(Direccion, on_delete=models.PROTECT)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pedido = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.id} de {self.cliente.nombre_completo}"

class DetallePedido(models.Model):
    # id_detalle (PK) implícito por Django
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # id_pedido
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)  # id_producto
    cantidad_solicitada = models.IntegerField()
    precio_al_momento = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Detalle del Pedido"
        verbose_name_plural = "Detalles del Pedido"
        unique_together = (('pedido', 'producto'),) # Clave compuesta

    def __str__(self):
        return f"Detalle {self.id} - {self.producto.nombre} en Pedido {self.pedido.id}"

class Envio(models.Model):
    # id_envio (PK) implícito por Django
    # Relación Uno a Uno
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)  # id_pedido
    numero_rastreo = models.CharField(max_length=100, unique=True)
    fecha_envio = models.DateField()
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2)
    estado_envio = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"

    def __str__(self):
        return f"Envío #{self.numero_rastreo} para Pedido {self.pedido.id}"