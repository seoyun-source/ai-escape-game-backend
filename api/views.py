# backend-django/api/views.py
import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

"""
개발용 인메모리 세션 저장소 (운영은 DB 권장)
구조:
SESSIONS[sid] = {
    "quiz": {"internet": bool, "memo": bool},
    "sms_solved": set(["caseA","caseB","caseC"])
}
"""
SESSIONS = {}


def _get_or_init_session(sid=None):
    if not sid or sid not in SESSIONS:
        sid = str(uuid.uuid4())
        SESSIONS[sid] = {
            "quiz": {"internet": False, "memo": False},
            "sms_solved": set(),
        }
    return sid


@csrf_exempt
def session_start(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)
    sid = _get_or_init_session()
    return JsonResponse({"session_id": sid})


def session_state(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET only"}, status=400)

    sid = request.GET.get("session_id")
    if not sid or sid not in SESSIONS:
        return JsonResponse({"error": "Invalid session"}, status=400)

    q = SESSIONS[sid]["quiz"]
    return JsonResponse(
        {"solved": {"internet": bool(q["internet"]), "memo": bool(q["memo"])}}
    )


# ========== 홈 화면 퍼즐 채점 ==========
@csrf_exempt
def quiz_check(request):
    """
    home_screen.html에서 호출:
    - 인터넷 퍼즐: { quiz_id: "home_internet", choice_index: int, session_id }
    - 메모 퍼즐:   { quiz_id: "home_memo", choices: [int,...], session_id }
    응답: { correct: bool, message?: str }
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    sid = payload.get("session_id")
    if not sid or sid not in SESSIONS:
        return JsonResponse({"error": "Invalid session"}, status=400)

    quiz_id = payload.get("quiz_id")

    if quiz_id == "home_internet":
        idx = payload.get("choice_index")
        ok = (idx == 0)  # 정답: 0번(HTTP 의심 링크)
        if ok:
            SESSIONS[sid]["quiz"]["internet"] = True
            return JsonResponse(
                {
                    "correct": True,
                    "message": "맞아. HTTP 형태는 보안이 허술하단 뜻이야. 그리고 낯선 주소는 일단 의심부터!",
                }
            )
        else:
            return JsonResponse(
                {"correct": False, "message": "아니야. 이건 정상적인 HTTPS 서브도메인 형태야."}
            )

    elif quiz_id == "home_memo":
        selected = payload.get("choices", [])
        try:
            selected_set = set(int(x) for x in selected)
        except Exception:
            return JsonResponse({"error": "choices must be int[]"}, status=400)

        ok = selected_set == {0, 2}  # 정답: 0,2만 체크
        if ok:
            SESSIONS[sid]["quiz"]["memo"] = True
            return JsonResponse({"correct": True})
        else:
            return JsonResponse({"correct": False})

    else:
        return JsonResponse({"error": "Unknown quiz_id"}, status=400)


# ========== 문자 앱 채점 ==========
ANSWER_KEY = {
    "caseA": {
        "truth": "phish",
        "reasons": {
            "급박한 기한",
            "환불/금전 미끼",
            "비공식/유사 도메인",
            "http/철자 변형(hxxp)",
        },
    },
    "caseB": {
        "truth": "phish",
        "reasons": {
            "브랜드/기관 스푸핑",
            "서브도메인/유사 도메인",
            "모호한 사유(보안등급 하향)",
            "login/secure 등 키워드",
        },
    },
    "caseC": {
        "truth": "safe",
        "reasons": {
            "공식 도메인",
            "발신/맥락 일치",
            "금전 미끼/긴급 압박 없음",
        },
    },
}


def _exact_match(selected, correct_set):
    # 순서 무관 완전일치(개수 동일)
    return set(selected) == set(correct_set)


@csrf_exempt
def sms_check(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    sid = payload.get("session_id")
    case_id = payload.get("case_id")
    judge = payload.get("judge")  # "phish" | "safe"
    reasons = payload.get("reasons", [])

    if not sid or sid not in SESSIONS:
        return JsonResponse({"error": "Invalid session"}, status=400)
    if case_id not in ANSWER_KEY or judge not in ("phish", "safe"):
        return JsonResponse({"error": "Invalid params"}, status=400)

    answer = ANSWER_KEY[case_id]
    correct = (judge == answer["truth"]) and _exact_match(reasons, answer["reasons"])

    if correct:
        SESSIONS[sid]["sms_solved"].add(case_id)

    return JsonResponse({"correct": bool(correct)})


# ========== 키 공개 (프론트에 키 없음) ==========
STAGE_KEYS = {"stage1": "YOU"}


@csrf_exempt
def key_reveal(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    sid = payload.get("session_id")
    if not sid or sid not in SESSIONS:
        return JsonResponse({"error": "Invalid session"}, status=400)

    # 문자 퍼즐 3개 전부 해결해야 공개
    solved_sms = SESSIONS[sid].get("sms_solved", set())
    if len(solved_sms) < 3:
        return JsonResponse({"error": "locked"}, status=403)

    return JsonResponse({"key": STAGE_KEYS["stage1"]})
