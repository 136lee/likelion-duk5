from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def create(request):
    categories = Category.objects.all()

    if request.method =="POST":
        title = request.POST.get('title') 
        content = request.POST.get('content')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        lat = request.POST.get('latitude')   # ← 추가
        lng = request.POST.get('longitude')  # ← 추가

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

        return redirect('map:list') #데이터 전송없이 url 이동만
    return render(request, 'post/create.html', {'categories': categories}) 

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
