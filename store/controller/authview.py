from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from store.forms import CustomUserForm

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация успешно заверешена")
            return redirect('/login')
    context = {'form': form}
    return render(request, "store/auth/register.html", context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "Вы уже авторизованы")
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            passwd = request.POST.get('password')

            user = authenticate(request, username=name, password=passwd)

            if user is not None:
                login(request, user)
                messages.success(request, "Авторизация пройдена")
                return redirect("/")
            else:
                messages.error(request, "Некорректное имя пользователя или пароль")
                return redirect("login/")
        return render(request, "store/auth/login.html")
            
def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Вы успешно вышли")
    return redirect("/")