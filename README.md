# 당근 중국어 스터디 사이트

주소: https://lkj640.github.io/carrot_chinese/

매주 목요일 저녁 · 교재: Learn Chinese with Pipo · Chinese Conversations HSK 1-2 (46편)

## 구성

| 파일 | 역할 |
|---|---|
| `index.html` | 첫 화면 — 다음 모임 공지 + 46주 학습 순서 + 모임 목록 |
| `meeting.html?d=YYYY-MM-DD` | 모임별 페이지 — 듣기(유튜브) · 교재 · 단어장 |
| `meetings.json` | **모임 목록과 공지. 매주 여기에 한 항목만 추가해요.** 시간·장소 기본값은 `defaults` |
| `plan.json` | 46주 학습 순서 (1주차 = 2026-10-29, 매주 목요일) |
| `meetings/<날짜>/` | `data.json`(汉字·병음·번역·단어), `workbook.html`, `workbook.pdf` |
| `tools/<날짜>/` | 그 주 원본: `lines.py`(문장·시각·병음·번역), `vocab.py`(단어), `build_book.py`(교재) |

공지 규칙: 오늘 이후 가장 가까운 모임이 맨 위에 나와요. 모임 당일은 `defaults.switchHour`(지금 23시)까지 '오늘 모임'으로 보여요.
모임 항목이 아직 없는 주는 `plan.json`의 다음 주차 주제가 공지 카드에 대신 나와요.

## 매주 새 모임 올리기

1. 유튜브 영상의 중국어 자막(시각 포함)으로 `tools/<날짜>/lines.py`를 만들어요.
   `("H", 구간 제목, {"A": "화자 이름", "B": "…"})`, `(화자, 시각초, "汉字", "병음", "한국어")` — 화자 A·B 대화, N 안내, V 핵심 단어
2. `vocab.py`에 `(汉字, 병음, 뜻)` 묶음
3. `python3 tools/make_data.py tools/<날짜> meetings/<날짜>/data.json`
4. 교재: `python3 tools/<날짜>/build_book.py tools/<날짜> meetings/<날짜>/workbook.html` → Chrome으로 PDF 저장
   (`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer --print-to-pdf=meetings/<날짜>/workbook.pdf file://…/workbook.html`)
5. `meetings.json`에 항목 추가 → `git add . && git commit -m "…" && git push`

병음은 不·一의 바뀐 성조를 그대로 적고(bú kèqi, yíhuìr), 3성+3성은 원래 성조로 적어요.
