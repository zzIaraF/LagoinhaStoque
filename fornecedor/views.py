from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Fornecedor
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def cadastrarfornecedor(request): #cadastro do fornecedor
    fornecedores = Fornecedor.objects.all()
    
    if request.method == 'POST':
        razaosocial = request.POST.get('razaosocial', '').strip()
        cnpj = request.POST.get('cnpj', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        endereco = request.POST.get('endereco', '').strip()

        try:
           
            if not razaosocial or razaosocial.isspace():
                raise ValueError("Razão social inválida!")

            
            cnpj = ''.join(char for char in cnpj if char.isdigit())
            if not cnpj.isdigit() or len(cnpj) != 14:
                raise ValueError("CNPJ inválido!")

          
            if not telefone.isdigit() or len(telefone) != 11:
                raise ValueError("Telefone inválido!")
            
            if not endereco or endereco.isspace():
                raise ValueError("Endereço inválido!")
            
            
            if Fornecedor.objects.filter(Q(razaosocial=razaosocial) | Q(cnpj=cnpj)).exists():
                raise ValueError("Razão social ou CNPJ já cadastrados!")

            # Obtém a data atual
            data = datetime.now()

            novo_fornecedor = Fornecedor(
                razaosocial=razaosocial,
                cnpj=cnpj,
                telefone=telefone,
                data=data,
                endereco=endereco,
            )

            novo_fornecedor.save()
            messages.success(request, "Fornecedor cadastrado com sucesso!")
            return redirect('listarfornecedor')

        except ValueError as e:
            messages.error(request, f"{e}")

    return render(request, 'fornecedor/cadastrarfornecedor.html', {'fornecedores': fornecedores})

@login_required(login_url='login')
def listarfornecedor(request):
    search_term = request.GET.get('search', '')
    fornecedores = Fornecedor.objects.all()

    if search_term:
        fornecedores = fornecedores.filter(Q(razaosocial__icontains=search_term) | Q(cnpj__icontains=search_term))

    return render(request, 'fornecedor/listarfornecedor.html', {'fornecedores': fornecedores, 'search_term': search_term})


@login_required(login_url='login')
def editar_fornecedor(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)

    if request.method == 'POST':
        fornecedor.razaosocial = request.POST.get('razaosocial', '').strip()
        fornecedor.cnpj = request.POST.get('cnpj', '').strip()
        fornecedor.telefone = request.POST.get('telefone', '').strip()
        fornecedor.endereco = request.POST.get('endereco','').strip()
        
        fornecedor.save()
        messages.success(request, "Fornecedor editado com sucesso!")
        return redirect('listarfornecedor')
    
    
    
    return render(request, 'fornecedor/editar_fornecedor.html', {'fornecedor': fornecedor})

@login_required(login_url='login')
def exibirfornecedor(request,fornecedor_id): # Exibição de produto
    fornecedor = get_object_or_404(Fornecedor, id= fornecedor_id )  
    context = {
        'fornecedor': fornecedor, 
    }

    

    return render(request, 'fornecedor/exibirfornecedor.html', context)

@login_required(login_url='login')
def inativar_fornecedor(request, fornecedor_id): # Inativação do fornecedor
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)

    if request.method == 'POST':
        fornecedor.ativo = False
        fornecedor.save()
        messages.success(request, f"Fornecedor {fornecedor.razaosocial} inativado com sucesso!")
        return redirect('listarfornecedor')

    return render(request, 'fornecedor/inativar_fornecedor.html', {'fornecedor': fornecedor})

@login_required(login_url='login')
def ativar_fornecedor(request, fornecedor_id): # Ativação do fornecedor
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
    fornecedor.ativo = True
    fornecedor.save()
    messages.success(request, f"Fornecedor {fornecedor.razaosocial} ativado com sucesso!")
    return redirect('listarfornecedor')
