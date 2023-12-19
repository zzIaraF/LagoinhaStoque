from django.shortcuts import render, redirect, get_object_or_404
from .models import Saidas
from estoque.models import Produto
from estoque.forms import ProdutosForm
from .forms import SaidasForm
from django.contrib import messages
from django.db.models import Sum, F
from django.db import models
from datetime import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def saidas(request):
    saida = None  
    if request.method == 'POST':
        form = SaidasForm(request.POST, request.FILES)
        if form.is_valid():
            nomedoproduto = form.cleaned_data['nomedoproduto']
            produto = Produto.objects.get(nome=nomedoproduto)
            quantidadesaida = form.cleaned_data['quantidade']

            if quantidadesaida > produto.estoque:
                messages.error(request, "Quantidade de produto maior que a disponível no estoque")
            else:
                # Salvar a saída 
                saida = form.save(commit=False)
                saida.produto = produto
                saida.save()

                # Atualizar a quantidade no produto
                produto.estoque -= quantidadesaida
                produto.save()
                messages.success(request, "Saída salva!")
    # diminui a quant no estoque
    if saida is not None:
        datasaida = saida.data
        saidas = Saidas.objects.filter(data=datasaida).order_by('-id')
        valortotal = saidas.aggregate(total=Sum(F('produto__precovenda') * F('quantidade'), output_field=models.FloatField()))['total'] or 0

        contexto = {
            'form': SaidasForm(),
            'saidas': saidas,
            'valortotal': valortotal,
        }

        return render(request, 'saidas/saidas.html', contexto)

    # pro formulário vir vazio
    form = SaidasForm()
    contexto = {
        'form': form,
    }
    return render(request, 'saidas/saidas.html', contexto)

@login_required(login_url='login')
#é para aparecer no HTML apenas as saidas da data que o usuario digitar
def exibirSaidas(request):
    form = SaidasForm(request.POST, request.FILES)
    if request.method == 'POST':
        form_data_str = request.POST.get('data')
        data = datetime.strptime(form_data_str, '%d/%m/%Y').date()
        saidas = Saidas.objects.order_by('-id').filter(data=data)
        valortotal = saidas.aggregate(total=Sum(F('produto__precovenda') * F('quantidade'), output_field=models.FloatField()))['total'] or 0
        contexto = {
            'saidas': saidas,
            'valortotal': valortotal,
            'form': SaidasForm(), 
        }
    return render(request, 'saidas/saidas.html', contexto)

@login_required(login_url='login')
def editSaidas(request, id):
    saida = get_object_or_404(Saidas, id=id)
    form = SaidasForm(instance=saida)

    if request.method == 'POST':
        form = SaidasForm(request.POST, instance=saida)

        if form.is_valid():
            nova_quantidade = form.cleaned_data['quantidade']
            quantidade_anterior = Saidas.objects.get(id=id).quantidade

            #diferença entre a nova quantidade e a quantidade original
            diferenca_quantidade = nova_quantidade - quantidade_anterior

           
            produto = saida.produto
            produto.estoque = F('estoque') - diferenca_quantidade
            produto.save()

            form.save()

            messages.success(request, "Saída editada")
            return redirect('saidas')

    contexto = {
        'form': form
    }      
    return render(request, 'saidas/editsaida.html', contexto)


@login_required(login_url='login')
def delSaidas(request, id):
    saida = get_object_or_404(Saidas, pk=id)
    if request.method == 'POST':
        quant = request.POST.get('quant')
        produto = saida.produto

        # add a quantidade de volta ao banco
        produto.estoque += int(quant)
        produto.save()        

        saida.delete()
        messages.success(request, "Saída deletado com sucesso!")
        return redirect('saidas')
    contexto = {
        'saida': saida
    }
    return render(request, 'saidas/excluir.html', contexto)

@login_required(login_url='login')
def lucro(request):
    return render(request, 'saidas/lucro.html')

@login_required(login_url='login')
def lucrodia(request):
    if request.method == 'POST':
        print("entrou")
        data = request.POST.get('dataDia')
        print(data)
        saidas = Saidas.objects.order_by('-id').filter(data=data)
        valortotal = saidas.aggregate(total=Sum(F('produto__precovenda') * F('quantidade'), output_field=models.FloatField()))['total'] or 0
        lucro = saidas.aggregate(total=Sum((F('produto__precovenda') - F('produto__preco')) * F('quantidade'), output_field=models.FloatField()))['total'] or 0
        quantidadetotal = saidas.aggregate(total_quantidade=Sum('quantidade'))['total_quantidade'] or 0       
        contexto = {
            'saidas': saidas,
            'valortotal': valortotal,
            'quantidadetotal': quantidadetotal,
            'lucro': lucro,
        }
    return render(request, 'saidas/lucro.html', contexto)

@login_required(login_url='login')
def lucromes(request):
    if request.method == 'POST':
        datainicial = request.POST.get('dataI')
        datafinal = request.POST.get('dataF')
        #pega a data que o user digitou e exibe
        saidas = Saidas.objects.filter(data__range=[datainicial, datafinal])

        valortotal = saidas.aggregate(total=Sum(F('produto__precovenda') * F('quantidade'), output_field=models.FloatField()))['total'] or 0
        quantidadetotal = saidas.aggregate(total_quantidade=Sum('quantidade'))['total_quantidade'] or 0
        lucro = saidas.aggregate(total=Sum((F('produto__precovenda') - F('produto__preco')) * F('quantidade'), output_field=models.FloatField()))['total'] or 0

        # Calcula a quantidade total no mês (quantidadetotalM)
    
        contexto = {
            'saidasM': saidas,
            'valortotalM': valortotal,
            'quantidadetotalM': quantidadetotal,
            'lucroM': lucro
        }
    return render(request, 'saidas/lucro.html', contexto)

