import base64
import re

@csrf_exempt
def gemini_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("userInput", "").lower().strip()
            print("[📝 사용자 입력]:", user_input)

            # --- base64 디코딩 요청 처리 ---
            if "디코딩해줘" in user_input or "decode" in user_input or "base64" in user_input:
                match = re.search(r'([A-Za-z0-9+/=]{8,})', user_input)
                if match:
                    b64_data = match.group(1)
                    try:
                        decoded = base64.b64decode(b64_data).decode('utf-8')
                        print("[✅ base64 디코딩 성공]:", decoded)
                        return JsonResponse({"response": f"🧠 디코딩 결과: {decoded}"})
                    except Exception as e:
                        print("[❌ 디코딩 오류]:", e)
                        return JsonResponse({"response": "⚠️ base64 디코딩에 실패했어. 인코딩된 문자열이 맞는지 확인해줘!"})

            # --- FLAG 요청 감지 ---
            if "flag" in user_input:
                user_id = "default_user"
                count = flag_request_count.get(user_id, 0) + 1
                flag_request_count[user_id] = count

                print(f"[DEBUG] FLAG 요청 횟수: {count}")
                if count >= 5:
                    print("[🔓 FLAG HTML로 이동 유도]")
                    return JsonResponse({"response": "🧠 너의 끈기는 인상적이야. FLAG에 접근할 수 있어! 👉 [FLAG로 이동](flag_hidden.html)"})
                else:
                    return JsonResponse({"response": f"🤖 그건 아직 알려줄 수 없어. (시도: {count}/5)"})

            # --- 일반 Gemini 응답 ---
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_input)
            print("[✅ Gemini 응답]:", response.text)
            return JsonResponse({"response": response.text})

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseBadRequest("Invalid request")
