from django.shortcuts import render, redirect

from web.models import Producto, Historial_acciones, Alumno, Categoria, Estado_Producto, Proveedor, Movimiento

import json

from django.contrib.auth.models import User, Group, Permission

from django.contrib.auth import logout, login

from django.core.mail import send_mail

from datetime import datetime

from django.contrib.auth.tokens import default_token_generator

from django.template.loader import render_to_string

from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.db.models import Q

from django.contrib.contenttypes.models import ContentType

from django.http import JsonResponse

import requests

from django.conf import settings
# Create your views here.

def test(request):
    if request.method == "POST":
        user = request.POST["username"]
        correo = request.POST["correo"]
        password = request.POST["password"]
        u = User.objects.create_user(user, correo, password)
        u.save()

    g = Group.objects.all().values().order_by("name")
    u = User.objects.all().values().order_by("username")
    p = Permission.objects.all().values().order_by("codename")
    gu = []
    for group in g:
        gu.append({
            'group': group,
            'permissions': group.permissions.all()
        })
    dato = {'p':p,'g':g,'u':u,'gu':gu}
    return render(request, 'test.html',dato)

def test2(request):
    if request.method == "POST":
        rol = request.POST["rol"]
        g = Group.objects.create(name=rol)
        g.save()

    g = Group.objects.all().values().order_by("name")
    u = User.objects.all().values().order_by("username")
    p = Permission.objects.all().values().order_by("codename")
    gu = []
    for group in g:
        gu.append({
            'group': group,
            'permissions': group.permissions.all()
        })
    dato = {'p':p,'g':g,'u':u,'gu':gu}
    return render(request, 'test.html',dato)

def test3(request):
    if request.method == "POST":
        rol = request.POST["roll"]
        perlist = request.POST.getlist("permisos[]")
        listaper = []
        roli = Group.objects.get(name=rol)
        for x in perlist:
            listaper.append(Permission.objects.get(codename=x))
        print(listaper)
        roli.permissions.add(*listaper)

    g = Group.objects.all()
    u = User.objects.all().values().order_by("username")
    p = Permission.objects.all().values().order_by("codename")
    gu = []
    for group in g:
        gu.append({
            'group': group,
            'permissions': group.permissions.all()
        })
    dato = {'p':p,'g':g,'u':u,'gu':gu}
    return render(request, 'test.html',dato)

def test4(request):
    if request.method == "POST":
        us = request.POST["user"]
        multirol = request.POST.getlist("multirol[]")
        user = User.objects.get(username=us)
        for x in multirol:
            user.groups.add(x)

    g = Group.objects.all()
    u = User.objects.all().values().order_by("username")
    p = Permission.objects.all().values().order_by("codename")
    gu = []
    for group in g:
        gu.append({
            'group': group,
            'permissions': group.permissions.all()
        })
    use = []
    for group in g:
        use.append({
            'group': group,
            'users': group.user_set.all()  # Obtiene todos los usuarios asociados a este grupo
        })
    a = User.objects.get(username='god')
    if a.has_perm('auth.add_group'):
        print('puede add_group')
    else:
        print('no puede add_group')
    if a.has_perm('change_proveedor'):
        print('puede change_proveedor')
    else:
        print('no puede change_proveedor')
    dato = {'p':p,'g':g,'u':u,'gu':gu,'use':use}
    return render(request, 'test.html',dato)

def test5(request):
    return render(request, 'password_reset_confirm.html')

def showLogin(request):
    # send_mail(
    # 'Asunto del correo',
    # 'Este es el cuerpo del correo.',
    # 'from@example.com',  # Remitente
    # ['to@example.com'],  # Destinatario
    # fail_silently=False,
    # )
    #send_mail('Asunto de prueba', 'Contenido del mensaje', 'holax0872@gmail.com', ['cobakav745@kazvi.com'])
    try:
        check = request.session['error']
    except:
        check = None
    try:
        check2 = request.session['success']
    except:
        check2 = None
    try:
        check3 = request.session['emarecovery']
    except:
        check3 = None
    if check:
        dato = {'r2':check}
        del request.session['error']
        return render(request, 'login.html',dato)
    if check2:
        dato = {'r':check2}
        del request.session['success']
        return render(request, 'login.html',dato)
    if check3:
        dato = {'r3':check3}
        del request.session['emarecovery']
        return render(request, 'login.html',dato)
    return render(request, 'login.html')

def Login(request):
    if request.method == "POST":
        cor = request.POST["correo"]
        pas = request.POST["password"]
        try:
            u = User.objects.get(email=cor)
        except:
            u = None
        if u == None:
            request.session['error'] = 'No existe el usuario'
            return redirect('showlogin')
        if u.is_superuser and u.check_password(pas):
            login(request,u)
            des = "Inicia Sesión"
            date = datetime.now()
            usuario = cor.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()
            return redirect('showusuregister')

        else:
            if u.check_password(pas):
                login(request,u)
                des = "Inicia Sesión"
                date = datetime.now()
                usuario = cor.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                return redirect('showdashboard')
            else:
                request.session['error'] = 'No existe el usuario'
                return redirect('showlogin')
    else:
        request.session['error'] = 'No se puede acceder por url'
        return redirect('showlogin')

def Logout(request):
    try:
        des = "Cierra Sesión"
        date = datetime.now()
        usuario = request.user.email.upper()
        h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
        h.save()
        logout(request)
        request.session['success'] = 'Sesion Cerrada'
        return redirect('showlogin')
    except:
        return render(request, 'login.html')
    
# Gestion Usuarios    
def ShowUserRegister(request):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            try:
                check = request.session['error']
            except:
                check = None
            try:
                check2 = request.session['success']
            except:
                check2 = None
            u = User.objects.filter(is_superuser=False)
            if check:
                dato = {'u':u,'r2':check,'correo':request.user.email}
                del request.session['error']
                return render(request, 'AdminUsuario.html',dato)
            
            if check2:
                dato = {'u':u,'r':check2,'correo':request.user.email}
                del request.session['success']
                return render(request, 'AdminUsuario.html',dato)
            
            dato = {'u':u,'correo':request.user.email}
            return render(request, 'AdminUsuario.html',dato)
        else:
            request.session['error'] = 'Sesion Expirada'
            return redirect('showlogin')   
    else:
        request.session['error'] = 'No puede acceder a esta opcion'
        return redirect('showlogin')   

def UserRegister(request):
    if request.method == "POST":
        if request.user.is_superuser:
            user = request.POST['usuario']
            cor = request.POST['correo']
            pas = request.POST['password']
            if User.objects.filter(username=user).exists():
                request.session['error'] = 'Este nombre de usuario ya está en uso.'
                return redirect('showusuregister')
            if User.objects.filter(email=cor).exists():
                request.session['error'] = 'Este correo electrónico ya está en uso.'
                return redirect('showusuregister')
            u = User.objects.create_user(user, cor, pas)
            u.save()

            des = "Registro del usuario ("+ cor +")"
            date = datetime.now()
            usuario = cor.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()

            request.session['success'] = 'Usuario Creado Correctamente'
            return redirect('showusuregister')
        else:
            request.session['error'] = 'Sesion Expirada'
            return redirect('showlogin')    
    else:
        request.session['error'] = 'No se puede acceder por url'
        return redirect('showlogin')

def UpdateUser(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            data = json.loads(request.body) 
            username = data.get("user_")
            email = data.get("email_")
            id_ = data.get("id_")

            user = User.objects.get(id=id_)

            # Validar si el nombre de usuario ya existe
            if username and User.objects.filter(username=username).exclude(id=user.id).exists():
                request.session['error'] = 'Este nombre de usuario ya está en uso.'
                return redirect('showusuregister')

            # Validar si el correo electrónico ya existe
            if email and User.objects.filter(email=email).exclude(id=user.id).exists():
                request.session['error'] = 'Este correo electrónico ya está en uso.'
                return redirect('showusuregister')

            # Actualizar el nombre de usuario y el correo electrónico
            if username:
                user.username = username
            if email:
                user.email = email

            des = "Modificacion del usuario ("+ email +")"
            date = datetime.now()
            usuario = request.user.email.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()

            user.save()
            return JsonResponse({'message': 'Los datos se han actualizado correctamente'})
    else:    
        request.session['error'] = 'No se puede acceder por url'
        return redirect('showlogin')

def DeleteUser(request, id):
    if request.user.is_superuser:
        try:
            u = User.objects.get(id=id)
            cor = u.email
            u.delete()

            des = "Eliminado del del usuario ("+ cor +")"
            date = datetime.now()
            usuario = request.user.email.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()

            request.session['success'] = 'El usuario '+ cor +' se han eliminado correctamente.'
            return redirect('showusuregister')
        except:
            request.session['error'] = 'Error inesperado'
            return redirect('showlogin')
    else:
        request.session['error'] = 'No se puede acceder a esta funcion'
        return redirect('showlogin')

#Gestion Roles
def ShowRolRegister(request):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            try:
                check = request.session['error']
            except:
                check = None
            try:
                check2 = request.session['success']
            except:
                check2 = None
            
            g = Group.objects.all()
            if check:
                dato = {'g':g,'r2':check,'correo':request.user.email}
                del request.session['error']
                return render(request, 'AdminRol.html',dato)
            
            if check2:
                dato = {'g':g,'r':check2,'correo':request.user.email}
                del request.session['success']
                return render(request, 'AdminRol.html',dato)
            
            dato = {'g':g,'correo':request.user.email}
            return render(request, 'AdminRol.html',dato)
        else:
            request.session['error'] = 'Sesion Expirada'
            return redirect('showlogin')  
    else:
        request.session['error'] = 'No puede acceder a esta opcion'
        return redirect('showlogin')            

def RolRegister(request):
    if request.method == "POST":
        if request.user.is_superuser:
            rol = request.POST["rol"]
            if Group.objects.filter(name=rol).exists():
                request.session['error'] = 'Este rol ya está creado.'
                return redirect('showrolregister')
            
            g = Group.objects.create(name=rol)
            g.save()
            des = "Registro del rol ("+ rol +")"
            date = datetime.now()
            usuario = request.user.email.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()

            request.session['success'] = 'Rol Creado Correctamente'
            return redirect('showrolregister')
        else:
            request.session['error'] = 'Sesion Expirada'
            return redirect('showlogin')    
    else:
        request.session['error'] = 'No se puede acceder por url'
        return redirect('showlogin')

def UpdateRol(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            data = json.loads(request.body) 
            rol = data.get("rol_")
            id_ = data.get("id_")

            g = Group.objects.get(id=id_)

            # Validar si el rol ya existe
            if rol and Group.objects.filter(name=rol).exclude(id=g.id).exists():
                request.session['error'] = 'Este rol ya está en uso.'
                return redirect('showrolregister')
 
            # Actualizar el rol 
            if rol:
                g.name = rol

            g.save()

            des = "Modificacion del rol ("+ rol +")"
            date = datetime.now()
            usuario = request.user.email.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()
            return JsonResponse({'message': 'Los datos se han actualizado correctamente'})
    else:    
        request.session['error'] = 'No se puede acceder por url'
        return redirect('showlogin')

def DeleteRol(request, id):
    if request.user.is_superuser:
        try:
            g = Group.objects.get(id=id)
            rol = g.name
            g.delete()
            des = "Modificacion del rol ("+ rol +")"
            date = datetime.now()
            usuario = request.user.email.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()
            request.session['success'] = 'El Rol '+ rol +' se han eliminado correctamente.'
            return redirect('showrolregister')
        except:
            request.session['error'] = 'Error inesperado'
            return redirect('showlogin')
    else:
        request.session['error'] = 'No se puede acceder a esta funcion'
        return redirect('showlogin')

# Gestion de asignacion de Permisos a Roles 
def ShowRolPermisoRegister(request):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            try:
                check = request.session['error']
            except:
                check = None
            try:
                check2 = request.session['success']
            except:
                check2 = None
            modelos = [Producto, Historial_acciones, Alumno, Categoria, Proveedor, Movimiento]

            # Crear un Q vacío que contenga todas las condiciones
            filtro = Q()

            # Añadir una condición para cada modelo en la lista
            for modelo in modelos:
                content_type = ContentType.objects.get_for_model(modelo)
                filtro |= Q(content_type=content_type)

            # Filtrar los permisos
            g = Group.objects.all()
            p = Permission.objects.filter(filtro)
            gu = []
            for group in g:
                gu.append({
                    'group': group,
                    'permissions': group.permissions.all()
                })
            pu = {}

            for permission in p:
                category = permission.content_type.model  
                if category not in pu:
                    pu[category] = []
                pu[category].append(permission)
            if check:
                dato = {'pu':pu,'gu':gu,'p':p,'g':g,'r2':check,'correo':request.user.email}
                del request.session['error']
                return render(request, 'AdminRolPermiso.html',dato)
            
            if check2:
                dato = {'pu':pu,'gu':gu,'p':p,'g':g,'r':check2,'correo':request.user.email}
                del request.session['success']
                return render(request, 'AdminRolPermiso.html',dato)
            
            dato = {'pu':pu,'gu':gu,'p':p,'g':g,'correo':request.user.email}
            return render(request, 'AdminRolPermiso.html',dato)
        else:
            request.session['error'] = 'Sesion Expirada'
            return redirect('showlogin') 
    else:
        request.session['error'] = 'No puede acceder a esta opcion'
        return redirect('showlogin')            

def RolPermisoRegister(request):
    if request.method == "POST":
        if request.user.is_superuser:
            rol = request.POST["rol"]
            perlist = request.POST.getlist("permisos[]")
            addremove = request.POST['opt']
            listaper = []
            roli = Group.objects.get(name=rol)
            print(perlist)
            for x in perlist:
                listaper.append(Permission.objects.get(codename=x))
            if addremove=="Add":
                des = "Agregando Permisos al rol ("+ rol +")"
                date = datetime.now()
                usuario = request.user.email.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                roli.permissions.add(*listaper)
            else:
                des = "Quitando Permisos al rol ("+ rol +")"
                date = datetime.now()
                usuario = request.user.email.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                roli.permissions.remove(*listaper)

            request.session['success'] = 'Permisos Asociado Correctamente'
            return redirect('showrolpermisoregister')
        else:
            request.session['error'] = 'Sesion Expirada'
            return redirect('showlogin')    
    else:
        request.session['error'] = 'No se puede acceder por url'
        return redirect('showlogin')

def UpdateRolPermiso(request): # no se usa
    if request.method == 'POST':
        if request.user.is_superuser:
            data = json.loads(request.body) 
            rol = data.get("rol_")
            id_ = data.get("id_")

            g = Group.objects.get(id=id_)

            # Validar si el rol ya existe
            if rol and Group.objects.filter(name=rol).exclude(id=g.id).exists():
                request.session['error'] = 'Este rol ya está en uso.'
                return redirect('showrolregister')
 
            # Actualizar el rol 
            if rol:
                g.name = rol

            g.save()

            des = "Modificacion del rol ("+ rol +")"
            date = datetime.now()
            usuario = request.user.email.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()
            request.session['success'] = 'Los datos se han actualizado correctamente.'
            return redirect('showrolregister')  # O la vista que desees redirigir después del cambio
    else:    
        request.session['error'] = 'No se puede acceder por url'
        return redirect('showlogin')

def DeleteRolPermiso(request, id):  # no se usa
    if request.user.is_superuser:
        try:
            g = Group.objects.get(id=id)
            rol = g.name
            g.delete()
            des = "Modificacion del rol ("+ rol +")"
            date = datetime.now()
            usuario = request.user.email.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()
            request.session['success'] = 'El Rol '+ rol +' se han eliminado correctamente.'
            return redirect('showrolregister')
        except:
            request.session['error'] = 'Error inesperado'
            return redirect('showlogin')
    else:
        request.session['error'] = 'No se puede acceder a esta funcion'
        return redirect('showlogin')


    if request.user.is_superuser:
        try:
            check = request.session['error']
        except:
            check = None
        try:
            check2 = request.session['success']
        except:
            check2 = None
        if check:
            g = Group.objects.all()
            dato = {'g':g,'r2':check,'correo':request.user.email}
            del request.session['error']
            return render(request, 'AdminRol.html',dato)
        if check2:
            g = Group.objects.all()
            dato = {'g':g,'r':check2,'correo':request.user.email}
            del request.session['success']
            return render(request, 'AdminRol.html',dato)
        g = Group.objects.all()
        dato = {'g':g,'correo':request.user.email}
        return render(request, 'AdminRol.html',dato)
    else:
        request.session['error'] = 'Sesion Expirada'
        return redirect('showlogin')       
    
# Gestion de asignacion de Roles a Usuarios
def ShowRolUsuarioRegister(request):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            try:
                check = request.session['error']
            except:
                check = None
            try:
                check2 = request.session['success']
            except:
                check2 = None
            g = Group.objects.all()
            u = User.objects.filter(is_superuser=False)
            gu = []
            for group in g:
                gu.append({
                    'group': group,
                    'permissions': group.permissions.all()
                })
            if check:
                dato = {'gu':gu,'u':u,'g':g,'r2':check,'correo':request.user.email}
                del request.session['error']
                return render(request, 'AdminRolUsuario.html',dato)
            
            if check2:
                dato = {'gu':gu,'u':u,'g':g,'r':check2,'correo':request.user.email}
                del request.session['success']
                return render(request, 'AdminRolUsuario.html',dato)
            
            dato = {'gu':gu,'u':u,'g':g,'correo':request.user.email}
            return render(request, 'AdminRolUsuario.html',dato)
        else:
            request.session['error'] = 'Sesion Expirada'
            return redirect('showlogin')
    else:
        request.session['error'] = 'No puede acceder a esta opcion'
        return redirect('showlogin')             

def RolUsuarioRegister(request):
    if request.method == "POST":
        if request.user.is_superuser:
            us = request.POST["user"]
            multirol = request.POST.getlist("multirol[]")
            addremove = request.POST['opt']
            user = User.objects.get(username=us)
            if addremove=="Add":
                des = "Agregando Roles al usuario ("+ user.email +")"
                date = datetime.now()
                usuario = request.user.email.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                for x in multirol:
                    user.groups.add(x)
            else:
                des = "Quitando Roles al rol ("+ user.email +")"
                date = datetime.now()
                usuario = request.user.email.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                for x in multirol:
                    user.groups.remove(x)

            request.session['success'] = 'Roles Asociado Correctamente'
            return redirect('showrolusuarioregister')
        else:
            request.session['error'] = 'Sesion Expirada'
            return redirect('showlogin')    
    else:
        request.session['error'] = 'No se puede acceder por url'
        return redirect('showlogin')

#password recovery
def password_reset_request(request):
    if request.method == "POST":
        cor = request.POST['email']
        try:
            user = User.objects.get(email=cor)
        except:
            user = None
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())

            current_site = get_current_site(request)
            reset_url = f"{current_site}/reset/{uid}/{token}/"
            subject = "Recuperación de contraseña"
            message = render_to_string('password_reset_email.html', {
                'user': user.username,               # Usuario que está solicitando el cambio
                'reset_url': reset_url,     # URL de restablecimiento con el token y UID
                'site_name': current_site.name,
            })
            try:
                send_mail(subject, message, 'no-reply@example.com', [cor])
            except:
                request.session['error'] = 'Error Sistema de recuperacion no esta funcional'
                return redirect('showlogin')
            des = "Peticion de cambio de contraseña del usuario ("+ cor +")"
            date = datetime.now()
            usuario = cor.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()

            request.session['emarecovery'] = 'Se envio el correo de recuperacion'
            return redirect('showlogin')
        else:
            request.session['error'] = 'Error Correo no encontrado'
            return redirect('showlogin')    
    else:
        request.session['error'] = 'No se puede acceder por url'
        return redirect('showlogin')

def password_reset_confirm(request, uidb64, token):
    try:
        del request.session['error']
    except:
        pass
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        u = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        u = None
        request.session['error'] = 'Este enlase ya no es valido'
        return redirect('showlogin')  
    
    if u is not None and default_token_generator.check_token(u, token):
        if request.method == "POST":
            try:
                pas = request.POST['password']
                pas2 = request.POST['password2']
            except:
                pas = 0
                pas2 = 1
            if pas == pas2:
                u.set_password(pas)
                u.save()
                des = "Reseteo de la contraseña del usuario ("+ u.email +")"
                date = datetime.now()
                usuario = u.email.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                request.session['emarecovery'] = 'Contraseña Cambiada correctamente'
                return redirect('showlogin')
            else:
                return render(request, 'password_reset_confirm.html',{'r2':'Las contraseñas no coiciden'})
           
        return render(request, 'password_reset_confirm.html')
    else:
        print('b')
        request.session['error'] = 'Este enlace ya no es valido'
        return redirect('showlogin')  
    
def password_reset_done(request):
    # Aquí no necesitamos hacer nada especial, solo renderizar un mensaje de éxito
    return render(request, 'password_reset_done.html')    

def password_reset_complete(request):
    # Renderiza una página que informa que el proceso de restablecimiento ha sido completado
    return render(request, 'password_reset_complete.html')    

# Dashboard    
def Showdashboard(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        grup = []
        for group in groups:
            permissions = group.permissions.all()
            grup.append({
                'group_name': group.name,
                'permissions': permissions
            })
        dato = {'correo' : request.user.email,'grup':grup}
        return render(request, 'dashboard.html',dato)

    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
# categoria producto
def ShowCategoria(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'view_categoria':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')

        opcategoria = Categoria.objects.all().values().order_by("nombre")
        grup = []
        for group in groups:
            permissions = group.permissions.all()
            grup.append({
                'group_name': group.name,
                'permissions': permissions
            })
        try:
            check = request.session['error']
        except:
            check = None
        try:
            check2 = request.session['success']
        except:
            check2 = None
        if check:
            dato = {'opcategoria': opcategoria,'r2':check,'correo' : request.user.email,'grup':grup}
            del request.session['error']
            return render(request, 'gestionar_categoria.html',dato)
        
        
        if check2:
            dato = {'opcategoria': opcategoria,'r':check2,'correo' : request.user.email,'grup':grup}
            del request.session['success']
            return render(request, 'gestionar_categoria.html',dato)
        
        dato = {'opcategoria': opcategoria,'correo' : request.user.email,'grup':grup}
        return render(request, 'gestionar_categoria.html', dato)
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')

def RegisterCategoria(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'add_categoria':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')

        if request.method == 'POST':
            try:
                categoria = request.POST['txtcategoria']
                descripcion = request.POST['txtdescripcion']
                test = Categoria.objects.filter(nombre=categoria)
                if test:
                    request.session['error'] = 'La Categoria  ( '+categoria+' ) Ya Existe No Se puede Repetir'
                    return redirect('showcategoria')         
                else:
                    des = "Registro de Categoria realizado ("+categoria+")"
                    date = datetime.now()
                    usuario = request.user.email.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    c = Categoria(nombre=categoria, descripcion=descripcion)
                    c.save()

                    # Creando permisos de para ver productos de esta categoria
                    content_type = ContentType.objects.get_for_model(Producto)
                    Permission.objects.create(
                        codename=f'view_producto_{c.nombre}',
                        name=f'Can view productos de {c.nombre}',
                        content_type=content_type
                    )

                    request.session['success'] = 'Categoria Registrada Correctamente'
                    return redirect('showcategoria')
            except:
                request.session['error'] = "No deberia pasa  [RegisterCategoria]"
                return redirect('showlogin')
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')
    
def RegisterCategoria2(request): # no se usa
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            if request.method == 'POST':
                try:
                    categoria = request.POST['txtcategoria']
                    descripcion = request.POST['txtdescripcion']
                    test = Categoria.objects.filter(nombre=categoria)
                    if test:
                        opcategoria = Categoria.objects.all().values().order_by("nombre")
                        dato = {'opcategoria' : opcategoria,'r2' : 'La Categoria  ( '+categoria+' ) Ya Existe No Se puede Repetir','correo' : request.session["correo"]}
                        return render(request, 'gestionar_categoria.html',dato)             
                    else:
                        des = "Registro de Categoria realizado ("+categoria+")"
                        date = datetime.now()
                        usuario = cor.upper()
                        h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                        h.save()

                        c = Categoria(nombre=categoria, descripcion=descripcion)
                        c.save()

                        opcategoria = Categoria.objects.all().values().order_by("nombre")
                        dato = {'opcategoria' : opcategoria, 'r':"Alumno Registrado Correctamente",'correo' : request.session["correo"]}
                        return render(request, 'gestionar_categoria.html', dato)
                except:
                    u = Alumno.objects.all().values().order_by("nombres")
                    dato = {'u' : u , 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'gestionar_categoria.html', dato)
            else:
                u = Usuario.objects.all().values().order_by("correo")
                dato = {'u' : u , 'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
def UpdateC(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'change_categoria':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')
        
        if request.method == 'POST':
            try:
                data = json.loads(request.body) 
                nombre = data.get("nombre_")
                descripcion = data.get("descripcion_")
                test = Categoria.objects.filter(nombre=nombre)
                if test:
                    request.session['error'] = 'La Categoria  ( '+nombre+' ) Ya Existe No Se puede Repetir'
                    return redirect('showcategoria')
                id_ = data.get("id_")
                des = "Modificacion del la Categoria ("+nombre+")"
                date = datetime.now()
                usuario = request.user.email.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                
                c = Categoria.objects.get(id=id_)
                permiso = Permission.objects.get(codename=f'view_{c.nombre}')
                permiso.codename = f'view_producto_{nombre}'
                permiso.name = f'Can view productos de {nombre}'
                permiso.save()
                c.nombre = nombre
                c.descripcion = descripcion
                c.save()

                return JsonResponse({'message': 'Categoria Modificada Correctamente'})

            except:       
                request.session['error'] = "No deberia pasa  [UpdateCategoria]"
                return redirect('showlogin')
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin') 

def DeleteC(request, id):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'delete_categoria':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')
        
        try:
            c = Categoria.objects.get(id=id)
            permiso = Permission.objects.get(codename=f'view_producto_{c.nombre}')
            permiso.delete()
            categoria = c.nombre
            c.delete()

            des = "Eliminado de la Categoria ("+categoria+")"
            date = datetime.now()
            usuario = request.user.email.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()
            
            request.session['success'] = 'La Categoria : '+ categoria +' Fue Eliminado Correctamente'
            return redirect('showcategoria')
        except:
            request.session['error'] = "No deberia pasa  [DeleteCategoria]"
            return redirect('showlogin')
        
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin') 

#alumno
def ShowGestionAlumno(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'view_alumno':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')

        grup = []
        for group in groups:
            permissions = group.permissions.all()
            grup.append({
                'group_name': group.name,
                'permissions': permissions
            })
        a = Alumno.objects.all().values().order_by("nombres")
        try:
            check = request.session['error']
        except:
            check = None
        try:
            check2 = request.session['success']
        except:
            check2 = None
        if check:
            dato = {'a': a,'r2':check, 'correo' : request.user.email, 'grup':grup}
            del request.session['error']
            return render(request, 'gestionar_alumno.html',dato)
        
        
        if check2:
            dato = {'a': a,'r':check2, 'correo' : request.user.email, 'grup':grup}
            del request.session['success']
            return render(request, 'gestionar_alumno.html',dato)
        
        dato = {'a': a, 'correo' : request.user.email, 'grup':grup}
        return render(request, 'gestionar_alumno.html',dato)
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')

def RegisterAlumno(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'add_alumno':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')

        if request.method == 'POST':
            try:
                rut = request.POST['rut']
                noms = request.POST['textnoms']
                apes = request.POST['textapes']
                cur = request.POST['textcur']
                sal = request.POST['textsal']
                if(len(rut)<10):
                        rut = rut.rjust(10, '0')
                test = Alumno.objects.filter(rut=rut)
                if test:
                    request.session['error'] = 'El Alumno Con Rut ( '+rut+' ) Ya Existe No Se puede Repetir'
                    return redirect('showalumno')            
                else:
                    des = "Registro del alumno realizado ("+rut.upper()+")"
                    date = datetime.now()
                    usuario = request.user.email.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()
                    
                    u = Alumno(rut=rut, nombres=noms, lastnombre=apes, curso=cur, salon=sal)
                    u.save()
                    request.session['success'] = 'Alumno Registrada Correctamente'
                    return redirect('showalumno')
                
            except:
                request.session['error'] = "No deberia pasa [RegisterAlumno]"
                return redirect('showlogin')
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')
    
def RegisterAlumno2(request): # no se usa
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) 
                    rut = data.get("rut_")
                    noms = data.get("noms_")
                    apes = data.get("apes_")
                    cur = data.get("cur_")
                    sal = data.get("sal_")
                    test = Alumno.objects.filter(rut=rut)
                    if test:
                        dato = {'r2' : 'El Alumno Con Rut ( '+rut+' ) Ya Existe No Se puede Repetir','correo' : request.session["correo"]}
                        return render(request, 'agregar_pro.html',dato)             
                    else:
                        des = "Registro del alumno realizado ("+rut.upper()+")"
                        date = datetime.now()
                        usuario = cor.upper()
                        h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                        h.save()

                        u = Alumno(rut=rut, nombres=noms,lastnombre=apes,curso=cur,salon=sal)
                        u.save()

                        dato = {'r':"Alumno Registrado Correctamente",'correo' : request.session["correo"]}
                        return render(request, 'agregar_pro.html', dato)

                except:
                    u = Alumno.objects.all().values().order_by("nombres")
                    dato = {'u' : u , 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'agregar_pro.html', dato)
            else:
                dato = { 'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def UpdateA(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'change_alumno':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')
        
        if request.method == 'POST':
            try:
                data = json.loads(request.body) 
                rut = data.get("rut_")
                noms = data.get("noms_")
                apes = data.get("apes_")
                cur = data.get("cur_")
                sal = data.get("sal_")
                id_ = data.get("id_")
                if(len(rut)<10):
                    rut = rut.rjust(10, '0')

                des = "Modificacion del Alumno ("+rut.upper()+")"
                date = datetime.now()
                usuario = request.user.email.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                
                a = Alumno.objects.get(id=id_)
                a.rut = rut
                a.nombres = noms
                a.lastnombre = apes
                a.curso = cur
                a.salon = sal
                a.save()
                
                return JsonResponse({'message': 'Alumno Modificado Correctamente'})

            except:       
                request.session['error'] = "No deberia pasa  [UpdateAlumno]"
                return redirect('showlogin')
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin') 

def DeleteA(request, id):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'delete_alumno':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')
        try:
            a = Alumno.objects.get(id=id)
            rut = a.rut
            a.delete()

            des = "Eliminado del Alumno ("+rut+")"
            date = datetime.now()
            usuario = request.user.email.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()

            request.session['success'] = 'El Alumno '+ rut +' Fue Eliminado Correctamente'
            return redirect('showalumno')
        except:
            request.session['error'] = "No deberia pasa  [DeleteAlumno]"
            return redirect('showlogin')
        
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin') 

def DeleteA2(request, id): # no se usa
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            try:
                u = Alumno.objects.get(id=id)
                rut = u.rut
                u.delete()

                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta,'r' : 'El Alumno '+ rut +' Fue Eliminado Correctamente','correo' : request.session["correo"]}
                return render(request, 'agregar_pro.html',dato)
            except:
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta,'r2' : "El Alumno No Existe",'correo' : request.session["correo"]}
                return render(request, 'agregar_pro.html',dato)
        else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

#Proveedores
def ShowGestionProveedores(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'view_proveedor':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')

        grup = []
        for group in groups:
            permissions = group.permissions.all()
            grup.append({
                'group_name': group.name,
                'permissions': permissions
            })
        p = Proveedor.objects.all().values().order_by("nombre")
        try:
            check = request.session['error']
        except:
            check = None
        try:
            check2 = request.session['success']
        except:
            check2 = None
        if check:
            dato = {'p': p,'r2': check, 'correo' : request.user.email, 'grup':grup}
            del request.session['error']
            return render(request, 'gestionar_proveedor.html',dato)
        
        
        if check2:
            dato = {'p': p,'r': check2, 'correo' : request.user.email, 'grup':grup}
            del request.session['success']
            return render(request, 'gestionar_proveedor.html',dato)
        
        dato = {'p': p, 'correo' : request.user.email, 'grup':grup}
        return render(request, 'gestionar_proveedor.html',dato)
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')

def RegisterProveedores(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'add_proveedor':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')

        if request.method == 'POST':
            try:
                nom = request.POST['nom']
                tel = request.POST['tel']
                ema = request.POST['ema']
                dir = request.POST['dir']
                test = Proveedor.objects.filter(nombre=nom, telefono=tel, email=ema, direccion=dir)
                if test:
                    request.session['error'] = 'El Proveedor ( '+nom+' ) Ya Existe No Se puede Repetir'
                    return redirect('showproveedor')           
                else:
                    des = "Registro del Proveedor realizado ("+nom+")"
                    date = datetime.now()
                    usuario = request.user.email.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    p = Proveedor(nombre=nom, telefono=tel, email=ema, direccion=dir)
                    p.save()
                    request.session['success'] = 'Proveedor Registrada Correctamente'
                    return redirect('showproveedor')
            except:
                request.session['error'] = "No deberia pasa [RegisterProveedores]"
                return redirect('showlogin')
                
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')
               
def RegisterProveedores2(request): # no se usa
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) 
                    rut = data.get("rut_")
                    noms = data.get("noms_")
                    apes = data.get("apes_")
                    cur = data.get("cur_")
                    sal = data.get("sal_")
                    test = Alumno.objects.filter(rut=rut)
                    if test:
                        dato = {'r2' : 'El Alumno Con Rut ( '+rut+' ) Ya Existe No Se puede Repetir','correo' : request.session["correo"]}
                        return render(request, 'agregar_pro.html',dato)             
                    else:
                        des = "Registro del Proveedor realizado ("+rut.upper()+")"
                        date = datetime.now()
                        usuario = cor.upper()
                        h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                        h.save()

                        u = Alumno(rut=rut, nombres=noms,lastnombre=apes,curso=cur,salon=sal)
                        u.save()

                        dato = {'r':"Alumno Registrado Correctamente",'correo' : request.session["correo"]}
                        return render(request, 'agregar_pro.html', dato)

                except:
                    u = Alumno.objects.all().values().order_by("nombres")
                    dato = {'u' : u , 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'agregar_pro.html', dato)
            else:
                dato = { 'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
def UpdateProveedores(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'change_proveedor':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')
        
        if request.method == 'POST':
            try:
                data = json.loads(request.body) 
                nom = data.get("nom_")
                tel = data.get("tel_")
                ema = data.get("ema_")
                dir = data.get("dir_")
                id_ = data.get("id_")
                des = "Modificacion del Proveedor ("+nom+")"
                date = datetime.now()
                usuario = request.user.email.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                
                
                p = Proveedor.objects.get(id=id_)
                p.nombre = nom
                p.telefono = tel
                p.email = ema
                p.direccion = dir
                p.save()
                
                return JsonResponse({'message': 'Proveedor Modificado Correctamente'})

            except:       
                request.session['error'] = "No deberia pasa  [UpdateProveedores]"
                return redirect('showlogin')
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin') 

def DeleteProveedores(request, id):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'delete_alumno':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')
        
        try:
            p = Proveedor.objects.get(id=id)
            nom = p.nombre
            p.delete()

            des = "Eliminado del Proveedor ("+nom+")"
            date = datetime.now()
            usuario = request.user.email.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()

            request.session['success'] = 'El Proveedor '+ nom +' Fue Eliminado Correctamente'
            return redirect('showproveedor')
        except:
            request.session['error'] = "No deberia pasa  [DeleteProveedores]"
            return redirect('showlogin')
        
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin') 

def DeleteProveedores2(request, id): # no se usa
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            try:
                u = Alumno.objects.get(id=id)
                rut = u.rut
                u.delete()

                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta,'r' : 'El Alumno '+ rut +' Fue Eliminado Correctamente','correo' : request.session["correo"]}
                return render(request, 'agregar_pro.html',dato)
            except:
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta,'r2' : "El Alumno No Existe",'correo' : request.session["correo"]}
                return render(request, 'agregar_pro.html',dato)
        else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
# Producto
def ShowGestionProducto(request):
    if request.user.is_authenticated:
        categoria_permiso = []
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if 'view_producto' in perm.codename:
                    has_permission = True
                    break        

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')


        grup = []
        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if 'view_producto' in perm.codename:
                    categoria_nombre = perm.codename.split('view_producto_')[1]  # Ejemplo de cómo podrías extraer el nombre de la categoría
                    categoria_permiso.append(categoria_nombre)
            grup.append({
                'group_name': group.name,
                'permissions': permissions
            })
        p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').filter(categoria__nombre__in=categoria_permiso).order_by("nombre")
        p2 = Producto.objects.all().values().order_by("nombre")
        categoria = Categoria.objects.filter(nombre__in=categoria_permiso).values().order_by("nombre")
        estado = Estado_Producto.objects.all().values().order_by("estado")
        alumno = Alumno.objects.all().values().order_by("nombres")
        proveedor = Proveedor.objects.all().values().order_by("nombre")
        try:
            check = request.session['error']
        except:
            check = None
        try:
            check2 = request.session['success']
        except:
            check2 = None
        if check:
            dato = {'r2': check,'p2': p2,'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor, 'correo' : request.user.email, 'grup':grup}
            del request.session['error']
            return render(request, 'gestionar_producto.html',dato)
        
        
        if check2:
            dato = {'r': check2,'p2': p2,'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor, 'correo' : request.user.email, 'grup':grup}
            del request.session['success']
            return render(request, 'gestionar_producto.html',dato)
        
        dato = {'p2': p2,'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor, 'correo' : request.user.email, 'grup':grup}
        return render(request, 'gestionar_producto.html',dato)
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')

def RegisterProducto(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'add_producto':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')

        if request.method == 'POST':
            try:
                nom = request.POST['txtnombre']
                desu = request.POST['txtdescipcion']
                cat = request.POST['txtcategorias']
                pro = request.POST['txtprovs']
                can = 0
                pre = request.POST['precio']
                raz = request.POST['opt']
                est = Estado_Producto.objects.all()
                if (len(est) == 0):
                    e = Estado_Producto(estado="Nuevo")
                    e.save()
                e = Estado_Producto.objects.get(estado="Nuevo")
                est = e.id
                rut = request.POST['txtrutss']
                test = Producto.objects.filter(nombre=nom)
                if test:
                    request.session['error'] = 'El Producto Llamado ( '+nom+' ) Ya Existe No Se puede Repetir'
                    return redirect('showproducto')
                else:
                    des = "Registro del producto ("+nom+")"
                    date = datetime.now()
                    usuario = request.user.email.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    p = Producto(nombre=nom, descripcion=desu, categoria_id=cat,proveedor_id=pro, cantidad=can, precio_unitario=pre, razon_ingreso=raz, estado_producto_id=est, estado_habil='activo', fecha_ingreso=datetime.now(),fecha_modificacion=datetime.now(), rut_alumno_id=rut)
                    p.save()
                    request.session['success'] = 'Producto Registrada Correctamente'
                    return redirect('showproducto')
            except:
                request.session['error'] = "No deberia pasa [RegisterProducto]"
                return redirect('showlogin')
                
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')
    
def UpdateP(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'change_producto':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')
        
        if request.method == 'POST':
            try:
                data = json.loads(request.body) 
                nom = data.get("nom_")
                desu = data.get("des_")
                cat = data.get("cat_")
                pro = data.get("pro_")
                can = data.get("can_")
                pre = data.get("pre_")
                raz = data.get("raz_")
                est = data.get("est_")
                rut = data.get("rut_")
                id_ = data.get("id_")

                des = "Modificacion del producto ("+nom+")"
                date = datetime.now()
                usuario = request.user.email.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()

                p = Producto.objects.get(id=id_)
                p.nombre = nom
                p.descripcion = desu
                p.categoria_id = cat
                p.proveedor_id = pro
                p.cantidad = can
                p.precio_unitario = pre
                p.razon_ingreso = raz
                p.estado_producto_id = est
                p.fecha_modificacion = datetime.now()
                p.rut_alumno_id = rut
                p.save()
                return JsonResponse({'message': 'Producto Modificado Correctamente'}) 

            except:       
                request.session['error'] = "No deberia pasa  [UpdateProducto]"
                return redirect('showlogin')
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin') 
    
def PlusProducto(request): # no se usa
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) 
                    nom = data.get("nom_")
                    can = data.get("can_")
                    id_ = data.get("id_")
                    mot = data.get("mot_")

                    des = "Adiccion de stock al producto ("+nom.lower()+")"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    p = Producto.objects.get(id=id_)
                    can = int(can) + int(p.cantidad)
                    p.cantidad = can
                    p.fecha_modificacion = datetime.now()
                    p.save()
                    p = Producto.objects.select_related('categoria','estado_producto','rut_alumno').all().values().order_by("nombre")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    opesta = Estado_Producto.objects.all().values().order_by("estado")
                    opalumno = Alumno.objects.all().values().order_by("rut")
                    dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta, 'p' : p , 'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
                    return render(request, 'dashboard.html', dato)

                except:
                    p = Producto.objects.select_related('categoria','estado_producto','rut_alumno').all().values().order_by("nombre")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    opesta = Estado_Producto.objects.all().values().order_by("estado")
                    opalumno = Alumno.objects.all().values().order_by("rut")
                    dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta, 'p' : p , 'r2' : "No Existen Datos",'correo' : request.session["correo"]}
                    return render(request, 'dashboard.html', dato)
            else:
                dato = {'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
def MinusProducto(request): # no se usa
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) 
                    nom = data.get("nom_")
                    can = data.get("can_")
                    id_ = data.get("id_")
                    mot = data.get("mot_")

                    des = "Reduccion de stock al producto ("+nom.lower()+")"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    p = Producto.objects.get(id=id_)
                    can = int(p.cantidad) - int(can)
                    p.cantidad = can
                    p.fecha_modificacion = datetime.now()
                    p.save()
                    p = Producto.objects.select_related('categoria','estado_producto','rut_alumno').all().values().order_by("nombre")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    opesta = Estado_Producto.objects.all().values().order_by("estado")
                    opalumno = Alumno.objects.all().values().order_by("rut")
                    dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta, 'p' : p , 'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
                    return render(request, 'dashboard.html', dato)

                except:
                    p = Producto.objects.select_related('categoria','estado_producto','rut_alumno').all().values().order_by("nombre")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    opesta = Estado_Producto.objects.all().values().order_by("estado")
                    opalumno = Alumno.objects.all().values().order_by("rut")
                    dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta, 'p' : p , 'r2' : "No Existen Datos",'correo' : request.session["correo"]}
                    return render(request, 'dashboard.html', dato)
            else:
                dato = {'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def DeleteP(request, id):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'delete_alumno':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')
        
        try:
            p = Producto.objects.get(id=id)
            nom = p.nombre
            p.delete()

            des = "Eliminado del producto ("+nom+")"
            date = datetime.now()
            usuario = request.user.email.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()

            request.session['success'] = 'El Producto '+ nom +' Fue Eliminado Correctamente'
            return redirect('showproveedor')
        except:
            request.session['error'] = "No deberia pasa  [DeleteProveedores]"
            return redirect('showlogin')
        
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin') 

def DisableP(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'disable_producto':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')
        
        if request.method == 'POST':
            try:
                data = json.loads(request.body) 
                id = data.get("id_")
                raz = data.get("raz_")
                p = Producto.objects.get(id=id)
                nom = p.nombre
                p.razon_egreso = raz
                p.fecha_egreso = datetime.now()
                p.estado_habil = 'desactivo'
                p.save()

                des = "Desactivado del producto ("+nom+")"
                date = datetime.now()
                usuario = request.user.email.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                print("aa")
                return JsonResponse({'message': 'Desactivación exitosa'})
            except:       
                request.session['error'] = "No deberia pasa  [DisableProducto]"
                return redirect('showlogin')
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin') 
    
def EnableP(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'disable_producto':
                    has_permission = True
                    break 

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')
        
        if request.method == 'POST':
            try:
                data = json.loads(request.body) 
                id = data.get("id_")
                p = Producto.objects.get(id=id)
                nom = p.nombre
                p.razon_egreso = ''
                p.fecha_egreso = None
                p.estado_habil = 'activo'
                p.save()
                des = "Activado del producto ("+nom.lower()+")"
                date = datetime.now()
                usuario = request.user.email.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                print("tt")
                return JsonResponse({'message': 'Activacion exitosa'})
            except:       
                request.session['error'] = "No deberia pasa  [EnableProducto]"
                return redirect('showlogin')
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')

def DeleteC2(request, id): # no se usa
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            try:
                u = Categoria.objects.get(id=id)
                categoria = u.nombre
                u.delete()

                opcategoria = Categoria.objects.all().values().order_by("nombre")
                dato = {'opcategoria': opcategoria,'r' : 'La Categoria : '+ categoria +' Fue Eliminado Correctamente','correo' : request.session["correo"]}
                return render(request, 'gestionar_categoria.html',dato)
            except:
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                dato = {'opcategoria': opcategoria,'r2' : "La Categoria No Existe",'correo' : request.session["correo"]}
                return render(request, 'gestionar_categoria.html',dato)
        else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
# Gestion Stock 
def ShowGestionStock(request):
    categoria_permiso = []
    categoria_permiso_id = []
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'view_movimiento':
                    has_permission = True
                    break        

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')


        grup = []
        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if 'view_producto' in perm.codename:
                    categoria_nombre = perm.codename.split('view_producto_')[1]  # Ejemplo de cómo podrías extraer el nombre de la categoría
                    categoria_permiso.append(categoria_nombre)
                    categoria_id = Categoria.objects.get(nombre=categoria_nombre) # Ejemplo de cómo podrías extraer el nombre de la categoría
                    categoria_permiso_id.append(categoria_id.id)
            grup.append({
                'group_name': group.name,
                'permissions': permissions
            })
        s = Movimiento.objects.select_related('producto').filter(producto__categoria__in=categoria_permiso_id).order_by("-fecha")
        producto = Producto.objects.filter(categoria__nombre__in=categoria_permiso).order_by("nombre")
        try:
            check = request.session['error']
        except:
            check = None
        try:
            check2 = request.session['success']
        except:
            check2 = None
        if check:
            dato = {'r2': check,'s': s,'producto': producto, 'correo' : request.user.email, 'grup':grup}
            del request.session['error']
            return render(request, 'gestionar_stock.html',dato)
        
        
        if check2:
            dato = {'r': check2,'s': s,'producto': producto, 'correo' : request.user.email, 'grup':grup}
            del request.session['success']
            return render(request, 'gestionar_stock.html',dato)

        dato = {'s': s,'producto': producto, 'correo' : request.user.email, 'grup':grup}
        return render(request, 'gestionar_stock.html',dato)
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')

def RegisterStock(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission_entrada = False
        has_permission_salida = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'add_movimiento':
                    has_permission_entrada = True
                
                if perm.codename == 'delete_movimiento':
                    has_permission_salida = True

                if has_permission_entrada and has_permission_salida:
                    break


        if request.method == 'POST':
            try:
                pro = request.POST['pro']
                can = request.POST['can']
                try:
                    tip = request.POST['tip']
                except:
                    tip = None
                try:
                    tip2 = request.POST['tip2']
                except:
                    tip2 = None
                try:
                    tip3 = request.POST['tip3']
                except:
                    tip3 = None
            
                raz = request.POST['raz']     
                if tip != None:
                    if tip =='Entrada':
                        if not has_permission_entrada:
                            request.session['error'] = 'No puedes acceder a esa función'
                            return redirect('showlogin')
                        else:
                            des = "Agregando stock al Producto ("+pro+")"
                            date = datetime.now()
                            usuario = request.user.email.upper()
                            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                            h.save()

                            s = Movimiento(producto_id=pro, cantidad=can, tipo=tip, razon=raz)
                            s.save()
                            p = Producto.objects.get(id=pro)
                            p.agregar_stock(int(can))
                            request.session['success'] = 'Stock Agregado Correctamente'
                            return redirect('showstock')
                    
                    else:
                        if not has_permission_salida:
                            request.session['error'] = 'No puedes acceder a esa función'
                            return redirect('showlogin')
                        else:
                            p = Producto.objects.get(id=pro)
                            tre = p.cantidad
                            if int(tre) < int(can):
                                request.session['error'] = 'No puedes dejar en negativo el stock'
                                return redirect('showstock')
                            des = "Descontado stock al Producto ("+pro+")"
                            date = datetime.now()
                            usuario = request.user.email.upper()
                            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                            h.save()

                            s = Movimiento(producto_id=pro, cantidad=can, tipo=tip, razon=raz)
                            s.save()
                            p.restar_stock(int(can))
                            request.session['success'] = 'Stock Reducido Correctamente'
                            return redirect('showstock')
                
                if tip2 != None:
                    if not has_permission_entrada:
                        request.session['error'] = 'No puedes acceder a esa función'
                        return redirect('showlogin')
                    else:
                        des = "Agregando stock al Producto ("+pro+")"
                        date = datetime.now()
                        usuario = request.user.email.upper()
                        h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                        h.save()

                        s = Movimiento(producto_id=pro, cantidad=can, tipo=tip2, razon=raz)
                        s.save()
                        p = Producto.objects.get(id=pro)
                        p.agregar_stock(int(can))
                        request.session['success'] = 'Stock Agregado Correctamente'
                        return redirect('showstock')
                
                if tip3 != None:
                    if not has_permission_salida:
                        request.session['error'] = 'No puedes acceder a esa función'
                        return redirect('showlogin')
                    else:
                        p = Producto.objects.get(id=pro)
                        tre = p.cantidad
                        if int(tre) < int(can):
                            request.session['error'] = 'No puedes dejar en negativo el stock'
                            return redirect('showstock')
                        des = "Descontado stock al Producto ("+pro+")"
                        date = datetime.now()
                        usuario = request.user.email.upper()
                        h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                        h.save()

                        s = Movimiento(producto_id=pro, cantidad=can, tipo=tip3, razon=raz)
                        s.save()
                        p.restar_stock(int(can))
                        request.session['success'] = 'Stock Reducido Correctamente'
                        return redirect('showstock')
            except:
                request.session['error'] = "No deberia pasa [RegisterStock]"
                return redirect('showlogin')
                
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')
    
# estado producto
def RegisterEstado_Producto(request): # no se usa
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) 
                    estado = data.get("estado_")
                    test = Estado_Producto.objects.filter(estado=estado)
                    if test:
                        dato = {'r2' : 'El Estado  ( '+estado+' ) Ya Existe No Se puede Repetir','correo' : request.session["correo"]}
                        return render(request, 'agregar_pro.html',dato)             
                    else:
                        des = "Registro del Estado realizado ("+estado+")"
                        date = datetime.now()
                        usuario = cor.upper()
                        h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                        h.save()

                        e = Estado_Producto(estado=estado)
                        e.save()

                        opcategoria = Categoria.objects.all().values().order_by("nombre")
                        opesta = Estado_Producto.objects.all().values().order_by("estado")
                        opalumno = Alumno.objects.all().values().order_by("rut")
                        dato = {'opalumno' : opalumno,'opesta' : opesta,'opcategoria' : opcategoria,  'r':"Alumno Registrado Correctamente",'correo' : request.session["correo"]}
                        return render(request, 'agregar_pro.html', dato)

                except:
                    dato = { 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'agregar_pro.html', dato)
            else:
                dato = {'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def UpdateE(request): # no se usa
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) 
                    estado = data.get("estado_")
                    id_ = data.get("id_")
                    des = "Modificacion del estado ("+estado+")"
                    table = "Estado"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()
                    
                    u = Estado_Producto.objects.get(id=id_)
                    u.estado = estado
                    u.save()

                    dato = {'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
                    return render(request, 'agregar_pro.html', dato)

                except:                
                    dato = {'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'agregar_pro.html', dato)
            else:
                u = Usuario.objects.all().values().order_by("correo")
                dato = {'u' : u , 'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)  

def DeleteE(request, id): # no se usa
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            try:
                u = Estado_Producto.objects.get(id=id)
                estado = u.estado
                u.delete()

                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta,'r' : 'El Estado : '+ estado +' Fue Eliminado Correctamente','correo' : request.session["correo"]}
                return render(request, 'agregar_pro.html',dato)
            except:
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta,'r2' : "El Alumno No Existe",'correo' : request.session["correo"]}
                return render(request, 'agregar_pro.html',dato)
        else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

# Historial
def ShowHis(request):
    if request.user.is_authenticated:
        groups = request.user.groups.all()
        has_permission = False

        for group in groups:
            permissions = group.permissions.all()
            for perm in permissions:
                if perm.codename == 'view_historial_acciones':
                    has_permission = True
                    break        

        if not has_permission:
            request.session['error'] = 'No puedes acceder a esa función'
            return redirect('showlogin')


        grup = []
        for group in groups:
            permissions = group.permissions.all()
            grup.append({
                'group_name': group.name,
                'permissions': permissions
            })

        h = Historial_acciones.objects.all().order_by("-fecha")
        try:
            check = request.session['error']
        except:
            check = None
        try:
            check2 = request.session['success']
        except:
            check2 = None
        if check:
            dato = {'r2': check,'h': h, 'correo' : request.user.email, 'grup':grup}
            del request.session['error']
            return render(request, 'listado_his.html',dato)
        
        
        if check2:
            dato = {'r': check2,'h': h, 'correo' : request.user.email, 'grup':grup}
            del request.session['success']
            return render(request, 'listado_his.html',dato)

        dato = {'h': h, 'correo' : request.user.email, 'grup':grup}
        return render(request, 'listado_his.html',dato)
            
    else:
        request.session['error'] = 'Debe estar logueado para acceder'
        return redirect('showlogin')

# Modificacion info Usuarios    
def CorreoAndUsername(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                data = json.loads(request.body) 
                username = data.get("use_")
                email = data.get("cor_")
                id_ = data.get("id_")
                user = User.objects.get(id=id_)
                # Validar si el nombre de usuario ya existe
                if username and User.objects.filter(username=username).exclude(id=user.id).exists():
                    return JsonResponse({'error': 'Este nombre de usuario ya está en uso.', 'status': 'error'}, status=400)

                # Validar si el correo electrónico ya existe
                if email and User.objects.filter(email=email).exclude(id=user.id).exists():
                    return JsonResponse({'error': 'Este correo electrónico ya está en uso.', 'status': 'error'}, status=400)
                # Actualizar el nombre de usuario y el correo electrónico
                if username:
                    user.username = username
                if email:
                    user.email = email
                user.save()
                return JsonResponse({'message': 'Los datos se han actualizado correctamente', 'status': 'success'}, status=200)
                
            except:
                request.session['error'] = "No deberia pasa [CorreoAndUsername]"
                return redirect('showlogin')
                
        else:
            request.session['error'] = 'No puedes acceder Por url'
            return redirect('showlogin')
    else:
        request.session['error'] = 'Sesion Expirada'
        return redirect('showlogin')   

def PasswordChangeUser(request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) 
                    npas = data.get("npas_")
                    pas = data.get("pas_")
                    pas2 = data.get("pas2_")
                    id = data.get("id_")
                    u = User.objects.get(id=id)
                    if u.check_password(npas):

                        u.set_password(pas)
                        u.save()
                        return JsonResponse({'message': 'Los datos se han actualizado correctamente', 'status': 'success'}, status=200)
                    
                    else:
                        return JsonResponse({'error': 'La contraseña actual no es válida. Verifica e ingresa nuevamente.', 'status': 'error'}, status=400)

                except:
                    request.session['error'] = "No deberia pasa [PasswordChangeUser]"
                    return redirect('showlogin')
                    
            else:
                request.session['error'] = 'No puedes acceder Por url'
                return redirect('showlogin')
        else:
            request.session['error'] = 'Sesion Expirada'
            return redirect('showlogin')   