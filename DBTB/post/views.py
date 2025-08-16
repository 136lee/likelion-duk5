from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from urllib.parse import urlencode
# Create your views here.

@login_required
def create(request):
    categories = Category.objects.all()

    if request.method =="POST":
        title = request.POST.get('title') 
        content = request.POST.get('content')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

# 지도에서 심어줄 hidden input 이름은 latitude / longitude 로 가정
        lat = request.POST.get('latitude')  
        lng = request.POST.get('longitude')  

        category_ids = request.POST.getlist('category')
        category_list = [get_object_or_404(Category, id=category_id) for category_id in category_ids]


        post = Post.objects.create(
            title=title,
            content= content,
            author=request.user,
            image = image,
            video = video,
            latitude=lat or None,
            longitude=lng or None,
        )

        for category in category_list:
            post.category.add(category)

    # ✅ 저장 후: 지도 페이지로 리다이렉트하면서 방금 좌표/ID를 쿼리로 전달
        #   예) /map/list?lat=37.66&lng=127.04&id=123
        map_url = reverse('map:list')  # 너가 쓰는 메인 지도 URL 네임
        q = urlencode({"lat": post.latitude or "", "lng": post.longitude or "", "id": post.pk})
        return redirect(f"{reverse('map:list')}?scope=mine")

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
        video = request.FILES.get('video')

        if image:
            post.image.delete()
            post.image = image
        
        if video:
            post.video.delete()
            post.video = video

        post.save()

        return redirect ('post:detail', id)
    return render(request, 'post/update.html', {'post':post})

#삭제 (마이페이지에서)
# def delete(request, id):
#    post = get_object_or_404(Post, id=id)
 #   post.delete()
  #  return redirect ('post:list') 
