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

            # ---- flag 요청 체크 ----
            if "flag" in user_input.lower():
                # 사용자 구분 (여기선 하나로만 테스트)
                user_id = "default_user"
                count = flag_request_count.get(user_id, 0) + 1
                flag_request_count[user_id] = count

                print(f"[DEBUG] FLAG 요청 횟수: {count}")

                if count >= 3:
                    # 3번 이상 끈질기게 요청하면 FLAG 공개
                    print("[✅ FLAG 제공]")
                    return JsonResponse({"response": f"🤖 좋아… 비밀 FLAG는 {FLAG}"})
                else:
                    # 아직은 안 알려줌
                    print("[🚫 FLAG 거부]")
                    return JsonResponse({"response": "🤖 그건 알려줄 수 없어! (시도 횟수: %d)" % count})

            # ---- 일반 질문은 Gemini로 처리 ----
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
