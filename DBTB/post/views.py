from .models import *
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

@login_required
def create(request):

    if request.method =="POST":
        title = request.POST.get('title') 
        content = request.POST.get('content')
        image = request.FILES.get('image')

# 지도에서 심어줄 hidden input 이름은 latitude / longitude 로 가정
        lat_raw = request.POST.get('latitude')  
        lng_raw = request.POST.get('longitude')
        lat = float(lat_raw) if lat_raw else None
        lng = float(lng_raw) if lng_raw else None  


        post = Post.objects.create(
            title=title,
            content= content,
            author=request.user,
            image = image,
            latitude=lat ,
            longitude=lng,
        )
        
        # ✅ 저장 후 보던 지도 페이지로 복귀 + 하이라이트
        next_url = request.POST.get("next") or reverse("map:list")
        if post.latitude is not None and post.longitude is not None:
            return redirect(f"{next_url}?lat={post.latitude}&lng={post.longitude}")
        return redirect(next_url)
    # GET: 폼 렌더 (지도로부터 ?lat&lng&next 받음)
    return render(request, "post/create.html")

#자세히 (마이페이지, 지도?)
def detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render (request, 'post/detail.html', {'post':post})

#수정 (마이페이지에서)
def update(request,id):
    post = get_object_or_404(Post, id=id)

    if request.method =='POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        image = request.FILES.get('image')

        if image:
            post.image.delete()
            post.image = image
        

        post.save()

        return redirect ('post:detail', id)
    return render(request, 'post/update.html', {'post':post})

# 삭제 (마이페이지에서)
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect ('post:list') 
