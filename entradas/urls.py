from django.urls import path
from . import views

urlpatterns = [
    path('entradas/', views.entradas, name="entradas"),
    path('exibir/', views.exibirEntradas, name="exibirentradas"),  
    path('editar/<int:id>/', views.editEntradas, name="edientradas"),
    path('deletar/<int:id>/', views.delEntradas, name="delentradas"),
]