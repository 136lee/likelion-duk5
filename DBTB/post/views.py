from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from openai import OpenAI
from .forms import *
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.conf import settings
import base64, mimetypes


#openai가 미디어 인식하게 하는 함수
def _file_to_data_url_from_field(image_field):
    image_field.open("rb")
    content = image_field.read()
    image_field.close()
    mime = getattr(image_field.file, "content_type", None) \
           or mimetypes.guess_type(image_field.name)[0] \
           or "image/jpeg"
    b64 = base64.b64encode(content).decode("utf-8")
    return f"data:{mime};base64,{b64}"

#ai 매칭
from django.http import JsonResponse

def matching(request, pk):
    post = get_object_or_404(Post, pk=pk)
    place = post.place.first()
    if not place:
        return HttpResponseBadRequest("이 포스트에 연결된 장소가 없습니다.")
    place_name = place.place_name.strip()

    if not (post.author_id == request.user.id or request.user.is_staff or request.user.is_superuser):
        return JsonResponse({"ok": False, "error": "권한이 없습니다."}, status=403)


    try:
        image_ref = _file_to_data_url_from_field(post.image)

        client = OpenAI(
            api_key=getattr(settings, "OPENAI_API_KEY", None) or getattr(settings, "OPEN_API_KEY", None)
        )

        system_prompt = (
            "당신은 유능한 여행 가이드입니다. 사진의 장면 특징을 추정하세요."
            "대한민국에서 비슷한 분위기의 유명한 장소를 한 곳 추천해 주세요. 각 장소는 다음과 같습니다."
            f"유사한 장소를 먼저 말해줘, 그리고 줄 바꿔서 {place_name}의 장점을 부각해서 유사한 장소와 비교해줘. 유사한 장소를 비하하지는 마."
            "응답은 3문장으로 끝내. 한국어 존댓말로."
        )

        resp = client.responses.create(
            model="gpt-5",
            input=[
                {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
                {"role": "user", "content": [
                    {"type": "input_text", "text": "아래 사진과 비슷하게 보이는 유명한 장소를 추천해 주시고, 비교를 작성해 주세요."},
                    {"type": "input_image", "image_url": image_ref}
                ]}
            ],
        )

        ai_text = getattr(resp, "output_text", None) or resp.output[0].content[0].text
        post.AI_matching = ai_text
        post.save(update_fields=["AI_matching"])
        return JsonResponse({"ok": True, "ai_text": ai_text})

    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)


#응답 평가
@require_POST
def ai_feedback(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # "true"면 True, 그 외는 False 처리
    is_positive = request.POST.get("is_positive") == "true"

    fb = AIFeedback.objects.update_or_create(
        post=post,
        user=request.user,
        defaults={"is_positive": is_positive},
    )

    return JsonResponse({
        "ok": True,
        "is_positive": fb.is_positive
    })



@require_POST
def recom_now(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    place = post.place.first()
    if not place:
        return HttpResponseBadRequest("이 포스트에 연결된 장소가 없습니다.")
    place_name = (getattr(place, "place_name", "") or "").strip()
    place_address = (getattr(place, "address", "") or "").strip()
    if not place_name:
        return HttpResponseBadRequest("장소명이 비어 있습니다.")
    if not place_address:
        return HttpResponseBadRequest("주소가 비어 있습니다.")

    client = OpenAI(
        api_key=getattr(settings, "OPENAI_API_KEY", None) or getattr(settings, "OPEN_API_KEY", None)
    )

    system_prompt = (
        "당신은 유능한 여행 가이드입니다. 주어진 장소 주변에서 "
        "지금 바로 할 수 있는 활동을 1가지만 40자 내로 추천하세요. "
        "한 줄 한국어(존댓말)로 답하세요."
        "'기' 로 끝나는 어미"
    )

    created = []
    for _ in range(3):
        resp = client.responses.create(
            model="gpt-5",
            input=[
                {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
                {"role": "user", "content": [
                    {"type": "input_text",
                     "text": f"장소: {place_name}\n주소: {place_address}\n"
                             f"나중에 계획해서 할 수 있는 활동 1가지를 반환하세요."},
                ]}
            ]
        )
        text = getattr(resp, "output_text", "").strip()
        if not text:
            continue

        rec = Recommend.objects.create(
            post=post,
            recom_now=text,
        )
        created.append(rec.recom_now)

    return JsonResponse({"ok": True, "created_count": len(created), "items": created}, json_dumps_params={"ensure_ascii": False},)


@require_POST
def recom_later(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    place = post.place.first()
    if not place:
        return HttpResponseBadRequest("이 포스트에 연결된 장소가 없습니다.")
    place_name = (getattr(place, "place_name", "") or "").strip()
    place_address = (getattr(place, "address", "") or "").strip()
    if not place_name:
        return HttpResponseBadRequest("장소명이 비어 있습니다.")
    if not place_address:
        return HttpResponseBadRequest("주소가 비어 있습니다.")

    client = OpenAI(
        api_key=getattr(settings, "OPENAI_API_KEY", None) or getattr(settings, "OPEN_API_KEY", None)
    )

    system_prompt = (
        "당신은 유능한 여행 가이드입니다. 주어진 장소 주변에서 "
        "나중에 계획해서 할 만한 활동을 정확히 1가지만 40자 내로 한 줄 추천하세요. "
        "정중한 한국어(존댓말)로 작성하세요. "
        "'기' 로 끝나는 어미"
    )

    created = []
    for _ in range(3):
        resp = client.responses.create(
            model="gpt-5",
            input=[
                {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
                {"role": "user", "content": [
                    {"type": "input_text",
                     "text": f"장소: {place_name}\n주소: {place_address}\n"
                             f"나중에 계획해서 할 수 있는 활동 1가지를 반환하세요."},
                ]}
            ]
        )
        text = getattr(resp, "output_text", "").strip()
        if not text:
            continue

        rec = Recommend.objects.create(
            post=post,
            recom_later=text,
        )
        created.append(rec.recom_later)

    return JsonResponse({"ok": True, "created_count": len(created), "items": created}, json_dumps_params={"ensure_ascii": False},)


#소감 작성
def create_comment(request):
    if request.method=="POST":
        comment=request.POST.get('comment')

        comment=Recommend.objects.create(
            comment=comment
        )
        return redirect('post:todo')
    return render(request, 'post/create_comment.html')

#포스트 디테일
def post_detail(request, post_id):
    posts = get_object_or_404(Post, pk=post_id)
    return render(request, "post/post.html", {'posts':posts})