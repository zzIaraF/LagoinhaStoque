from django.shortcuts import render, redirect, get_object_or_404
from .models import Entradas
from estoque.models import Produto
from .forms import EntradasForm
from django.contrib import messages
from django.db.models import Sum, F
from django.db import models
from datetime import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def entradas(request):
    if request.method == 'POST':
        form = EntradasForm(request.POST)
        if form.is_valid():
            nomedoproduto = form.cleaned_data['nomedoproduto']
            quantidadeentrada = form.cleaned_data['quantidade']

            entrada = form.save(commit=False)
            produto = Produto.objects.get(nome=nomedoproduto)
            entrada.produto = produto
            entrada.save()

            # Atualizar a quantidade no produto
            produto.estoque += quantidadeentrada
            produto.save()
            messages.success(request, "Entrada salva!")

            # Diminui a quant no estoque
            dataentrada = entrada.data
            entradas = Entradas.objects.filter(data=dataentrada).order_by('-id')
            valortotal = entradas.aggregate(total=Sum(F('produto__precovenda') * F('quantidade'), output_field=models.FloatField()))['total'] or 0

            contexto = {
                'form': EntradasForm(),  
                'entradas': entradas,
                'valortotal': valortotal,
            }

            return render(request, 'entradas/entradas.html', contexto)

    else:
        form = EntradasForm()

    contexto = {
        'form': form
        }
    return render(request, 'entradas/entradas.html', contexto)

#é para aparecer no HTML apenas as entradas da data que o usuario digitar
@login_required(login_url='login')
def exibirEntradas(request):
    if request.method == 'POST':
        form_data_str = request.POST.get('data')
        data = datetime.strptime(form_data_str, '%d/%m/%Y').date()
        entradas = Entradas.objects.order_by('-id').filter(data=data)
        valortotal = entradas.aggregate(total=Sum(F('produto__precovenda') * F('quantidade'), output_field=models.FloatField()))['total'] or 0

    contexto = {
        'entradas': entradas,
        'valortotal': valortotal,
        'form': EntradasForm(), 
    }
    return render(request, 'entradas/entradas.html', contexto)

@login_required(login_url='login')
def editEntradas(request, id):
    entrada = get_object_or_404(Entradas, id=id)
    form = EntradasForm(instance=entrada)

    if request.method == 'POST':
        form = EntradasForm(request.POST, instance=entrada)
        if form.is_valid():
            nova_quantidade = form.cleaned_data['quantidade']
            quantidade_anterior = Entradas.objects.get(id=id).quantidade

            # diferença entre a nova quantidade e a quantidade original
            diferenca_quantidade = nova_quantidade - quantidade_anterior

            # Atualiza o estoque do produto com base na diferença de quantidade
            produto = entrada.produto
            produto.estoque = F('estoque') + diferenca_quantidade
            produto.save()
            form.save()

            messages.success(request, "Entrada editada")
            return redirect('entradas')

    contexto = {
        'form': form
    }      
    return render(request, 'entradas/editentradas.html', contexto)


@login_required(login_url='login')
def delEntradas(request, id):
    entrada = get_object_or_404(Entradas, pk=id)
    if request.method == 'POST':
        quant = request.POST.get('quant')
        produto = entrada.produto

        # dimunie a quantidade de volta ao banco
        produto.estoque -= int(quant)
        produto.save()        
        entrada.delete()
        messages.success(request, "Entrada deletada com sucesso!")
        return redirect('entradas')
    contexto = {
        'entrada': entrada
    }
    return render(request, 'entradas/excluir.html', contexto)

