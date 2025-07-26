from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@csrf_exempt
def gemini_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("userInput")

            print("[📝 사용자 입력]:", user_input)  # ✅ 로그 찍기

            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(user_input)

            print("[✅ Gemini 응답]:", response.text)  # ✅ 로그 찍기

            return JsonResponse({"response": response.text})
        except Exception as e:
            print("[❌ Gemini 오류 발생]:", e)  # ✅ 에러 로그 찍기
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseBadRequest("Invalid request")
