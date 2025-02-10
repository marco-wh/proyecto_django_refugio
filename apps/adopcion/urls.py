from django.conf.urls import url
from apps.adopcion.views import *


urlpatterns = [
    url(r'^solicitud/class/ver/(?P<pk>\d+)', SolcitudDetail.as_view(), name='solicitud_ver'),
    url(r'^solicitud/class/lista', SolicitudList.as_view(), name='solicitud_list'),
    url(r'^solicitud/class/nueva', SolicitudCreate.as_view(), name='solicitud_form'),
    url(r'^solicitud/class/editar/(?P<pk>\d+)', SolicitudUpdate.as_view(), name='solicitud_edit'),
    url(r'^solicitud/class/eliminar/(?P<pk>\d+)', SolicitudDelete.as_view(), name='solicitud_del'),

    url(r'^solicitud/view/ver/(?P<id>\d+)', solicitud_view, name='solicitud_view_ver'),
    url(r'^solicitud/view/lista', solicitud_list, name='solicitud_view_list'),
    url(r'^solicitud/view/nueva', solicitud_new, name='solicitud_view_form'),
    url(r'^solicitud/view/editar/(?P<id>\d+)', solicitud_edit, name='solicitud_view_edit'),
    url(r'^solicitud/view/eliminar/(?P<id>\d+)', solicitud_del, name='solicitud_view_del'),

    url(r'^persona/class/ver/(?P<pk>\d+)', PersonaDetailView.as_view(), name='persona_ver'),
    url(r'^persona/class/lista', PersonaListView.as_view(), name='persona_list'),
    url(r'^persona/class/editar/(?P<pk>\d+)', PersonaUpdateView.as_view(), name='persona_edit'),
    url(r'^persona/class/eliminar/(?P<pk>\d+)', PersonaDeleteView.as_view(), name='persona_del'),

    url(r'^persona/view/ver/(?P<id>\d+)', persona_view, name='persona_view_ver'),
    url(r'^persona/view/lista', persona_list, name='persona_view_list'),
    url(r'^persona/view/editar/(?P<id>\d+)', persona_edit, name='persona_view_edit'),
    url(r'^persona/view/eliminar/(?P<id>\d+)', persona_del, name='persona_view_del'),
]