import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicalshop.settings')

import django
django.setup()

import random
from faker import Faker
from musicalapp.models import Comprador, Instrumento, ListaHistorial, HistorialCompra


fake = Faker()

def generar_historial_compras():
    # Obtiene una lista de todos los compradores y productos
    compradores = Comprador.objects.all()
    productos = Instrumento.objects.all()

    # Itera sobre los compradores y agrega historial de compras aleatorios
    for comprador in compradores:
        cantidad_productos = random.randint(5, 20)  # Genera un número aleatorio de productos de 5 a 20
        productos_seleccionados = random.sample(list(productos), cantidad_productos)  # Selecciona productos aleatorios

        for producto in productos_seleccionados:
            precio_producto = producto.precio
            cantidad = random.randint(1, 5)  # Genera una cantidad aleatoria entre 1 y 5
            subtotal = precio_producto * cantidad

            # Crea un registro en la lista de historial de compras
            lista_historial = ListaHistorial.objects.create(
                precio=precio_producto,
                cantidad=cantidad,
                intrumento=producto,
                comprador=comprador,
                subtotal=subtotal
            )

            # Crea un registro en el historial de compra asociado a la lista creada
            HistorialCompra.objects.create(
                comprador=comprador,
                lista_compra=lista_historial
            )

            print(f"Se ha creado un registro en el historial de compra para {comprador} - {producto}")


generar_historial_compras()
