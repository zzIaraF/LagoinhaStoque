from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categoria,Produto, Fornecedor
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import ProtectedError
from rolepermissions.decorators import has_permission_decorator, has_role_decorator


@login_required(login_url='login')
@login_required
def add_produtos(request): # Cadastrar produto
    categorias = Categoria.objects.all()
    fornecedores = Fornecedor.objects.filter(ativo=True)
    user = request.user

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        preco = request.POST.get('preco', '0').replace(',', '.')  # vai substituir a vírgula por ponto
        precovenda = request.POST.get('precovenda', '0').replace(',', '.')  
        estoquemin_str = request.POST.get('estoquemin', '0').replace(',', '.')  
        ncm = request.POST.get('ncm', '')
        descricao = request.POST.get('descricao', '').strip() 

        try:
            # Vai converter os números de string para decimal ou inteiro
            preco_decimal = Decimal(preco)
            precovenda_decimal = Decimal(precovenda)
            estoquemin_float = float(estoquemin_str)

            # Verifica se a quantidade mínima é um número inteiro
            if estoquemin_float.is_integer():
                estoquemin_int = int(estoquemin_float)
            else:
                raise ValueError("A quantidade mínima deve ser um número inteiro.")

            if preco_decimal <= Decimal('0'):
                messages.error(request, "O preço deve ser maior que zero.")
            elif descricao == "" or descricao.isspace():
                messages.error(request, "Descrição inválida!")
            elif nome == "" or nome.isspace():
                messages.error(request, "Nome inválido!")
            elif precovenda_decimal <= Decimal('0'):
                messages.error(request, "O preço de venda deve ser maior que zero.")
            elif estoquemin_int <= 0:
                messages.error(request, "O estoque mínimo deve ser maior que zero.")
            else:
                categoria_id = request.POST.get('categoria')
                categoria = get_object_or_404(Categoria, pk=categoria_id)

                fornecedor_id = request.POST.get('fornecedor')
                fornecedor = get_object_or_404(Fornecedor, pk=fornecedor_id)

                # Vai definir que a quantidade padrão ao criar um novo produto será "0"
                quantidade_padrao = 0

                novo_cadastro = Produto(
                    nome=nome,
                    preco=preco_decimal,
                    precovenda=precovenda_decimal,
                    estoque=quantidade_padrao,
                    estoquemin=estoquemin_int,
                    categoria=categoria,
                    fornecedor=fornecedor,
                    ncm=ncm,
                    descricao=descricao,
                    usuario=user
                )
                novo_cadastro.save()

                messages.success(request, "Produto cadastrado com sucesso!")
                return redirect('listaProdutos')

        except ValueError as e:
            messages.error(request, f" {e}")
            return redirect('add_produtos')

    return render(request, 'estoque/add_produtos.html', {'categorias': categorias, 'fornecedores': fornecedores})


@login_required(login_url='login')
def prod_exibir(request, produto_id,fornecedor_id): # Exibição de produto
    produto = get_object_or_404(Produto, id=produto_id)
    fornecedor = get_object_or_404(Fornecedor, id= fornecedor_id )  
    context = {
        'produto': produto,
        'fornecedor': fornecedor, 
    }

    return render(request, 'estoque/prod_exibir.html', context)


@login_required(login_url='login')
def listaProdutos(request): # Listagem de produto
    produtos = Produto.objects.all()
    if request.GET.get('pesquisa'):
        pesq = request.GET.get('pesquisa')
        produtos = produtos.filter(Q(nome__icontains=pesq)).order_by('-id')
    else:
        produtos = Produto.objects.order_by('-id').filter
    contexto = {
        'produtos': produtos,
    } 
    return render(request, 'estoque/listaProdutos.html', contexto)


@login_required(login_url='login')
def editarProdutos(request, produto_id):  # Editar produto
    produto = get_object_or_404(Produto, pk=produto_id)
    categorias = Categoria.objects.all()
    fornecedores = Fornecedor.objects.filter(ativo=True)

    if request.method == 'POST':
        produto.nome = request.POST.get('nome', '')
        produto.descricao = request.POST.get('descricao', '')
        preco_str = request.POST.get('preco', '')
        precovenda_str = request.POST.get('precovenda', '')
        estoquemin_str = request.POST.get('estoquemin', '0').replace(',', '.')
        ncm = request.POST.get('ncm', '')

        categoria_id = request.POST.get('categoria')
        fornecedor_id = request.POST.get('fornecedor')

        try:
            # Validação e conversão de preços e estoquemin
            preco_str = preco_str.replace(',', '.')
            precovenda_str = precovenda_str.replace(',', '.')
            produto.preco = Decimal(preco_str)
            produto.precovenda = Decimal(precovenda_str)
            produto.estoquemin = int(estoquemin_str)

            # Validação e atribuição de categoria
            categoria = get_object_or_404(Categoria, pk=categoria_id)
            produto.categoria = categoria

            # Validação e atribuição de fornecedor
            fornecedor = get_object_or_404(Fornecedor, pk=fornecedor_id)
            produto.fornecedor = fornecedor

            produto.ncm = ncm
            produto.save()

            messages.success(request, "Produto editado com sucesso!")
            return redirect('listaProdutos')

        except( ValueError, Fornecedor.ObjectDoesNotExist) as e:
            messages.error(request, f"Erro ao editar o produto: {e}")

    return render(request, 'estoque/editarProdutos.html', {'produto': produto, 'categorias': categorias, 'fornecedores': fornecedores})



@login_required(login_url='login')
def cadastrarCategorias(request): # cadastro de categoria
    if request.method == 'POST':
        nome = request.POST.get('nome').strip()
        
        if nome == "":
            messages.error(request, "Nome inválido!")
            return render(request, 'estoque/add_categoria.html')             
        nova_categoria = Categoria(
            nome=nome)
        nova_categoria.save()
        messages.success(request, "Categoria cadastrada com sucesso!")
        return redirect('listagem_categorias')
    return render(request, 'estoque/add_categoria.html')


@login_required(login_url='login')
def listaCategorias(request): #listagem de categorias
    categorias = Categoria.objects.all()
    if request.GET.get('pesquisa'):
        pesq = request.GET.get('pesquisa')
        categorias = categorias.filter(Q(nome__icontains=pesq)).order_by('-id')
    else:
        categorias = Categoria.objects.order_by('-id').filter
    contexto = {
        'categorias': categorias,
    } 
    return render(request, 'estoque/cat_listagem.html', contexto)



@login_required(login_url='login')
def cat_editar(request, categoria_id): #editar de categorias
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    contexto = {
        'categoria': categoria
    }
    if request.method == "POST":
        nome = request.POST.get('nome').strip()

        if nome == "":
            messages.error(request, "Nome inválido!")
            return render(request, 'estoque/cat_editar.html', contexto)             
          
        categoria.nome = nome
        categoria.save()
        messages.success(request, "Categoria editada com sucesso!")
        return redirect('listagem_categorias')
    return render(request, 'estoque/cat_editar.html', contexto)

  
@has_permission_decorator('ex_cat')
def cat_excluir(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, "Categoria deletada com sucesso!")
            return redirect('listagem_categorias')
        except ProtectedError:
            messages.error(request, "Você não pode excluir uma categoria que está cadastrada em um produto.")
    contexto = {
        'categoria': categoria
    }
    return render(request, 'estoque/excluir.html', contexto)  



