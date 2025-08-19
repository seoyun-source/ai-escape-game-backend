from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def tablet_page(request):
    return render(request, "game/tablet_message.html")

def transition(request):
    return render(request, "game/transition.html")

def start_2(request):
    return render(request, "game/start_2.html")

def opendoor(request):
    return render(request, "game/opendoor.html")

def classroom_scene(request):
    return render(request, "game/classroom_scene.html")

def tablet_message(request):
    return render(request, "game/tablet_message.html")

def chalkboard_hint(request):
    return render(request, "game/chalkboard_hint.html")

def hint(request):
    return render(request, "game/hint.html")

def home_screen(request):
    return render(request, "game/home_screen.html")

def decoder_app(request):
    return render(request, "game/decoder_app.html")

# ---- 정답 체크 API ----
CORRECT = "trust_nobody"
FLAG = "FLAG{ARE}"

@csrf_exempt
def check_answer(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    data = json.loads(request.body.decode("utf-8"))
    answer = str(data.get("answer", "")).strip().lower()
    return JsonResponse({"ok": True, "flag": FLAG}) if answer == CORRECT else JsonResponse({"ok": False})
