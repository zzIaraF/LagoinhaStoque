"""
URL configuration for projetoLagoinha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('adminSuperupper/', admin.site.urls),
    path('estoque/', include ('estoque.urls')),
    path('fornecedor/', include ('fornecedor.urls')),
    path('', include ('home.urls')),
    path('user/', include ('user.urls')),
    path('saidas/', include ('saidas.urls')),
    path('entradas/', include ('entradas.urls')),
]


handler404 = "home.views.handler404"
handler403 = "home.views.handler403"
handler500 = "home.views.handler500"

