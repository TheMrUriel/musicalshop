import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicalshop.settings')

import django
django.setup()

from django.contrib.auth.models import User
from faker import Faker
from musicalapp.models import Comprador

fake = Faker()

def generar_compradores(n):
    for _ in range(n):
        # Generar datos falsos para el comprador
        username = fake.user_name()
        
        email = fake.email()
        nombre = fake.first_name()
        apellido = fake.last_name()
        edad = fake.random_int(min=18, max=90)
        calle = fake.street_address()
        ciudad = fake.city()
        estado = fake.state()
        codigo_postal = fake.zipcode()
        genero = fake.random_element(elements=('Masculino', 'Femenino', 'Otro'))
        password = 'password123'
        
        # Crear el usuario asociado
        user = User.objects.create_user(username=username, email=email,password=password)
        
        # Crear el comprador y asociarlo al usuario
        comprador = Comprador.objects.create(usuario=user, correo=email, nombre=nombre, apellido=apellido, edad=edad,
                                              calle=calle, ciudad=ciudad, estado=estado, codigo_postal=codigo_postal,
                                              genero=genero)
        print(f'Se ha creado el comprador: {comprador.nombre} {comprador.apellido}')

if __name__ == '__main__':
    num_compradores = 50  # Cambia este valor al número deseado de compradores
    generar_compradores(num_compradores)
