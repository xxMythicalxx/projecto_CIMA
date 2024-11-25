from django.db import models

# Create your models here.
class Alumno(models.Model):
    rut = models.TextField(max_length=15)
    nombres = models.TextField(max_length=30)
    lastnombre = models.TextField(max_length=30)
    curso = models.TextField(max_length=20)
    salon = models.TextField(max_length=20)

    def __str__(self):
        return str(self.rut)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    
class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.TextField()

    def __str__(self):
        return self.nombre

class Estado_Producto(models.Model):
    estado = models.TextField(max_length=15)

    def __str__(self):
        return str(self.estado)

class Producto(models.Model):
    estado_ha = [
    ("activo", "activo"),
    ("desactivo", "desactivo"),
    ]
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    razon_ingreso = models.TextField()
    estado_producto = models.ForeignKey(Estado_Producto, on_delete=models.CASCADE)
    estado_habil = models.TextField(max_length=20, choices=estado_ha)
    fecha_ingreso = models.DateTimeField()
    fecha_modificacion = models.DateTimeField()
    fecha_egreso = models.DateTimeField(null=True, blank=True)
    razon_egreso = models.TextField(max_length=100)
    rut_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("enable_producto", "Puede activar producto"),
            ("disable_producto", "Puede desactivar producto"),
        ]

    def __str__(self):
        return str(self.nombre)
    
    def restar_stock(self, cantidad_salida):
        if self.cantidad >= cantidad_salida:
            self.cantidad -= cantidad_salida
            self.save()

    def agregar_stock(self, cantidad_entrada):
        self.cantidad += cantidad_entrada
        self.save()

class Movimiento(models.Model):
    TIPOS_DE_MOVIMIENTO = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida')
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    tipo = models.CharField(max_length=7, choices=TIPOS_DE_MOVIMIENTO)
    fecha = models.DateTimeField(auto_now_add=True)
    razon = models.CharField(max_length=100)  # razon de porque realizó el movimiento

    def __str__(self):
        return f"{self.producto.nombre} - {self.get_tipo_display()} - {self.cantidad}"
# class Usuario(models.Model):
#     correo = models.TextField(max_length=15)
#     password = models.TextField(max_length=20)
#     tipo = models.ForeignKey(Categoria, on_delete=models.CASCADE)
#     create_alumno = models.BooleanField()
#     create_estado = models.BooleanField()

#     def __str__(self):
#         return str(self.correo)
    
class Historial_acciones(models.Model):
    usuario = models.TextField(max_length=20)
    descripcion = models.TextField(max_length=200)
    fecha = models.DateTimeField()

    def __str__(self):
        return str(self.usuario) + ' - ' + str(self.des)
    

    