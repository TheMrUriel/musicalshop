from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.contrib.postgres.fields import ArrayField
from django.db.models import Avg
import math

class Instrumento(models.Model):
    id = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    texto = models.TextField()
    imagen = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50)
    Puntuacion = models.IntegerField(default='0')

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['nombre']

class Comprador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    correo = models.EmailField(max_length=255)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    edad = models.PositiveIntegerField()
    calle = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255) 
    estado = models.CharField(max_length=255)  
    codigo_postal = models.CharField(max_length=10)
    genero = models.CharField(max_length=255)  



    def __str__(self):
        return f"{self.usuario}"
    

class Ratings(models.Model):
    RatingID = models.AutoField(primary_key=True)
    InstrumentosID = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    ClienteID = models.ForeignKey(Comprador, on_delete=models.CASCADE)
    Puntuacion = models.IntegerField()
    Comentario = models.CharField(max_length=255)

    
    def __str__(self):
        return f"usuario: {self.ClienteID}, {self.Puntuacion} estrellas, {self.InstrumentosID}"
    
    class Meta:
        # Restricción única compuesta para evitar múltiples ratings por el mismo comprador para un mismo instrumento
        unique_together = ('InstrumentosID', 'ClienteID')


class Lista(models.Model):
    precio = models.FloatField()
    cantidad = models.PositiveIntegerField(default=1)
    intrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    comprador = models.ForeignKey(Comprador, null=True, blank=True, on_delete=models.SET_NULL)
    subtotal = models.FloatField(default=0)

    def __str__(self):
        return f"{self.intrumento}"

class ListaHistorial(models.Model):
    precio = models.FloatField()
    cantidad = models.PositiveIntegerField(default=1)
    intrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    comprador = models.ForeignKey(Comprador, null=True, blank=True, on_delete=models.SET_NULL)
    subtotal = models.FloatField(default=0)

    def __str__(self):
        return f"{self.intrumento}"

class HistorialCompra(models.Model):
    comprador = models.ForeignKey(Comprador, on_delete=models.CASCADE)
    lista_compra = models.ForeignKey(ListaHistorial, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comprador.usuario.username} - {self.fecha_compra}"
    

class Carrito(models.Model):
    comprador=models.ForeignKey(Comprador,on_delete=models.CASCADE)
    intrumentos = models.ManyToManyField(Lista, related_name='Instrumento_en_carrito')

    def __str__(self):
        return f"Carrito de {self.comprador}"