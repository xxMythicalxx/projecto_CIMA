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
from django.views.generic import TemplateView

urlpatterns = [
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
    path('DeleteP/<int:id>', views.DeleteP),
    # admin Usuarios
    path('ShowListU', views.ShowUsuario),
    path('ShowRegistrarU', views.ShowRegisterUsuario),
    path('RegistrarU', views.RegisterUsuario),
    path('UpdateU', views.UpdateU),
    path('DeleteU/<int:id>', views.DeleteU),
    # usuario menu
    path('usumenu', views.ShowUsuarioMenu),
]



