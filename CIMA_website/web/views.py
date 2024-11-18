import base64

from django.shortcuts import render

from web.models import Producto, Usuario, Historial_acciones, Alumno, Categoria, Estado_Producto, Proveedor, Movimiento

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
            date = datetime.now()
            usuario = cor.upper()
            h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
            h.save()
            p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
            opesta = Estado_Producto.objects.all().values().order_by("estado")
            opcategoria = Categoria.objects.all().values().order_by("nombre")
            opalumno = Alumno.objects.all().values().order_by("rut")
            dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta,'p': p, 'correo' : cor.upper(),'correo' : request.session["correo"],'r':'Bienvenido '+ request.session["correo"]}
            return render(request, 'dashboard.html',dato)

        else:
            pas.encode("ascii")
            pasby = bytes(pas, encoding='utf-8')
            pas_encode64 = base64.b64encode(pasby)
            encode = pas_encode64.decode('ascii')
            check = Usuario.objects.filter(correo=cor,password=encode).values()
            if check:
                tip = Usuario.objects.get(correo=cor,password=encode)
                print(tip.tipo_id)
                request.session['status'] = True
                request.session["correo"] = cor.upper()
                request.session["tipo"] = str(tip.tipo_id)

                des = "Inicia Sesión"
                date = datetime.now()
                usuario = cor.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()
                p = Producto.objects.filter(categoria_id=tip.tipo_id).select_related('categoria','estado_producto','rut_alumno').all().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta,'p': p, 'correo' : cor.upper(),'correo' : request.session["correo"],'r':'Bienvenido '+ request.session["correo"]}
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
        date = datetime.now()
        usuario = cor.upper()
        h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
        h.save()
        return render(request, 'login.html',dato)
    except:
        return render(request, 'login.html')

# Dashboard    
def Showdashboard(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            dato = {'correo' : request.session["correo"]}
            return render(request, 'dashboard.html',dato)
            
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
# categoria producto
def ShowCategoria(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            opcategoria = Categoria.objects.all().values().order_by("nombre")
            dato = {'opcategoria': opcategoria,'correo' : request.session["correo"]}
            return render(request, 'gestionar_categoria.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


def RegisterCategoria(request):
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
                    categoria = data.get("categoria_")
                    test = Categoria.objects.filter(nombre=categoria)
                    if test:
                        dato = {'r2' : 'La Categoria  ( '+categoria+' ) Ya Existe No Se puede Repetir','correo' : request.session["correo"]}
                        return render(request, 'agregar_pro.html',dato)             
                    else:
                        des = "Registro de Categoria realizado ("+categoria+")"
                        date = datetime.now()
                        usuario = cor.upper()
                        h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                        h.save()

                        c = Categoria(nombre=categoria)
                        c.save()

                        opcategoria = Categoria.objects.all().values().order_by("nombre")
                        opesta = Estado_Producto.objects.all().values().order_by("estado")
                        opalumno = Alumno.objects.all().values().order_by("rut")
                        dato = {'opalumno' : opalumno,'opesta' : opesta,'opcategoria' : opcategoria,  'r':"Alumno Registrado Correctamente",'correo' : request.session["correo"]}
                        return render(request, 'agregar_pro.html', dato)
                except:
                    u = Alumno.objects.all().values().order_by("nombres")
                    dato = {'u' : u , 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'listado_alu.html', dato)
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
    
def RegisterCategoria2(request):
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
                    nombre = data.get("nombre_")
                    descripcion = data.get("descripcion_")
                    id_ = data.get("id_")
                    des = "Modificacion del la Categoria ("+nombre+")"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()
                    
                    c = Categoria.objects.get(id=id_)
                    c.nombre = nombre
                    c.descripcion = descripcion
                    c.save()

                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    dato = {'opcategoria' : opcategoria, 'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
                    return render(request, 'gestionar_categoria.html', dato)

                except:       
                    opcategoria = Categoria.objects.all().values().order_by("nombre")         
                    dato = {'opcategoria' : opcategoria, 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'gestionar_categoria.html', dato)
            else:
                dato = {'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = {'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)  

def DeleteC(request, id):
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


#alumno
def ShowGestionAlumno(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            a = Alumno.objects.all().values().order_by("nombres")
            dato = {'a': a,'correo' : request.session["correo"]}
            return render(request, 'gestionar_alumno.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


def RegisterAlumno(request):
    if request.method == 'POST':
        check = request.session.get("status")
        cor = request.session.get("correo")
        if check is True:
            try:
                u = User.objects.get(email=cor)
            except User.DoesNotExist:
                u = None
            if u is not None:
                rut = request.POST['rut']
                noms = request.POST['textnoms']
                apes = request.POST['textapes']
                cur = request.POST['textcur']
                sal = request.POST['textsal']
                if(len(rut)<10):
                        rut = rut.rjust(10, '0')
                test = Alumno.objects.filter(rut=rut)
                if test:
                    a = Alumno.objects.all().values().order_by("nombres")
                    dato = {'a': a,'r2' : 'El Alumno Con Rut ( '+rut+' ) Ya Existe No Se puede Repetir','correo' : request.session["correo"]}
                    return render(request, 'gestionar_alumno.html',dato)             
                else:
                    des = "Registro del alumno realizado ("+rut.upper()+")"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()
                    
                    u = Alumno(rut=rut, nombres=noms,lastnombre=apes,curso=cur,salon=sal)
                    u.save()
                    a = Alumno.objects.all().values().order_by("nombres")
                    dato = {'a': a, 'r' : 'Alumno Registrado Correctamente','correo' : request.session["correo"]}
                    return render(request, 'gestionar_alumno.html',dato)
                
            else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
            
        else:
            dato = { 'r2' : 'Debe estar logueado para acceder' }
            return render(request, 'login.html', dato)  
               
    else:
        dato = {'r2' : 'No se puede acceder por URL'}
        return render(request, 'login.html',dato)
    
def RegisterAlumno2(request):
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
                    id_ = data.get("id_")
                    if(len(rut)<10):
                        rut = rut.rjust(10, '0')

                    des = "Modificacion del Alumno ("+rut.upper()+")"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()
                    
                    a = Alumno.objects.get(id=id_)
                    a.rut = rut
                    a.nombres = noms
                    a.lastnombre = apes
                    a.curso = cur
                    a.salon = sal
                    a.save()

                    a = Alumno.objects.all().values().order_by("nombres")
                    dato = {'a' : a ,  'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
                    return render(request, 'gestionar_alumno.html', dato)

                except:
                    a = Alumno.objects.all().values().order_by("nombres")
                    dato = {'a' : a , 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'gestionar_alumno.html', dato)
            else:
                dato = {'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def DeleteA(request, id):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            try:
                a = Alumno.objects.get(id=id)
                rut = a.rut
                a.delete()

                a = Alumno.objects.all().values().order_by("nombres")
                dato = {'a' : a ,'r' : 'El Alumno '+ rut +' Fue Eliminado Correctamente', 'u': u,'correo' : request.session["correo"]}
                return render(request, 'gestionar_alumno.html',dato)
            except:
                a = Alumno.objects.all().values().order_by("correo")
                dato = {'a' : a ,'r2' : "El Alumno No Existe", 'u': u,'correo' : request.session["correo"]}
                return render(request, 'gestionar_alumno.html',dato)
        else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def DeleteA2(request, id):
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
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            p = Proveedor.objects.all().values().order_by("nombre")
            dato = {'p': p,'correo' : request.session["correo"]}
            return render(request, 'gestionar_proveedor.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


def RegisterProveedores(request):
    if request.method == 'POST':
        check = request.session.get("status")
        cor = request.session.get("correo")
        if check is True:
            try:
                u = User.objects.get(email=cor)
            except User.DoesNotExist:
                u = None
            if u is not None:
                nom = request.POST['nom']
                tel = request.POST['tel']
                ema = request.POST['ema']
                dir = request.POST['dir']
                test = Proveedor.objects.filter(nombre=nom, telefono=tel, email=ema, direccion=dir)
                if test:
                    p = Proveedor.objects.all().values().order_by("nombre")
                    dato = {'p': p,'r2' : 'El Proveedor ( '+nom+' ) Ya Existe No Se puede Repetir','correo' : request.session["correo"]}
                    return render(request, 'gestionar_proveedor.html',dato)             
                else:
                    des = "Registro del Proveedor realizado ("+nom+")"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    p = Proveedor(nombre=nom, telefono=tel, email=ema, direccion=dir)
                    p.save()
                    p = Proveedor.objects.all().values().order_by("nombre")
                    dato = {'p': p, 'r' : 'Proveedor Registrado Correctamente','correo' : request.session["correo"]}
                    return render(request, 'gestionar_proveedor.html',dato)
                
            else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
            
        else:
            dato = { 'r2' : 'Debe estar logueado para acceder' }
            return render(request, 'login.html', dato)  
               
    else:
        dato = {'r2' : 'No se puede acceder por URL'}
        return render(request, 'login.html',dato)
    
def RegisterProveedores2(request):
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
                    tel = data.get("tel_")
                    ema = data.get("ema_")
                    dir = data.get("dir_")
                    id_ = data.get("id_")
                    des = "Modificacion del Proveedor ("+nom+")"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()
                    
                    
                    p = Proveedor.objects.get(id=id_)
                    p.nombre = nom
                    p.telefono = tel
                    p.email = ema
                    p.direccion = dir
                    p.save()
                    

                    p = Proveedor.objects.all().values().order_by("nombre")
                    dato = {'p' : p ,  'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
                    return render(request, 'gestionar_proveedor.html', dato)

                except:
                    p = Proveedor.objects.all().values().order_by("nombre")
                    dato = {'p' : p , 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'gestionar_proveedor.html', dato)
            else:
                dato = {'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def DeleteProveedores(request, id):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            try:
                p = Proveedor.objects.get(id=id)
                nom = p.nombre
                p.delete()

                p = Proveedor.objects.all().values().order_by("nombre")
                dato = {'p' : p ,'r' : 'El Proveedor '+ nom +' Fue Eliminado Correctamente', 'u': u,'correo' : request.session["correo"]}
                return render(request, 'gestionar_proveedor.html',dato)
            except:
                p = Proveedor.objects.all().values().order_by("nombre")
                dato = {'p' : p ,'r2' : "El Alumno No Existe", 'u': u,'correo' : request.session["correo"]}
                return render(request, 'gestionar_proveedor.html',dato)
        else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def DeleteProveedores2(request, id):
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
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
            p2 = Producto.objects.all().values().order_by("nombre")
            categoria = Categoria.objects.all().values().order_by("nombre")
            estado = Estado_Producto.objects.all().values().order_by("estado")
            alumno = Alumno.objects.all().values().order_by("nombres")
            proveedor = Proveedor.objects.all().values().order_by("nombre")
            dato = {'p2': p2,'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor,'correo' : request.session["correo"]}
            return render(request, 'gestionar_producto.html',dato)
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
                    dato = {'r2' : 'El Producto Llamado ( '+nom+' ) Ya Existe No Se puede Repetir','correo' : request.session["correo"]}
                    return render(request, 'gestionar_producto.html',dato)
                else:
                    des = "Registro del producto ("+nom.lower()+")"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    p = Producto(nombre=nom, descripcion=desu, categoria_id=cat,proveedor_id=pro, cantidad=can, precio_unitario=pre, razon_ingreso=raz, estado_producto_id=est, estado_habil='activo', fecha_ingreso=datetime.now(),fecha_modificacion=datetime.now(), rut_alumno_id=rut)
                    p.save()
                    p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
                    categoria = Categoria.objects.all().values().order_by("nombre")
                    estado = Estado_Producto.objects.all().values().order_by("estado")
                    alumno = Alumno.objects.all().values().order_by("nombres")
                    proveedor = Proveedor.objects.all().values().order_by("nombre")
                    dato = {'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor, 'r' : 'Registro Realizado Correctamente','correo' : request.session["correo"]}
                    return render(request, 'gestionar_producto.html',dato)
            else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'Debe estar logueado para acceder' }
            return render(request, 'login.html', dato)         
    else:
        dato = {'r2' : 'No se puede acceder por URL'}
        return render(request, 'login.html',dato)
    



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
                    desu = data.get("des_")
                    cat = data.get("cat_")
                    pro = data.get("pro_")
                    can = data.get("can_")
                    pre = data.get("pre_")
                    raz = data.get("raz_")
                    est = data.get("est_")
                    rut = data.get("rut_")
                    id_ = data.get("id_")

                    des = "Modificacion del producto ("+nom.lower()+")"
                    date = datetime.now()
                    usuario = cor.upper()
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
                    p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
                    categoria = Categoria.objects.all().values().order_by("nombre")
                    estado = Estado_Producto.objects.all().values().order_by("estado")
                    alumno = Alumno.objects.all().values().order_by("nombres")
                    proveedor = Proveedor.objects.all().values().order_by("nombre")
                    dato = {'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor, 'r' : 'Modicado Correctamente','correo' : request.session["correo"]}
                    return render(request, 'gestionar_producto.html',dato)

                except:
                    p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
                    categoria = Categoria.objects.all().values().order_by("nombre")
                    estado = Estado_Producto.objects.all().values().order_by("estado")
                    alumno = Alumno.objects.all().values().order_by("nombres")
                    proveedor = Proveedor.objects.all().values().order_by("nombre")
                    dato = {'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor, 'r2' : '???','correo' : request.session["correo"]}
                    return render(request, 'gestionar_producto.html',dato)
            else:
                dato = {'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
def PlusProducto(request):
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
    
def MinusProducto(request):
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
                date = datetime.now()
                usuario = cor.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()

                p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
                categoria = Categoria.objects.all().values().order_by("nombre")
                estado = Estado_Producto.objects.all().values().order_by("estado")
                alumno = Alumno.objects.all().values().order_by("nombres")
                proveedor = Proveedor.objects.all().values().order_by("nombre")
                dato = {'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor, 'r' : 'El Producto '+ nom +' Fue Eliminado Correctamente','correo' : request.session["correo"]}
                return render(request, 'gestionar_producto.html',dato)
            except:
                p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
                categoria = Categoria.objects.all().values().order_by("nombre")
                estado = Estado_Producto.objects.all().values().order_by("estado")
                alumno = Alumno.objects.all().values().order_by("nombres")
                proveedor = Proveedor.objects.all().values().order_by("nombre")
                dato = {'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor,'r2' : "El Producto No Existe",'correo' : request.session["correo"]}
                return render(request, 'gestionar_producto.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def DisableP(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
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

                des = "Desactivado del producto ("+nom.lower()+")"
                date = datetime.now()
                usuario = cor.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()

                p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
                categoria = Categoria.objects.all().values().order_by("nombre")
                estado = Estado_Producto.objects.all().values().order_by("estado")
                alumno = Alumno.objects.all().values().order_by("nombres")
                proveedor = Proveedor.objects.all().values().order_by("nombre")
                dato = {'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor,'r' : 'El Producto '+ nom +' Fue Desactivado Correctamente','correo' : request.session["correo"]}
                return render(request, 'dashboard.html',dato)
            except:
                p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
                categoria = Categoria.objects.all().values().order_by("nombre")
                estado = Estado_Producto.objects.all().values().order_by("estado")
                alumno = Alumno.objects.all().values().order_by("nombres")
                proveedor = Proveedor.objects.all().values().order_by("nombre")
                dato = {'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor,'r2' : "El Producto No Existe",'correo' : request.session["correo"]}
                return render(request, 'dashboard.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
def EnableP(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            try:
                data = json.loads(request.body) 
                id = data.get("id_")
                p = Producto.objects.get(id=id)
                nom = p.nombre
                print("a")
                p.razon_egreso = ''
                print("b")
                p.fecha_egreso = None
                print("c")
                p.estado_habil = 'activo'
                print("d")
                p.save()
                print("e")
                des = "Activado del producto ("+nom.lower()+")"
                date = datetime.now()
                usuario = cor.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()

                p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
                categoria = Categoria.objects.all().values().order_by("nombre")
                estado = Estado_Producto.objects.all().values().order_by("estado")
                alumno = Alumno.objects.all().values().order_by("nombres")
                proveedor = Proveedor.objects.all().values().order_by("nombre")
                dato = {'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor,'correo' : request.session["correo"]}
                return render(request, 'dashboard.html',dato)
            except:
                p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
                categoria = Categoria.objects.all().values().order_by("nombre")
                estado = Estado_Producto.objects.all().values().order_by("estado")
                alumno = Alumno.objects.all().values().order_by("nombres")
                proveedor = Proveedor.objects.all().values().order_by("nombre")
                dato = {'p': p,'categoria': categoria,'estado': estado,'alumno': alumno,'proveedor': proveedor,'r2' : "El Producto No Existe",'correo' : request.session["correo"]}
                return render(request, 'dashboard.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)



def DeleteC2(request, id):
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
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            s = Movimiento.objects.select_related('producto').all().order_by("-fecha")
            producto = Producto.objects.all().values().order_by("nombre")
            dato = {'s': s,'producto': producto, 'correo' : request.session["correo"]}
            return render(request, 'gestionar_stock.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


def RegisterStock(request):
    if request.method == 'POST':
        check = request.session.get("status")
        cor = request.session.get("correo")
        if check is True:
            try:
                u = User.objects.get(email=cor)
            except User.DoesNotExist:
                u = None
            if u is not None:
                pro = request.POST['pro']
                can = request.POST['can']
                tip = request.POST['tip']
                raz = request.POST['raz']       

                if tip =='Entrada':
                    des = "Agregando stock al Producto ("+pro.upper()+")"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    s = Movimiento(producto_id=pro, cantidad=can, tipo=tip, razon=raz)
                    s.save()
                    p = Producto.objects.get(id=pro)
                    p.agregar_stock(int(can))
                    s = Movimiento.objects.select_related('producto').all().order_by("-fecha")
                    producto = Producto.objects.all().values().order_by("nombre")
                    dato = {'s': s,'producto': producto, 'r' : 'Usuario Registrado Correctamente','correo' : request.session["correo"]}
                    return render(request, 'gestionar_stock.html',dato)
                else:
                    des = "Descontado stock al Producto ("+pro.upper()+")"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    s = Movimiento(producto_id=pro, cantidad=can, tipo=tip, razon=raz)
                    s.save()
                    p = Producto.objects.get(id=pro)
                    p.restar_stock(int(can))
                    s = Movimiento.objects.select_related('producto').all().order_by("-fecha")
                    producto = Producto.objects.all().values().order_by("nombre")
                    dato = {'s': s,'producto': producto, 'r' : 'Usuario Registrado Correctamente','correo' : request.session["correo"]}
                    return render(request, 'gestionar_stock.html',dato)
                
            else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
            
        else:
            dato = { 'r2' : 'Debe estar logueado para acceder' }
            return render(request, 'login.html', dato)  
               
    else:
        dato = {'r2' : 'No se puede acceder por URL'}
        return render(request, 'login.html',dato)
    

def UpdateS(request):
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
                    tip = data.get("tip_")
                    creusu = data.get("creaalu_")
                    creest = data.get('creaest_')
                    pas.encode("ascii")
                    pasby = bytes(pas, encoding='utf-8')
                    pas_encode64 = base64.b64encode(pasby)
                    encode = pas_encode64.decode('ascii')
                    id_ = data.get("id_")

                    des = "Modificacion del usuario ("+corr.upper()+")"
                    table = "Usuario"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    u = Usuario.objects.get(id=id_)
                    u.correo = corr
                    u.password = encode
                    u.tipo_id = tip
                    u.create_alumno = creusu
                    u.create_estado = creest
                    u.save()

                    u = Usuario.objects.select_related('tipo').all().order_by("correo")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    dato = {'opcategoria':opcategoria, 'u' : u ,  'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
                    return render(request, 'gestionar_stock.html', dato)

                except:
                    u = Usuario.objects.select_related('tipo').all().order_by("correo")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    dato = {'opcategoria':opcategoria, 'u' : u , 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'gestionar_stock.html', dato)
            else:
                dato = { 'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def DeleteS(request, id):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            try:
                u = Usuario.objects.get(id=id)
                corr = u.correo
                u.delete()

                u = Usuario.objects.select_related('tipo').all().order_by("correo")
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                dato = {'opcategoria':opcategoria, 'r' : 'El Usuario '+ corr +' Fue Eliminado Correctamente', 'u': u,'correo' : request.session["correo"]}
                return render(request, 'listado_usu.html',dato)
            except:
                u = Usuario.objects.select_related('tipo').all().order_by("correo")
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                dato = {'opcategoria':opcategoria, 'r2' : "El Usuario No Existe", 'u': u,'correo' : request.session["correo"]}
                return render(request, 'listado_usu.html',dato)
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
            u = Usuario.objects.select_related('tipo').all().order_by("correo")
            opcategoria = Categoria.objects.all().values().order_by("nombre")
            dato = {'opcategoria':opcategoria, 'u': u, 'correo' : request.session["correo"]}
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
                tip = request.POST['txtcategorias']
                try:
                    crealu = request.POST['crearalumnos']
                    crealu = True 
                except:
                    crealu = False
                try:  
                    creaest = request.POST['crearestados']
                    creaest = True
                except:
                    creaest = False
                if tpas1 != tpas2:
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    dato = {'opcategoria':opcategoria,'r2' : 'Las constraseñas no coinciden','correo' : request.session["correo"]}
                    return render(request, 'agregar_usu.html',dato)
                test = Usuario.objects.filter(correo=corr)
                if test:
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    dato = {'opcategoria':opcategoria,'r2' : 'El Correo ( '+corr+' ) Ya Existe No Se puede Repetir','correo' : request.session["correo"]}
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
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    u = Usuario(correo=corr, password=encode, tipo_id=tip, create_alumno=crealu, create_estado=creaest)
                    u.save()
                    u = Usuario.objects.select_related('tipo').all().order_by("correo")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    dato = {'opcategoria':opcategoria, 'u': u, 'r' : 'Usuario Registrado Correctamente','correo' : request.session["correo"]}
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
            opcategoria = Categoria.objects.all().values().order_by("nombre")
            dato = {'opcategoria': opcategoria,'correo' : request.session["correo"]}
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
                    tip = data.get("tip_")
                    creusu = data.get("creaalu_")
                    creest = data.get('creaest_')
                    pas.encode("ascii")
                    pasby = bytes(pas, encoding='utf-8')
                    pas_encode64 = base64.b64encode(pasby)
                    encode = pas_encode64.decode('ascii')
                    id_ = data.get("id_")

                    des = "Modificacion del usuario ("+corr.upper()+")"
                    table = "Usuario"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    u = Usuario.objects.get(id=id_)
                    u.correo = corr
                    u.password = encode
                    u.tipo_id = tip
                    u.create_alumno = creusu
                    u.create_estado = creest
                    u.save()

                    u = Usuario.objects.select_related('tipo').all().order_by("correo")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    dato = {'opcategoria':opcategoria, 'u' : u ,  'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
                    return render(request, 'listado_usu.html', dato)

                except:
                    u = Usuario.objects.select_related('tipo').all().order_by("correo")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    dato = {'opcategoria':opcategoria, 'u' : u , 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'listado_usu.html', dato)
            else:
                dato = { 'r2' : "No puedes acceder Por url" }
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
        if u is not None:
            try:
                u = Usuario.objects.get(id=id)
                corr = u.correo
                u.delete()

                u = Usuario.objects.select_related('tipo').all().order_by("correo")
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                dato = {'opcategoria':opcategoria, 'r' : 'El Usuario '+ corr +' Fue Eliminado Correctamente', 'u': u,'correo' : request.session["correo"]}
                return render(request, 'listado_usu.html',dato)
            except:
                u = Usuario.objects.select_related('tipo').all().order_by("correo")
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                dato = {'opcategoria':opcategoria, 'r2' : "El Usuario No Existe", 'u': u,'correo' : request.session["correo"]}
                return render(request, 'listado_usu.html',dato)
        else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


# estado producto
def RegisterEstado_Producto(request):
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

def UpdateE(request):
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

def DeleteE(request, id):
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
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is not None:
            h = Historial_acciones.objects.all().order_by("-fecha")
            dato = {'h': h,'correo' : request.session["correo"]}
            return render(request, 'listado_his.html',dato)
            
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
# Usuario
def ShowUsuarioMenu(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    tip = request.session.get("tipo")
    try:
        u = User.objects.get(email=cor)
    except User.DoesNotExist:
        u = None
    if u is None:
        if check:
            p = Producto.objects.filter(categoria_id=tip).select_related('categoria','estado_producto','rut_alumno').all().order_by("nombre")
            opesta = Estado_Producto.objects.all().values().order_by("estado")
            opalumno = Alumno.objects.all().values().order_by("rut")
            dato = {'opesta':opesta, 'opalumno':opalumno, 'tip':tip,'p': p,'correo' : request.session["correo"]}
            return render(request, 'usuario.html',dato)
        else:
            dato = {'r2' : 'Debe estar logueado para acceder'}
            return render(request, 'login.html',dato)
    else:
        dato = { 'r2' : 'No puedes acceder esa funcion' }
        return render(request, 'login.html', dato)
    
def RegisterProductoUsu(request):
    if request.method == 'POST':
        check = request.session.get("status")
        cor = request.session.get("correo")
        tip = request.session.get("tipo")
        if check is True:
            try:
                u = User.objects.get(email=cor)
            except User.DoesNotExist:
                u = None
            if u is None:
                nom = request.POST['txtnombre']
                desu = request.POST['txtdescipcion']
                cat = tip
                can = request.POST['cantidad']
                pre = request.POST['precio']
                raz = request.POST['opt']
                est = request.POST['txtestados']
                rut = request.POST['txtrutss']
                test = Producto.objects.filter(nombre=nom)
                if test:
                    dato = {'r2' : 'El Producto Llamado ( '+nom+' ) Ya Existe No Se puede Repetir','correo' : request.session["correo"]}
                    return render(request, 'agregar_pro.html',dato)
                else:
                    des = "Registro del producto ("+nom.lower()+")"
                    table = "Producto"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    p = Producto(nombre=nom, descripcion=desu, categoria_id=cat, cantidad=can, precio=pre, razon_ingreso=raz, estado_producto_id=est, estado_habil='activo', fecha_ingreso=datetime.now(),fecha_modificacion=datetime.now(), rut_alumno_id=rut)
                    p.save()
                    p = Producto.objects.select_related('categoria','estado_producto','rut_alumno','proveedor').all().order_by("nombre")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    opesta = Estado_Producto.objects.all().values().order_by("estado")
                    opalumno = Alumno.objects.all().values().order_by("rut")
                    dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta,'p': p, 'r' : 'Registro Realizado Correctamente','correo' : request.session["correo"]}
                    return render(request, 'usuario.html',dato)
            else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'Debe estar logueado para acceder' }
            return render(request, 'login.html', dato)         
    else:
        dato = {'r2' : 'No se puede acceder por URL'}
        return render(request, 'login.html',dato)
       
def UpdateP2(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is None:
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) 
                    nom = data.get("nom_")
                    desu = data.get("des_")
                    cat = data.get("cat_")
                    can = data.get("can_")
                    pre = data.get("pre_")
                    raz = data.get("raz_")
                    est = data.get("est_")
                    rut = data.get("rut_")
                    id_ = data.get("id_")

                    des = "Modificacion del producto ("+nom.lower()+")"
                    table = "Producto"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()

                    p = Producto.objects.get(id=id_)
                    p.nombre = nom
                    p.descripcion = desu
                    p.categoria_id = cat
                    p.cantidad = can
                    p.precio = pre
                    p.razon_ingreso = raz
                    p.estado_producto_id = est
                    p.fecha_modificacion = datetime.now()
                    p.rut_alumno_id = rut
                    p.save()
                    p = Producto.objects.select_related('categoria','estado_producto','rut_alumno').all().values().order_by("nombre")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    opesta = Estado_Producto.objects.all().values().order_by("estado")
                    opalumno = Alumno.objects.all().values().order_by("rut")
                    dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta, 'p' : p , 'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
                    return render(request, 'usuario.html', dato)

                except:
                    p = Producto.objects.select_related('categoria','estado_producto','rut_alumno').all().values().order_by("nombre")
                    opcategoria = Categoria.objects.all().values().order_by("nombre")
                    opesta = Estado_Producto.objects.all().values().order_by("estado")
                    opalumno = Alumno.objects.all().values().order_by("rut")
                    dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta, 'p' : p , 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'usuario.html', dato)
            else:
                dato = {'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


def DeleteP2(request, id):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is None:
            try:
                p = Producto.objects.get(id=id)
                nom = p.nombre
                p.delete()

                des = "Eliminado del producto ("+nom.lower()+")"
                table = "Producto"
                date = datetime.now()
                usuario = cor.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()

                p = Producto.objects.select_related('categoria','estado_producto','rut_alumno').all().values().order_by("nombre")
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'r' : 'El Producto '+ nom +' Fue Eliminado Correctamente', 'p': p,'correo' : request.session["correo"]}
                return render(request, 'usuario.html',dato)
            except:
                p = Producto.select_related('categoria','estado_producto','rut_alumno').objects.all().values().order_by("nombre")
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta, 'p' : p ,'r2' : "El Producto No Existe",'correo' : request.session["correo"]}
                return render(request, 'usuario.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def DisableP2(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is None:
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

                des = "Desactivado del producto ("+nom.lower()+")"
                table = "Producto"
                date = datetime.now()
                usuario = cor.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()

                p = Producto.objects.select_related('categoria','estado_producto','rut_alumno').all().values().order_by("nombre")
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'r' : 'El Producto '+ nom +' Fue Desactivado Correctamente', 'p': p,'correo' : request.session["correo"]}
                return render(request, 'usuario.html',dato)
            except:
                p = Producto.objects.select_related('categoria','estado_producto','rut_alumno').all().values().order_by("nombre")
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta, 'p' : p ,'r2' : "El Producto No Existe",'correo' : request.session["correo"]}
                return render(request, 'usuario.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
def EnableP2(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is None:
            try:
                data = json.loads(request.body) 
                id = data.get("id_")
                p = Producto.objects.get(id=id)
                nom = p.nombre
                print("a")
                p.razon_egreso = ''
                print("b")
                p.fecha_egreso = None
                print("c")
                p.estado_habil = 'activo'
                print("d")
                p.save()
                print("e")
                des = "Activado del producto ("+nom.lower()+")"
                table = "Producto"
                date = datetime.now()
                usuario = cor.upper()
                h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                h.save()

                p = Producto.objects.select_related('categoria','estado_producto','rut_alumno').all().values().order_by("nombre")
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'r' : 'El Producto '+ nom +' Fue Activado Correctamente', 'p': p,'correo' : request.session["correo"]}
                return render(request, 'usuario.html',dato)
            except:
                p = Producto.objects.select_related('categoria','estado_producto','rut_alumno').all().values().order_by("nombre")
                opcategoria = Categoria.objects.all().values().order_by("nombre")
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'opalumno': opalumno,'opcategoria': opcategoria,'opesta': opesta, 'p' : p ,'r2' : "El Producto No Existe",'correo' : request.session["correo"]}
                return render(request, 'usuario.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
def ShowRegisterProductoUsu(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is None:
            u = Usuario.objects.get(correo=cor)
            a = u.create_alumno
            b = u.create_estado
            opesta = Estado_Producto.objects.all().values().order_by("estado")
            opalumno = Alumno.objects.all().values().order_by("rut")
            dato = {'opalumno': opalumno,'opesta': opesta,'a' : a,'b':b,'correo' : request.session["correo"]}
            return render(request, 'usuario_agregar_pro.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)    

def RegisterAlumnoUsu(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is None:
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
                        table = "Alumno"
                        date = datetime.now()
                        usuario = cor.upper()
                        h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                        h.save()

                        u = Alumno(rut=rut, nombres=noms,lastnombre=apes,curso=cur,salon=sal)
                        u.save()

                        dato = {'r':"Alumno Registrado Correctamente",'correo' : request.session["correo"]}
                        return render(request, 'usuario_agregar_pro.html', dato)

                except:
                    u = Alumno.objects.all().values().order_by("nombres")
                    dato = {'u' : u , 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'usuario_agregar_pro.html', dato)
            else:
                dato = { 'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)
    
def UpdateAUsu(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is None:
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) 
                    rut = data.get("rut_")
                    noms = data.get("noms_")
                    apes = data.get("apes_")
                    cur = data.get("cur_")
                    sal = data.get("sal_")
                    id_ = data.get("id_")
                    des = "Modificacion del Alumno ("+rut.upper()+")"
                    table = "Alumno"
                    date = datetime.now()
                    usuario = cor.upper()
                    h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                    h.save()
                    
                    u = Alumno.objects.get(id=id_)
                    u.rut = rut
                    u.nombres = noms
                    u.lastnombre = apes
                    u.curso = cur
                    u.salon = sal
                    u.save()

                    u = Alumno.objects.all().values().order_by("nombres")
                    dato = {'u' : u ,  'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
                    return render(request, 'usuario.html', dato)

                except:
                    u = Alumno.objects.all().values().order_by("nombres")
                    
                    dato = {'u' : u , 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'usuario.html', dato)
            else:
                dato = {'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def DeleteAUsu(request, id):
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

                u = Alumno.objects.all().values().order_by("nombres")

                dato = {'r' : 'El Alumno '+ rut +' Fue Eliminado Correctamente', 'u': u,'correo' : request.session["correo"]}
                return render(request, 'listado_alu.html',dato)
            except:
                u = Usuario.objects.all().values().order_by("correo")

                dato = {'r2' : "El Alumno No Existe", 'u': u,'correo' : request.session["correo"]}
                return render(request, 'listado_alu.html',dato)
        else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def RegisterEstado_ProductoUsu(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is None:
            if request.method == 'POST':
                try:
                    data = json.loads(request.body) 
                    estado = data.get("estado_")
                    test = Estado_Producto.objects.filter(estado=estado)
                    if test:
                        dato = {'r2' : 'El Estado  ( '+estado+' ) Ya Existe No Se puede Repetir','correo' : request.session["correo"]}
                        return render(request, 'usuario_agregar_pro.html',dato)             
                    else:
                        des = "Registro del Estado realizado ("+estado+")"
                        table = "estado"
                        date = datetime.now()
                        usuario = cor.upper()
                        h = Historial_acciones(descripcion=des, fecha=date, usuario=usuario)
                        h.save()

                        e = Estado_Producto(estado=estado)
                        e.save()

                        opesta = Estado_Producto.objects.all().values().order_by("estado")
                        opalumno = Alumno.objects.all().values().order_by("rut")
                        dato = {'opalumno' : opalumno,'opesta' : opesta, 'r':"Alumno Registrado Correctamente",'correo' : request.session["correo"]}
                        return render(request, 'usuario_agregar_pro.html', dato)

                except:
                    dato = { 'r2' : "No Existen Datos",'correo' : request.session["correo"] }
                    return render(request, 'usuario_agregar_pro.html', dato)
            else:
                dato = {'r2' : "No puedes acceder Por url" }
                return render(request, 'login.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)

def UpdateEUsu(request):
    check = request.session.get("status")
    cor = request.session.get("correo")
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is None:
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

                    opesta = Estado_Producto.objects.all().values().order_by("estado")
                    opalumno = Alumno.objects.all().values().order_by("rut")
                    dato = {'opalumno' : opalumno,'opesta' : opesta, 'r':"Datos Modificados Correctamente",'correo' : request.session["correo"]}
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

def DeleteEUsu(request, id):
    check = request.session.get("status")
    cor = request.session.get("correo")
    
    if check is True:
        try:
            u = User.objects.get(email=cor)
        except User.DoesNotExist:
            u = None
        if u is None:
            try:
                u = Estado_Producto.objects.get(id=id)
                estado = u.estado
                u.delete()

                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'opalumno': opalumno,'opesta': opesta,'r' : 'El Estado : '+ estado +' Fue Eliminado Correctamente','correo' : request.session["correo"]}
                return render(request, 'agregar_pro.html',dato)
            except:
                opesta = Estado_Producto.objects.all().values().order_by("estado")
                opalumno = Alumno.objects.all().values().order_by("rut")
                dato = {'opalumno': opalumno,'opesta': opesta,'r2' : "El Alumno No Existe",'correo' : request.session["correo"]}
                return render(request, 'agregar_pro.html',dato)
        else:
                dato = { 'r2' : 'No puedes acceder esa funcion' }
                return render(request, 'login.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'login.html', dato)


