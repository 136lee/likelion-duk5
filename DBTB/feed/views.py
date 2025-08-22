from django.shortcuts import render, redirect, get_object_or_404
from post.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
import re

ALLOWED_DONGS = {"도봉동", "창동", "방학동", "쌍문동"}  # 제한 없애려면 빈 set() 또는 None로

# '...동'만 뽑는 간단 정규화
DONG_RE = re.compile(r'([가-힣0-9]+동)')

def _normalize_dong(s: str) -> str:
    if not s:
        return ""
    s = s.strip()
    # "서울 도봉구 쌍문동" 같은 형태에서 마지막 '...동'만 추출
    m = DONG_RE.search(s)
    return m.group(1) if m else s

def feed(request, dong=None):
    q = (request.GET.get("q") or "").strip()

    # ✅ path 파라미터든 ?dong= 이든 모두 수용
    dong = _normalize_dong(dong or request.GET.get("dong") or "")

    qs = (Post.objects
          .all()
          .select_related("author")    # place가 FK면 여기에 "place" 추가
          .prefetch_related("scrap"))  # 구조에 맞게 조정

    # ✅ 동 필터
    if dong:
        if ALLOWED_DONGS and dong not in ALLOWED_DONGS:
            return render(request, "feed/show_feed.html",
                          {"posts": [], "dong": dong, "q": q})

       # ✅ 기존 조건은 유지 + Post.dong / Post.address 도 함께 매칭
        qs = qs.filter(
            Q(dong=dong) |                        # ← 새로 추가: Post.dong 정확일치
            Q(address__icontains=dong) |          # ← 새로 추가: Post.address(지번) 폴백
            Q(place__address__icontains=dong)     # ← 기존 유지
        )

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
