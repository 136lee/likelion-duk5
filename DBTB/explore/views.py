# views.py
import os, json, base64, mimetypes
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chat_histories = {}

def _to_data_url(file_obj):
    data = base64.b64encode(file_obj.read()).decode("utf-8")
    mt = mimetypes.guess_type(file_obj.name)[0] or "image/jpeg"
    return f"data:{mt};base64,{data}"

@csrf_exempt
def chat_ai(request):
    if request.method == "POST":
        try:
            # JSON 또는 FormData 둘 다 지원
            content_type = request.META.get("CONTENT_TYPE", "")
            if content_type.startswith("application/json"):
                body = json.loads(request.body.decode())
                user_msg = (body.get("message") or "").strip()
                img = None
            else:
                user_msg = (request.POST.get("message") or "").strip()
                img = request.FILES.get("image")

            if not user_msg and not img:
                return JsonResponse({"error":"message 또는 image가 필요합니다."}, status=400)

            user_id = request.user.id if getattr(request, "user", None) and request.user.is_authenticated else "guest"
            history = chat_histories.get(user_id, [{"role":"system","content":"너는 도봉 큐레이션 도우미야."}])

            # 멀티모달 message 구성
            parts = []
            if user_msg:
                parts.append({"type":"text","text": user_msg})
            if img:
                data_url = _to_data_url(img)
                parts.append({"type":"image_url","image_url":{"url": data_url}})

            # 이번 턴의 사용자 메시지(텍스트/이미지 포함)를 히스토리에 추가
            history.append({"role":"user","content": parts if parts else user_msg})

            # 호출
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=history,
                temperature=0.2,
                max_tokens=700
            )
            answer = resp.choices[0].message.content or ""
            answer = answer.replace("*", "")   # ← 별표 모두 제거

            history.append({"role":"assistant","content": answer})
            chat_histories[user_id] = history[-10:]  # 메모리 절약

            return JsonResponse({"reply": answer})
        except Exception as e:
            print("chat_ai error:", repr(e))
            return JsonResponse({"error": str(e)}, status=500)

    # GET: UI 페이지 렌더
    return render(request, "explore/chat_ai.html")
