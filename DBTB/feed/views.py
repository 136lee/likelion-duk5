from django.shortcuts import render, redirect, get_object_or_404
from post.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

ALLOWED_DONGS = {"도봉동", "창동", "방학동", "쌍문동"}

def feed(request, dong=None):
    q = (request.GET.get("q") or "").strip()

    qs = (
        Post.objects
        .all()
        .select_related("author")
        .prefetch_related("place", "scrap")
    )

    if dong:
        if dong not in ALLOWED_DONGS:
            return render(request, "feed/show_feed.html", {"posts": [], "dong": dong, "q": q})
        qs = qs.filter(place__address__icontains=dong)

    if q:
        qs = qs.filter(
            Q(place__name__icontains=q) |
            Q(place__address__icontains=q) |
            Q(author__nickname__icontains=q)
        )

    posts = qs.order_by("-id").distinct()
    return render(request, "feed/show_feed.html", {"posts": posts, "dong": dong, "q": q})


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

def feed_search(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return redirect("feed:feed_all")

    qs = (
        Post.objects
        .all()
        .select_related("author")
        .prefetch_related("place", "scrap")
        .filter(
            Q(place__name__icontains=q) |
            Q(place__address__icontains=q) |
            Q(author__nickname__icontains=q) 

        )
        .order_by("-id")
        .distinct()
    )
    return render(request, "feed/show_feed.html", {"posts": qs, "q": q, "dong": None})
