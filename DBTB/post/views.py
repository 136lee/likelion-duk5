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
