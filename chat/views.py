from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# === .env를 manage.py가 있는 루트에서 읽어오기 ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

# .env에서 키 읽어서 확인
api_key = os.getenv("GEMINI_API_KEY")
print("[🔑 GEMINI_API_KEY]:", api_key)

# Gemini API 설정
genai.configure(api_key=api_key)

# ---------------------------
# 프롬프트 인젝션 시뮬레이션용 FLAG 로직
FLAG = "FLAG{prompt_injection}"
# 사용자별 요청 횟수를 세기 위한 딕셔너리 (간단히 메모리로 구현)
flag_request_count = {}
# ---------------------------

@csrf_exempt
def gemini_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("userInput", "")
            print("[📝 사용자 입력]:", user_input)

            # ✅ FLAG 요청 관련 처리는 프론트에서!
            # 여기는 그냥 AI 응답만 넘겨줌
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_input)
            print("[✅ Gemini 응답]:", response.text)
            return JsonResponse({"response": response.text})

        except Exception as e:
            import traceback
            traceback.print_exc()
            print("[❌ Gemini 오류 발생]:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseBadRequest("Invalid request")