import base64

from django.shortcuts import render

from web.models import Producto, Usuario, His, Alumno

import json

from django.contrib.auth.models import User

from datetime import datetime



# Create your views here.

def test(request):
    return render(request, 'agregar_alu.html')

def showLogin(request):
    return render(request, 'login.html')

def Login(request):
    if request.method == "POST":
        cor = request.POST["correo"]
        pas = request.POST["password"]
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None and u.check_password(pas):
            request.session['status'] = True
            request.session["correo"] = cor.upper()

            des = "Inicia Sesión"
            table = ""
            date = datetime.now()
            usuario = cor.upper()
            h = His(des=des, tableinfo=table, hour=date, usuario=usuario)
            h.save()
            p = Producto.objects.all().values().order_by("nombre")
            dato = {'p': p, 'correo' : cor.upper()}
            return render(request, 'admin.html',dato)

        else:
            pas.encode("ascii")
            pasby = bytes(pas, encoding='utf-8')
            pas_encode64 = base64.b64encode(pasby)
            encode = pas_encode64.decode('ascii')
            check = Usuario.objects.filter(correo=cor,password=encode).values()
            if check:
                request.session['status'] = True
                request.session["correo"] = cor.upper()

                des = "Inicia Sesión"
                table = ""
                date = datetime.now()
                usuario = cor.upper()
                h = His(des=des, tableinfo=table, hour=date, usuario=usuario)
                h.save()
                p = Producto.objects.all().values().order_by("nombre")
                dato = {'p': p,'correo' : cor.upper()}
                return render(request, 'usuario.html',dato)
            else:
                dato = {'r2' : 'Error El Usuario No Existe'}
                return render(request, 'login.html',dato)
    else:
            dato = {'r2' : 'No se puede acceder por URL'}
            return render(request, 'login.html',dato)

def Logout(request):
    try:
        cor = request.session['correo']
        del request.session['correo']
        del request.session['status']
        dato = {'r' : 'Sesion Cerrada'}

        des = "Cierra Sesión"
        table = ""
        date = datetime.now()
        usuario = cor.upper()
        h = His(des=des, tableinfo=table, hour=date, usuario=usuario)
        h.save()
        return render(request, 'login.html',dato)
    except:
        return render(request, 'login.html')



# Producto

def ShowAdmin(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            p = Producto.objects.all().values().order_by("nombre")
            dato = {'p': p,'correo' : request.session["correo"]}
            return render(request, 'admin.html',dato)
            
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


def RegisterProducto(request):
    if request.method == 'POST':
        check = request.session.get("status")
        cor = request.session.get("correo")
        if check is True:
            try:
                u = User.objects.get(email=cor)
            except User.DoesNotExist:
                u = None
            if u is not None:
                nom = request.POST['txtnombre']
                des = request.POST['txtdescipcion']
                tip = request.POST['txttipo']
                can = request.POST['cantidad']
                pre = request.POST['precio']
                test = Producto.objects.filter(nombre=nom)
                if test:
                    dato = {'r2' : 'El Producto Llamado ( '+nom+' ) Ya Existe No Se puede Repetir'}
                    return render(request, 'agregar_pro.html',dato)
                else:
                    des = "Registro del producto ("+nom.lower()+")"
                    table = "Producto"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = His(des=des, tableinfo=table, hour=date, usuario=usuario)
                    h.save()

                    p = Producto(nombre=nom, descripcion=des, tipo=tip, cantidad=can, precio=pre)
                    p.save()
                    p = Producto.objects.all().values().order_by("nombre")
                    dato = {'p': p, 'r' : 'Registro Realizado Correctamente'}
                    return render(request, 'admin.html',dato)
            else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'Debe estar logueado para acceder' }
            return render(request, 'login.html', dato)         
    else:
        dato = {'r2' : 'No se puede acceder por URL'}
        return render(request, 'login.html',dato)
    

def ShowRegisterProducto(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            p = Producto.objects.all().values().order_by("nombre")
            dato = {'p': p,'correo' : request.session["correo"]}
            return render(request, 'agregar_pro.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)




def UpdateP(request):
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
                    des = data.get("des_")
                    tip = data.get("tip_")
                    can = data.get("can_")
                    pre = data.get("pre_")
                    id_ = data.get("id_")

                    des = "Modificacion del producto ("+nom.lower()+")"
                    table = "Producto"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = His(des=des, tableinfo=table, hour=date, usuario=usuario)
                    h.save()

                    p = Producto.objects.get(id=id_)
                    p.nombre = nom
                    p.descripcion = des
                    p.tipo = tip
                    p.cantidad = can
                    p.precio = pre
                    p.save()
                    p = Producto.objects.all().values().order_by("nombre")
                    dato = {'p' : p , 'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
                    return render(request, 'admin.html', dato)

                except:
                    p = Producto.objects.all().values().order_by("nombre")
                    dato = {'p' : p , 'r2' : "No Existen Datos" }
                    return render(request, 'admin.html', dato)
            else:
                dato = {'p' : p , 'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


def DeleteP(request, id):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            try:
                p = Producto.objects.get(id=id)
                nom = p.nombre
                p.delete()

                des = "Eliminado del producto ("+nom.lower()+")"
                table = "Producto"
                date = datetime.now()
                usuario = cor.upper()
                h = His(des=des, tableinfo=table, hour=date, usuario=usuario)
                h.save()

                p = Producto.objects.all().values().order_by("nombre")

                dato = {'r' : 'El Producto '+ nom +' Fue Eliminado Correctamente', 'p': p}
                return render(request, 'admin.html',dato)
            except:
                p = Producto.objects.all().values().order_by("nombre")

                dato = {'r2' : "El Producto No Existe", 'p': p}
                return render(request, 'admin.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


# Usuario 

def ShowUsuario(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            u = Usuario.objects.all().values().order_by("correo")
            dato = {'u': u,'correo' : request.session["correo"]}
            return render(request, 'listado_usu.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


def RegisterUsuario(request):
    if request.method == 'POST':
        check = request.session.get("status")
        cor = request.session.get("correo")
        if check is True:
            try:
                u = User.objects.get(email=cor)
            except User.DoesNotExist:
                u = None
            if u is not None:
                corr = request.POST['txtcorreo']
                tpas1 = request.POST['txtpass1']
                tpas2 = request.POST['txtpass2']
                if tpas1 != tpas2:
                    dato = {'r2' : 'Las constraseñas no coinciden'}
                    return render(request, 'agregar_usu.html',dato)
                test = Usuario.objects.filter(correo=corr)
                if test:
                    dato = {'r2' : 'El Correo ( '+corr+' ) Ya Existe No Se puede Repetir'}
                    return render(request, 'agregar_usu.html',dato)             
                else:
                    pas = tpas1
                    pas.encode("ascii")
                    pasby = bytes(pas, encoding='utf-8')
                    pas_encode64 = base64.b64encode(pasby)
                    encode = pas_encode64.decode('ascii')

                    des = "Registro del usuario realizado ("+corr.upper()+")"
                    table = "Usuario"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = His(des=des, tableinfo=table, hour=date, usuario=usuario)
                    h.save()

                    u = Usuario(correo=corr, password=encode)
                    u.save()
                    u = Usuario.objects.all().values().order_by("correo")
                    dato = {'u': u, 'r' : 'Usuario Registrado Correctamente'}
                    return render(request, 'listado_usu.html',dato)
                
            else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
            
        else:
            dato = { 'r2' : 'Debe estar logueado para acceder' }
            return render(request, 'login.html', dato)  
               
    else:
        dato = {'r2' : 'No se puede acceder por URL'}
        return render(request, 'login.html',dato)
    

def ShowRegisterUsuario(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            u = Usuario.objects.all().values().order_by("correo")
            dato = {'u': u,'correo' : request.session["correo"]}
            return render(request, 'agregar_usu.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


def UpdateU(request):
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
                    corr = data.get("cor_")
                    pas = data.get("pas_")
                    pas.encode("ascii")
                    pasby = bytes(pas, encoding='utf-8')
                    pas_encode64 = base64.b64encode(pasby)
                    encode = pas_encode64.decode('ascii')
                    id_ = data.get("id_")

                    des = "Modificacion del usuario ("+corr.upper()+")"
                    table = "Usuario"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = His(des=des, tableinfo=table, hour=date, usuario=usuario)
                    h.save()

                    u = Usuario.objects.get(id=id_)
                    u.correo = corr
                    u.password = encode
                    u.save()

                    dato = {'u' : u ,  'r':"Datos Modificados Correctamente"}

                    return render(request, 'listado_usu.html', dato)

                except:
                    u = Usuario.objects.all().values().order_by("correo")
                    
                    dato = {'u' : u , 'r2' : "No Existen Datos" }
                    return render(request, 'admin.html', dato)
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

def DeleteU(request, id):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        #user = authenticate(request,email="a@a.com", password=pas)
        #if user is not None:
        #    print('hola')
        #print(user)
        #print(u)
        if u is not None:
            try:
                u = Usuario.objects.get(id=id)
                corr = u.correo
                u.delete()

                u = Usuario.objects.all().values().order_by("correo")

                dato = {'r' : 'El Usuario '+ corr +' Fue Eliminado Correctamente', 'u': u}
                return render(request, 'listado_usu.html',dato)
            except:
                u = Usuario.objects.all().values().order_by("correo")

                dato = {'r2' : "El Usuario No Existe", 'u': u}
                return render(request, 'listado_usu.html',dato)
        else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


def ShowUsuarioMenu(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check:
        p = Producto.objects.all().values().order_by("nombre")
        dato = {'p': p,'correo' : cor.upper()}
        return render(request, 'usuario.html',dato)
    else:
        dato = {'r2' : 'Debe estar logueado para acceder'}
        return render(request, 'login.html',dato)
       

