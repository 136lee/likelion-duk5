import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt   # 처음엔 편하게, 나중에 제거

from .models import Post
from map.models import Place

@require_POST
@csrf_exempt
def create_post(request):
    data = json.loads(request.body or "{}")
    place = Place.objects.get(id=data["place_id"])
    post = Post.objects.create(
        place=place,
        rating=int(data.get("rating", 5)),
        content=data.get("content",""),
        # user=request.user if request.user.is_authenticated else None
    )
    return JsonResponse({"id": post.id}, status=201)

def list_by_place(request, place_id):
    qs = Post.objects.filter(place_id=place_id).order_by("-id")
    return JsonResponse([{"id":p.id,"rating":p.rating,"content":p.content} for p in qs], safe=False)