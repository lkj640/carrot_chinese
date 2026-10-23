"""2주차 자기소개 교재(workbook.html) 만들기 → Chrome으로 PDF 출력.
python3 tools/2026-11-05/build_book.py tools/2026-11-05 meetings/2026-11-05/workbook.html
"""
import sys, html
work, out = sys.argv[1:3]
sys.path.insert(0, work)
from lines import L
from vocab import VOCAB

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
def dend(i): return D[i + 1]["lines"][0][1] if i + 1 < len(D) else 16 * 60 + 34

def zh(s): return f'<span class="zh" lang="zh-CN">{e(s)}</span>'

def dialog(i):
    d = D[i]
    rows = []
    for s, t, z, py, ko in d["lines"]:
        if s not in "AB":
            continue
        rows.append(f'<div class="dl"><div class="dw {s}">{e(d["who"][s])}<span>{fmt(t)}</span></div>'
                    f'<div><b class="zh" lang="zh-CN">{e(z)}</b><i class="py">{e(py)}</i></div><small class="dk">{e(ko)}</small></div>')
    scene = d["lines"][0]
    return (f'<h3 class="scene"><span class="sn">대화 {i+1}</span> {zh(scene[2])} <span class="sk">{e(scene[4])} · {fmt(scene[1])}</span></h3>'
            '<div class="dlg">' + "".join(rows) + "</div>")

def words(i, j):
    # 대화마다 표 하나씩, 두 표를 나란히 (이번 주는 대화가 길어서 자리를 아껴요)
    out = []
    for k in (i, j):
        tr = "".join(f'<tr><td class="wz">{zh(z)}</td><td class="wp">{e(py)}</td><td>{e(ko)}</td></tr>'
                     for s, t, z, py, ko in D[k]["lines"] if s == "V")
        out.append(f'<table class="t words" style="flex:1"><tr><th colspan="3">대화 {k+1}</th></tr>' + tr + "</table>")
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
<div class="ct"><h1>왕초보 중국어<br>자기소개 교재</h1>
<div class="cs">Learn Chinese with Pipo · HSK 1~2 대화 2주차 · 16:34</div>
<div class="big" lang="zh-CN">我叫…。很高兴认识你！</div>
<table class="toc">
<tr><th>시작</th><td>성조 변화 복습 · 자기소개 공식 · 나라 이름 만들기</td></tr>
<tr><th>LESSON 1</th><td>수업 첫날 · 유학생 사무실 (是 · 什么 · 的 · 还在)</td></tr>
<tr><th>LESSON 2</th><td>입사 면접 · 언어 교환 (哪国人 · 在 + 장소 · 会 · 可以)</td></tr>
<tr><th>LESSON 3</th><td>룸메이트 · 신입 연수 (从…来 · 以前/现在 · 吧)</td></tr>
<tr><th>LESSON 4</th><td>주민센터 · 헬스장 (多久了 · 동사 + 了 + 기간 · 一周三次)</td></tr>
<tr><th>LESSON 5</th><td>학부모 · 사진 동호회 (几 · 你的呢 · 可能 · 爱好)</td></tr>
<tr><th>부록</th><td>정답 · 자기소개 질문과 대답 총정리 · 단어장</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_chinese → 11월 5일 모임 (문장을 누르면 그 부분부터 재생 · 병음과 한국어 번역 보기)<br>
각 레슨 구성: 오늘의 목표 → 영상 속 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기</div></div>
<div class="stripe"></div></section>''')

# ---------- 시작 ----------
P.append('<section class="lesson"><div class="hd"><div class="k">开始 · 시작</div><h1>시작하기 전에: 자기소개 공식</h1></div>'
 + box("이 교재로 공부하는 방법", "<p>① 대화를 먼저 읽고 → ② 사이트의 '듣기'에서 문장을 눌러 듣고 → ③ <b>'현재 문장 반복'</b>으로 따라 말하고 → ④ 연습 문제를 풀어요. 마지막에는 <b>내 자기소개</b>를 중국어로 완성해서 모임에서 발표해요!</p>", "g")
 + h("성조 변화", "1주차 복습 · 이번 영상 속 예") + f'''
<table class="t"><tr><th>규칙</th><th>원래</th><th>실제 소리</th><th>영상 속 예</th></tr>
<tr><td>3성 + 3성 → <b>2성</b> + 3성</td><td>hěn hǎo</td><td><b>hén</b> hǎo</td><td>{Z("你好 · 很好 · 我也是 · 很远")}</td></tr>
<tr><td><b>不</b> + 4성 → bú</td><td>bù shì</td><td><b>bú</b> shì</td><td>{Z("不是 · 不会 · 不错")}</td></tr>
<tr><td><b>一</b> + 4성 → yí · 그 밖 → yì</td><td>yī</td><td><b>yì</b>diǎnr · <b>yì</b>qǐ</td><td>{Z("一点儿 · 一起 · 一些 · 一周")}</td></tr></table>
<p class="sm">※ 병음은 不·一의 바뀐 성조를 그대로 적었어요. 3성+3성은 원래 성조로 적고, 읽을 때만 바꿔요. (我也是 wǒ yě shì → wó yě shì)</p>
''' + h("발음", "이번 영상에서 자주 나오는 소리") + f'''
<table class="t"><tr><th>병음</th><th>소리</th><th>예</th></tr>
<tr><td><b>zh · ch · sh · r</b></td><td>혀끝을 말아 올려서 — 즈·츠·스·르</td><td>{Z("中国")} Zhōngguó · {Z("工程师")} gōngchéngshī · {Z("是")} shì · {Z("人")} rén</td></tr>
<tr><td><b>z · c · s</b></td><td>혀를 펴고 — 쯔·츠·쓰</td><td>{Z("做")} zuò · {Z("次")} cì · {Z("三")} sān</td></tr>
<tr><td><b>j · q · x</b></td><td>지·치·시</td><td>{Z("叫")} jiào · {Z("请问")} qǐngwèn · {Z("学生")} xuésheng</td></tr>
<tr><td><b>-r</b> (儿화)</td><td>끝에 혀를 말아요</td><td>{Z("哪儿")} nǎr · {Z("这儿")} zhèr · {Z("一点儿")} yìdiǎnr</td></tr></table>
''' + h("자기소개 공식", "이 다섯 문장이면 자기소개 끝!")
 + '<div class="two">' + box("나를 소개하는 5문장", f'<p>{Z("我叫○○。")} 저는 ○○라고 해요.<br>{Z("我是韩国人。")} 한국 사람이에요.<br>{Z("我是学生 / 老师。")} 학생 / 선생님이에요.<br>{Z("我在首尔工作。")} 서울에서 일해요.<br>{Z("很高兴认识你！")} 만나서 반가워요!</p><p class="sm">首尔 Shǒu\'ěr = 서울</p>')
 + box("나라 + 人 / 语 · 文", f'<p>{Z("韩国")} Hánguó 한국 → {Z("韩国人")} 한국 사람 · {Z("韩语")} 한국어<br>{Z("中国")} Zhōngguó 중국 → {Z("中国人")} · {Z("中文 / 汉语")}<br>{Z("美国 · 英国")} 미국 · 영국 → {Z("英文")} 영어<br>{Z("日本 · 法国 · 德国")} 일본 · 프랑스 · 독일</p><p class="sm">나라 이름 뒤에 人을 붙이면 "그 나라 사람"이 돼요.</p>') + "</div>"
 + h("10가지 장면", "이번 영상에 나오는 대화")
 + '<table class="t scenes">' + "".join(
     f'<tr><td>대화 {i+1}</td><td>{fmt(dstart(i))}</td><td>{zh(D[i]["lines"][0][2])}</td><td>{e(D[i]["lines"][0][4])}</td></tr>' for i in range(10)) + "</table>"
 + "</section>")

# ---------- LESSON 1 ----------
P.append(lesson(1, 0, "중국어 수업 첫날 · 유학생 사무실에서", [
    "<b>我叫…</b>로 이름을 말하고 <b>你叫什么名字？</b>로 물을 수 있다.",
    "<b>你是…人吗？</b>로 국적을 묻고 <b>我是…人</b>으로 대답할 수 있다.",
    "<b>你的中文很好！</b>처럼 칭찬하고 <b>我还在学习</b>로 겸손하게 대답할 수 있다."])
 + h("문법", "是 · 什么 · 的")
 + '<div class="two">' + box("① A 是 B = A는 B예요", f'<p>{Z("我是中国人。")} 저는 중국 사람이에요.<br>{Z("我是美国人。")} 저는 미국 사람이에요.</p><p class="sm">부정은 {Z("不是")} bú shì: {Z("我不是学生。")} 저는 학생이 아니에요.</p>')
 + box("② 什么 = 무엇 (묻는 자리에 그대로)", f'<p>{Z("你叫什么名字？")} 이름이 뭐예요?<br>→ {Z("我叫汤姆。")} 저는 톰이에요.</p><p class="sm">대답할 때는 <b>什么 자리에 답을 넣기만</b> 하면 돼요. 어순이 그대로예요!</p>') + "</div>"
 + '<div class="two">' + box("③ 사람 + 的 + 명사 = ~의", f'<p>{Z("你的中文很好！")} 당신의 중국어는 아주 좋아요!<br>{Z("我的名字")} 제 이름</p>')
 + box("④ 还在 + 동사 = 아직 ~하는 중", f'<p>{Z("我还在学习。")} 아직 배우는 중이에요.<br>칭찬받으면: {Z("谢谢！我还在学习。")}</p>') + "</div>"
 + box("⑤ 我也觉得… · 我们可以一起…", f'<p>{Z("我也觉得这里很好。")} 저도 여기가 좋다고 생각해요.<br>{Z("我们可以一起学习中文。")} 우리 같이 중국어 공부하면 되겠네요.</p>', "g")
 + h("단어", "대화 1·2 핵심 단어") + words(0, 1)
 + h("연습 A", "알맞은 말을 골라 넣으세요. (吗 · 什么 · 的 · 是)")
 + ol([f'你是日本人 {BS}？', f'你叫 {BS} 名字？', f'你 {BS} 中文很好！', f'我 {BS} 美国人。'])
 + h("연습 B", "중국어로 옮겨 보세요.")
 + ol([f'저는 ○○라고 해요. (내 이름으로) → {B}', f'중국 사람이에요? → {B}', f'저는 한국 사람이에요. → {B}', f'중국어 정말 잘하시네요! → {B}'])
 + h("말하기", "영상 속 사람에게 나에 대해 대답해 보세요")
 + say(("小红", "你叫什么名字？", "이름이 뭐예요?"), ("汤姆", "你是日本人吗？", "일본 사람이에요?"))
 + "</section>")

# ---------- LESSON 2 ----------
P.append(lesson(2, 2, "입사 면접 · 언어 교환 모임", [
    "<b>你是哪国人？</b>으로 국적을 물을 수 있다.",
    "<b>你做什么工作？ 你在哪儿工作？</b>로 직업과 일하는 곳을 물을 수 있다.",
    "<b>会</b>(할 줄 안다)와 <b>可以</b>(해도 된다)를 구분해 쓸 수 있다."])
 + h("문법", "哪 · 在 + 장소 · 会와 可以")
 + '<div class="two">' + box("① 哪 + 国 + 人？ = 어느 나라 사람?", f'<p>{Z("你是哪国人？")} 어느 나라 사람이에요?<br>→ {Z("我是韩国人。")} 한국 사람이에요.</p><p class="sm">哪 nǎ 어느 ↔ 那 nà 그것 — 성조가 달라요!</p>')
 + box("② 在 + 장소 + 동사 = ~에서 …하다", f'<p>{Z("你在哪儿工作？")} 어디에서 일해요?<br>→ {Z("我在北京工作。")} 베이징에서 일해요.</p><p class="sm">1주차 {Z("我在学习")}(지금 ~하는 중)와 달리 在 뒤에 <b>장소</b>가 와요.</p>') + "</div>"
 + '<div class="two">' + box("③ 会 = (배워서) 할 줄 안다", f'<p>{Z("你会说英文吗？")} 영어 할 줄 알아요?<br>→ {Z("会，我会说英文。")} / {Z("不会。")} / {Z("会一点儿。")}</p>')
 + box("④ 可以 = ~해도 된다 · ~할 수 있다", f'<p>{Z("我可以坐这儿吗？")} 여기 앉아도 돼요?<br>→ {Z("当然可以！请坐。")} 물론이죠! 앉으세요.<br>{Z("我可以教你。")} 제가 가르쳐 드릴 수 있어요.</p>') + "</div>"
 + box("⑤ 동사 + 得 + 很好 = ~를 잘하다", f'<p>{Z("说得很好！")} 말을 잘하네요! · {Z("你做什么工作？")} 무슨 일 하세요? (做 = 하다)</p>', "g")
 + h("단어", "대화 3·4 핵심 단어") + words(2, 3)
 + h("연습 A", "会 또는 可以를 넣으세요.")
 + ol([f'你 {BS} 说英文吗？ (영어 할 줄 알아요?)', f'我 {BS} 坐这儿吗？ (여기 앉아도 돼요?)', f'我不 {BS} 说韩语。 (한국어 할 줄 몰라요.)', f'我 {BS} 教你。 (제가 가르쳐 드릴게요.)'])
 + h("연습 B", "( ) 안의 내용으로 대답해 보세요.")
 + ol([f'你是哪国人？ (한국) → {B}', f'你做什么工作？ (선생님) → {B}', f'你在哪儿工作？ (서울 首尔) → {B}', f'你会说中文吗？ (조금) → {B}'])
 + h("말하기", "면접관의 질문에 내 이야기로 대답해 보세요")
 + say(("면접관", "你是哪国人？", "어느 나라 사람이에요?"), ("면접관", "你做什么工作？", "무슨 일 하세요?"))
 + "</section>")

# ---------- LESSON 3 ----------
P.append(lesson(3, 4, "룸메이트 첫 만남 · 회사 신입 연수", [
    "<b>你从哪儿来？ 我从…来。</b>로 어디서 왔는지 말할 수 있다.",
    "<b>以前</b>과 <b>现在</b>로 예전과 지금의 일을 말할 수 있다.",
    "<b>大家好！</b>로 여러 사람 앞에서 인사하고 <b>…吧</b>로 제안할 수 있다."])
 + h("문법", "从…来 · 以前/现在 · 吧")
 + '<div class="two">' + box("① 从 + 장소 + 来 = ~에서 왔다", f'<p>{Z("你从哪儿来？")} 어디에서 왔어요?<br>→ {Z("我从加拿大来。")} 캐나다에서 왔어요.<br>→ {Z("我从韩国来。")} 한국에서 왔어요.</p>')
 + box("② 以前 ↔ 现在", f'<p>{Z("你以前做什么工作？")} 전에는 무슨 일 했어요?<br>{Z("我以前是医生。")} 전에는 의사였어요.<br>{Z("现在我想换工作。")} 지금은 일을 바꾸고 싶어요.</p><p class="sm">중국어는 동사 모양이 안 바뀌어요. 以前·现在 같은 <b>시간 낱말</b>로 때를 나타내요.</p>') + "</div>"
 + '<div class="two">' + box("③ 大家好！ = 여러분 안녕하세요!", f'<p>여러 사람 앞에서 자기소개를 시작할 때:<br>{Z("大家好！我叫陈丽。")}</p><p class="sm">1주차 공식 "사람 + 好" 그대로예요. (老师好 · 大家好)</p>')
 + box("④ 문장 끝 吧 = ~하자 (제안)", f'<p>{Z("我们一起工作吧。")} 우리 같이 일해요.<br>{Z("我们可以互相帮助。")} 우리 서로 도울 수 있겠네요.<br>→ {Z("好主意！")} 좋은 생각이에요!</p>') + "</div>"
 + box("⑤ 我学中文 · 我学英文 — 学 + 언어", f'<p>{Z("我学中文。")} 저는 중국어를 배워요. · {Z("加拿大很远啊！")} 캐나다는 정말 멀네요! (문장 끝 啊 = 감탄)</p>', "g")
 + h("단어", "대화 5·6 핵심 단어") + words(4, 5)
 + h("연습 A", "알맞은 말을 넣으세요. (从 · 以前 · 现在 · 吧)")
 + ol([f'你 {BS} 哪儿来？', f'我 {BS} 是医生。 (전에는 의사였어요.)', f'{BS} 我想换工作。 (지금은 일을 바꾸고 싶어요.)', f'我们一起工作 {BS}。'])
 + h("연습 B", "상황에 맞는 말을 고르세요.")
 + '<table class="t match"><tr><td>① 여러 사람 앞에서 인사할 때</td><td>ⓐ 很远啊！</td></tr><tr><td>② 상대의 제안이 마음에 들 때</td><td>ⓑ 大家好！</td></tr><tr><td>③ 새 룸메이트의 고향을 물을 때</td><td>ⓒ 好主意！</td></tr><tr><td>④ 상대가 아주 먼 나라에서 왔을 때</td><td>ⓓ 你从哪儿来？</td></tr></table>'
 + h("말하기", "새 룸메이트·동료에게 대답해 보세요")
 + say(("张伟", "你从哪儿来？", "어디에서 왔어?"), ("刘强", "你以前做什么工作？", "전에는 무슨 일 했어요?"))
 + "</section>")

# ---------- LESSON 4 ----------
P.append(lesson(4, 6, "동네 주민센터 · 헬스장에서", [
    "<b>多久了？</b>로 얼마나 됐는지 묻고 <b>동사 + 了 + 기간</b>으로 대답할 수 있다.",
    "<b>每天 · 一周三次</b>로 얼마나 자주 하는지 말할 수 있다.",
    "<b>我在银行工作</b>처럼 일하는 곳을 말할 수 있다."])
 + h("문법", "기간 · 횟수 말하기")
 + '<div class="two">' + box("① …多久了？ = ~한 지 얼마나 됐어요?", f'<p>{Z("你来中国多久了？")} 중국에 온 지 얼마나 됐어요?<br>{Z("你住在这儿多久了？")} 여기 산 지 얼마나 됐어요?</p><p class="sm">多久 duō jiǔ = 얼마나 오래</p>')
 + box("② 동사 + 了 + 기간 (+ 了)", f'<p>{Z("我来了三个月。")} 온 지 석 달 됐어요.<br>{Z("我学了两年。")} 2년 배웠어요.<br>{Z("我住了十年了。")} 10년째 살고 있어요. (끝의 了 = 지금도 계속)</p>') + "</div>"
 + '<div class="two">' + box("③ 얼마나 자주? 每天 · 一周 + 숫자 + 次", f'<p>{Z("你每天来健身房吗？")} 헬스장에 매일 와요?<br>→ {Z("不是每天，一周三次。")} 매일은 아니고, 일주일에 세 번이요.<br>{Z("我一周锻炼两次。")} 저는 일주일에 두 번 운동해요.</p>')
 + box("④ 二 èr 과 两 liǎng", f'<p>숫자 2를 셀 때는 二, <b>개수·기간 앞</b>에서는 两.<br>{Z("两年 · 两次 · 两个月")} ↔ {Z("二月 · 第二 · 十二")}</p>') + "</div>"
 + box("⑤ 来 + 동사 = ~하러 오다 · 有什么需要帮忙的，找我", f'<p>{Z("你也来锻炼吗？")} 당신도 운동하러 왔어요? · {Z("有什么需要帮忙的，找我。")} 도움이 필요하면 저를 찾아요.</p>', "g")
 + h("단어", "대화 7·8 핵심 단어") + words(6, 7)
 + h("연습 A", "( ) 안의 내용으로 대답해 보세요.")
 + ol([f'你学中文多久了？ (석 달) → {B}', f'你住在这儿多久了？ (5년째) → {B}', f'你每天来健身房吗？ (일주일에 두 번) → {B}', f'你在哪儿工作？ (은행) → {B}'])
 + h("연습 B", "낱말을 순서대로 배열하세요.")
 + ol([f'{Z("了 / 我 / 十年 / 住 / 了")} → {B}', f'{Z("三次 / 一周 / 我 / 来")} → {B}'])
 + h("말하기", "새 이웃과 헬스장 친구에게 대답해 보세요")
 + say(("王芳", "你住在这儿多久了？", "여기 산 지 얼마나 됐어요?"), ("安娜", "你学中文多久了？", "중국어 배운 지 얼마나 됐어요?"))
 + "</section>")

# ---------- LESSON 5 ----------
P.append(lesson(5, 8, "학교 행사의 학부모 · 사진 동호회", [
    "<b>几</b>로 작은 숫자를 묻고 <b>你的呢？</b>로 되물을 수 있다.",
    "<b>可能</b>으로 짐작을 말할 수 있다.",
    "<b>这是我的爱好</b>로 취미를 말하고 나만의 자기소개를 완성할 수 있다."])
 + h("문법", "几 · 你的呢 · 可能 · 爱好")
 + '<div class="two">' + box("① 几 + 양사·명사 = 몇 ~?", f'<p>{Z("你的孩子在几年级？")} 아이가 몇 학년이에요?<br>→ {Z("在三年级。")} 3학년이에요.<br>{Z("一周几次？")} 일주일에 몇 번?</p><p class="sm">几는 대개 10보다 작은 수를 물을 때 써요.</p>')
 + box("② 你的呢？ = 당신의 것은요?", f'<p>{Z("在三年级。你的呢？")} 3학년이에요. 댁의 (아이)는요?</p><p class="sm">앞에 나온 명사(孩子)는 빼고 的만 남겨요. {Z("我的孩子也在三年级。")}</p>') + "</div>"
 + '<div class="two">' + box("③ 可能 = 아마 ~일 거예요", f'<p>{Z("真巧！他们可能是同学。")} 이런 우연이! 아이들이 같은 반일지도 몰라요.</p>')
 + box("④ 취미 말하기", f'<p>{Z("你喜欢摄影吗？")} 사진 찍는 거 좋아해요?<br>→ {Z("非常喜欢！这是我的爱好。")} 정말 좋아해요! 제 취미예요.<br>{Z("我的爱好是摄影。")} 제 취미는 사진이에요.</p>') + "</div>"
 + box("⑤ 有很多 + 명사 · 一些 + 명사", f'<p>{Z("我们有很多共同点。")} 우리는 공통점이 많아요. · {Z("我可以教你一些技巧。")} 요령을 좀 가르쳐 드릴게요.</p>', "g")
 + h("단어", "대화 9·10 핵심 단어") + words(8, 9)
 + h("연습 A", "알맞은 말을 넣으세요. (几 · 的 · 可能 · 喜欢)")
 + ol([f'你的孩子在 {BS} 年级？', f'我的孩子在三年级。你 {BS} 呢？', f'他们 {BS} 是同学。', f'你 {BS} 摄影吗？'])
 + h("연습 B", "중국어로 옮겨 보세요.")
 + ol([f'저는 간호사예요. → {B}', f'이건 제 취미예요. → {B}', f'우리 공통점이 많네요. → {B}'])
 + h("최종 미션", "나만의 자기소개 만들기 (모임에서 발표해요!)")
 + f'''<table class="t mine"><tr><th>순서</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>① 인사</td><td>{Z("大家好！ / 你好！")}</td><td></td></tr>
<tr><td>② 이름</td><td>{Z("我叫…。")}</td><td></td></tr>
<tr><td>③ 나라</td><td>{Z("我是韩国人。我从…来。")}</td><td></td></tr>
<tr><td>④ 직업·일하는 곳</td><td>{Z("我是…。我在…工作。")}</td><td></td></tr>
<tr><td>⑤ 할 줄 아는 말</td><td>{Z("我会说…。我学中文学了…。")}</td><td></td></tr>
<tr><td>⑥ 취미</td><td>{Z("我喜欢…。这是我的爱好。")}</td><td></td></tr>
<tr><td>⑦ 마무리</td><td>{Z("很高兴认识大家！")}</td><td></td></tr></table>'''
 + box("예시", f'<p>{Z("大家好！我叫金民浩。我是韩国人，我从首尔来。我是工程师，我在银行工作。我会说英文，我学中文学了三个月。我喜欢摄影，这是我的爱好。很高兴认识大家！")}</p><p class="sm">金民浩 Jīn Mínhào 김민호 · 学中文学了三个月 = 중국어를 석 달 배웠어요 · 很高兴认识大家 = 여러분을 만나서 반가워요</p>')
 + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>이름을 말하고 상대 이름을 물을 수 있다. (我叫… · 你叫什么名字？)</li><li>국적을 묻고 대답할 수 있다. (你是哪国人？ · 我是韩国人)</li><li>직업과 일하는 곳을 말할 수 있다. (我是… · 我在…工作)</li><li>会와 可以를 구분해 쓸 수 있다.</li><li>얼마나 됐는지·얼마나 자주 하는지 말할 수 있다. (多久了 · 一周三次)</li><li>7문장 자기소개를 중국어로 발표할 수 있다.</li></ul>'
 + "</section>")

# ---------- 부록 ----------
P.append(f'''<section class="lesson"><div class="hd"><div class="k">附录 A</div><h1>정답</h1></div><div class="ans-list">
<p><b>Lesson 1</b> A: 1 吗 · 2 什么 · 3 的 · 4 是 &nbsp;|&nbsp; B: 1 我叫○○。 · 2 你是中国人吗？ · 3 我是韩国人。 · 4 你的中文很好！</p>
<p><b>Lesson 2</b> A: 1 会 · 2 可以 · 3 会 · 4 可以 &nbsp;|&nbsp; B: 1 我是韩国人。 · 2 我是老师。 · 3 我在首尔工作。 · 4 会一点儿。</p>
<p><b>Lesson 3</b> A: 1 从 · 2 以前 · 3 现在 · 4 吧 &nbsp;|&nbsp; B: ①ⓑ ②ⓒ ③ⓓ ④ⓐ</p>
<p><b>Lesson 4</b> A: 1 我学了三个月。 · 2 我住了五年了。 · 3 不是每天，一周两次。 · 4 我在银行工作。 &nbsp;|&nbsp; B: 1 我住了十年了。 · 2 我一周来三次。</p>
<p><b>Lesson 5</b> A: 1 几 · 2 的 · 3 可能 · 4 喜欢 &nbsp;|&nbsp; B: 1 我是护士。 · 2 这是我的爱好。 · 3 我们有很多共同点。</p>
</div>
<div class="hd" style="margin-top:26px"><div class="k">附录 B</div><h1>자기소개 질문과 대답 총정리</h1></div>
<table class="t"><tr><th>묻는 것</th><th>질문</th><th>대답</th></tr>
<tr><td>이름</td><td>{Z("你叫什么名字？")}</td><td>{Z("我叫○○。")}</td></tr>
<tr><td>국적</td><td>{Z("你是哪国人？ / 你是中国人吗？")}</td><td>{Z("我是韩国人。")}</td></tr>
<tr><td>출신</td><td>{Z("你从哪儿来？")}</td><td>{Z("我从韩国来。")}</td></tr>
<tr><td>직업</td><td>{Z("你做什么工作？")}</td><td>{Z("我是老师。 / 我是学生。")}</td></tr>
<tr><td>일하는 곳</td><td>{Z("你在哪儿工作？")}</td><td>{Z("我在北京工作。")}</td></tr>
<tr><td>언어</td><td>{Z("你会说英文吗？")}</td><td>{Z("会。 / 会一点儿。 / 不会。")}</td></tr>
<tr><td>기간</td><td>{Z("你来中国多久了？")}</td><td>{Z("我来了三个月。")}</td></tr>
<tr><td>횟수</td><td>{Z("你每天来吗？")}</td><td>{Z("不是每天，一周三次。")}</td></tr>
<tr><td>취미</td><td>{Z("你喜欢摄影吗？")}</td><td>{Z("非常喜欢！这是我的爱好。")}</td></tr></table>
</section>''')

voc = ['<section class="lesson"><div class="hd"><div class="k">附录 C</div><h1>단어장</h1><div class="s">사이트의 \'단어장\'과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="3">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span>{zh(z)}</td><td class="wp">{e(py)}</td><td>{e(ko)}</td></tr>' for z, py, ko in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))


CSS = open(f"{work}/../book.css", encoding="utf-8").read() + open(f"{work}/../book_zh.css", encoding="utf-8").read()
CSS += ".lesson .dlg .dl{padding:2px 0}"  # 이번 주는 대화가 14줄씩이라 조금 촘촘하게
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>중국어 자기소개 교재 2주차</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
