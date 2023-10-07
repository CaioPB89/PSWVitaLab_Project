from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate,login
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        primeiro_nome = request.POST.get("primeiro_nome")
        ultimo_nome = request.POST.get("ultimo_nome")
        username = request.POST.get("username")
        senha = request.POST.get("senha")
        email = request.POST.get("email")
        confirmar_senha = request.POST.get("confirmar_senha")

        if User.objects.filter(username=username).exists():
            messages.add_message(request,constants.ERROR,'Username já existe')
            return redirect('/usuarios/cadastro')
        if not senha == confirmar_senha:
            messages.add_message(request,constants.ERROR,'As senhas não são iguais')
            return redirect('/usuarios/cadastro')
        if len(senha) < 6:
            messages.add_message(request,constants.ERROR,'A sua senha deve ter no minimo 7 digitos')
            return redirect('/usuarios/cadastro')
        
        # TODO validar se o username do ussuario já existe
        try:
            user = User.objects.create_user(
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                username = username,
                email = email,
                password = senha,
            )
            messages.add_message(request,constants.SUCCESS,'Usuario cadastrado com sucesso')
        except:
            messages.add_message(request,constants.ERROR,'Erro interno do sistema, tente contatar um ADM')
            return redirect('/usuarios/cadastro')
        return redirect('/usuarios/cadastro')
def logar(request):
    if request.method == 'GET':  
        return render(request,'login.html')   
    if request.method == 'POST':
        username=request.POST.get('username')
        senha=request.POST.get('senha')

        user = authenticate(username=username,password=senha)
        if user:
            login(request,user)
            return redirect('/exames/solicitar_exames/')
        else:
            messages.add_message(request,constants.ERROR,'Username ou senha invalidos')
            return redirect('/usuarios/login')