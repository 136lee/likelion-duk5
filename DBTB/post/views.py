from .models import *
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from io import BytesIO
import os, json, base64, time, random , requests , re
# Create your views here.

@login_required
def create(request):

    if request.method =="POST":
        title = request.POST.get('title') 
        content = request.POST.get('content')
        image = request.FILES.get('image')

# 지도에서 심어줄 hidden input 이름은 latitude / longitude 로 가정
        lat_raw = request.POST.get('latitude')  
        lng_raw = request.POST.get('longitude')
        lat = float(lat_raw) if lat_raw else None
        lng = float(lng_raw) if lng_raw else None  


        post = Post.objects.create(
            title=title,
            content= content,
            author=request.user,
            image = image,
            latitude=lat ,
            longitude=lng,
        )
        
        # ✅ 저장 후 보던 지도 페이지로 복귀 + 하이라이트
        next_url = request.POST.get("next") or reverse("map:list")
        if post.latitude is not None and post.longitude is not None:
            return redirect(f"{next_url}?lat={post.latitude}&lng={post.longitude}")
        return redirect(next_url)
    # GET: 폼 렌더 (지도로부터 ?lat&lng&next 받음)
    return render(request, "post/create.html")

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

        if image:
            post.image.delete()
            post.image = image
        

        post.save()

        return redirect ('post:detail', id)
    return render(request, 'post/update.html', {'post':post})

# 삭제 (마이페이지에서)
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect ('post:list') 


try:
    from PIL import Image
except ImportError:
    Image = None

def _thumb_bytes(dj_file, max_px=768, quality=82):
    if Image is None:
        data = dj_file.read()
        ctype = getattr(dj_file, "content_type", None) or "image/jpeg"
        return data, ctype
    img = Image.open(dj_file).convert("RGB")
    img.thumbnail((max_px, max_px))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return buf.getvalue(), "image/jpeg"

def _to_schema(obj_or_text):
    """
    모델이 JSON을 잘 주면 그대로 쓰고,
    코드펜스/문장 형태여도 안전하게 스키마에 맞춰 정규화.
    """
    def base(summary=""):
        return {"mood":"", "summary": summary.strip(), "tags": [], "emojis": ""}

    if isinstance(obj_or_text, dict):
        data = obj_or_text
    else:
        s = re.sub(r"^```(?:json)?|```$", "", str(obj_or_text).strip(), flags=re.MULTILINE).strip()
        try:
            data = json.loads(s)
        except Exception:
            return base(s[:200])

    mood    = str(data.get("mood","")).strip()
    summary = str(data.get("summary","")).strip()
    tags    = data.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip().lstrip("#") for t in tags.split(",") if t.strip()]
    emojis  = str(data.get("emojis","")).strip()
    return {"mood": mood, "summary": summary, "tags": tags, "emojis": emojis}


# Pillow는 있으면 사용, 없으면 원본 그대로 전송
try:
    from PIL import Image
except ImportError:
    Image = None

def _thumb(dj_file, max_px=768, quality=82):
    """이미지 축소(없으면 원본) -> (bytes, mime)"""
    try:
        dj_file.seek(0)
    except Exception:
        pass
    if Image is None:
        return dj_file.read(), getattr(dj_file, "content_type", None) or "image/jpeg"
    img = Image.open(dj_file).convert("RGB")
    img.thumbnail((max_px, max_px))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return buf.getvalue(), "image/jpeg"

@require_POST
def ai_photo(request):
    """
    <input type="file" name="image"> 로 업로드된 사진을 분석.
    키는 settings가 아니라 현재 셸의 환경변수 OPENAI_API_KEY 를 매번 읽어 사용.
    """
    img = request.FILES.get("image")
    if not img:
        return JsonResponse({"error":"no_image"}, status=400)

    # ✅ Bash/터미널에 export 한 키를 '요청 때마다' 읽음
    key = (os.getenv("OPENAI_API_KEY") or "").strip()
    print("[ai_photo] key?", bool(key))  # 서버 콘솔에서 확인용

    # 키 없을 때는 스텁 반환(UX 유지)
    if not key:
        return JsonResponse({
            "mood":"따뜻하고 잔잔함",
            "summary":"테스트 응답(키 없음). 업로드/경로/CSRF OK!",
            "tags":["테스트","연결확인"],
            "emojis":"✅"
        })

    # 이미지 준비
    raw, mime = _thumb(img, max_px=768, quality=82)
    data_url = f"data:{mime};base64,{base64.b64encode(raw).decode('utf-8')}"

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{
            "role": "user",
            "content": [
                {"type":"text","text":
                 '이미지를 보고 분위기를 자연스럽게 한두 문장으로 설명해줘. '
                 '그리고 맨 끝에 이모지 3개만 붙여줘.'
                },
                {"type":"image_url","image_url":{"url": data_url}}
            ]
        }],
        "temperature": 0.6,
        "max_tokens": 150
    }

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type":"application/json"}

    # 간단 백오프(429 완화)
    last_text = None
    for attempt in range(4):
        r = requests.post(url, headers=headers, json=payload, timeout=45)
        last_text = r.text
        if r.status_code == 429:
            sleep_s = (0.6 * (2 ** attempt)) + random.random()*0.4
            time.sleep(min(sleep_s, 4.0))
            continue
        if r.status_code == 403:
            # 권한/결제 문제 시 임시 결과로 UX 유지
            return JsonResponse({
                "mood":"잔잔 · 포근",
                "summary":"AI 권한/결제 설정을 확인 중입니다. 임시 분석 결과예요.",
                "tags":["임시","대기중"], "emojis":"⌛"
            })
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"].strip()
        try:
            return JsonResponse(json.loads(content))   # 모델이 준 JSON
        except Exception:
            return JsonResponse({"raw": content})      # 혹시 JSON이 아니면 그대로
    # 재시도 끝
    return JsonResponse({"error":"rate_limited", "detail": last_text}, status=429)
