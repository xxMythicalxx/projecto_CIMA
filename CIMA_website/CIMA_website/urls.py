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
    # Recuperacion de Contraseña
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    # test
    # path('test', views.test),
    # path('test2', views.test2),
    # path('test3', views.test3),
    # path('test4', views.test4), 
    # path('test5', views.test5), 
    path('admin/', admin.site.urls),
    # incio de session
    path('',views.showLogin, name='showlogin'),
    path('login',views.Login),
    path('logout',views.Logout),
    path('logout',views.Logout),
    #admin de Usuarios
    path('showUsuregister',views.ShowUserRegister, name='showusuregister'),
    path('usuRegister',views.UserRegister),
    path('UpdateUser', views.UpdateUser),
    path('DeleteUser/<int:id>', views.DeleteUser),
    #admin de Roles
    path('showRolregister',views.ShowRolRegister, name='showrolregister'),
    path('rolRegister',views.RolRegister),
    path('UpdateRol', views.UpdateRol),
    path('DeleteRol/<int:id>', views.DeleteRol),
    #admin de Roles Permisos
    path('showRolPermisoregister',views.ShowRolPermisoRegister, name='showrolpermisoregister'),
    path('rolPermisoRegister',views.RolPermisoRegister),
    #admin de Roles Usuarios
    path('showRolUsuarioregister',views.ShowRolUsuarioRegister, name='showrolusuarioregister'),
    path('rolUsuarioRegister',views.RolUsuarioRegister),
    #dashboard
    path('adminn', views.Showdashboard, name='showdashboard'),
    # Usuario Categoria Producto
    path('ShowGestionC', views.ShowCategoria, name='showcategoria'),
    path('RegistrarC', views.RegisterCategoria),
    path('RegistrarC2', views.RegisterCategoria2), # no se usa
    path('UpdateC', views.UpdateC),
    path('DeleteC/<int:id>', views.DeleteC),
    path('DeleteC2/<int:id>', views.DeleteC2), # no se usa
    # Usuario Alumnos
    path('ShowGestionA', views.ShowGestionAlumno, name='showalumno'),
    path('RegistrarA', views.RegisterAlumno),
    path('RegistrarA2', views.RegisterAlumno2), # no se usa
    path('UpdateA', views.UpdateA),
    path('DeleteA/<int:id>', views.DeleteA),
    path('DeleteA2/<int:id>', views.DeleteA2), # no se usa
    # Usuario Proveedor
    path('ShowGestionProveedor', views.ShowGestionProveedores, name='showproveedor'),
    path('RegistrarProveedor', views.RegisterProveedores),
    path('RegistrarProveedor2', views.RegisterProveedores2), # no se usa
    path('UpdateProveedor', views.UpdateProveedores),
    path('DeleteProveedor/<int:id>', views.DeleteProveedores),
    path('DeleteProveedor2/<int:id>', views.DeleteProveedores2), # no se usa
    # Usuario Productos
    path('ShowGestionP', views.ShowGestionProducto, name='showproducto'),
    path('RegistrarP', views.RegisterProducto),
    path('UpdateP', views.UpdateP),
    path('EnableP', views.EnableP),
    path('DisableP', views.DisableP),
    path('PlusP', views.PlusProducto),
    path('MinusP', views.MinusProducto),
    path('DeleteP/<int:id>', views.DeleteP),
    # Usuario Stock
    path('ShowGestionS', views.ShowGestionStock,  name='showstock'),
    path('RegistrarS', views.RegisterStock),
    # Usuario Estado Producto
    path('RegistrarE', views.RegisterEstado_Producto), # no se usa
    path('UpdateE', views.UpdateE), # no se usa
    path('DeleteE/<int:id>', views.DeleteE), # no se usa
    # Usuario historial
    path('ShowHis', views.ShowHis),
    # Usuario historial
    path('changeusu', views.CorreoAndUsername),
    path('passchangeusu', views.PasswordChangeUser),
]



