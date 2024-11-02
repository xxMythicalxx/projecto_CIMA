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
    # admin Productos
    path('adminn', views.ShowAdmin),
    path('ShowRegistrarP', views.ShowRegisterProducto),
    path('RegistrarP', views.RegisterProducto),
    path('UpdateP', views.UpdateP),
    path('EnableP', views.EnableP),
    path('DisableP', views.DisableP),
    path('DeleteP/<int:id>', views.DeleteP),
    # admin Usuarios
    path('ShowListU', views.ShowUsuario),
    path('ShowRegistrarU', views.ShowRegisterUsuario),
    path('RegistrarU', views.RegisterUsuario),
    path('UpdateU', views.UpdateU),
    path('DeleteU/<int:id>', views.DeleteU),
    # admin Alumnos
    path('ShowListA', views.ShowAlumno),
    path('ShowRegistrarA', views.ShowRegisterAlumno),
    path('RegistrarA', views.RegisterAlumno),
    path('RegistrarA2', views.RegisterAlumno2),
    path('UpdateA', views.UpdateA),
    path('DeleteA/<int:id>', views.DeleteA),
    path('DeleteA2/<int:id>', views.DeleteA2),
    #admin Estado Producto
    path('RegistrarE', views.RegisterEstado_Producto),
    path('UpdateE', views.UpdateE),
    path('DeleteE/<int:id>', views.DeleteE),
    #admin Categoria Producto
    path('RegistrarC', views.RegisterCategoria),
    path('UpdateC', views.UpdateC),
    path('DeleteC/<int:id>', views.DeleteC),
    # usuario menu
    path('usumenu', views.ShowUsuarioMenu),
]



