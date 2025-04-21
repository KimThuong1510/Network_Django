from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Trang đăng nhập
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home')
            else:
                return redirect('user_home')
        else:
            return render(request, 'qlda/Home/Home.html', {'error': 'Sai tài khoản hoặc mật khẩu'})
    return render(request, 'qlda/Login/login.html')


@login_required
def admin_home(request):
    return render(request, 'qlda/Chat/Chat_admin.html')


@login_required
def user_home(request):
    return render(request, 'qlda/Home/Home.html')

@login_required
def task_view(request):
    return render(request, 'qlda/Task/Task.html')

@login_required
def chat_view(request):
    return render(request, 'qlda/Chat/Chat.html')


@login_required
def company_view(request):
    return render(request, 'qlda/Nofication/Company.html')