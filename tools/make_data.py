"""모임 자료(tools/<날짜>/lines.py · vocab.py)를 사이트용 data.json으로 변환합니다.

사용법:  python3 tools/make_data.py tools/2026-10-29 meetings/2026-10-29/data.json

lines.py
  L = [("H", 구간 제목, {"A": "엄마", "B": "아들"}),   # 구간마다 화자 이름(선택)
       ("A", 시각(초), "汉字", "병음", "한국어"), ...]
  화자: A·B = 대화 인물, N = 장면 제목·안내, V = 핵심 단어
vocab.py
  VOCAB = [("묶음 제목", [("汉字", "병음", "뜻"), ...]), ...]
"""
import json, sys

DEFAULT_WHO = {"A": "A", "B": "B", "N": "📢", "V": "단어"}

if __name__ == "__main__":
    src, out = sys.argv[1:3]
    sys.path.insert(0, src)
    from lines import L
    from vocab import VOCAB
    secs, prev = [], -1
    for x in L:
        if x[0] == "H":
            secs.append({"title": x[1], "who": x[2] if len(x) > 2 else {}, "lines": []})
            continue
        s, t, zh, py, ko = x
        assert t >= prev, f"시각 순서가 뒤집혔어요: {t} {zh}"
        prev = t
        secs[-1]["lines"].append({"s": s, "t": t, "es": zh, "py": py, "ko": ko})
    vocab = [{"title": t, "rows": [list(r) for r in rows]} for t, rows in VOCAB]
    json.dump({"speakers": DEFAULT_WHO, "sections": secs, "vocab": vocab},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(out, sum(len(s["lines"]) for s in secs), "lines,", len(secs), "sections,", sum(len(v["rows"]) for v in vocab), "words")
