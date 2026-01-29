from django.urls import path
from . import views

app_name = 'curriculum'

urlpatterns = [
    
    # Página principal
    path('', views.home, name='home'),

    # Mi Hoja de Vida - Solo usuarios autenticados
    path('mi-hoja-vida/', views.mi_hoja_vida, name='mi_hoja_vida'),
    
    # Autenticación
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Panel de gestión
    path('panel-gestion/', views.panel_gestion, name='panel_gestion'),
    
    # Datos personales
    path('agregar-datos-personales/', views.agregar_datos_personales, name='agregar_datos_personales'),
    path('editar-datos-personales/', views.editar_datos_personales, name='editar_datos_personales'),
    
    # Experiencia laboral
    path('agregar-experiencia/', views.agregar_experiencia, name='agregar_experiencia'),
    path('editar-experiencia/<int:pk>/', views.editar_experiencia, name='editar_experiencia'),
    path('eliminar-experiencia/<int:pk>/', views.eliminar_experiencia, name='eliminar_experiencia'),
    
    # Reconocimientos
    path('agregar-reconocimiento/', views.agregar_reconocimiento, name='agregar_reconocimiento'),
    path('editar-reconocimiento/<int:pk>/', views.editar_reconocimiento, name='editar_reconocimiento'),
    path('eliminar-reconocimiento/<int:pk>/', views.eliminar_reconocimiento, name='eliminar_reconocimiento'),
    
    # Cursos
    path('agregar-curso/', views.agregar_curso, name='agregar_curso'),
    path('editar-curso/<int:pk>/', views.editar_curso, name='editar_curso'),
    path('eliminar-curso/<int:pk>/', views.eliminar_curso, name='eliminar_curso'),
    
    # Productos académicos
    path('agregar-producto-academico/', views.agregar_producto_academico, name='agregar_producto_academico'),
    path('editar-producto-academico/<int:pk>/', views.editar_producto_academico, name='editar_producto_academico'),
    path('eliminar-producto-academico/<int:pk>/', views.eliminar_producto_academico, name='eliminar_producto_academico'),
    
    # Productos laborales
    path('agregar-producto-laboral/', views.agregar_producto_laboral, name='agregar_producto_laboral'),
    path('editar-producto-laboral/<int:pk>/', views.editar_producto_laboral, name='editar_producto_laboral'),
    path('eliminar-producto-laboral/<int:pk>/', views.eliminar_producto_laboral, name='eliminar_producto_laboral'),
    
    # Venta Garage
    path('agregar-venta/', views.agregar_venta, name='agregar_venta'),
    path('editar-venta/<int:pk>/', views.editar_venta, name='editar_venta'),
    path('eliminar-venta/<int:pk>/', views.eliminar_venta, name='eliminar_venta'),

    # Descargar PDF
    path('descargar-pdf/', views.descargar_pdf, name='descargar_pdf'),
]