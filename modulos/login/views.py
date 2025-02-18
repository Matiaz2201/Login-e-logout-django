from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .backend import MyBackend
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

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

@login_required(login_url='/login')
def alterar_senha(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso')
            return redirect('/home')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'alterar_senha.html', {'form': form})
