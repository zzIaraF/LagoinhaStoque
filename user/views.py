from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages, auth
from .forms import UserForm, UserEditForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role, remove_role
from django.db.models import ProtectedError
from rolepermissions.decorators import has_permission_decorator, has_role_decorator

# Create your views here.
@has_role_decorator('gerente')
def create(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.is_active = True 
        form.save()
        opc = request.POST.get('opc')
        if opc == '0':
            assign_role(form, 'gerente')
        else:
            assign_role(form, 'vendedor')
        return redirect('exibiruser')
    contexto = {
        'form': form,
        'form_errors': form.errors.items()
    }
    return render(request, 'user/cadastro.html', contexto)


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, 'Usuário deslogado!')
    return redirect('login')

@has_role_decorator('gerente')
def exibiruser(request):
    usuarios = User.objects.all()
    contexto = {
        'usuarios': usuarios,
    }       
    return render(request, 'user/exibiruser.html', contexto)

@has_role_decorator('gerente')
def edituser(request, id):
    user = get_object_or_404(User, id=id)
    form = UserEditForm(instance=user)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)

        if form.is_valid():
            opc = request.POST.get('opc')
            if opc == '0':
                assign_role(user, 'gerente')
                remove_role(user, 'vendedor') # remove o grupo
                # senao ficaria com os dois
                # vai sorrir de Natanael dnv kkkkk
            else:
                assign_role(user, 'vendedor')
                remove_role(user, 'gerente')
            
            # Atualiza o campo opc no formulário 
            form.cleaned_data['opc'] = opc
            form.save()
            messages.success(request, "Opção do usuário atualizada com sucesso.")
            return redirect('home')
        else:
            messages.error(request, "Erro ao atualizar opção do usuário")

    contexto = {
        'form': form,
    }
    return render(request, 'user/edituser.html', contexto)

@has_permission_decorator('edit_user')
@login_required
def editpropriouser(request):  # edição de usuário
    user = request.user
    form = UserEditForm(instance=user)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect('home')
            

    contexto = {
        'form': form,  
        'form_errors': form.errors.items()
    }
    return render(request, 'user/edituser.html', contexto)

@has_role_decorator('gerente')
@login_required
def excUser(request, id):
    user = request.user
    usuario = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        if usuario == user:
            messages.error(request, "você não pode apagar seu proprio usuario")
        else:
            try:
                usuario.delete()
                messages.success(request, "Usuario deletado com sucesso!")
                return redirect('exibiruser')
            except ProtectedError:
                messages.error(request, "erro.")
    contexto = {
        'usuario': usuario
    }
    return render(request, 'user/excluir.html', contexto)  

