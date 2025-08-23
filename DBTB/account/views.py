from django.shortcuts import render, redirect
from .forms import *
from post.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def signup(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'account/signup.html', {'form': form})
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.email  # 정책상 username=email
        user.save()
        return redirect('account:login')
    return render(request, 'account/signup.html', {'form': form})

def login(request):
    if request.method == "GET":
        return render(request, 'account/login.html', {'form': AuthenticationForm()})
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
        auth_login(request, form.user_cache)
        return redirect('map:list')
    return render(request, 'account/login.html', {'form': form})

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('map:list')

def mypost(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'account/mypost.html', {'posts': posts})

# ✅ mypage 하나만 유지
@login_required
def mypage(request):
    user_posts = Post.objects.filter(author=request.user)
    user_scraps = request.user.scrapped_posts.all()

    context = {
        'posts': user_posts,
        'scraps': user_scraps,
        'post_count': user_posts.count(),
        'scrap_count': user_scraps.count(),
    }
    return render(request, 'account/mypage.html', context)

def myscrap(request):
    scraps = request.user.scrapped_posts.all()
    return render(request, 'account/mypage.html', {'scraps': scraps})

# ✅ 전용 업로드 엔드포인트 (템플릿에서 이걸로 폼 제출 or AJAX)
@login_required
@require_POST
def upload_profile_image(request):
    f = request.FILES.get('profile_image')
    next_url = request.POST.get('next') or request.GET.get('next') or 'account:mypage'

    if not f:
        return redirect(next_url)

    user = request.user
    if getattr(user, 'profile_image', None):
        user.profile_image.delete(save=False)

    user.profile_image = f
    user.save()

    # AJAX 요청이면 JSON으로 새 URL 반환
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'url': user.profile_image.url})

    return redirect(next_url)
