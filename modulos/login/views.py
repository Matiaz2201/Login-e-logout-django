from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from .backend import MyBackend
from django.contrib import messages

# Os metodos de login e logout são definidos com um do_ antes para que não se
# confuda com a função login e logout importada do django

# Create your views here.

@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')

def do_login(request):
    if request.method == 'POST':
        if MyBackend.checkUser(username=request.POST['username']) == False:
            messages.warning(request, 'Usuario não existente')
            # Evento back usuario incorreto
        else:
            if MyBackend.checkPassword(username=request.POST['username'], password=request.POST['password']) == False:
                messages.warning(request, 'Senha incorreta')
                # Evento back senha incorreta
        user = MyBackend.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/home')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def do_logout(request):
    logout(request)
    return redirect('/login')
