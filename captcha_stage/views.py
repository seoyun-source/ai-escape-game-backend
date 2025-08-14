# captcha_stage/views.py
import io, json, random, re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from captcha.image import ImageCaptcha
from PIL import Image, ImageDraw, ImageFilter

# (선택) 랜덤/고정 캡션 텍스트. 실제 정답 판정에는 사용하지 않음.
CAPTCHA_VISUAL_TEXTS = ["N3X7ST4GE", "S3CUR1TY", "TRUSTNO1", "YOUAREFAKE"]

def index(request):
    return render(request, "final/stage1_puzzle.html")  # templates 안 쓰면 settings.TEMPLATES['DIRS']에 final 폴더 등록

@require_http_methods(["GET"])
def generate_captcha(request):
    """
    서버에서 캡챠 이미지를 생성해 반환.
    실제 정답 판정은 YOU ARE FAKE(= "YOUAREFAKE")로만 수행할 예정.
    """
    # 시각적으로 보일 텍스트(연출용). 실제 정답 판정은 이 값을 쓰지 않음.
    visual_text = random.choice(CAPTCHA_VISUAL_TEXTS)

    # 이미지 생성
    width, height = 320, 100
    image_captcha = ImageCaptcha(width=width, height=height)
    img = image_captcha.generate_image(visual_text)

    # 후처리(스큐/노이즈/블러)
    draw = ImageDraw.Draw(img)
    # 라인 노이즈
    for _ in range(7):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        color = (random.randint(80,160), random.randint(80,160), random.randint(80,160))
        draw.line([(x1,y1),(x2,y2)], fill=color, width=2)
    # 점 노이즈
    for _ in range(350):
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        color = (random.randint(90,200), random.randint(90,200), random.randint(90,200))
        draw.point((x,y), fill=color)
    img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.2,0.6)))

    # PNG 응답
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return HttpResponse(buf, content_type="image/png")

@require_http_methods(["POST"])
def check_captcha(request):
    """
    입력값을 백엔드에서만 판정.
    - 공백/기호 제거 + 대문자화 → "YOUAREFAKE"와 일치하면 True
    """
    try:
        data = json.loads(request.body.decode())
    except Exception:
        return JsonResponse({"correct": False})

    raw = (data.get("answer") or "")
    normalized = re.sub(r'[^A-Z0-9]', '', raw.upper())
    is_correct = (normalized == "YOUAREFAKE")
    return JsonResponse({"correct": is_correct})
