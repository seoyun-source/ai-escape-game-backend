# === (1) 세션 시작 시 진행상태 포함 ===
# SESS[sid] = {"link": None, "clues": [], "solved": {"internet": False, "memo": False}}
@app.post("/session/start", response_model=StartResp)
def session_start():
    sid = uuid4().hex
    SESS[sid] = {"link": None, "clues": [], "solved": {"internet": False, "memo": False}}
    return {"session_id": sid}

# === (2) 홈 화면에서 쓸 정답표 ===
ANSWER_KEY.update({
    "home_internet": { "type": "single", "answer": 0 },    # 아래 인터넷 퍼즐에서 0번 보기가 '의심 링크'라고 가정
    "home_memo":     { "type": "multi",  "answers": [0,2] } # 메모 퍼즐에서 0,2번 체크가 정답이라고 가정
})

# === (3) 퀴즈 체크 API 확장: 단일/복수 모두 처리 + 진행도 갱신 ===
from typing import Optional, List

class CheckReq(BaseModel):
    quiz_id: str
    choice_index: Optional[int] = None  # single용
    choices: Optional[List[int]] = None # multi용
    session_id: Optional[str] = None    # 진행도 반영하려면 세션 필요

QUIZ_TO_FLAG = {
    "home_internet": "internet",
    "home_memo": "memo",
}

@app.post("/quiz/check", response_model=CheckResp)
def quiz_check(req: CheckReq):
    key = ANSWER_KEY.get(req.quiz_id)
    if not key:
        raise HTTPException(400, "unknown quiz_id")

    correct = False
    if key["type"] == "single":
        if req.choice_index is None:
            raise HTTPException(400, "choice_index required")
        correct = (req.choice_index == key["answer"])

    elif key["type"] == "multi":
        if req.choices is None:
            raise HTTPException(400, "choices required")
        correct = sorted(req.choices) == sorted(key["answers"])
    else:
        raise HTTPException(400, "unsupported quiz type")

    # 세션 진행도 갱신(있을 때만)
    if correct and req.session_id:
        s = SESS.get(req.session_id)
        if s and "solved" in s and req.quiz_id in QUIZ_TO_FLAG:
            s["solved"][QUIZ_TO_FLAG[req.quiz_id]] = True

    msg = "정답!" if correct else "아쉬움! 다시 생각해보자."
    return {"correct": correct, "message": msg}

# === (4) 홈 화면에서 잠금 해제 상태 확인 ===
@app.get("/session/state")
def session_state(session_id: str):
    s = SESS.get(session_id)
    if not s:
        raise HTTPException(400, "no session")
    return {"solved": s.get("solved", {"internet": False, "memo": False})}
