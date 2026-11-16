"""5주차 가족 이야기 교재(workbook.html) 만들기 → Chrome으로 PDF 출력.
python3 tools/2026-11-26/build_book.py tools/2026-11-26 meetings/2026-11-26/workbook.html
"""
import sys, html
work, out = sys.argv[1:3]
sys.path.insert(0, work)
from lines import L
from vocab import VOCAB
sys.path.insert(0, f"{work}/..")
from ruby import zp

e = lambda s: html.escape(s, quote=False)
fmt = lambda t: f"{int(t)//60}:{int(t)%60:02d}"

# 대화별로 묶기: [(제목, 화자이름, [줄...])]
D = []
for x in L:
    if x[0] == "H":
        D.append({"title": x[1], "who": x[2], "lines": []})
    else:
        D[-1]["lines"].append(x)

def dstart(i): return D[i]["lines"][0][1]
def dend(i): return D[i + 1]["lines"][0][1] if i + 1 < len(D) else 14 * 60 + 35

def zh(s): return f'<span class="zh" lang="zh-CN">{e(s)}</span>'

def dialog(i):
    d = D[i]
    rows = []
    for s, t, z, py, ko in d["lines"]:
        if s not in "AB":
            continue
        rows.append(f'<div class="dl"><div class="dw {s}">{e(d["who"][s])}<span>{fmt(t)}</span></div>'
                    f'<div>{zp(z, py, "b")}</div><small class="dk">{e(ko)}</small></div>')
    scene = d["lines"][0]
    return (f'<h3 class="scene"><span class="sn">대화 {i+1}</span> {zh(scene[2])} <span class="sk">{e(scene[4])} · {fmt(scene[1])}</span></h3>'
            '<div class="dlg">' + "".join(rows) + "</div>")

def words(i, j):
    # 대화마다 표 하나씩, 두 표를 나란히 (이번 주는 대화가 길어서 자리를 아껴요)
    out = []
    for k in (i, j):
        tr = "".join(f'<tr><td class="wz">{zp(z, py)}</td><td>{e(ko)}</td></tr>'
                     for s, t, z, py, ko in D[k]["lines"] if s == "V")
        out.append(f'<table class="t words" style="flex:1"><tr><th colspan="2">대화 {k+1}</th></tr>' + tr + "</table>")
    return '<div class="two">' + "".join(out) + "</div>"

def h(tag, title): return f'<h2><span class="tag">{tag}</span>{title}</h2>'

def lesson(no, i, title, goals):
    g = "".join(f"<li>{x}</li>" for x in goals)
    return (f'<section class="lesson"><div class="hd"><div class="k">LESSON {no} · {fmt(dstart(i))}–{fmt(dend(i+1))}</div><h1>{title}</h1>'
            f'<div class="s">영상 대화 {i+1} · 대화 {i+2}</div></div><div class="goal"><b>오늘의 목표</b><ul>{g}</ul></div>'
            + h("대화", "영상 속 대화") + dialog(i) + dialog(i + 1))

def ol(items):
    return '<ol class="q">' + "".join(f"<li><span class=n>{k}</span>{x}</li>" for k, x in enumerate(items, 1)) + "</ol>"

B = '<span class="bl"></span>'
BS = '<span class="bl s"></span>'

def say(*qs):
    rows = ""
    for who, q, hint in qs:
        rows += (f'<div class="dl"><div class="dw B">{who}</div><div><b class="zh" lang="zh-CN">{e(q)}</b><small>{e(hint)}</small></div></div>'
                 '<div class="dl"><div class="dw T">나</div><div class="ans"></div></div>')
    return '<div class="dlg">' + rows + "</div>"

def box(title, body, cls="y"):
    return f'<div class="box {cls}"><b>{title}</b>{body}</div>'


def Z(s): return f'<span class="zh" lang="zh-CN">{s}</span>'

P = []

# ---------- 표지 ----------
P.append(f'''<section class="cover"><div class="stripe"></div>
<div class="ct"><h1>왕초보 중국어<br>가족 이야기 교재</h1>
<div class="cs">Learn Chinese with Pipo · HSK 1~2 대화 5주차 · 14:35</div>
<div class="big" lang="zh-CN">你家有几口人？</div>
<table class="toc">
<tr><th>시작</th><td>가족 호칭 · 두 주인공의 가족 · 이번 주 대화 순서</td></tr>
<tr><th>LESSON 1</th><td>몇 식구예요? · 아빠의 직업 (几口人 · 都有谁 · 和 · 吧)</td></tr>
<tr><th>LESSON 2</th><td>엄마의 직업 · 오빠의 직장 (教 · 当 · 哪个 · 常/不常 · 给…打电话)</td></tr>
<tr><th>LESSON 3</th><td>왕밍의 가족 · 누나의 직업 (有…也有… · 能 · 有时候)</td></tr>
<tr><th>LESSON 4</th><td>대학생 남동생 · 부모님의 일상 (想当 · 说得很好 · 她做的菜 · 最)</td></tr>
<tr><th>LESSON 5</th><td>주말 계획 · 가족사진 (打算 · 坐火车 · 这是… · 像)</td></tr>
<tr><th>부록</th><td>정답 · 가족 이야기 질문과 대답 총정리 · 단어장</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_chinese → 11월 26일 모임 (문장을 누르면 그 부분부터 재생 · 병음과 한국어 번역 보기)<br>
각 레슨 구성: 오늘의 목표 → 영상 속 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기</div></div>
<div class="stripe"></div></section>''')

# ---------- 시작 ----------
P.append('<section class="lesson"><div class="hd"><div class="k">开始 · 시작</div><h1>시작하기 전에: 가족 호칭</h1></div>'
 + box("이번 주는 이런 영상이에요", "<p>열 개의 대화가 한 편의 이야기예요. 새로 친구가 된 <b>리메이(李美)</b>와 <b>왕밍(王明)</b>이 서로의 가족 — 몇 식구인지, 무슨 일을 하는지, 평소에 뭘 하는지 — 를 묻고 답해요. 마지막에는 가족사진도 보여 줘요. 모임에 <b>우리 가족사진</b> 한 장을 가져오세요!</p>", "g")
 + h("가족 호칭", "중국어로 우리 가족 부르기") + f'''
<table class="t"><tr><th>윗사람</th><td>{Z("爸爸")} 아빠 · {Z("妈妈")} 엄마 · {Z("父母")} 부모 · {Z("爷爷 / 奶奶")} 할아버지 / 할머니 (보너스)</td></tr>
<tr><th>형제자매</th><td>{Z("哥哥")} 형·오빠 · {Z("姐姐")} 누나·언니 · {Z("弟弟")} 남동생 · {Z("妹妹")} 여동생</td></tr>
<tr><th>모두</th><td>{Z("家人")} 가족 · {Z("全家")} 온 가족 · {Z("一家人")} 한 가족</td></tr></table>
<p class="sm">※ 중국어는 말하는 사람이 남자든 여자든 같아요. 哥哥 = 형도 되고 오빠도 돼요.</p>
''' + h("두 주인공", "영상 속 두 사람의 가족") + f'''
<table class="t"><tr><th></th><th>{Z("李美")} 리메이 — 4식구</th><th>{Z("王明")} 왕밍 — 5식구</th></tr>
<tr><td>아빠</td><td>{Z("医生")} 의사 · 상하이의 큰 병원</td><td>—</td></tr>
<tr><td>엄마</td><td>{Z("老师")} 중학교 중국어 선생님</td><td>—</td></tr>
<tr><td>형제자매</td><td>{Z("哥哥")} 엔지니어 · 상하이 회사 2년 차</td><td>{Z("姐姐")} 26살 간호사 · {Z("弟弟")} 18살 대학생(영어 전공)</td></tr></table>
'''
 + h("10가지 장면", "이번 영상에 나오는 대화")
 + '<table class="t scenes">' + "".join(
     f'<tr><td>대화 {i+1}</td><td>{fmt(dstart(i))}</td><td>{zh(D[i]["lines"][0][2])}</td><td>{e(D[i]["lines"][0][4])}</td></tr>' for i in range(10)) + "</table>"
 + "</section>")

# ---------- LESSON 1 ----------
P.append(lesson(1, 0, "몇 식구예요? · 아빠의 직업", [
    "<b>你家有几口人？</b>으로 식구 수를 묻고 답할 수 있다.",
    "<b>都有谁？ — 有爸爸、妈妈和我</b>로 가족을 소개할 수 있다.",
    "<b>…吧？</b>로 짐작하며 물을 수 있다."])
 + h("문법", "几口人 · 都有谁 · 和 · 吧")
 + '<div class="two">' + box("① 你家有几口人？ = 몇 식구예요?", f'<p>{Z("你家有几口人？")}<br>→ {Z("我家有四口人。")} 우리 가족은 네 명이에요.</p><p class="sm">口 kǒu = 식구를 세는 말 (입이 몇 개?) · 사람 일반은 {Z("个")}</p>')
 + box("② 都有谁？ — 有 A、B 和 C", f'<p>{Z("都有谁？")} 누구누구예요?<br>→ {Z("有爸爸、妈妈、哥哥和我。")}</p><p class="sm">和 hé = 그리고 · 여러 개를 늘어놓을 땐 마지막 사이에만 和를 써요.</p>') + "</div>"
 + '<div class="two">' + box("③ 是 + 직업 · 在 + 장소 + 工作", f'<p>{Z("你爸爸做什么工作？")} → {Z("我爸爸是医生。")}<br>{Z("他在哪儿工作？")} → {Z("他在医院工作。")}</p><p class="sm">2주차 자기소개와 같은 모양 — 주어만 爸爸로 바꿨어요!</p>')
 + box("④ 문장 + 吧？ = ~죠? (짐작)", f'<p>{Z("医生工作很忙吧？")} 의사는 많이 바쁘시죠?<br>{Z("你们会想他吧？")} 보고 싶겠네요?</p>') + "</div>"
 + box("⑤ 不是 · 也 · 但是", f'<p>{Z("你家人都在北京吗？ — 不是，我爸爸妈妈在上海。")} · {Z("他也在上海工作。")} · {Z("但是他很喜欢这个工作。")} 그래도 그 일을 좋아하세요.</p>', "g")
 + h("단어", "대화 1·2 핵심 단어") + words(0, 1)
 + h("연습 A", "알맞은 말을 골라 넣으세요. (几 · 谁 · 和 · 吧)")
 + ol([f'你家有 {BS} 口人？', f'都有 {BS}？', f'爸爸、妈妈 {BS} 我。', f'医生工作很忙 {BS}？'])
 + h("연습 B", "우리 가족 이야기로 대답해 보세요.")
 + ol([f'你家有几口人？ → {B}', f'都有谁？ → {B}'])
 + h("말하기", "왕밍에게 우리 가족을 소개해 보세요")
 + say(("王明", "你家有几口人？", "가족이 몇 명이에요?"), ("王明", "你爸爸做什么工作？", "아버지는 무슨 일을 하세요?"))
 + "</section>")

# ---------- LESSON 2 ----------
P.append(lesson(2, 2, "엄마의 직업 · 오빠의 새 직장", [
    "<b>她教汉语 · 她喜欢当老师</b>로 가족의 일을 설명할 수 있다.",
    "<b>他常回家吗？ — 不常回</b>로 얼마나 자주 하는지 말할 수 있다.",
    "칭찬에 <b>哪里哪里</b>로 겸손하게 대답할 수 있다."])
 + h("문법", "教 · 当 · 哪个 · 常 · 给…打电话")
 + '<div class="two">' + box("① 教 + 과목 · 当 + 직업", f'<p>{Z("她教什么？")} → {Z("她教汉语。")} 중국어를 가르쳐요.<br>{Z("她喜欢当老师吗？")} 선생님 일을 좋아하세요?</p><p class="sm">当 dāng = (어떤 직업·역할을) 하다, 되다</p>')
 + box("② 哪个 + 명사 = 어느 ~", f'<p>{Z("在哪个学校？")} 어느 학교에서요?<br>→ {Z("在一个中学。")} 한 중학교에서요.</p><p class="sm">哪儿 = 어디 · 哪个 = 어느 것</p>') + "</div>"
 + '<div class="two">' + box("③ 常 ↔ 不常 · 太…了", f'<p>{Z("他常回家吗？")} 집에 자주 와요?<br>→ {Z("不常回。工作太忙了。")} 자주 못 와요. 일이 너무 바빠요.</p><p class="sm">太 + 형용사 + 了 = 너무 ~하다</p>')
 + box("④ 给 + 사람 + 打电话", f'<p>{Z("我们常给他打电话。")} 우리가 자주 오빠한테 전화해요.<br>{Z("我妈妈常打电话。")} 엄마가 자주 전화하세요.</p>') + "</div>"
 + box("⑤ 칭찬받으면 哪里哪里 · 刚 + 기간", f'<p>{Z("工程师！很厉害！")} 엔지니어! 대단하네요! → {Z("哪里哪里。他刚工作两年。")} 뭘요. 이제 겨우 2년 됐어요.</p>', "g")
 + h("단어", "대화 3·4 핵심 단어") + words(2, 3)
 + h("연습 A", "알맞은 말을 넣으세요. (教 · 当 · 常 · 给)")
 + ol([f'她 {BS} 汉语。', f'她喜欢 {BS} 老师吗？', f'他 {BS} 回家吗？', f'我们常 {BS} 他打电话。'])
 + h("연습 B", "상황에 맞는 말을 고르세요.")
 + '<table class="t match"><tr><td>① 칭찬을 들었을 때</td><td>ⓐ 很厉害！</td></tr><tr><td>② 바빠서 집에 못 갈 때</td><td>ⓑ 不太大，但是很好。</td></tr><tr><td>③ 상대 가족이 대단할 때</td><td>ⓒ 哪里哪里。</td></tr><tr><td>④ 회사가 크냐고 물을 때</td><td>ⓓ 工作太忙了。</td></tr></table>'
 + h("말하기", "왕밍에게 엄마와 형제자매 이야기를 해 보세요")
 + say(("王明", "你妈妈也工作吗？", "어머니도 일하세요?"), ("王明", "他常回家吗？", "집에 자주 와요?"))
 + "</section>")

# ---------- LESSON 3 ----------
P.append(lesson(3, 4, "왕밍의 가족 · 누나의 직업", [
    "<b>有…也有…</b>로 가족 구성을 말할 수 있다.",
    "<b>能 + 동사</b>로 '~할 수 있어서'를 말할 수 있다.",
    "<b>有时候 · 很有意义</b>로 일에 대한 느낌을 말할 수 있다."])
 + h("문법", "有…也有… · 了 · 能 · 有时候")
 + '<div class="two">' + box("① 有 A 也有 B = A도 있고 B도 있다", f'<p>{Z("你有姐姐也有弟弟啊！")} 누나도 있고 남동생도 있네요!<br>→ {Z("是啊，我们家很热闹。")} 네, 우리 집은 북적북적해요.</p>')
 + box("② 工作了吗？ = (이제) 일해요?", f'<p>{Z("你姐姐工作了吗？")} 누나는 (학교 졸업하고) 일해요?<br>→ {Z("工作了。她是护士。")}</p><p class="sm">了 = 이미 그렇게 됐다 (변화)</p>') + "</div>"
 + '<div class="two">' + box("③ 能 + 동사 = ~할 수 있다", f'<p>{Z("她说能帮助别人很开心。")}<br>다른 사람을 도울 수 있어서 기쁘대요.</p><p class="sm">她说 + 문장 = 그녀가 ~라고 말했다</p>')
 + box("④ 有时候 = 가끔 · 很有意义 = 의미 있다", f'<p>{Z("是的，有时候很累。")} 네, 가끔은 피곤해해요.<br>{Z("但是很有意义。")} 그래도 의미 있는 일이에요.</p>') + "</div>"
 + box("⑤ 나이 묻기 복습 (4주차)", f'<p>{Z("你姐姐多大了？")} → {Z("她二十六岁。")} · {Z("你弟弟呢？")} → {Z("他今年十八岁。")}</p>', "g")
 + h("단어", "대화 5·6 핵심 단어") + words(4, 5)
 + h("연습 A", "알맞은 말을 넣으세요. (也 · 能 · 有时候 · 有意义)")
 + ol([f'你有姐姐 {BS} 有弟弟啊！', f'她说 {BS} 帮助别人很开心。', f'{BS} 很累。', f'但是很 {BS}。'])
 + h("연습 B", "중국어로 옮겨 보세요.")
 + ol([f'우리 집은 북적북적해요. → {B}', f'우리 누나는 간호사예요. → {B}'])
 + h("말하기", "리메이의 질문에 우리 형제자매 이야기로 대답해 보세요")
 + say(("李美", "你有兄弟姐妹吗？", "형제자매 있어요?"), ("李美", "他/她工作了吗？", "(형제자매는) 일해요?"))
 + "</section>")

# ---------- LESSON 4 ----------
P.append(lesson(4, 6, "대학생 남동생 · 부모님의 일상", [
    "<b>他想当英语老师</b>로 가족의 꿈을 말할 수 있다.",
    "<b>她做的菜</b>처럼 '동사 + 的 + 명사'로 꾸며 말할 수 있다.",
    "<b>平时 · 最喜欢</b>으로 가족의 일상과 취향을 말할 수 있다."])
 + h("문법", "在上大学 · 说得很好 · 想当 · 的 · 最")
 + '<div class="two">' + box("① 上 + 학교 = 학교에 다니다", f'<p>{Z("你弟弟在上学吗？")} 남동생은 학교 다녀요?<br>→ {Z("对，他在上大学。")} 네, 대학교 다녀요.<br>{Z("他学什么专业？")} → {Z("他学英语。")}</p>')
 + box("② 동사 + 得 + 很好 · 想当 + 직업", f'<p>{Z("他英语说得很好。")} 영어를 아주 잘해요.<br>{Z("他想当英语老师。")} 영어 선생님이 되고 싶대요.<br>{Z("我们都支持他。")} 우리 모두 응원해요.</p>') + "</div>"
 + '<div class="two">' + box("③ 동사 + 的 + 명사 = ~한 것", f'<p>{Z("她做的菜好吃吗？")} 어머니가 만든 요리는 맛있어요?<br>{Z("我最喜欢吃她做的菜。")} 엄마가 해 준 음식을 제일 좋아해요.</p><p class="sm">她做 (그녀가 만든) + 的 + 菜 (요리)</p>')
 + box("④ 平时 · 喜欢 + 동사", f'<p>{Z("你爸爸妈妈平时在家做什么？")}<br>→ {Z("我爸爸喜欢看书。")} 아빠는 책 읽기를 좋아해요.<br>→ {Z("我妈妈喜欢做饭。")} 엄마는 요리를 좋아해요.</p>') + "</div>"
 + box("⑤ 最 = 가장 · 一家人在一起真好", f'<p>{Z("你真幸福！")} 정말 행복하겠다! · {Z("周末我们常一起吃饭。")} 주말엔 자주 같이 밥 먹어요. · {Z("一家人在一起真好。")} 가족이 함께면 참 좋아요.</p>', "g")
 + h("단어", "대화 7·8 핵심 단어") + words(6, 7)
 + h("연습 A", "알맞은 말을 넣으세요. (的 · 得 · 最 · 想当)")
 + ol([f'她做 {BS} 菜很好吃。', f'他英语说 {BS} 很好。', f'我 {BS} 喜欢吃她做的菜。', f'他 {BS} 英语老师。'])
 + h("연습 B", "( ) 안의 내용으로 대답해 보세요.")
 + ol([f'你爸爸妈妈平时在家做什么？ (아빠: 책 읽기 · 엄마: 요리) → {B}', f'他学什么专业？ (중국어) → {B}'])
 + h("말하기", "우리 가족의 일상을 말해 보세요")
 + say(("李美", "你爸爸妈妈平时在家做什么？", "부모님은 평소 집에서 뭘 하세요?"), ("李美", "你妈妈做的菜好吃吗？", "어머니 요리는 맛있어요?"))
 + "</section>")

# ---------- LESSON 5 ----------
P.append(lesson(5, 8, "주말 계획 · 가족사진 보여 주기", [
    "<b>这个周末你有什么计划？</b>로 계획을 묻고 <b>想 · 打算 · 要</b>로 대답할 수 있다.",
    "<b>坐火车回去</b>처럼 교통수단을 말할 수 있다.",
    "가족사진을 보여 주며 <b>这是我爸爸 · 你和你妈妈很像</b>으로 이야기할 수 있다."])
 + h("문법", "계획 말하기 · 坐 · 这是 · 像")
 + '<div class="two">' + box("① 계획 묻기", f'<p>{Z("这个周末你有什么计划？")}<br>{Z("你周末有什么安排吗？")}<br>둘 다 "주말에 뭐 해요?"</p>')
 + box("② 想 · 打算 · 要 + 동사", f'<p>{Z("我想回家看看我的家人。")} 집에 가서 가족을 보고 싶어요.<br>{Z("你打算什么时候走？")} 언제 갈 계획이에요?<br>{Z("我要在学校学习。")} 학교에서 공부할 거예요.</p><p class="sm">想 하고 싶다 · 打算 ~할 계획이다 · 要 ~할 것이다(의지)</p>') + "</div>"
 + '<div class="two">' + box("③ 坐 + 교통수단 + 동사", f'<p>{Z("星期五晚上坐火车回去。")} 금요일 저녁에 기차 타고 가요.<br>{Z("坐公交车 · 坐飞机")} 버스를 타다 · 비행기를 타다</p>')
 + box("④ 这是… · A 和 B 很像", f'<p>{Z("这是我爸爸。他很帅吧？")} 우리 아빠예요. 멋있죠?<br>{Z("你和你妈妈很像！")} 엄마를 많이 닮았네요!<br>→ {Z("大家都这么说。")} 다들 그렇게 말해요.</p>') + "</div>"
 + box("⑤ 很久没…了 · 一定 · 祝你… · 希望…", f'<p>{Z("很久没回家了吧？")} 집에 안 간 지 오래됐죠? · {Z("一定很想你。")} 분명 보고 싶어 하실 거예요. · {Z("祝你旅途愉快！")} · {Z("希望你有机会见到他们。")}</p>', "g")
 + h("단어", "대화 9·10 핵심 단어") + words(8, 9)
 + h("연습 A", "알맞은 말을 넣으세요. (打算 · 坐 · 像 · 这是)")
 + ol([f'你 {BS} 什么时候走？', f'星期五晚上 {BS} 火车回去。', f'你和你妈妈很 {BS}！', f'{BS} 我哥哥。'])
 + h("연습 B", "중국어로 옮겨 보세요.")
 + ol([f'이번 주말에 무슨 계획 있어요? → {B}', f'집에 가서 가족을 보고 싶어요. → {B}'])
 + h("최종 미션", "우리 가족사진으로 가족 소개하기")
 + f'''<table class="t mine"><tr><th>순서</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>① 식구 수</td><td>{Z("我家有…口人。")}</td><td></td></tr>
<tr><td>② 누구누구</td><td>{Z("有爸爸、妈妈…和我。")}</td><td></td></tr>
<tr><td>③ 사진 보여 주기</td><td>{Z("这是我…。")}</td><td></td></tr>
<tr><td>④ 직업·사는 곳</td><td>{Z("他/她是…。他/她在…工作。")}</td><td></td></tr>
<tr><td>⑤ 좋아하는 것</td><td>{Z("他/她平时喜欢…。")}</td><td></td></tr>
<tr><td>⑥ 닮은 사람·마무리</td><td>{Z("我和…很像。我很爱我的家人。")}</td><td></td></tr></table>'''
 + box("예시", f'<p>{Z("我家有四口人：爸爸、妈妈、姐姐和我。这是我爸爸，他是工程师，在首尔工作。这是我妈妈，她平时喜欢做饭，她做的菜非常好吃！这是我姐姐，她是护士。大家都说我和我妈妈很像。我很爱我的家人。")}</p>')
 + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>你家有几口人？ 都有谁？로 가족을 묻고 답할 수 있다.</li><li>가족의 직업과 일하는 곳을 말할 수 있다.</li><li>常·不常·有时候로 얼마나 자주인지 말할 수 있다.</li><li>她做的菜처럼 的로 꾸며 말할 수 있다.</li><li>想·打算·要로 주말 계획을 말할 수 있다.</li><li>가족사진을 보여 주며 这是…로 소개할 수 있다.</li></ul>'
 + "</section>")

# ---------- 부록 ----------
P.append(f'''<section class="lesson"><div class="hd"><div class="k">附录 A</div><h1>정답</h1></div><div class="ans-list">
<p><b>Lesson 1</b> A: 1 几 · 2 谁 · 3 和 · 4 吧 &nbsp;|&nbsp; B: 예) 我家有三口人。 · 有爸爸、妈妈和我。</p>
<p><b>Lesson 2</b> A: 1 教 · 2 当 · 3 常 · 4 给 &nbsp;|&nbsp; B: ①ⓒ ②ⓓ ③ⓐ ④ⓑ</p>
<p><b>Lesson 3</b> A: 1 也 · 2 能 · 3 有时候 · 4 有意义 &nbsp;|&nbsp; B: 1 我们家很热闹。 · 2 我姐姐是护士。</p>
<p><b>Lesson 4</b> A: 1 的 · 2 得 · 3 最 · 4 想当 &nbsp;|&nbsp; B: 1 我爸爸喜欢看书，我妈妈喜欢做饭。 · 2 他学汉语。</p>
<p><b>Lesson 5</b> A: 1 打算 · 2 坐 · 3 像 · 4 这是 &nbsp;|&nbsp; B: 1 这个周末你有什么计划？ · 2 我想回家看看我的家人。</p>
</div>
<div class="hd" style="margin-top:26px"><div class="k">附录 B</div><h1>가족 이야기 질문과 대답 총정리</h1></div>
<table class="t"><tr><th>묻는 것</th><th>질문</th><th>대답</th></tr>
<tr><td>식구 수</td><td>{Z("你家有几口人？")}</td><td>{Z("我家有四口人。")}</td></tr>
<tr><td>누구누구</td><td>{Z("都有谁？")}</td><td>{Z("有爸爸、妈妈、哥哥和我。")}</td></tr>
<tr><td>사는 곳</td><td>{Z("你家人都在北京吗？")}</td><td>{Z("不是，我爸爸妈妈在上海。")}</td></tr>
<tr><td>직업</td><td>{Z("你爸爸做什么工作？")}</td><td>{Z("我爸爸是医生。")}</td></tr>
<tr><td>일하는 곳</td><td>{Z("他在哪儿工作？")}</td><td>{Z("他在医院工作。")}</td></tr>
<tr><td>가르치는 것·전공</td><td>{Z("她教什么？ / 他学什么专业？")}</td><td>{Z("她教汉语。 / 他学英语。")}</td></tr>
<tr><td>얼마나 자주</td><td>{Z("他常回家吗？")}</td><td>{Z("不常回。工作太忙了。")}</td></tr>
<tr><td>평소</td><td>{Z("你爸爸妈妈平时在家做什么？")}</td><td>{Z("我爸爸喜欢看书。")}</td></tr>
<tr><td>계획</td><td>{Z("这个周末你有什么计划？")}</td><td>{Z("我想回家看看我的家人。")}</td></tr>
<tr><td>사진</td><td>{Z("这是你爸爸吗？")}</td><td>{Z("对，这是我爸爸。")}</td></tr></table>
</section>''')

voc = ['<section class="lesson"><div class="hd"><div class="k">附录 C</div><h1>단어장</h1><div class="s">사이트의 \'단어장\'과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="2">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span>{zp(z, py)}</td><td>{e(ko)}</td></tr>' for z, py, ko in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))


CSS = open(f"{work}/../book.css", encoding="utf-8").read() + open(f"{work}/../book_zh.css", encoding="utf-8").read()
CSS += ".lesson .dlg .dl{padding:2px 0}"  # 대화가 길어서 조금 촘촘하게
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>중국어 가족 이야기 교재 5주차</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
