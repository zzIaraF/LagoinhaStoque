from django.urls import path
from . import views

urlpatterns = [
    path('saidas/', views.saidas, name="saidas"),
    path('saidas/<int:id>/', views.editSaidas, name="editsaidas"),
    path('exibir/', views.exibirSaidas, name="exibirsaidas"),
    path('deletar/<int:id>/', views.delSaidas, name="delsaidas"),
    path('lucro/', views.lucro, name="lucro"),
    path('lucrodiario/', views.lucrodia, name="lucrodia"),
    path('lucromensal/', views.lucromes, name="lucromes"),
    
]