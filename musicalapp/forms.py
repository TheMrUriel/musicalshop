from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from django.forms.widgets import PasswordInput, TextInput
from django.template.loader import render_to_string

class StarRatingWidget(forms.widgets.Widget):
    template_name = 'Conex/star_rating_widget.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return render_to_string(self.template_name, context)

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)
        context['widget']['value'] = value
        return context

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Comprador
        fields = ['nombre', 'apellido', 'edad', 'genero', 'calle', 'ciudad', 'estado', 'codigo_postal']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Ratings
        fields = ['Puntuacion', 'Comentario']
        widgets = {
            'Puntuacion': StarRatingWidget(),  # Utiliza el widget personalizado
            'Comentario': forms.Textarea(attrs={'rows': 4})  # Para mostrar el texto del instrumento
        }  


class CompradorForm(forms.ModelForm):

    apellido = forms.CharField(max_length=255)
    edad = forms.IntegerField()
    calle = forms.CharField(max_length=255)
    ciudad = forms.CharField(max_length=255)
    estado = forms.CharField(max_length=255)
    codigo_postal = forms.CharField(max_length=10)
    colonia = forms.CharField(max_length=255)
    genero = forms.ChoiceField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')], required=True)

    class Meta:
        model = Comprador
        fields = ['nombre', 'apellido', 'edad', 'genero','calle','ciudad','estado','codigo_postal','colonia']     

class CreateUserForm(UserCreationForm):
    nombre = forms.CharField(max_length=255)
    email = forms.EmailField(required=True)
    apellido = forms.CharField(max_length=255)
    edad = forms.IntegerField()
    calle = forms.CharField(max_length=255)
    ciudad = forms.CharField(max_length=255)
    estado = forms.CharField(max_length=255)
    codigo_postal = forms.CharField(max_length=10)
    numero_casa = forms.CharField(max_length=255)
    colonia = forms.CharField(max_length=255)
    genero = forms.ChoiceField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nombre', 'apellido', 'edad', 'genero','calle','ciudad','estado','codigo_postal','colonia','numero_casa']

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Crea el perfil del comprador asociado
            Comprador.objects.create(
                usuario=user,
                correo=user.email,
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                edad=self.cleaned_data['edad'],
                calle=self.cleaned_data['calle'],
                ciudad=self.cleaned_data['ciudad'],
                estado=self.cleaned_data['estado'],
                codigo_postal=self.cleaned_data['codigo_postal'],
                colonia=self.cleaned_data['colonia'],
                numero_casa=self.cleaned_data['numero_casa'],
                genero=self.cleaned_data['genero']
            )
        return user



class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())