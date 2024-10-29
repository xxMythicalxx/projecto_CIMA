from django.contrib import admin

from web.models import Producto, Usuario, His, Alumno

# Register your models here.

class AlumnoAdmin(admin.ModelAdmin):
    list_display=['id', 'rut', 'nombres', 'lastnombre', 'curso', 'salon']

class HisAdmin(admin.ModelAdmin):
    list_display=['id', 'usuario', 'descripcion', 'tableinfo', 'hour']

class productoAdmin(admin.ModelAdmin):
    list_display=['id','nombre', 'descripcion', 'tipo', 'categoria', 'cantidad', 'precio', 'estado_producto', 'estado_habil', 'fecha_ingreso', 'fecha_egreso', 'rut_alumno']
    
class usuarioAdmin(admin.ModelAdmin):
    list_display=['id', 'correo', 'password']

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(His, HisAdmin)
admin.site.register(Producto, productoAdmin)
admin.site.register(Usuario, usuarioAdmin)