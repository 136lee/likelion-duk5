import os, json
import openai
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

openai.api_key = os.getenv("OPENAI_API_KEY")  # bash에서 export 한 키 사용

chat_histories = {}  # 메모리에 간단히 저장 (테스트용)

@csrf_exempt
def chat_ai(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user_id = request.user.id if request.user.is_authenticated else "guest"
        user_msg = body.get("message")

        history = chat_histories.get(user_id, [
            {"role":"system", "content":"너는 도봉 큐레이션 도우미야."}
        ])
        history.append({"role":"user", "content":user_msg})

        # OpenAI API 호출
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=history
        )
        answer = resp.choices[0].message["content"]

        history.append({"role":"assistant", "content":answer})
        chat_histories[user_id] = history[-10:]  # 최근 10개만 유지

        return JsonResponse({"reply": answer})

    # ✅ GET 요청이면 챗 UI 보여주기
    return render(request, "explore/chat_ai.html")
