from django.db import models

# Create your models here.
class Usuario(models.Model):
    nom = models.TextField(max_length=15)
    pas = models.TextField(max_length=20)

    def __str__(self):
        return str(self.nom)

class Size(models.Model):
    nomsize = models.TextField(max_length=100)
    
    def __str__(self):
        return str(self.nomsize)

class Nroom(models.Model):
    nomcroom = models.TextField(max_length=100)
    
    def __str__(self):
        return str(self.nomcroom)

class Hotel(models.Model):
    name = models.TextField(max_length=50)
    description = models.TextField(max_length=50)
    Nhotel = models.TextField(max_length=50)
    type = models.TextField(max_length=50)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.TextField(max_length=50)
    Nroom = models.ForeignKey(Nroom, on_delete=models.CASCADE)
    Nbathroom = models.TextField(max_length=50)

class His(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    des = models.TextField(max_length=200)
    tableinfo = models.TextField(max_length=100)
    hour = models.DateTimeField()