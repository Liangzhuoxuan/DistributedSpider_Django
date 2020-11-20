from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print(username, password)
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            print('111')
            if user:
                print('222')
                if user.is_active:
                    login(request, user)
                return redirect('trackBack')
                # todo spiderkeeper直接不用登录账号
            else:
                print('333')
                tips = '账号密码错误，请重新输入'
                messages.error(request, tips)
                return render(request, 'index.html', locals())
        else:
            print('444')
            tips = '用户不存在，请注册'
            messages.error(request, tips)
            return render(request, 'index.html', locals())
    return redirect('/')

# 登录直接跳5000了
def registerView(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print(username,password)
        if User.objects.filter(username=username):
            print('555')
            tips = '用户已经存在'
            messages.info(request, tips)
        else:
            print('666')
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return render(request, 'index.html')
    return render(request, 'index.html', locals())