from django.shortcuts import render

from hotel.models import His, Hotel, Usuario, Size, Nroom

from datetime import datetime
# Create your views here.

def ShowIndex(request):
    return render(request, 'index.html')





def Login(request):
    if request.method == "POST":
        nom = request.POST["nom"]
        pas = request.POST["pas"]

        check = Usuario.objects.filter(nom=nom,pas=pas).values()
        if check:
            request.session['status'] = True
            request.session['id'] = check[0]['id']
            request.session["nomusu"] = nom.upper()

            dato = {'nomusu' : nom.upper()}

            des = "Inicia Sesión"
            table = ""
            date = datetime.now()
            usuario = request.session["id"]
            h = His(des=des, tableinfo=table, hour=date, usuario_id=usuario)
            h.save()

            if nom.upper() == 'ADMIN':
                return render(request, 'admin.html',dato)
            else:
                return render(request, 'usuario.html',dato)
        else:
            dato = {'r2' : 'Error El Usuario No Existe'}
            return render(request, 'index.html',dato)
    else:
            dato = {'r2' : 'No se puede acceder por URL'}
            return render(request, 'index.html',dato)





def Logout(request):
    try:
        nom = request.session['nomusu']
        del request.session['nomusu']
        del request.session['status']

        des = "Cierra Sesión"
        table = ""
        date = datetime.now()
        usuario = request.session["id"]
        h = His(des=des, tableinfo=table, hour=date, usuario_id=usuario)
        h.save()

        return render(request, 'index.html')
    except:
        return render(request, 'index.html')





def ShowAdmin(request):
    check = request.session.get("status")
    nom = request.session.get("nomusu")
    
    if check is True:
        if nom.upper() == 'ADMIN':
            dato = {'nomusu' : request.session["nomusu"]}
            return render(request, 'admin.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'index.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'index.html', dato)





def ShowRegisterSize(request):
    check = request.session.get('status')
    if check is True:
        if request.session['nomusu'].upper() == "ADMIN":
            sizes = Size.objects.all().values().order_by('nomsize')
            dato = {'nomusu' : request.session['nomusu'], 'sizes' : sizes}

            return render(request, 'registersize.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'index.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'index.html', dato)





def RegisterSize(request):
    if request.method == 'POST':
        nom = request.POST['txtsize'].upper()

        check = Size.objects.filter(nomsize=nom)
        if check:
            sizes = Size.objects.all().values().order_by("nomsize")

            dato = {'r2' : 'El Tamaño Llamado ( '+nom+' ) Ya Existe No Se puede Repetir', 'sizes': sizes, 'nomusu' : request.session['nomusu']}
            return render(request, 'registersize.html',dato)
        else:
            sizes =  Size(nomsize=nom)
            sizes.save()

            des = "Register tamaño realizado ("+nom.lower()+")"
            table = "Size"
            date = datetime.now()
            usuario = request.session["id"]
            h = His(des=des, tableinfo=table, hour=date, usuario_id=usuario)
            h.save()

            sizes = Size.objects.all().values().order_by("nomsize")

            dato = {'r' : 'Tamaño ( '+nom+' ) Registrado Correctamente', 'sizes': sizes, 'nomusu' : request.session['nomusu']}
            return render(request, 'registersize.html',dato)
    else:
        sizes = Size.objects.all().values().order_by("nomsize")

        dato = {'r2' : 'Debe Presionar El Botón Para Registrar Un Tamaño', 'sizes': sizes, 'nomusu' : request.session['nomusu']}
        return render(request, 'registersize.html',dato)





def ShowUpdateSize(request, id):
    try:
        check = request.session.get('status')
        if check is True:
            size = Size.objects.get(id=id)

            sizes = Size.objects.all().values().order_by('nomsize')

            dato = {'nomusu' : request.session['nomusu'], 'size' : size, 'sizes' : sizes}
            return render(request, 'updatesize.html',dato)
        else:
            dato = { 'r2' : 'Debe estar logueado para acceder' }
            return render(request, 'index.html', dato)
    except:
        sizes = Size.objects.all().values().order_by('nomsize')
        dato = {'nomusu' : request.session['nomusu'], 'r2' : "El Tamaño Con ID ("+str(id)+") No Existe", 'sizes' : sizes}
        return render(request, 'registersize.html',dato)





def UpdateSize(request, id):
    try:
        nom =request.POST['txtsize'].upper()

        size = Size.objects.get(id=id)
        size.nomsize = nom
        size.save()

        des = "Update tamaño realizado ("+nom.lower()+")"
        table = "Size"
        date = datetime.now()
        usuario = request.session["id"]
        h = His(des=des, tableinfo=table, hour=date, usuario_id=usuario)
        h.save()

        sizes = Size.objects.all().values().order_by("nomsize")

        dato = {'r' : 'Tamaño Actualizado Correctamente', 'sizes': sizes, 'nomusu' : request.session['nomusu']}
        return render(request, 'registersize.html',dato)

    except:
        sizes = Size.objects.all().values().order_by("nomsize")

        dato = {'r2' : "El Tamaño Con ID ("+str(id)+") No Existe", 'sizes': sizes, 'nomusu' : request.session['nomusu']}
        return render(request, 'registersize.html',dato)





def DeteleSize(request, id):
    try:
        size = Size.objects.get(id=id)
        nom = size.nomsize
        size.delete()

        des = "Delete tamaño realizado ("+nom.lower()+")"
        table = "Size"
        date = datetime.now()
        usuario = request.session["id"]
        h = His(des=des, tableinfo=table, hour=date, usuario_id=usuario)
        h.save()

        sizes = Size.objects.all().values().order_by("nomsize")

        dato = {'r' : 'Tamaño Eliminado Correctamente', 'sizes': sizes, 'nomusu' : request.session['nomusu']}
        return render(request, 'registersize.html',dato)
    except:
        sizes = Size.objects.all().values().order_by("nomsize")

        dato = {'r2' : "El Tamaño Con ID ("+str(id)+") No Existe", 'sizes': sizes, 'nomusu' : request.session['nomusu']}
        return render(request, 'registersize.html',dato)




def ShowRegisterRoom(request):
    check = request.session.get('status')
    if check is True:
        if request.session['nomusu'].upper() == "ADMIN":
            room = Nroom.objects.all().values().order_by('nomcroom')
            dato = {'nomusu' : request.session['nomusu'], 'room' : room}

            return render(request, 'registerroom.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'index.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'index.html', dato)





def RegisterRoom(request):
    if request.method == 'POST':
        nom = request.POST['txtroom'].upper()

        check = Nroom.objects.filter(nomcroom=nom)
        if check:
            room = Nroom.objects.all().values().order_by("nomcroom")

            dato = {'r2' : 'Las Habitaciones Llamada ( '+nom+' ) Ya Existe No Se puede Repetir', 'room': room, 'nomusu' : request.session['nomusu']}
            return render(request, 'registerroom.html',dato)
        else:
            room =  Nroom(nomcroom=nom)
            room.save()

            des = "Register Habitaciones realizado ("+nom.lower()+")"
            table = "Nroom"
            date = datetime.now()
            usuario = request.session["id"]
            h = His(des=des, tableinfo=table, hour=date, usuario_id=usuario)
            h.save()

            room = Nroom.objects.all().values().order_by("nomcroom")

            dato = {'r' : 'Habitaciones ( '+nom+' ) Registrado Correctamente', 'room': room, 'nomusu' : request.session['nomusu']}
            return render(request, 'registerroom.html',dato)
    else:
        room = Nroom.objects.all().values().order_by("nomcroom")

        dato = {'r2' : 'Debe Presionar El Botón Para Registrar Algunas Habitaciones', 'room': room, 'nomusu' : request.session['nomusu']}
        return render(request, 'registerroom.html',dato)





def ShowUpdateRoom(request, id):
    try:
        check = request.session.get('status')
        if check is True:
            ro = Nroom.objects.get(id=id)

            room = Nroom.objects.all().values().order_by('nomcroom')

            dato = {'nomusu' : request.session['nomusu'], 'ro' : ro, 'room' : room}
            return render(request, 'updateroom.html',dato)
        else:
            dato = { 'r2' : 'Debe estar logueado para acceder' }
            return render(request, 'index.html', dato)
    except:
        room = Nroom.objects.all().values().order_by('nomcroom')
        dato = {'nomusu' : request.session['nomusu'], 'r2' : "Las Habitaciones Con ID ("+str(id)+") No Existe", 'room' : room}
        return render(request, 'registerroom.html',dato)





def UpdateRoom(request, id):
    try:
        nom =request.POST['txtroom'].upper()

        room = Nroom.objects.get(id=id)
        room.nomcroom = nom
        room.save()

        des = "Update Habitaciones realizado ("+nom.lower()+")"
        table = "Nroom"
        date = datetime.now()
        usuario = request.session["id"]
        h = His(des=des, tableinfo=table, hour=date, usuario_id=usuario)
        h.save()

        room = Nroom.objects.all().values().order_by("nomcroom")

        dato = {'r' : 'Habitaciones Actualizada Correctamente', 'room': room, 'nomusu' : request.session['nomusu']}
        return render(request, 'registerroom.html',dato)

    except:
        room = Nroom.objects.all().values().order_by("nomcroom")

        dato = {'r2' : "Las Habitaciones Con ID ("+str(id)+") No Existe", 'room': room, 'nomusu' : request.session['nomusu']}
        return render(request, 'registerroom.html',dato)





def DeteleRoom(request, id):
    try:
        room = Nroom.objects.get(id=id)
        nom = room.nomcroom
        room.delete()

        des = "Delete Habitaciones realizado ("+nom.lower()+")"
        table = "Nroom"
        date = datetime.now()
        usuario = request.session["id"]
        h = His(des=des, tableinfo=table, hour=date, usuario_id=usuario)
        h.save()

        room = Nroom.objects.all().values().order_by("nomcroom")

        dato = {'r' : 'Habitaciones Eliminadas Correctamente', 'room': room, 'nomusu' : request.session['nomusu']}
        return render(request, 'registerroom.html',dato)
    except:
        room = Nroom.objects.all().values().order_by("nomcroom")

        dato = {'r2' : "Las Habitaciones Con ID ("+str(id)+") No Existe", 'room': room, 'nomusu' : request.session['nomusu']}
        return render(request, 'registerroom.html',dato)




def ShowHis(request):
    check = request.session.get('status')
    if check is True:
        if request.session['nomusu'].upper() == "ADMIN":

            h = His.objects.select_related('usuario').all().order_by('hour')

            dato = {'nomusu':request.session["nomusu"], 'h': h}
            return render(request, 'historial.html', dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'index.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'index.html', dato)





def showUsuario(request):
    check = request.session.get("status")
    nom = request.session.get("nomusu")

    if check is True:
        if nom.upper() != 'ADMIN':
            dato = {'nomusu' : request.session["nomusu"]}
            return render(request, 'usuario.html',dato)
        else:
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'index.html', dato)
    else:
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'index.html', dato)




def showList(request):
    check = request.session.get("status")
    nom = request.session.get("nomusu")

    if check is True:
        if nom.upper() != 'ADMIN':
            
            h = Hotel.objects.select_related('size','Nroom').all().order_by("name")
            datos = { 'h' : h, 'nomusu': request.session["nomusu"]}
            
            return render(request, 'listado.html',datos)
        
        else:
            
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'index.html', dato)
    
    else:
        
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'index.html', dato)



def deleteHotel(request, id):
    try:
        h = Hotel.objects.get(id=id)
        nom = h.name
        h.delete()

        des = "Delete Hotel realizado ("+nom.lower()+")"
        table = "Hotel"
        date = datetime.now()
        usuario = request.session["id"]
        h = His(des=des, tableinfo=table, hour=date, usuario_id=usuario)
        h.save()

        h = Hotel.objects.all().values().order_by("name")

        dato = {'r' : 'Cuarto de Hotel Eliminadas Correctamente', 'h': h, 'nomusu' : request.session['nomusu']}
        return render(request, 'listado.html',dato)
    except:
        h = Hotel.objects.all().values().order_by("name")

        dato = {'r2' : "El Cuarto De Hotel Con ID ("+str(id)+") No Existe", 'h': h, 'nomusu' : request.session['nomusu']}
        return render(request, 'listado.html',dato)




def showRegister(request):
    check = request.session.get("status")
    nom = request.session.get("nomusu")

    if check is True:
        if nom.upper() != 'ADMIN':

            opsize = Size.objects.all().values().order_by("nomsize")
            oproom = Nroom.objects.all().values().order_by("nomcroom")

            dato = {'nomusu' : request.session["nomusu"], 'opsize': opsize, 'oproom' : oproom}
            return render(request, 'registrar.html',dato)
        
        else:
            
            dato = { 'r2' : 'No puedes acceder esa funcion' }
            return render(request, 'index.html', dato)
    
    else:
        
        dato = { 'r2' : 'Debe estar logueado para acceder' }
        return render(request, 'index.html', dato)




def RegisterHotel(request):
    if request.method == 'POST':
        nom = request.POST['txtnom']
        des = request.POST['txtdes']
        nho = request.POST['txtnhot']
        tip = request.POST['opt']
        siz = request.POST['sizes']
        pre = request.POST['txtpre']
        roo = request.POST['cuarto']
        ban = request.POST['txtnban']
        test = Hotel.objects.filter(name=nom)
        if test:

            opsize = Size.objects.all().values().order_by("nomsize")
            oproom = Nroom.objects.all().values().order_by("nomcroom")

            dato = {'r2' : 'El Hotel Llamado ( '+nom+' ) Ya Existe No Se puede Repetir','nomusu' : request.session["nomusu"], 'opsize': opsize, 'oproom' : oproom}
            return render(request, 'registrar.html',dato)

        else:
            i = Hotel(name=nom, description=des, Nhotel=nho, type=tip, size_id=siz, price=pre, Nroom_id=roo, Nbathroom=ban)
            i.save()

            des = "Register hotel realizado ("+nom.lower()+")"
            table = "Hotel"
            date = datetime.now()
            usuario = request.session["id"]
            h = His(des=des, tableinfo=table, hour=date, usuario_id=usuario)
            h.save()

            opsize = Size.objects.all().values().order_by("nomsize")
            oproom = Nroom.objects.all().values().order_by("nomcroom")

            dato = {'r' : 'Registro Realizado','nomusu' : request.session["nomusu"], 'opsize': opsize, 'oproom' : oproom}
            return render(request, 'registrar.html',dato)
    else:
        opsize = Size.objects.all().values().order_by("nomsize")
        oproom = Nroom.objects.all().values().order_by("nomcroom")

        dato = {'r2' : 'Debe Presionar El Botón Para Registrar Un Cuarto De Hotel', 'opsize': opsize, 'oproom' : oproom, 'nomusu': request.session["nomusu"]}
        return render(request, 'registrar.html',dato)







def showUpdate(request, id):
    try:
        check = request.session.get("status")
        if check is True:
            test = Hotel.objects.get(id = id)
            opsize = Size.objects.all().values().order_by("nomsize")
            oproom = Nroom.objects.all().values().order_by("nomcroom")
            h = Hotel.objects.select_related('size','Nroom').filter(id=id).order_by("name")

            dato = {'nomusu' : request.session["nomusu"], 'opsize': opsize, 'oproom' : oproom, 'test' : test,'h':h}
            return render(request, 'actualizar.html',dato)
    except:
        opsize = Size.objects.all().values().order_by("nomsize")
        oproom = Nroom.objects.all().values().order_by("nomcroom")

        dato = {'r2' : 'EL ID : ['+str(id)+'] no existe', 'opsize': opsize, 'oproom' : oproom, 'nomusu': request.session["nomusu"]}
        return render(request, 'listado.html',dato)




def Update(request, id):
    try:
        nom = request.POST['txtnom']
        des = request.POST['txtdes']
        nho = request.POST['txtnhot']
        tip = request.POST['opt']
        siz = request.POST['sizes']
        pre = request.POST['txtpre']
        roo = request.POST['cuarto']
        ban = request.POST['txtnban']


        h = Hotel.objects.get(id=id)
        h.name = nom
        h.description = des
        h.Nhotel = nho
        h.type = tip
        h.size_id = siz
        h.price = pre
        h.Nroom_id = roo
        h.Nbathroom = ban
        h.save()

        
        # se registra en la tabla historial.
        des = "Update hotel realizado ("+nom.lower()+")"
        table = "Hotel"
        date = datetime.now()
        usuario = request.session["id"]
        h = His(des=des, tableinfo=table, hour=date, usuario_id=usuario)
        h.save()


        h = Hotel.objects.select_related('size','Nroom').all().order_by("name")


        dato = {'nomusu' : request.session["nomusu"], 'h' : h ,  'r':"Datos Modificados Correctamente"}

        return render(request, 'listado.html', dato)

    except:
        
        h = Hotel.objects.select_related('size','Nroom').all().order_by("name")
        
        dato = { 'nomusu' : request.session["nomusu"],  'h' : h , 'r2' : "El ID ("+str(id)+") No Existe" }

        return render(request, 'registrar.html', dato)
