from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name="create"),
    path('logout/', views.logout, name="logout"),
    path('usuarios/', views.exibiruser, name="exibiruser"),
    path('editar/<int:id>/', views.edituser, name="ediuser"),
    path('editar/', views.editpropriouser, name="editpropriouser"),
    path('deletar/<int:id>/', views.excUser, name="excUser"),
]
