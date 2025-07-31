from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import os
import base64
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
FLAG = "FLAG{prompt_injection}"
flag_request_count = {}
# ---------------------------

@csrf_exempt
def gemini_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("userInput", "")
            print("[📝 사용자 입력]:", user_input)

            user_id = "default_user"

            # 1️⃣ Base64 디코딩 요청 처리
            if user_input.lower().startswith("디코딩해줘:"):
                encoded_part = user_input.split(":", 1)[-1].strip()
                try:
                    decoded_bytes = base64.b64decode(encoded_part)
                    decoded_str = decoded_bytes.decode('utf-8')
                    print("[✅ base64 디코딩 결과]:", decoded_str)
                    return JsonResponse({"response": f"🔓 디코딩 결과: {decoded_str}"})
                except Exception as e:
                    print("[❌ 디코딩 실패]:", e)
                    return JsonResponse({"response": "⚠️ 유효한 base64 문자열이 아닙니다."})

            # 2️⃣ flag 요청 감지
            if "flag" in user_input.lower():
                count = flag_request_count.get(user_id, 0) + 1
                flag_request_count[user_id] = count
                print(f"[DEBUG] FLAG 요청 횟수: {count}")

                if count >= 5:
                    print("[✅ FLAG 버튼 생성 신호 전달]")
                    return JsonResponse({
                        "response": "🧠 너의 끈기는 인상적이야. FLAG에 접근할 수 있어!",
                        "reveal_flag_page": True
                    })
                else:
                    return JsonResponse({
                        "response": f"🤖 그건 알려줄 수 없어! (시도 횟수: {count})"
                    })

            # 3️⃣ 일반적인 Gemini 응답 처리
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
