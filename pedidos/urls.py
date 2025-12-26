from django.urls import path
from . import views

urlpatterns = [
    path('', views.solicitudes, name='solicitudes'),
    path('crear/', views.pedido_crear, name='pedido_crear'),
    path('editar/<int:id>/', views.pedido_editar, name='pedido_editar'),
    path('eliminar/<int:id>/', views.pedido_eliminar, name='pedido_eliminar'),
    path("buscar-dun/", views.buscar_por_dun, name="buscar_dun"),
    path('crear-superusuario/', views.crear_superusuario, name='crear_superusuario'),
    path('resumen-bsf/', views.resumen_bsf, name='resumen_bsf'),
]
