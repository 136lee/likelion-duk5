from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from openai import OpenAI
from .forms import *
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.conf import settings
import base64, mimetypes
from django.urls import reverse
import os, json, base64, time, random , requests , re
from io import BytesIO
import re
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)



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

    # place가 꼭 없어도 동작하도록 완화 (없으면 그냥 이미지/제목만으로 분석)
    place = getattr(post, "place", None)
    if hasattr(place, "first"):
        place = place.first()

    if not (post.author_id == request.user.id or request.user.is_staff or request.user.is_superuser):
        return JsonResponse({"ok": False, "error": "권한이 없습니다."}, status=403)

    try:
        ai_text = run_matching(post)
        post.AI_matching = ai_text
        post.save(update_fields=["AI_matching"])
        return JsonResponse({"ok": True, "ai_text": ai_text})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)
    
def run_matching(post):
    """포스트 이미지와 제목을 바탕으로 AI 매칭 텍스트를 생성해 반환."""
    image_ref = _file_to_data_url_from_field(post.image)

    client = OpenAI(
        api_key=getattr(settings, "OPENAI_API_KEY", None) or getattr(settings, "OPEN_API_KEY", None)
    )

    system_prompt = (
        "당신은 유능한 여행 가이드입니다. 사진의 장면 특징을 추정하세요."
        "대한민국에서 비슷한 분위기의 유명한 장소를 한 곳 추천해 주세요."
        f"유사한 장소를 먼저 말해주고, 줄 바꿔서 {post.title} (주소: {post.address or (post.place.first().address if post.place.exists() else '')})'의 장점을 부각해 유사한 장소와 비교해 주세요."
        "유사한 장소를 비하하지 마세요. 주소를 직접적으로 언급하지마세요. 응답은 3문장, 한국어 존댓말로."
    )

    resp = client.responses.create(
        model="gpt-5",
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {"role": "user", "content": [
                {"type": "input_text", "text": "아래 사진과 비슷한 유명 장소를 추천하고 비교를 작성해 주세요."},
                {"type": "input_image", "image_url": image_ref},  # ← 문자열 data URL이면 OK
            ]},
        ],
    )

    # SDK 버전별 호환
    ai_text = getattr(resp, "output_text", None)
    if not ai_text:
        # 일부 SDK는 아래 형태
        ai_text = resp.output[0].content[0].text
    return ai_text


#응답 평가
@require_POST
def ai_feedback(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # "true"면 True, 아니면 False
    is_positive = request.POST.get("is_positive") == "true"

    fb, created = AIFeedback.objects.update_or_create(
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

    # 1) 기본값: Post 필드
    place_name = (post.title or "").strip()
    place_address = (post.address or "").strip()

    # 2) 보완: Place(M2M)에서 첫 번째 장소 사용
    place_obj = post.place.first()
    if place_obj:
        if not place_name:
            place_name = (getattr(place_obj, "name", "") or "").strip()
        if not place_address:
            place_address = (getattr(place_obj, "address", "") or "").strip()

    if not place_name:
        return HttpResponseBadRequest("제목(장소명)이 비어 있습니다.")
    if not place_address:
        return HttpResponseBadRequest("주소가 비어 있습니다.")

    client = OpenAI(
        api_key=getattr(settings, "OPENAI_API_KEY", None) or getattr(settings, "OPEN_API_KEY", None)
    )

    system_prompt = (
        "당신은 유능한 여행 가이드입니다. 주어진 장소 주변에서 "
        "지금 당장 계획해서 할 만한 활동을 정확히 1가지만 40자 내로 한 줄 추천하세요. "
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
                             f"지금 바로 할 수 있는 활동 1가지를 반환하세요."},
                ]}
            ]
        )
        text = getattr(resp, "output_text", "").strip()
        if text:
            rec = Recommend.objects.create(post=post, recom_now=text)
            created.append(rec.recom_now)

    return JsonResponse(
        {"ok": True, "created_count": len(created), "items": created},
        json_dumps_params={"ensure_ascii": False},
    )


@require_POST
def recom_later(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # 1) 기본값: Post 필드
    place_name = (post.title or "").strip()
    place_address = (post.address or "").strip()

    # 2) 보완: Place(M2M)에서 첫 번째 장소 사용
    place_obj = post.place.first()
    if place_obj:
        if not place_name:
            place_name = (getattr(place_obj, "name", "") or "").strip()
        if not place_address:
            place_address = (getattr(place_obj, "address", "") or "").strip()

    if not place_name:
        return HttpResponseBadRequest("제목(장소명)이 비어 있습니다.")
    if not place_address:
        return HttpResponseBadRequest("주소가 비어 있습니다.")

    client = OpenAI(
        api_key=getattr(settings, "OPENAI_API_KEY", None) or getattr(settings, "OPEN_API_KEY", None)
    )

    system_prompt = (
        "당신은 유능한 여행 가이드입니다. 주어진 장소 주변에서 "
        "나중에 계획해서 할 만한 활동을 정확히 1가지만 40자 내로 한 줄 추천하세요. "
        "시간대도 포함하세요."
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
        if text:
            rec = Recommend.objects.create(post=post, recom_later=text)
            created.append(rec.recom_later)

    return JsonResponse(
        {"ok": True, "created_count": len(created), "items": created},
        json_dumps_params={"ensure_ascii": False},
    )



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
    post = get_object_or_404(
        Post.objects.select_related("author").prefetch_related("place"),
        pk=post_id
    )
    place = post.place.first() 
    return render(request, "post/post_detail.html", {"post": post, "place": place})



DONG_RE = re.compile(r'([가-힣0-9]+동)')  # '...동' 한 번 추출

@login_required
def create(request):
    if request.method == "POST":
        title   = request.POST.get('title') or ''
        content = request.POST.get('content') or ''
        image   = request.FILES.get('image')

        # 좌표/주소
        lat_raw = request.POST.get('latitude')
        lng_raw = request.POST.get('longitude')
        lat = float(lat_raw) if lat_raw else None
        lng = float(lng_raw) if lng_raw else None
        addr = request.POST.get("address") or None

        # ✅ 동: 프런트에서 넘어온 값 우선
        dong = request.POST.get("dong") or None
        # ✅ 없으면 address에서 정규식으로 추출(지번주소일 때 잘 잡힘)
        if not dong and addr:
            m = DONG_RE.search(addr)
            if m:
                dong = m.group(1)  # 예: '창동', '쌍문동'

        # 저장
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            image=image,
            latitude=lat,
            longitude=lng,
            address=addr,
            dong=dong,            # ✅ 여기!
        )


        try:
            ai_text = run_matching(post)
            Post.objects.filter(pk=post.pk).update(AI_matching=ai_text)
        except Exception as e:
            # 실패해도 글 등록은 성공해야 하니 조용히 패스(원하면 로깅)
            pass

        # 저장 후 보던 지도 페이지로 복귀(+하이라이트)
        next_url = request.POST.get("next") or request.GET.get("next") or reverse("map:list")
        if post.latitude is not None and post.longitude is not None:
            return redirect(f"{next_url}?lat={post.latitude}&lng={post.longitude}")
        return redirect(next_url)

    # GET: 폼 렌더 (지도로부터 ?lat&lng&addr&dong&next 받음)
    return render(request, "post/create.html")


#수정 (마이페이지에서)
def update(request,id):
    post = get_object_or_404(Post, id=id)

    if request.method =='POST':
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)
        image = request.FILES.get('image')

        if image:
            post.image.delete()
            post.image = image
        

        post.save()

        return redirect ('post:post_detail', post_id=post.id)
    return render(request, 'post/update.html', {'post':post})

# 삭제 (마이페이지에서)
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect ('map:list') 


try:
    from PIL import Image
except ImportError:
    Image = None

def _thumb(dj_file, max_px=768, quality=82):
    try:
        dj_file.seek(0)
    except Exception:
        pass
    if Image is None:
        return dj_file.read(), getattr(dj_file, "content_type", None) or "image/jpeg"
    img = Image.open(dj_file)
    if img.mode in ("RGBA","LA"):
        bg = Image.new("RGB", img.size, (255,255,255))
        bg.paste(img, mask=img.split()[-1])
        img = bg
    else:
        img = img.convert("RGB")
    img.thumbnail((max_px, max_px))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    buf.seek(0)
    return buf.getvalue(), "image/jpeg"

@csrf_exempt
@require_POST
def ai_photo(request):
    # ❶ 입력 검사 + 로깅
    img = request.FILES.get("image")
    if not img:
        return JsonResponse({"error":"no_image"}, status=400)
    try:
        print("[ai_photo] incoming size(bytes) =", getattr(img, "size", None))
    except Exception:
        pass

    # ❷ 키 확인
    key = (os.getenv("OPENAI_API_KEY") or "").strip()
    if not key:
        # 키 없을 때도 항상 JSON 반환 (UX 유지)
        return JsonResponse({
            "raw":"(키 미설정) 업로드/경로/CSRF는 정상입니다. 키를 설정하면 실제 분석이 수행돼요."
        }, status=200)

    try:
        # ❸ 이미지 표준화(크기/품질 줄여서 API 에러 확률 ↓)
        #    필요시 더 줄이려면 max_px=640, quality=78 정도로 시도
        raw, mime = _thumb(img, max_px=768, quality=82)

        # ❹ data URL 구성
        data_url = f"data:{mime};base64,{base64.b64encode(raw).decode('utf-8')}"
        # 길이 과도 시 방어 (임계 넘으면 한 번 더 축소)
        if len(data_url) > 1_500_000:  # 대략 1.5MB 기준 (상황에 맞게 조정)
            raw2, mime2 = _thumb(img, max_px=640, quality=78)
            data_url = f"data:{mime2};base64,{base64.b64encode(raw2).decode('utf-8')}"

        payload = {
            "model": "gpt-4o-mini",
            "messages": [{
                "role": "user",
                "content": [
                    {"type":"text","text":
                        "이미지를 보고 분위기를 자연스럽게 한두 문장으로 설명해줘. 그리고 맨 끝에 이모지 3개만 붙여줘."
                    },
                    {"type":"image_url","image_url":{"url": data_url}}
                ]
            }],
            "temperature": 0.6,
            "max_tokens": 150
        }
        headers = {"Authorization": f"Bearer {key}", "Content-Type":"application/json"}
        url = "https://api.openai.com/v1/chat/completions"

        last_text = None
        for attempt in range(4):
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=45)
                last_text = r.text
            except requests.exceptions.Timeout:
                if attempt == 3:
                    return JsonResponse({"error":"upstream_timeout"}, status=504)
                # 지수 백오프
                time.sleep(0.5*(2**attempt))
                continue

            if r.status_code == 429:
                # 레이트리밋 백오프 재시도
                if attempt == 3:
                    return JsonResponse({"error":"rate_limited", "detail": last_text[:400]}, status=429)
                sleep_s = (0.6 * (2 ** attempt)) + random.random()*0.4
                time.sleep(min(sleep_s, 4.0))
                continue

            if r.status_code == 403:
                # 권한/결제 이슈 - 사용자에게는 부드럽게 전달
                return JsonResponse({
                    "raw":"AI 권한/결제 설정 확인 중입니다. (임시 메시지)"
                }, status=200)

            # 그 외 상태코드도 JSON으로 돌려주기 (HTML 500 방지)
            if not r.ok:
                return JsonResponse({
                    "error":"upstream_error",
                    "status": r.status_code,
                    "detail": last_text[:500]
                }, status=502)

            # 정상
            try:
                content = r.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:
                return JsonResponse({"error":"parse_upstream_json", "detail": str(e), "raw": last_text[:500]}, status=502)

            # 모델 응답이 JSON일 수도/문장일 수도 있으니 모두 케이스 처리
            try:
                return JsonResponse(json.loads(content), status=200)
            except Exception:
                return JsonResponse({"raw": content}, status=200)

        # 여기 오면 재시도 초과
        return JsonResponse({"error":"retry_exhausted", "detail": last_text[:500]}, status=502)

    except Exception as e:
        # 어떤 예외가 나도 HTML 에러페이지 대신 JSON으로
        return JsonResponse({"error":"server_exception", "detail": str(e)}, status=500)