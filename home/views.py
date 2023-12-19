from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request, 'home/index.html')


def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        auth.login(request, form.get_user())
        return redirect('home')
    contexto = {
        'form': form,
        'form_errors': form.errors.items()
    }
    return render(request, 'home/login.html', contexto)

def handler404(request, exception):
    return render(request, 'home/404.html')

def handler403(request, exception):
    return render(request, 'home/403.html')

def handler500(request):
    return render(request, 'home/500.html')