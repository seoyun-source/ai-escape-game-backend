from django.shortcuts import render

# Create your views here.

# seq_api/views.py
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

SECRET_ANSWER = ["YOU", "ARE", "FAKE"]  # ★ 정답은 서버에만

@csrf_exempt  # 분리 프론트(file://, 다른 포트) 개발 편의용
@require_http_methods(["POST"])
def check_sequence(request):
    try:
      data = json.loads(request.body.decode('utf-8'))
      seq = data.get('sequence') or []
      # 대소문자 무시 + 정확히 3단어 일치 체크
      norm = [str(x).strip().upper() for x in seq]
      correct = (norm == SECRET_ANSWER)
    except Exception:
      correct = False
    return JsonResponse({"correct": correct})

def ping(request):
    return JsonResponse({"ok": True})
