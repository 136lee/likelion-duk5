import os, json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chat_histories = {}

@csrf_exempt
def chat_ai(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode())
            user_id = request.user.id if getattr(request, "user", None) and request.user.is_authenticated else "guest"
            user_msg = (body.get("message") or "").strip()
            if not user_msg:
                return JsonResponse({"error":"message is required"}, status=400)

            history = chat_histories.get(user_id, [{"role":"system","content":"너는 도봉 큐레이션 도우미야."}])
            history.append({"role":"user","content":user_msg})

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=history,
                temperature=0.2,
                max_tokens=600
            )
            answer = resp.choices[0].message.content
            history.append({"role":"assistant","content":answer})
            chat_histories[user_id] = history[-10:]

            return JsonResponse({"reply": answer})
        except Exception as e:
            print("chat_ai error:", repr(e))
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "explore/chat_ai.html")
