from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from apps.adopcion.forms import *
from apps.adopcion.models import *


class SolicitudList(ListView):
    model = Solicitud
    template_name = 'adopcion/solicitud_list.html'

class SolcitudDetail(DetailView):
    model = Solicitud
    template_name = 'adopcion/solicitud_detail.html'
    context_object_name = 'solicitud'

    def get_object(self, queryset=None):
        solicitud = self.model.objects.filter(pk=self.kwargs['pk'])
        if solicitud:
            return solicitud[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'No se encontró la solicitud')
            return redirect('adopcion:solicitud_list')
        else:
            return super().dispatch(request, *args, **kwargs)

class SolicitudCreate(CreateView):
    model = Solicitud
    template_name = 'adopcion/solicitud_form.html'
    form_class = SolicitudForm
    second_form_class = PersonaForm
    success_url = reverse_lazy('adopcion:solicitud_list')

    def get_context_data(self, **kwargs):
        context = super(SolicitudCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)

        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object

        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)

        if form.is_valid() and form2.is_valid():
            solicitud = form.save(commit=False)
            solicitud.persona = form2.save()
            solicitud.save()

            messages.success(request, 'Solicitud registrada exitosamente')
            return HttpResponseRedirect(self.get_success_url())

        else:
            messages.error(request, 'Error al registrarse. Corriga los datos e intentelo de nuevo.')
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class SolicitudUpdate(UpdateView):
    model = Solicitud
    template_name = 'adopcion/solicitud_edit.html'
    form_class = SolicitudForm
    success_url = reverse_lazy('adopcion:solicitud_list')

    def get_context_data(self, **kwargs):
        context = super(SolicitudUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)

        solicitud = self.model.objects.get(id=pk)

        if 'form' not in context:
            context['form'] = self.form_class()

        context['id'] = pk
        return context

    def get_object(self, queryset=None):
        solicitud = self.model.objects.filter(pk=self.kwargs['pk'])
        if solicitud:
            return solicitud[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'No se encontró la solicitud')
            return redirect('adopcion:solicitud_list')
        else:
            return super(SolicitudUpdate, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_solicitud = self.kwargs.get('pk', 0)
        solicitud = self.model.objects.get(id=id_solicitud)
        form = self.form_class(request.POST, instance=solicitud)

        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud actualizada exitosamente')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request, 'Error al actualizar. Corrige los datos e intentelo de nuevo.')

        return render(request, self.template_name, {'form': form})

class SolicitudDelete(DeleteView):
    model = Solicitud
    template_name = "adopcion/solicitud_delete.html"
    success_url = reverse_lazy('adopcion:solicitud_list')

    def get_object(self, queryset=None):
        solicitud = self.model.objects.filter(pk=self.kwargs['pk'])
        if solicitud:
            return solicitud[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'No se encontró la solicitud')
            return redirect('adopcion:solicitud_list')
        else:
            return super(SolicitudDelete, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super(SolicitudDelete, self).delete(request, *args, **kwargs)
        messages.success(request, 'Solicitud eliminada exitosamente')
        return response

def solicitud_view(request, id):
    solicitud = Solicitud.objects.filter(id=id)

    if solicitud:
        return render(request, 'adopcion/solicitud_detail.html', {'solicitud': solicitud[0]})
    else:
        messages.error(request, 'No se encontró la solicitud.')
        return redirect('adopcion:solicitud_view_list')

def solicitud_list(request):
    solicitudes = Solicitud.objects.all()
    context = {'object_list': solicitudes}
    return render(request, 'adopcion/solicitud_list.html', context)

def solicitud_new(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        form2 = PersonaForm(request.POST)

        if form.is_valid() and form2.is_valid():
            solicitud = form.save(commit=False)
            solicitud.persona = form2.save()
            solicitud.save()

            messages.success(request, 'Solicitud registrada exitosamente')
            return redirect('adopcion:solicitud_view_list')

        else:
            messages.error(request, 'Error al registar. Corrige los datos e intentelo de nuevo.')
            context = {'form': form, 'form2': form2}
    else:
       context = {'form': SolicitudForm(), 'form2': PersonaForm()}

    return render(request, 'adopcion/solicitud_form.html', context)

def solicitud_edit(request, id):
    solicitud = Solicitud.objects.filter(id=id)
    if solicitud:
        solicitud = solicitud[0]
    else:
        messages.error(request, 'No se encontró la solicitud.')
        return redirect('adopcion:solicitud_view_list')

    if request.method == 'POST':
        form = SolicitudForm(request.POST, instance=solicitud)

        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud actualizada exitosamente')
            return redirect('adopcion:solicitud_view_list')
        else:
            messages.error(request, 'Error al actualizar. Corrige los datos e intentelo de nuevo.')
    else:
        form = SolicitudForm(instance=solicitud)

    return render(request, 'adopcion/solicitud_edit.html', {'form': form})

def solicitud_del(request, id):
    solicitud = Solicitud.objects.filter(id=id)
    if solicitud:
        solicitud = solicitud[0]
    else:
        messages.error(request, 'No se encontró la solicitud.')
        return redirect('adopcion:solicitud_view_list')

    if request.method == 'POST':
        solicitud.delete()
        messages.success(request, 'Solicitud eliminada exitosamente')
        return redirect('adopcion:solicitud_view_list')

    return render(request, 'adopcion/solicitud_delete.html', {'object': solicitud})

class PersonaListView(ListView):
    model = Persona
    template_name = 'adopcion/persona_list.html'
    context_object_name = 'personas'

class PersonaDetailView(DetailView):
    model = Persona
    template_name = 'adopcion/persona_detail.html'
    context_object_name = 'persona'

    def get_object(self, queryset=None):
        persona = self.model.objects.filter(pk=self.kwargs['pk'])
        if persona:
            return persona[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'No se encontó a la persona')
            return redirect('adopcion:persona_list')
        else:
            return super(PersonaDetailView, self).dispatch(request, *args, **kwargs)

class PersonaUpdateView(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'adopcion/persona_edit.html'
    success_url = reverse_lazy('adopcion:persona_list')

    def get_object(self, queryset=None):
        persona = self.model.objects.filter(pk=self.kwargs['pk'])
        if persona:
            return persona[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'No se encontró la persona')
            return redirect('adopcion:persona_list')
        else:
            return super(PersonaUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Persona actualizada exitosamente')
        return super(PersonaUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar a la persona. Corrige los datos e intentelo de nuevo.')
        return super(PersonaUpdateView, self).form_invalid(form)

class PersonaDeleteView(DeleteView):
    model = Persona
    template_name = 'adopcion/persona_delete.html'
    context_object_name = 'persona'
    success_url = reverse_lazy('adopcion:persona_list')

    def get_object(self, queryset=None):
        persona = self.model.objects.filter(pk=self.kwargs['pk'])
        if persona:
            return persona[0]
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(request, 'No se encontro la persona')
            return redirect('adopcion:persona_list')
        else:
            return super(PersonaDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super(PersonaDeleteView, self).delete(request, *args, **kwargs)
        messages.success(request, 'Persona eliminada exitosamente')
        return response

def persona_view(request, id):
    persona = Persona.objects.filter(id=id)

    if persona:
        return render(request, 'adopcion/persona_detail.html', {'persona': persona[0]})
    else:
        messages.error(request, 'No se encontró a la persona.')
        return redirect('adopcion:persona_view_list')

def persona_list(request):
    personas = Persona.objects.all()
    context = {'personas': personas}
    return render(request, 'adopcion/persona_list.html', context)

def persona_edit(request, id):
    persona = Persona.objects.filter(id=id)
    if persona:
        persona = persona[0]
    else:
        messages.error(request, 'No se encontró a la persona.')
        return redirect('adopcion:persona_list')

    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)

        if form.is_valid():
            form.save()
            messages.success(request, 'Persona actualizada exitosamente')
            return redirect('adopcion:persona_view_list')
        else:
            messages.error(request, 'Error al actualizar. Corrige los datos e intentelo de nuevo.')
    else:
        form = PersonaForm(instance=persona)

    return render(request, 'adopcion/persona_edit.html', {'form': form})

def persona_del(request, id):
    persona = Persona.objects.filter(id=id)
    if persona:
        persona = persona[0]
    else:
        messages.error(request, 'No se encontró a la persona.')
        return redirect('adopcion:persona_list')

    if request.method == 'POST':
        persona.delete()
        messages.success(request, 'Persona eliminada exitosamente')
        return redirect('adopcion:persona_view_list')

    return render(request, 'adopcion/persona_delete.html', {'persona': persona})