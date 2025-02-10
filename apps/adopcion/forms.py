from django import forms
from apps.adopcion.models import *

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona

        fields = [
            'nombre',
            'apellidos',
            'edad',
            'telefono',
            'email',
            'domicilio',
        ]

        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'edad': 'Edad',
            'telefono': 'Teléfono',
            'email': 'Email',
            'domicilio': 'Domicilio'
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilio': forms.Textarea(attrs={'class': 'form-control'})
        }


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud

        fields = [
            'persona',
            'numero_mascotas',
            'razones'
        ]

        labels = {
            'persona': 'Persona Solicitante',
            'numero_mascotas': 'Número de mascotas',
            'razones': 'Razones'
        }

        widgets = {
            'persona': forms.Select(attrs={'class': 'form-control'}),
            'numero_mascotas': forms.TextInput(attrs={'class': 'form-control'}),
            'razones': forms.Textarea(attrs={'class': 'form-control'})
        }