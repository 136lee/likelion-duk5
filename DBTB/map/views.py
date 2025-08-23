# map/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from post.models import Post

DOBONG_CENTER = {"lat": 37.668, "lng": 127.047}

def list(request):
    return render(request, "map/list.html", {"scope": "list", "center": DOBONG_CENTER})

@login_required
def mine(request):
    return render(request, "map/list.html", {"scope": "mine", "center": DOBONG_CENTER})

def posts_api(request):
    scope = request.GET.get("scope", "list")  # 'list' | 'mine'
    qs = Post.objects.all()

    if scope == "mine":
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "auth required"}, status=401)
        qs = qs.filter(author=request.user)

    data = []
    for p in qs:
        lat = float(p.latitude) if p.latitude is not None else None
        lng = float(p.longitude) if p.longitude is not None else None

        # ✅ 절대 URL로 변환 (없으면 None)
        if getattr(p, "image", None) and getattr(p.image, "url", None):
            image_url = request.build_absolute_uri(p.image.url)
        else:
            image_url = None

        data.append({
            "id": p.id,
            "title": p.title or "",
            "lat": lat,     # 프론트가 기대하는 이름
            "lng": lng,
            "address": p.address,
            "image_url": image_url,   # ✅ 추가
        })
    return JsonResponse(data, safe=False)
