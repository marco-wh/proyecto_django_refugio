from django import forms
from apps.mascota.models import *
from django.contrib.admin.widgets import AdminFileWidget

class MascotaForm(forms.ModelForm):

    class Meta:
        model = Mascota

        fields = [
            'nombre',
            'sexo',
            'edad',
            'fecha_rescate',
            'persona',
            'vacuna',
            'imagen'
        ]

        labels = {
            'nombre' : 'Nombre',
            'sexo' : 'Sexo',
            'edad' : 'Edad',
            'fecha_rescate' : 'Fecha de rescate',
            'persona' : 'Persona',
            'vacuna' : 'Vacuna',
            'imagen' : 'Foto'
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_rescate': forms.TextInput(attrs={'class': 'form-control'}),
            'persona': forms.Select(attrs={'class': 'form-control'}),
            'vacuna': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'imagen' : AdminFileWidget(attrs={'class': 'form-control'}),
        }


class VacunaForm(forms.ModelForm):

    class Meta:
        model = Vacuna

        fields = ['nombre',]

        labels = {'nombre' : 'Nombre',}

        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control'}),}


