"""
URL configuration for CIMA_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import views

urlpatterns = [
    # test
    path('test', views.test),
    path('admin/', admin.site.urls),
    # incio de session
    path('',views.showLogin),
    path('login',views.Login),
    path('logout',views.Logout),
    #dashboard
    path('adminn', views.Showdashboard),
    #admin Categoria Producto
    path('ShowGestionC', views.ShowCategoria),
    path('RegistrarC', views.RegisterCategoria),
    path('RegistrarC2', views.RegisterCategoria2),
    path('UpdateC', views.UpdateC),
    path('DeleteC/<int:id>', views.DeleteC),
    path('DeleteC2/<int:id>', views.DeleteC2),
    # admin Alumnos
    path('ShowGestionA', views.ShowGestionAlumno),
    path('RegistrarA', views.RegisterAlumno),
    path('RegistrarA2', views.RegisterAlumno2),
    path('UpdateA', views.UpdateA),
    path('DeleteA/<int:id>', views.DeleteA),
    path('DeleteA2/<int:id>', views.DeleteA2),
    # admin Alumnos
    path('ShowGestionProveedor', views.ShowGestionProveedores),
    path('RegistrarProveedor', views.RegisterProveedores),
    path('RegistrarProveedor2', views.RegisterProveedores2),
    path('UpdateProveedor', views.UpdateProveedores),
    path('DeleteProveedor/<int:id>', views.DeleteProveedores),
    path('DeleteProveedor2/<int:id>', views.DeleteProveedores2),
    # admin Alumnos
    path('ShowGestionA', views.ShowGestionAlumno),
    path('RegistrarA', views.RegisterAlumno),
    path('RegistrarA2', views.RegisterAlumno2),
    path('UpdateA', views.UpdateA),
    path('DeleteA/<int:id>', views.DeleteA),
    path('DeleteA2/<int:id>', views.DeleteA2),
    # admin Productos
    path('ShowGestionP', views.ShowGestionProducto),
    path('RegistrarP', views.RegisterProducto),
    path('UpdateP', views.UpdateP),
    path('EnableP', views.EnableP),
    path('DisableP', views.DisableP),
    path('PlusP', views.PlusProducto),
    path('MinusP', views.MinusProducto),
    path('DeleteP/<int:id>', views.DeleteP),
    # admin Stock
    path('ShowGestionS', views.ShowGestionStock),
    path('RegistrarS', views.RegisterStock),
    path('UpdateS', views.UpdateS),
    path('DeleteS/<int:id>', views.DeleteS),
    # admin Usuarios
    path('ShowListU', views.ShowUsuario),
    path('ShowRegistrarU', views.ShowRegisterUsuario),
    path('RegistrarU', views.RegisterUsuario),
    path('UpdateU', views.UpdateU),
    path('DeleteU/<int:id>', views.DeleteU),
    #admin Estado Producto
    path('RegistrarE', views.RegisterEstado_Producto),
    path('UpdateE', views.UpdateE),
    path('DeleteE/<int:id>', views.DeleteE),
    #admin historial
    path('ShowHis', views.ShowHis),
    # usuario menu
    path('usumenu', views.ShowUsuarioMenu),
    path('UpdatePusu', views.UpdateP2),
    path('RegistrarPusu', views.RegisterProductoUsu),
    path('ShowRegistrarPusu', views.ShowRegisterProductoUsu),
    path('EnablePusu', views.EnableP2),
    path('DisablePusu', views.DisableP2),
    path('DeletePusu/<int:id>', views.DeleteP2),
    #usuario Estado producto
    path('RegistrarEusu', views.RegisterEstado_ProductoUsu),
    path('UpdateEusu', views.UpdateEUsu),
    path('DeleteEusu/<int:id>', views.DeleteEUsu),
    # admin Alumnos
    path('RegistrarAusu', views.RegisterAlumnoUsu),
    path('UpdateAusu', views.UpdateAUsu),
    path('DeleteAusu/<int:id>', views.DeleteAUsu),
]



