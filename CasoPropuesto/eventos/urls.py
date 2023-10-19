from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('evento/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('crear_evento/', views.crear_evento, name='crear_evento'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('crear_registro_evento/', views.crear_registro_evento, name='crear_registro_evento'),
    path('lista_eventos/', views.lista_eventos, name='lista_eventos'),
     path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('lista_registros_evento/', views.lista_registros_evento, name='lista_registros_evento'),
    path('editar_evento/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eliminar_evento/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('editar_registro_evento/<int:registro_id>/', views.editar_registro_evento, name='editar_registro_evento'),
    path('eliminar_registro_evento/<int:registro_id>/', views.eliminar_registro_evento, name='eliminar_registro_evento'),
   
]