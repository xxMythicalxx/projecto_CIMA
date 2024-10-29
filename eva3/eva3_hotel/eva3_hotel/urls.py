"""eva3_hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from hotel import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.ShowIndex),
    path('login', views.Login),
    path('logout', views.Logout),

    path('adminn', views.ShowAdmin),

    path('sregistersize', views.ShowRegisterSize),
    path('registersize', views.RegisterSize),
    path('supdatesize/<int:id>', views.ShowUpdateSize),
    path('updatesize/<int:id>', views.UpdateSize),
    path('deletesize/<int:id>', views.DeteleSize),

    path('sregisterroom', views.ShowRegisterRoom),
    path('registerroom', views.RegisterRoom),
    path('supdateroom/<int:id>', views.ShowUpdateRoom),
    path('updateroom/<int:id>', views.UpdateRoom),
    path('deleteroom/<int:id>', views.DeteleRoom),

    path('historial', views.ShowHis),

    path('usuario', views.showUsuario),
    path('sregistrar', views.showRegister),
    path('registrar', views.RegisterHotel),
    path('sactualizar/<int:id>', views.showUpdate),
    path('actualizar/<int:id>', views.Update),
    path('listado', views.showList),
    path('delete/<int:id>', views.deleteHotel),
]
