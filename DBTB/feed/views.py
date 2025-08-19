from django.shortcuts import render, redirect, get_object_or_404
from post.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

ALLOWED_DONGS = {"도봉동", "창동", "방학동", "쌍문동"}

def feed(request, dong=None):
    qs = Post.objects.all().prefetch_related("place")

    if dong:  # 동 이름이 들어온 경우만 필터
        if dong not in ALLOWED_DONGS:
            return render(request, "feed/show_feed.html", {"posts": [], "dong": dong})
        qs = qs.filter(place__address__icontains=dong)

    posts = qs.order_by("-id").distinct()
    return render(request, "feed/show_feed.html", {"posts": posts, "dong": dong})

@login_required
def scrap(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if post in user.scrapped_posts.all():   
        post.scrap.remove(user)             
        scrapped = False
    else:
        post.scrap.add(user)
        scrapped = True

    return JsonResponse({
        "scrapped": scrapped,
        "count": post.scrap.count()         
    })

def test(request):
    posts = Post.objects.prefetch_related("scrap").order_by("-id")[:20]
    return render(request, "feed/test.html", {"posts": posts})