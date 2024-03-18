import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicalshop.settings')

import django
django.setup()

import random
from musicalapp.models import Ratings, Instrumento, Comprador
from faker import Faker
from django.shortcuts import get_object_or_404
from django.db.models import Avg

fake = Faker()

def generar_comentario(producto, estrellas):
    if estrellas == 5:
        comentarios = [
            f"¡{producto.nombre} es simplemente asombroso! ¡No puedo estar más feliz con mi compra!",
            f"He estado esperando tanto tiempo para obtener {producto.nombre} y no me decepcionó. Simplemente increíble.",
            f"Después de mucho investigar, decidí comprar {producto.nombre} y no me arrepiento en absoluto. ¡Una joya!",
            f"¡Hecho a la medida para mis necesidades! La calidad es impresionante.",
            f"¡Increíblemente versátil! No puedo creer lo bien que funciona en diferentes situaciones.",
            f"¡Superó mis expectativas! Definitivamente vale la pena el dinero.",
            f"Simplemente espectacular. No puedo dejar de usarlo desde que llegó.",
            f"Lo mejor de lo mejor. No hay otro producto que se compare.",
            f"No puedo imaginar mi vida sin {producto.nombre}. Una compra increíble.",
            f"¡La perfección hecha instrumento! No tengo palabras para describir lo feliz que estoy.",
            "Simplemente asombroso. No tengo nada más que decir.",
            "El mejor producto que he comprado. No puedo creer lo increíble que es.",
            "Una experiencia fantástica. Recomiendo encarecidamente este producto.",
            "¡No te arrepentirás de comprar este producto! Es absolutamente asombroso.",
            "Me ha impresionado mucho este producto. La calidad es excepcional.",
            "Simplemente excelente. No puedo recomendarlo lo suficiente.",
            "Increíblemente bueno. Vale cada centavo.",
            "Un producto excepcional. No hay nada más que decir.",
            "La calidad es inigualable. Estoy muy impresionado.",
            "Simplemente perfecto. No hay defectos en absoluto."
        ]
        comentario = random.choice(comentarios)
    elif estrellas == 4:
        comentarios = [
            f"Estoy muy contento con mi compra de {producto.nombre}. Lo recomendaría definitivamente!",
            f"{producto.nombre} superó mis expectativas! Definitivamente vale la pena el dinero.",
            f"Excelente producto. La calidad y el rendimiento son excepcionales.",
            f"¡Me encanta mi {producto.nombre}! Ha mejorado mi experiencia musical.",
            f"¡Tan versátil! Puedo usarlo en tantas situaciones diferentes.",
            f"¡Increíble calidad! No puedo creer lo bien hecho que está.",
            f"Una gran adición a mi colección de instrumentos. No puedo esperar para usarlo más.",
            f"Simplemente impresionante. No hay nada más que decir.",
            f"No puedo imaginar no tener {producto.nombre}. Lo recomendaría a cualquiera.",
            f"¡Sorprendentemente bueno! No esperaba que fuera tan genial.",
            "¡Muy impresionado con este producto! La calidad es excelente.",
            "¡Me ha encantado usar este producto! Funciona perfectamente.",
            "La mejor compra que he hecho. Estoy muy satisfecho.",
            "Increíblemente feliz con mi compra. No puedo quejarme.",
            "Simplemente genial. No puedo decir suficientes cosas buenas.",
            "Excelente valor por el precio. Definitivamente lo recomendaría.",
            "La calidad es excepcional. No puedo creer lo bien hecho que está.",
            "Muy satisfecho con este producto. No tengo quejas en absoluto.",
            "Recomendaría este producto a cualquiera. Es increíble.",
            "Fantástico producto. No me arrepiento en absoluto de mi compra."
        ]
        comentario = random.choice(comentarios)
    elif estrellas == 3:
        comentarios = [
            f"{producto.nombre} es decente. No está mal, pero podría mejorar.",
            f"No es perfecto, pero {producto.nombre} hace el trabajo. No me puedo quejar.",
            f"Esperaba un poco más de {producto.nombre}, pero en general está bien.",
            f"Podría ser mejor, pero {producto.nombre} hace el trabajo. No es excepcional, pero funciona.",
            f"¡No está mal! Podría haber sido mejor, pero funciona para lo que lo necesito.",
            f"Es lo suficientemente bueno. No es perfecto, pero puedo vivir con eso.",
            f"Aceptable, pero no excelente. Podría ser mejor, pero no me quejaré.",
            f"Ni bueno ni malo. Es solo un producto promedio.",
            f"Esperaba más de {producto.nombre}, pero lo usaré. No es terrible, pero tampoco es genial.",
            f"No es lo mejor, pero es aceptable. No me impresionó mucho.",
            "No es tan malo como pensé. Funciona bastante bien.",
            "No está mal por el precio. Podría haber sido mejor.",
            "No es increíble, pero no es terrible. Funciona para lo que necesito.",
            "No puedo quejarme demasiado. Cumple su función.",
            "Es decente por el precio. No es lo mejor, pero funciona.",
            "Bastante bueno para el precio. No tengo quejas.",
            "Está bien para el uso diario. No es nada especial.",
            "Podría ser mejor, pero no me quejaré. Funciona bien.",
            "No es genial, pero no es terrible. Funciona para lo que necesito.",
            "No es el mejor, pero no es el peor. Funciona decentemente."
        ]
        comentario = random.choice(comentarios)
    elif estrellas == 2:
        comentarios = [
            f"No estoy muy impresionado con {producto.nombre}. No cumple completamente con mis expectativas.",
            f"No es tan bueno como pensaba que sería. Me decepcionó un poco.",
            f"Esperaba más de {producto.nombre}. No es terrible, pero definitivamente podría ser mejor.",
            f"Podría ser mejor. No estoy completamente satisfecho con mi compra.",
            f"¡No estoy emocionado! No es lo que esperaba en absoluto.",
            f"No tan bueno como esperaba. Me decepcionó un poco la calidad.",
            f"No tan genial como pensaba que sería. No cumplió completamente con mis expectativas.",
            f"No tan impresionado como esperaba estar. Esperaba más.",
            f"No cumplió con mis expectativas. Definitivamente podría ser mejor.",
            f"Un poco decepcionado con {producto.nombre}. No es lo que esperaba.",
            "Podría haber sido mejor. No estoy muy satisfecho.",
            "No tan bueno como esperaba. Un poco decepcionado.",
            "No es lo mejor, pero podría ser peor. No estoy muy impresionado.",
            "No es el peor, pero definitivamente podría ser mejor. No estoy impresionado.",
            "No es genial, pero no es terrible. Me siento un poco decepcionado.",
            "No es increíble, pero no es terrible. No estoy demasiado feliz.",
            "Es aceptable, pero no lo recomendaría. No me impresionó mucho.",
            "No es lo mejor, pero no es lo peor. Podría ser mejor.",
            "No es genial, pero podría ser peor. No estoy impresionado.",
            "No es lo mejor, pero funciona. No estoy muy emocionado."
        ]
        comentario = random.choice(comentarios)
    elif estrellas == 1:
        comentarios = [
            f"No recomendaría {producto.nombre} en absoluto. Una experiencia muy decepcionante.",
            f"¡Horrible! No puedo creer lo malo que es.",
            f"Lo peor que he comprado. Me arrepiento completamente.",
            f"¡Una completa pérdida de dinero! No vale la pena en absoluto.",
            f"No es lo que esperaba en absoluto. ¡Tan decepcionante!",
            f"Nunca volvería a comprar {producto.nombre}. Una experiencia terrible.",
            f"No puedo creer lo malo que es. No hay nada positivo que decir.",
            f"¡No compres esto! Es una completa basura.",
            f"No vale la pena. No hagas el mismo error que yo.",
            f"Lo peor que he tenido. No puedo expresar lo malo que es.",
            "Absolutamente terrible. No hay nada bueno que decir.",
            "Lo peor que he probado. No puedo recomendarlo.",
            "Un desastre completo. No vale la pena en absoluto.",
            "No compraría esto de nuevo. Fue una completa pérdida de dinero.",
            "No es lo que esperaba en absoluto. Totalmente decepcionado.",
            "No lo recomendaría a nadie. Fue una experiencia terrible.",
            "No hay nada bueno que decir. Fue una experiencia desagradable.",
            "No es lo que esperaba en absoluto. Muy decepcionado.",
            "No lo compres. Es un completo desperdicio de dinero.",
            "Fue un error comprar esto. No puedo creer lo malo que es."
        ]
        comentario = random.choice(comentarios)
    elif estrellas == 0:
        comentarios = [
            f"Es un mal producto para {producto.nombre}. No vale la pena en absoluto.",
            f"No recomendaría {producto.nombre} en absoluto. Una experiencia terrible.",
            f"¡No compres esto! Es una completa basura.",
            f"No vale la pena. No hagas el mismo error que yo.",
            f"Nunca volvería a comprar {producto.nombre}. No es lo que esperaba en absoluto.",
            f"No es lo que esperaba en absoluto. ¡Tan decepcionante!",
            f"Una completa pérdida de dinero. No vale la pena en absoluto.",
            f"Lo peor que he comprado. Me arrepiento completamente.",
            f"No puedo creer lo malo que es. No hay nada positivo que decir.",
            f"No es lo que esperaba en absoluto. Una experiencia muy decepcionante.",
            "Absolutamente terrible. No hay nada bueno que decir.",
            "Lo peor que he probado. No puedo recomendarlo.",
            "Un desastre completo. No vale la pena en absoluto.",
            "No compraría esto de nuevo. Fue una completa pérdida de dinero.",
            "No es lo que esperaba en absoluto. Totalmente decepcionado.",
            "No lo recomendaría a nadie. Fue una experiencia terrible.",
            "No hay nada bueno que decir. Fue una experiencia desagradable.",
            "No es lo que esperaba en absoluto. Muy decepcionado.",
            "No lo compres. Es un completo desperdicio de dinero.",
            "Fue un error comprar esto. No puedo creer lo malo que es."
        ]
        comentario = random.choice(comentarios)

    return comentario


def asignar_calificaciones_aleatorias():
    compradores = Comprador.objects.all()
    instrumentos = Instrumento.objects.all()

    # Asignar calificaciones aleatorias a los productos
    for comprador in compradores:
        num_productos_a_calificar = random.randint(1, 10)
        productos_a_calificar = random.sample(list(instrumentos), num_productos_a_calificar)

        for producto in productos_a_calificar:
            if not Ratings.objects.filter(ClienteID=comprador, InstrumentosID=producto).exists():
                estrellas = random.randint(0, 5)
                comentario = generar_comentario(producto, estrellas)

                rating = Ratings.objects.create(
                    InstrumentosID=producto,
                    ClienteID=comprador,
                    Puntuacion=estrellas,
                    Comentario=comentario
                )
                actualizar_promedio_instrumento(producto)      

    # Verificar si todos los productos tienen al menos una calificación
    for producto in instrumentos:
        if not Ratings.objects.filter(InstrumentosID=producto).exists():
            # Si el producto no tiene calificaciones, asigna una calificación aleatoria
            comprador = random.choice(compradores)
            estrellas = random.randint(0, 5)
            comentario = generar_comentario(producto, estrellas)

            rating = Ratings.objects.create(
                InstrumentosID=producto,
                ClienteID=comprador,
                Puntuacion=estrellas,
                Comentario=comentario
            )
            actualizar_promedio_instrumento(producto)      
            


def actualizar_promedio_instrumento(instrumento):
    # Obtener todas las calificaciones para el instrumento
    calificaciones = Ratings.objects.filter(InstrumentosID=instrumento)
    
    # Calcular el promedio de las calificaciones
    promedio_calificaciones = calificaciones.aggregate(Avg('Puntuacion'))['Puntuacion__avg']
    
    # Actualizar el campo de promedio en el modelo del instrumento
    instrumento.Puntuacion = promedio_calificaciones
    instrumento.save()

# Llamar a la función para asignar calificaciones aleatorias
asignar_calificaciones_aleatorias()

