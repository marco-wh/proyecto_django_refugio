from django.conf.urls import url
from apps.mascota.views import *


urlpatterns = [
    url(r'^class/nuevo$', MascotaCreateView.as_view(), name='mascota_new'),
    url(r'^class/listar$', MascotaList.as_view(), name='mascota_list'),
    url(r'^class/editar/(?P<pk>\d+)/$', MascotaUpdateView.as_view(), name='mascota_edit'),
    url(r'^class/eliminar/(?P<pk>\d+)/$', MascotaDeleteView.as_view(), name='mascota_del'),
    url(r'^class/ver/(?P<pk>\d+)/$', MascotaDetailView.as_view(), name='mascota_ver'),

    url(r'^view/nuevo$', mascota_new, name='mascota_view_new'),
    url(r'^view/listar$', mascota_list, name='mascota_view_list'),
    url(r'^view/editar/(?P<id>\d+)/$', mascota_edit, name='mascota_view_edit'),
    url(r'^view/eliminar/(?P<id>\d+)/$', mascota_delete, name='mascota_view_del'),
    url(r'^view/ver/(?P<id>\d+)/$', mascota_view, name='mascota_view_ver'),
]
