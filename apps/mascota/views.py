import os

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages

from apps.mascota.forms import MascotaForm
from apps.mascota.models import *
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

def mascota_view(request, id):
    mascota = Mascota.objects.filter(id=id)

    if mascota:
        mascota = mascota[0]
        return render(request, 'mascota/mascota_detail.html', {'object': mascota})
    else:
        messages.error(request, "No existe el registro de la mascota.")
        return redirect('mascota:mascota_view_list')

def mascota_new(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mascota registrada correctamente.')
            return redirect('mascota:mascota_view_list')
        else:
            messages.error(request, "Los datos ingresados son incorrectos. Corrígelos e intentalo de nuevo")
    else:
        form = MascotaForm()

    return render(request, 'mascota/mascota_form.html', {'form': form})

def mascota_list(request):

    mascotas = Mascota.objects.all().order_by('id')
    context = {'object_list': mascotas}
    return render(request, 'mascota/mascota_list.html', context)

def mascota_edit(request, id):

    mascota = Mascota.objects.filter(id=id)
    if not mascota:
        messages.error(request, "No existe el registro de la mascota.")
        return redirect('mascota:mascota_view_list')

    mascota = mascota[0]
    ruta = mascota.imagen.path

    if request.method == 'GET':
        form = MascotaForm(instance=mascota)
    else:
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            if 'imagen' in form.files:
                if os.path.exists(ruta):
                    os.remove(ruta)

            form.save()
            messages.success(request, 'Mascota actualizada correctamente.')
            return redirect('mascota:mascota_view_list')
        else:
            messages.error(request, "Los datos ingresados son incorrectos. Corrígelos e intentalo de nuevo")

    return render(request, 'mascota/mascota_form.html', {'form': form})

def mascota_delete(request, id):
    mascota = Mascota.objects.filter(id=id)
    if not mascota:
        messages.error(request, "No existe el registro de la mascota.")
        return redirect('mascota:mascota_view_list')

    mascota = mascota[0]
    ruta = mascota.imagen.path

    if request.method == 'POST':
        mascota.delete()
        if os.path.exists(ruta):
            os.remove(ruta)

        messages.success(request, 'Mascota eliminada correctamente.')
        return redirect('mascota:mascota_view_list')

    return render(request, 'mascota/mascota_delete.html', {'object': mascota})

class MascotaList(ListView):
    model = Mascota
    template_name = 'mascota/mascota_list.html'

class MascotaCreateView(CreateView):
    model = Mascota
    form_class = MascotaForm
    template_name = "mascota/mascota_form.html"
    success_url = reverse_lazy('mascota:mascota_list')

    def form_valid(self, form):
        messages.success(self.request, 'Mascota creada correctamente.')
        return super(MascotaCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear mascota. Corrige los datos e intentalo de nuevo')
        return super(MascotaCreateView, self).form_invalid(form)

class MascotaUpdateView(UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = "mascota/mascota_form.html"
    success_url = reverse_lazy('mascota:mascota_list')

    def get_object(self, queryset=None):
        mascota = Mascota.objects.filter(id=self.kwargs['pk'])
        if mascota:
            return super(MascotaUpdateView, self).get_object(mascota)
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, "No existe el registro de la mascota.")
            return redirect('mascota:mascota_view_list')
        else:
            return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        id_mascota = self.kwargs.get('pk', 0)
        mascota = self.model.objects.get(id=id_mascota)
        ruta = mascota.imagen.path
        form = self.form_class(request.POST, request.FILES, instance=mascota)

        if form.is_valid():
            if 'imagen' in form.files:
                if os.path.exists(ruta):
                    os.remove(ruta)

            form.save()
            messages.success(request, 'Mascota actualizada correctamente.')
            return redirect('mascota:mascota_list')
        else:
            messages.error(request, "Error al actualizar mascota. Corrige los datos e intentalo de nuevo")
            return render(request, 'mascota/mascota_form.html', {'form': form})

class MascotaDeleteView(DeleteView):
    model = Mascota
    template_name = "mascota/mascota_delete.html"
    success_url = reverse_lazy('mascota:mascota_list')

    def get_object(self, queryset=None):
        id_mascota = self.kwargs.get('pk', 0)
        mascota = self.model.objects.filter(id=id_mascota)
        if mascota:
            return mascota[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, "No existe el registro de la mascota.")
            return redirect('mascota:mascota_view_list')
        else:
            return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        mascota = self.model.objects.get(id=self.kwargs['pk'])
        ruta = mascota.imagen.path
        response = super(MascotaDeleteView, self).delete(request, *args, **kwargs)

        if os.path.exists(ruta):
            os.remove(ruta)

        messages.success(request, 'Mascota eliminada correctamente.')
        return response

class MascotaDetailView(DetailView):
    model = Mascota
    templ_name = 'mascota/mascota_detail.html'

    def get_object(self, queryset=None):
        id_mascota = self.kwargs.get('pk', 0)
        mascota = self.model.objects.filter(id=id_mascota)
        if mascota:
            return mascota[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, "No existe el registro de la mascota.")
            return redirect('mascota:mascota_view_list')
        else:
            return super().dispatch(request, *args, **kwargs)