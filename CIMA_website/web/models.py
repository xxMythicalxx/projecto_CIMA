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
    tipo = models.TextField(max_length=30)

    def __str__(self):
        return str(self.tipo)

class Estado_Producto(models.Model):
    estado = models.TextField(max_length=15)

    def __str__(self):
        return str(self.estado)

class Producto(models.Model):
    estado_ha = [
    ("activo", "activo"),
    ("desactivo", "desactivo"),
    ]
    nombre = models.TextField(max_length=15)
    descripcion = models.TextField(max_length=100)
    tipo = models.TextField(max_length=15)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    estado_producto = models.ForeignKey(Estado_Producto, on_delete=models.CASCADE)
    estado_habil = models.TextField(max_length=20, choices=estado_ha)
    fecha_ingreso = models.DateTimeField()
    fecha_egreso = models.DateTimeField()
    rut_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)
    
class Tipo_usuario(models.Model):
    tipo = models.TextField(max_length=15)

    def __str__(self):
        return str(self.tipo)

class Usuario(models.Model):
    correo = models.TextField(max_length=15)
    password = models.TextField(max_length=20)
    tipo = models.ForeignKey(Tipo_usuario, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.correo)
    
class His(models.Model):
    usuario = models.TextField(max_length=20)
    descripcion = models.TextField(max_length=200)
    tableinfo = models.TextField(max_length=100)
    hour = models.DateTimeField()

    def __str__(self):
        return str(self.usuario) + ' - ' + str(self.des)
    

    