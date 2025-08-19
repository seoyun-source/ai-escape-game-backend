const express = require("express");
const path = require("path");
const app = express();

app.use(express.json());
app.use(express.static(__dirname));

const CORRECT = "trust_nobody";
const FLAG = "FLAG{ARE}"; // 서버에만 보관

app.post("/api/check-answer", (req, res) => {
  const { answer } = req.body || {};
  const ok = String(answer).trim().toLowerCase() === CORRECT;

  if (ok) {
    res.json({ ok: true, flag: FLAG }); // 정답일 때만 flag 전달
  } else {
    res.json({ ok: false });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server on http://localhost:${PORT}`));
