from django.shortcuts import render, redirect
from .forms import *
from post.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method=='GET':
        form=SignUpForm()
        return render(request, 'account/signup.html', {'form':form})
    form=SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('account:login')
    else:
        return render(request, 'account/signup.html', {'form':form})
    
def login(request):
    if request.method=="GET":
        return render(request, 'account/login.html', {'form':AuthenticationForm()})
    form=AuthenticationForm(request, request.POST)
    if form.is_valid():
        auth_login(request,  form.user_cache)
        return redirect('map:list')
    return render(request, 'account/login.html', {'form':form})

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('map:list')


def mypage(request):
    return render(request, 'account/mypage.html')

def mypost(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'account/mypost.html', {'posts':posts})

@login_required
def user_info(request):
    if request.method =="POST":
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            request.user.profile_image.delete()
            request.user.profile_image = profile_image
            request.user.save()

    return render(request, 'account/user_info.html')