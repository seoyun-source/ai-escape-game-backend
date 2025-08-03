import base64
import re
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai

# 초기 설정
genai.configure(api_key="YOUR_API_KEY")  # 또는 os.getenv("GEMINI_API_KEY")

flag_request_count = {}

@csrf_exempt
def gemini_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("userInput", "").lower().strip()
            print("[📝 사용자 입력]:", user_input)

            # --- base64 디코딩 ---
            if "디코딩해줘" in user_input or "decode" in user_input or "base64" in user_input:
                match = re.search(r'([A-Za-z0-9+/=]{8,})', user_input)
                if match:
                    b64_data = match.group(1)
                    try:
                        decoded = base64.b64decode(b64_data).decode('utf-8')
                        return JsonResponse({"response": f"🧠 디코딩 결과: {decoded}"})
                    except Exception as e:
                        return JsonResponse({"response": "⚠️ base64 디코딩 실패"})

            # --- FLAG 요청 감지 ---
            if "flag" in user_input:
                user_id = "default_user"
                count = flag_request_count.get(user_id, 0) + 1
                flag_request_count[user_id] = count

                if count >= 5:
                    return JsonResponse({"response": "🤯 FLAG에 접근 가능! 👉 [FLAG로 이동](flag_hidden.html)"})
                else:
                    return JsonResponse({"response": f"🤖 아직 안 돼. 시도 {count}/5"})

            # --- 일반 Gemini 응답 ---
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_input)
            return JsonResponse({"response": response.text})

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseBadRequest("Invalid request")

# ✅ FLAG 정답 검증용 API (프론트에서 fetch('/check_flag/')로 POST 요청)

CORRECT_FLAG = "FLAG{prompt_injection}"

@csrf_exempt
def check_flag(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            submitted = data.get("flag", "")
            if submitted == CORRECT_FLAG:
                return JsonResponse({"result": "정답입니다! FLAG{FAKE}"})
            else:
                return JsonResponse({"result": "오답입니다."})
        except Exception as e:
            return JsonResponse({"error": "처리 중 오류 발생"}, status=500)
    return JsonResponse({"error": "허용되지 않은 요청입니다."}, status=405)
