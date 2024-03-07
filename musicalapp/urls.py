from django.contrib import admin
from django.urls import path
from .views import *
from . import views

app_name = "musicalapp"

urlpatterns = [
    path('prueba/<int:id>/', prueba, name='prueba'),

    # Inicio
    path('', Home, name='home'),
    path('home/', Home, name='home'),

    path('register/', register, name="register"),
    path('login/',my_login, name='my-login'),
    path('logout/', user_logout, name="user-logout"),

    path('usuario/', usuario_page, name="usuario_page"),

    path('usuario/editar/',usuario_editar, name="usuario_editar"),
    path('usuario/historial/',historial,name="historial"),


    # Instrumentos
    path('instrumentos/', lista_instrumentos, name='lista_instrumentos'),
    path('instrumentos/<int:id>/', views.detalle_instrumento, name='detalle_instrumento'),

    path('eliminar-rating/<int:id>/', views.eliminar_comentario_y_rating, name='eliminar_rating'),

    path('instrumentos/piano/', instrumentos_teclas, name='instrumentos_teclas'),
    path('instrumentos/accesorios/', instrumentos_accesorios, name='instrumentos_accesorios'),
    path('instrumentos/viento/', instrumentos_alientos, name='instrumentos_alientos'),
    path('instrumentos/amplificadores/', instrumentos_amplificadores, name='instrumentos_amplificadores'),
    path('instrumentos/bajos-electricos/', instrumentos_bajos_electricos, name='instrumentos_bajos_electricos'),
    path('instrumentos/baterias/', instrumentos_baterias, name='instrumentos_baterias'),
    path('instrumentos/guitarras-acusticas/', instrumentos_guitarras_acusticas, name='instrumentos_guitarras_acusticas'),
    path('instrumentos/guitarras-acusticas-cuerdas-para-acustica/', instrumentos_guitarras_acusticas_cuerdas_para_acustica, name='instrumentos_guitarras_acusticas_cuerdas_para_acustica'),
    path('instrumentos/guitarras-electricas/', instrumentos_guitarras_electricas, name='instrumentos_guitarras_electricas'),
    path('instrumentos/guitarras-electricas-cuerdas/', instrumentos_guitarras_electricas_cuerdas, name='instrumentos_guitarras_electricas_cuerdas'),
    path('instrumentos/pedales-y-efectos/', instrumentos_pedales_y_efectos, name='instrumentos_pedales_y_efectos'),
    path('instrumentos/platillos/', instrumentos_platillos, name='instrumentos_platillos'),
    path('instrumentos/ukuleles/', instrumentos_ukuleles, name='instrumentos_ukuleles'),
    path('instrumentos/violines/', instrumentos_violines, name='instrumentos_violines'),

    #Marcas
    path('instrumentos/marca/Bamboo/', bamboo, name='bamboo'),
    path('instrumentos/marca/Daddario/', daddario, name='daddario'),
    path('instrumentos/marca/Fender/', fender, name='fender'),
    path('instrumentos/marca/Line6/', line6, name='line6'),
    path('instrumentos/marca/New Beat/', new_Beat, name='new_beat'),
    path('instrumentos/marca/Paiste/', paiste, name='paiste'),
    path('instrumentos/marca/Serpentario/', serpentario, name='serpentario'),
    path('instrumentos/marca/Squier/', squier, name='squier'),
    path('instrumentos/marca/Yamaha/', yamaha, name='yamaha'),

    #venta
    path('carrito/', carrito, name='carrito'),
    path('agregar-al-carrito/<int:id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('agregar-uno-al-carrito/<int:id>/', uno_agregar_al_carrito, name='uno_agregar_al_carrito'),
    path('quitar-del-carrito/<int:id>/', quitar_del_carrito, name='quitar_del_carrito'),
    path('pagar/', completar_pago, name='completar_pago'),
]
