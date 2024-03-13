from django.shortcuts import render
from django.db.models import Q
from functools import wraps
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render
from .models import Instrumento
from .forms import *
from django.contrib.auth.models import auth
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login, logout
from allauth.account.decorators import login_required
from django.db.models import F
from .forms import RatingForm 
from .models import Ratings  
from django.contrib import messages



def prueba(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)
    instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")
    instrumento.descripcion = [descripcion.strip() for descripcion in instrumento.descripcion]
    context = {'instrumento': instrumento}
    return render(request, 'Conex/a.html', context)

fondo_instrumento ='https://wallpaperbat.com/img/6982-music-instruments-wallpaper.jpg'

# Inicio
def Home(request):
    productos_populares = Instrumento.objects.order_by('-Puntuacion')[:5]
    
    return render(request, 'Inicio/Home.html', {'productos_populares': productos_populares})




#Sesión comprador
def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige al usuario a donde desees después del registro
            return redirect("/login/")
    else:
        form = CreateUserForm()
    return render(request, 'Inicio/register.html', {'registerform': form})
    
def my_login(request):
    auth.logout(request)
    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("/home/")


    context = {'loginform':form}

    return render(request, 'Inicio/login.html', context=context)



def user_logout(request):

    auth.logout(request)

    return redirect("/home/")




def comprador_login(request):
    return render(request, 'Inicio/login.html')

def comprador_register(request):
    return render(request, 'Inicio/register.html')

def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and Comprador.objects.filter(usuario=request.user).exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect("musicalapp:my-login")
    return _wrapped_view

@user_required
def usuario_page(request):
    # Obtener las calificaciones del usuario actual
    calificaciones_usuario = Ratings.objects.filter(ClienteID=request.user.comprador)

    # Obtener los instrumentos relacionados con las calificaciones del usuario
    instrumentos_calificados = [calificacion.InstrumentosID for calificacion in calificaciones_usuario]

    # Procesar cualquier búsqueda y ordenamiento que desees aplicar a los instrumentos
    instrumentos_calificados = procesar_busqueda_y_ordenamiento(instrumentos_calificados, request)

    # Crear una lista para almacenar los comentarios y los instrumentos asociados
    comentarios_instrumentos = []

    # Iterar sobre las calificaciones del usuario para obtener los comentarios y los instrumentos asociados
    for calificacion in calificaciones_usuario:
        instrumento = calificacion.InstrumentosID
        comentario = calificacion.Comentario
        Puntuacion = calificacion.Puntuacion
        comentarios_instrumentos.append((instrumento, comentario,Puntuacion))


    # Renderizar la plantilla con los instrumentos calificados por el usuario
    return render(request, 'Inicio/usuario.html', {'comentarios_instrumentos': comentarios_instrumentos,'instrumentos': instrumentos_calificados})


@user_required
def usuario_editar(request):
    usuario = request.user  # Obtén el usuario actual
    comprador = usuario.comprador  # Obtén el perfil del comprador asociado al usuario

    if request.method == 'POST':
        form = CompradorForm(request.POST, instance=comprador)
        if form.is_valid():
            form.save()  # Guarda los datos actualizados del comprador
            return redirect('musicalapp:usuario_page')  # Redirecciona a la página deseada después de la edición
    else:
        form = CompradorForm(instance=comprador)  # Crea el formulario con los datos actuales del comprador

    return render(request, 'Inicio/usuario_editar.html', {'form': form})


@user_required
def historial(request):
    # Obtener todas las compras del historial
    historial_compras = HistorialCompra.objects.all()

    # Renderizar el template con el historial de compras
    return render(request, 'Inicio/historial.html', {'historial_compras': historial_compras})


@user_required
def carrito(request):
    comprador_actual = Comprador.objects.get(usuario=request.user)
    carrito, creado = Carrito.objects.get_or_create(comprador=comprador_actual)

    # Obtener todos los instrumentos en el carrito
    instrumentos_en_carrito = carrito.intrumentos.all()
    
    # Calcular el monto final sumando los precios de todos los instrumentos en el carrito
    montofinal = sum(lista.subtotal for lista in instrumentos_en_carrito)

    return render(request, 'Venta/carrito.html', {'instrumentos_en_carrito': instrumentos_en_carrito, 'montofinal': montofinal})


def agregar_al_carrito(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)

    if request.method == 'POST':
        cantidad = request.POST.get('cant', 1)

        try:
            cantidad = int(cantidad)
            comprador_actual = Comprador.objects.get(usuario=request.user)

            carrito, creado = Carrito.objects.get_or_create(comprador=comprador_actual)

            nuevo_lista = Lista.objects.create(
                precio=instrumento.precio,
                cantidad=cantidad,
                intrumento=instrumento,
                comprador=comprador_actual,
                subtotal=instrumento.precio * cantidad,
            )
            carrito.intrumentos.add(nuevo_lista)

            messages.success(request, f'Producto(s) agregado(s) al carrito exitosamente.')
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('musicalapp:carrito') 


def uno_agregar_al_carrito(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)
    
    comprador_actual = Comprador.objects.get(usuario=request.user)

    carrito, creado = Carrito.objects.get_or_create(comprador=comprador_actual)

    nuevo_lista = Lista.objects.create(
        precio=instrumento.precio,
        intrumento=instrumento,
        comprador=comprador_actual,
        subtotal=instrumento.precio,
        
    )
    carrito.intrumentos.add(nuevo_lista)

    return redirect('musicalapp:carrito') 

def quitar_del_carrito(request, id):
    lista = get_object_or_404(Lista, id=id)

    if request.method == 'POST':
        comprador_actual = get_object_or_404(Comprador, usuario=request.user)
        carrito = get_object_or_404(Carrito, comprador=comprador_actual)

        carrito.intrumentos.remove(lista)

        lista.delete()

        messages.success(request, 'Producto quitado del carrito exitosamente.')

    return redirect('musicalapp:carrito')

########################################################################################################################
def procesar_busqueda_y_ordenamiento(instrumentos, request):
    # Procesa el parámetro de búsqueda por nombre
    buscar_nombre = request.GET.get('buscar_nombre')
    if buscar_nombre:
        # Separa los términos de búsqueda por espacios
        terminos_busqueda = buscar_nombre.split()
        
        # Crea una consulta que busque cada término en el nombre del instrumento
        consulta_nombre = Q()
        for termino in terminos_busqueda:
            consulta_nombre |= Q(nombre__icontains=termino)
        
        # Aplica la consulta de búsqueda al conjunto de instrumentos
        instrumentos = instrumentos.filter(consulta_nombre)

    # Procesa el parámetro de búsqueda por marca
    buscar_marca = request.GET.get('buscar_marca')
    if buscar_marca:
        # Separa los términos de búsqueda por espacios
        terminos_busqueda_marca = buscar_marca.split()
        
        # Crea una consulta que busque cada término en la marca del instrumento
        consulta_marca = Q()
        for termino in terminos_busqueda_marca:
            consulta_marca |= Q(marca__icontains=termino)
        
        # Aplica la consulta de búsqueda por marca al conjunto de instrumentos
        instrumentos = instrumentos.filter(consulta_marca)

    # Procesa el formulario de ordenamiento
    if 'ordenar_por_precio' in request.GET:
        ordenar_por_precio = request.GET.get('ordenar_por_precio')
        if ordenar_por_precio:
            if ordenar_por_precio == 'asc':
                instrumentos = instrumentos.order_by(F('precio').asc(nulls_last=True))
            elif ordenar_por_precio == 'desc':
                instrumentos = instrumentos.order_by(F('precio').desc(nulls_last=True))
            elif ordenar_por_precio =='rebmon':
                instrumentos = instrumentos.order_by('-nombre')
            elif ordenar_por_precio =='puntuacion1':
                instrumentos = instrumentos.order_by('Puntuacion')
            elif ordenar_por_precio =='puntuacion2':
                instrumentos = instrumentos.order_by('-Puntuacion')             
    return instrumentos


# Instrumentos
def lista_instrumentos(request):
    instrumentos = Instrumento.objects.all()
    tipo_instrumento = 'Productos'

    for instrumento in instrumentos:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos = procesar_busqueda_y_ordenamiento(instrumentos, request)
    
    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos, 'tipo_instrumento': tipo_instrumento, 'fondo_instrumento': fondo_instrumento})

def lista_marcas(request):
    instrumentos = Instrumento.objects.all()
    tipo_instrumento = 'Productos'

    for instrumento in instrumentos:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos = procesar_busqueda_y_ordenamiento(instrumentos, request)

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': instrumentos, 'tipo_instrumento': tipo_instrumento, 'fondo_instrumento': fondo_instrumento})


def eliminar_comentario_y_rating(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)
    Ratings.objects.filter(InstrumentosID=instrumento).delete()
    # Puedes agregar aquí la lógica para eliminar el comentario del instrumento si es necesario
    return redirect('musicalapp:detalle_instrumento', id=id)


def detalle_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)
    instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")
    instrumento.descripcion = [descripcion.strip() for descripcion in instrumento.descripcion]

    # Obtener los ratings y comentarios para este instrumento
    ratings = Ratings.objects.filter(InstrumentosID=instrumento)

    # Calcular la puntuación promedio dinámicamente
    promedio = ratings.aggregate(avg_puntuacion=Avg('Puntuacion'))['avg_puntuacion'] or 0
    instrumento1 = get_object_or_404(Instrumento, id=id)
    instrumento1.Puntuacion = promedio
    instrumento1.save()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            cliente = request.user.comprador
            rating, created = Ratings.objects.update_or_create(
                InstrumentosID=instrumento,
                ClienteID=cliente,
                defaults={'Puntuacion': form.cleaned_data['Puntuacion'],
                          'Comentario': form.cleaned_data['Comentario']}
            )
            return redirect('musicalapp:detalle_instrumento', id=id)  # Redirige a la misma página de detalle
    else:
        if request.user.is_authenticated:
            cliente = request.user.comprador
            rating_instance = Ratings.objects.filter(InstrumentosID=instrumento, ClienteID=cliente).first()
            if rating_instance:
                form = RatingForm(instance=rating_instance)
            else:
                form = RatingForm()
        else:
            form = None

    cantidad_usuarios = Ratings.objects.filter(InstrumentosID=instrumento).values('ClienteID').distinct().count()

    # Renderizar el formulario de rating y los detalles del instrumento
    context = {'instrumento': instrumento, 'ratings': ratings, 'form': form, 'promedio': promedio, 'cantidad_usuarios': cantidad_usuarios}
    return render(request, 'Productos/detalle_instrumento.html', context)


# Accesorios
def instrumentos_accesorios(request):
    instrumentos_accesorios = Instrumento.objects.filter(tipo='accesorios')
    tipo_instrumento = 'Accesorios'
    fondo_instrumento = 'https://img.freepik.com/free-photo/volumetric-musical-background-with-treble-clef-notes-generative-ai_169016-29576.jpg?size=626&ext=jpg&ga=GA1.1.1700460183.1708214400&semt=ais'
    for instrumento in instrumentos_accesorios:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_accesorios = procesar_busqueda_y_ordenamiento(instrumentos_accesorios, request)
    
    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_accesorios, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Alientos
def instrumentos_alientos(request):
    instrumentos_alientos = Instrumento.objects.filter(tipo='alientos')
    tipo_instrumento = 'Instrumentos de viento'
    fondo_instrumento = 'https://p0.piqsels.com/preview/857/353/296/music-saxophone-summer-gold-thumbnail.jpg'
    for instrumento in instrumentos_alientos:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_alientos = procesar_busqueda_y_ordenamiento(instrumentos_alientos, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_alientos, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Amplificadores
def instrumentos_amplificadores(request):
    instrumentos_amplificadores = Instrumento.objects.filter(tipo='amplificadores')
    tipo_instrumento = 'Amplificadores'
    fondo_instrumento = 'https://c.wallhere.com/photos/12/c9/1920x1080_px_Amplifiers_headphones_Jack_Microphones_Potentiometer-1226283.jpg!d'
    for instrumento in instrumentos_amplificadores:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_amplificadores = procesar_busqueda_y_ordenamiento(instrumentos_amplificadores, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_amplificadores, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Bajos eléctricos
def instrumentos_bajos_electricos(request):
    instrumentos_bajos_electricos = Instrumento.objects.filter(tipo='bajos-electricos')
    tipo_instrumento = 'Bajos electricos'
    fondo_instrumento = 'https://c.wallhere.com/photos/10/b6/electric_guitar_instrument_string-735641.jpg!d'
    for instrumento in instrumentos_bajos_electricos:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_bajos_electricos = procesar_busqueda_y_ordenamiento(instrumentos_bajos_electricos, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_bajos_electricos, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Baterías
def instrumentos_baterias(request):
    instrumentos_baterias = Instrumento.objects.filter(tipo='baterias')
    tipo_instrumento = 'Baterias'
    fondo_instrumento = 'https://c.wallhere.com/photos/58/80/4000x2250_px_Benzin_Machine_Cymbals_Drummer_drums_Kick_Kris_Kroschel-1339801.jpg!d'
    for instrumento in instrumentos_baterias:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_baterias = procesar_busqueda_y_ordenamiento(instrumentos_baterias, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_baterias, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Guitarras acústicas
def instrumentos_guitarras_acusticas(request):
    instrumentos_guitarras_acusticas = Instrumento.objects.filter(tipo='guitarras-acusticas')
    tipo_instrumento = 'Guitarras acusticas'
    fondo_instrumento = 'https://c.wallhere.com/photos/1e/c1/1920x1440_px_entertainment_guitars_instuments_music_Musical_Strings-1721181.jpg!d'
    for instrumento in instrumentos_guitarras_acusticas:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_guitarras_acusticas = procesar_busqueda_y_ordenamiento(instrumentos_guitarras_acusticas, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_guitarras_acusticas, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Guitarras acústicas con cuerdas para acústica
def instrumentos_guitarras_acusticas_cuerdas_para_acustica(request):
    instrumentos_guitarras_acusticas_cuerdas_para_acustica = Instrumento.objects.filter(tipo='guitarras-acusticas-cuerdas-para-acustica')
    tipo_instrumento = 'Cuerdas de guitarras acusticas'
    fondo_instrumento = 'https://c.wallhere.com/photos/c7/36/light_music_blur_canon_dark_blurry_warm_dof-583182.jpg!d'
    for instrumento in instrumentos_guitarras_acusticas_cuerdas_para_acustica:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_guitarras_acusticas_cuerdas_para_acustica = procesar_busqueda_y_ordenamiento(instrumentos_guitarras_acusticas_cuerdas_para_acustica, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_guitarras_acusticas_cuerdas_para_acustica, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Guitarras eléctricas
def instrumentos_guitarras_electricas(request):
    instrumentos_guitarras_electricas = Instrumento.objects.filter(tipo='guitarras-electricas')
    tipo_instrumento = 'Guitarras electricas'
    fondo_instrumento = 'https://c.wallhere.com/photos/5b/ca/guitar_Stratocaster_Marshall_Fender_Blender_electric_guitar-2238784.jpg!d'
    for instrumento in instrumentos_guitarras_electricas:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_guitarras_electricas = procesar_busqueda_y_ordenamiento(instrumentos_guitarras_electricas, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_guitarras_electricas, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Guitarras eléctricas con cuerdas
def instrumentos_guitarras_electricas_cuerdas(request):
    instrumentos_guitarras_electricas_cuerdas = Instrumento.objects.filter(tipo='guitarras-electricas-cuerdas')
    tipo_instrumento = 'Cuerdas de guitarras electricas'
    fondo_instrumento = 'https://c.wallhere.com/photos/ac/ce/music_electric_guitar-2205119.jpg!d'
    for instrumento in instrumentos_guitarras_electricas_cuerdas:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_guitarras_electricas_cuerdas = procesar_busqueda_y_ordenamiento(instrumentos_guitarras_electricas_cuerdas, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_guitarras_electricas_cuerdas, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Pedales y efectos
def instrumentos_pedales_y_efectos(request):
    instrumentos_pedales_y_efectos = Instrumento.objects.filter(tipo='pedales-y-efectos')
    tipo_instrumento = 'Pedales y efectos'
    fondo_instrumento = 'https://c.wallhere.com/photos/79/78/boss_musician_effects_boots_guitar_echo_wires_roland-851671.jpg!d'
    for instrumento in instrumentos_pedales_y_efectos:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_pedales_y_efectos = procesar_busqueda_y_ordenamiento(instrumentos_pedales_y_efectos, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_pedales_y_efectos, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Platillos
def instrumentos_platillos(request):
    instrumentos_platillos = Instrumento.objects.filter(tipo='platillos')
    tipo_instrumento = 'Platillos'
    fondo_instrumento = 'https://c.wallhere.com/photos/58/80/4000x2250_px_Benzin_Machine_Cymbals_Drummer_drums_Kick_Kris_Kroschel-1339801.jpg!d'
    for instrumento in instrumentos_platillos:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_platillos = procesar_busqueda_y_ordenamiento(instrumentos_platillos, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_platillos, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Teclas
def instrumentos_teclas(request):
    instrumentos_teclas = Instrumento.objects.filter(tipo='piano')
    tipo_instrumento = 'Pianos'
    fondo_instrumento = 'https://images3.alphacoders.com/133/1338175.png'
    for instrumento in instrumentos_teclas:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_teclas = procesar_busqueda_y_ordenamiento(instrumentos_teclas, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_teclas, 'tipo_instrumento': tipo_instrumento, 'fondo_instrumento': fondo_instrumento,'fondo_instrumento': fondo_instrumento})

# Ukuleles
def instrumentos_ukuleles(request):
    instrumentos_ukuleles = Instrumento.objects.filter(tipo='ukuleles')
    tipo_instrumento = 'Ukuleles'
    fondo_instrumento = 'https://c.wallhere.com/photos/df/7b/Danbo_Amazon_cityscape_bridge_building-11633.jpg!d'
    for instrumento in instrumentos_ukuleles:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_ukuleles = procesar_busqueda_y_ordenamiento(instrumentos_ukuleles, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_ukuleles, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})

# Violines
def instrumentos_violines(request):
    instrumentos_violines = Instrumento.objects.filter(tipo='violines')
    tipo_instrumento = 'Violines'
    fondo_instrumento = 'https://c.wallhere.com/photos/ae/00/1920x1200_px_entertainment_Instrument_music_Musical_Orchestra_People_Strings-1721365.jpg!d'
    for instrumento in instrumentos_violines:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    instrumentos_violines = procesar_busqueda_y_ordenamiento(instrumentos_violines, request)

    return render(request, 'Productos/lista_instrumentos.html', {'instrumentos': instrumentos_violines, 'tipo_instrumento': tipo_instrumento,'fondo_instrumento': fondo_instrumento})


#########################################################################################################################
# Marcas
def yamaha(request):
    yamaha = Instrumento.objects.filter(marca='Yamaha')
    marca_instrumento = 'Yamaha'
    fondo_instrumento = 'https://yamahamusical.co/wp-content/uploads/2019/03/img-slider.jpg'
    for instrumento in yamaha:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    yamaha = procesar_busqueda_y_ordenamiento(yamaha, request)

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': yamaha, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})

def bamboo(request):
    bamboo = Instrumento.objects.filter(marca='Bamboo')
    marca_instrumento = 'Bamboo'
    fondo_instrumento = 'https://acdn.mitiendanube.com/stores/813/752/themes/style/img-1351479246-1629913301-8d2c4d1891921aee538af8ef2c23c9371629913302.png?68177806'
    for instrumento in bamboo:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    bamboo = procesar_busqueda_y_ordenamiento(bamboo, request)

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': bamboo, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})

def daddario(request):
    daddario = Instrumento.objects.filter(marca='Daddario')
    marca_instrumento = 'Daddario'
    fondo_instrumento = 'https://www.centerlom.com/img/marcas/banner_mobile_9.jpg?v=1623868015'
    for instrumento in daddario:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    daddario = procesar_busqueda_y_ordenamiento(daddario, request)

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': daddario, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})

def new_Beat(request):
    new_Beat = Instrumento.objects.filter(marca='New Beat')
    marca_instrumento = 'New Beat'
    fondo_instrumento = 'https://www.newbeat.com.mx/wp-content/uploads/2021/05/new-beat-19.jpg'
    for instrumento in new_Beat:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    new_Beat = procesar_busqueda_y_ordenamiento(new_Beat, request)

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': new_Beat, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})


def line6(request):
    line6 = Instrumento.objects.filter(marca='Line6')
    marca_instrumento = 'Line6'
    fondo_instrumento = 'https://l6c-acdn2.line6.net/data/6/0a020a41edb4653bfea096948/image/jpeg/r17673_'
    for instrumento in line6:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    line6 = procesar_busqueda_y_ordenamiento(line6, request)

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': line6, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})

def fender(request):
    fender = Instrumento.objects.filter(marca='Fender')
    marca_instrumento = 'Fender'
    fondo_instrumento = 'https://tucsonmusicscene.com/wp-content/uploads/2018/08/Fender-Stratocaster.png'
    for instrumento in fender:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    fender = procesar_busqueda_y_ordenamiento(fender, request)

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': fender, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})

def peavey(request):
    peavey = Instrumento.objects.filter(marca='Peavey')
    marca_instrumento = 'Peavey'
    fondo_instrumento = 'https://cdn.shopify.com/s/files/1/0051/6787/8335/products/bks1.jpg?v=1630518900'
    for instrumento in peavey:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    peavey = procesar_busqueda_y_ordenamiento(peavey, request)

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': peavey, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})

def proline(request):
    proline = Instrumento.objects.filter(marca='Proline')
    marca_instrumento = 'Proline'
    fondo_instrumento = 'https://www.intermusic-pro.com/31242-thickbox_default/proline-laptop-stand.jpg'
    for instrumento in proline:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    proline = procesar_busqueda_y_ordenamiento(proline, request)

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': proline, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})

def paiste(request):
    paiste = Instrumento.objects.filter(marca='Paiste')
    marca_instrumento = 'Paiste'
    fondo_instrumento = 'https://upload.wikimedia.org/wikipedia/commons/f/fb/Paiste_cymbal_close.jpg'
    for instrumento in paiste:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    paiste = procesar_busqueda_y_ordenamiento(paiste, request) 

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': paiste, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})

def serpentario(request):
    serpentario = Instrumento.objects.filter(marca='Serpentario')
    marca_instrumento = 'Serpentario'
    fondo_instrumento = 'https://img.freepik.com/foto-gratis/signo-zodiaco-leo-cielo-azul-horoscopo-fondo-astrologia-leo-horoscopo-azul_559531-11845.jpg?size=626&ext=jpg&ga=GA1.1.1687694167.1704067200&semt=ais'
    for instrumento in serpentario:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    serpentario = procesar_busqueda_y_ordenamiento(serpentario, request) 

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': serpentario, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})

def squier(request):
    squier = Instrumento.objects.filter(marca='Squier')
    marca_instrumento = 'Squier'
    fondo_instrumento = 'https://cdn.shoplightspeed.com/shops/609677/files/36542291/image.jpg'
    for instrumento in squier:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    squier = procesar_busqueda_y_ordenamiento(squier, request) 

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': squier, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})

def markbass(request):
    markbass = Instrumento.objects.filter(marca='Markbass')
    marca_instrumento = 'Markbass'
    fondo_instrumento = 'https://l6c-acdn2.line6.net/data/6/0a020a41edb4653bfea096948/image/jpeg/r17673_'
    for instrumento in markbass:
        instrumento.descripcion = instrumento.descripcion.replace("[", "").replace("]", "").split(", ")

    markbass = procesar_busqueda_y_ordenamiento(markbass, request)

    return render(request, 'Productos/lista_marcas.html', {'instrumentos': markbass, 'marca_instrumento': marca_instrumento,'fondo_instrumento': fondo_instrumento})




def completar_pago(request):
    # Obtener el comprador actual
    comprador_actual = Comprador.objects.get(usuario=request.user)
    
    # Obtener la lista de compra del comprador actual
    lista_compra = Lista.objects.filter(comprador=comprador_actual)
    
    # Crear una entrada en la lista de historial para cada elemento de la lista de compra
    for item in lista_compra:
        ListaHistorial.objects.create(
            precio=item.precio,
            cantidad=item.cantidad,
            intrumento=item.intrumento,
            comprador=comprador_actual,
            subtotal=item.subtotal
        )
    
    # Crear una entrada en el historial de compras para cada elemento de la lista de compra
    for item in lista_compra:
        # Obtener solo un objeto de ListaHistorial que cumpla con los criterios
        historial_item = ListaHistorial.objects.filter(intrumento=item.intrumento, comprador=comprador_actual).first()
        if historial_item:
            HistorialCompra.objects.create(comprador=comprador_actual, lista_compra=historial_item)
    
    # Eliminar la lista de compra
    lista_compra.delete()
    
    # Redirigir al usuario a la página de inicio
    return redirect('musicalapp:home')