from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from captcha.image import ImageCaptcha
from PIL import ImageDraw, ImageFilter
import io, json, random

CAPTCHA_TEXT = "YOU ARE FAKE"  # 정답은 서버에만 저장

def index(request):
    return render(request, "captcha_stage/stage1_puzzle.html")

def generate_captcha(request):
    # 세션에 정답 저장
    request.session['captcha_text'] = CAPTCHA_TEXT.upper()

    # 기본 CAPTCHA 이미지 생성
    image_captcha = ImageCaptcha(width=300, height=100)
    img = image_captcha.generate_image(CAPTCHA_TEXT)

    # 노이즈 라인 추가
    draw = ImageDraw.Draw(img)
    for _ in range(5):
        x1, y1, x2, y2 = random.randint(0, 300), random.randint(0, 100), random.randint(0, 300), random.randint(0, 100)
        draw.line(((x1, y1), (x2, y2)), fill=(150, 150, 150), width=2)

    # 블러 효과
    img = img.filter(ImageFilter.GaussianBlur(0.6))

    # PNG로 응답
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return HttpResponse(buffer, content_type="image/png")

@require_http_methods(["POST"])
def check_captcha(request):
    data = json.loads(request.body.decode())
    answer = (data.get("answer") or "").strip().upper()
    correct = request.session.get("captcha_text", "")
    return JsonResponse({"correct": answer == correct})

