import json
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from post.models import Post
from post.models import Category  # 카테고리 사용

def _posts_to_json(qs):
    data = [
        {"id": p.id, "title": p.title, "lat": p.latitude, "lng": p.longitude}
        for p in qs
        if p.latitude is not None and p.longitude is not None
    ]
    return json.dumps(data, ensure_ascii=False)

def list(request):
    categories = Category.objects.all()
    qs = Post.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    return render(request, "map/list.html", {
        "scope": "all",
        "posts_json": _posts_to_json(qs),
        "categories": categories, 
    })

@login_required
def mine(request):
    if not request.user.is_authenticated:
        return redirect("map:list")
    
    categories = Category.objects.all()
    qs = Post.objects.filter(author=request.user)\
            .exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    return render(request, "map/list.html", {
        "scope": "mine",
        "posts_json": _posts_to_json(qs),
        "categories": categories, 
    })
