from django.contrib import admin

from hotel.models import Usuario ,Size ,Nroom ,Hotel, His
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=['id','nom','pas']
    
class SizeAdmin(admin.ModelAdmin):
    list_display=['id','nomsize']

class NroomAdmin(admin.ModelAdmin):
    list_display=['id','nomcroom']
    
class HotelAdmin(admin.ModelAdmin):
    list_display=['id','name','description','Nhotel','type','size','price','Nroom','Nbathroom']

class HisAdmin(admin.ModelAdmin):
    list_display=['id','des','tableinfo','hour','usuario']
    
admin.site.register(Usuario, UserAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Nroom, NroomAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(His, HisAdmin)