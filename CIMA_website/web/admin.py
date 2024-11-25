from django.contrib import admin

from web.models import Producto, Historial_acciones, Alumno

# Register your models here.

class AlumnoAdmin(admin.ModelAdmin):
    list_display=['id', 'rut', 'nombres', 'lastnombre', 'curso', 'salon']

class HisAdmin(admin.ModelAdmin):
    list_display=['id', 'usuario', 'descripcion', 'fecha']

class productoAdmin(admin.ModelAdmin):
    list_display=['id','nombre', 'descripcion', 'categoria', 'cantidad', 'precio_unitario','razon_ingreso', 'estado_producto', 'estado_habil', 'fecha_ingreso','fecha_modificacion','fecha_egreso', 'razon_egreso', 'rut_alumno']
    
# class usuarioAdmin(admin.ModelAdmin):
#     list_display=['id', 'correo', 'password', 'tipo', 'create_alumno', 'create_estado']

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Historial_acciones, HisAdmin)
# admin.site.register(Producto, productoAdmin)
# admin.site.register(Usuario, usuarioAdmin)