"""4주차 짧은 생활 대화 ②(나이·생일) 교재(workbook.html) 만들기 → Chrome으로 PDF 출력.
python3 tools/2026-11-19/build_book.py tools/2026-11-19 meetings/2026-11-19/workbook.html
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
def dend(i): return D[i + 1]["lines"][0][1] if i + 1 < len(D) else 15 * 60 + 24

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
<div class="ct"><h1>왕초보 중국어<br>생활 대화 교재 ② · 나이와 생일</h1>
<div class="cs">Learn Chinese with Pipo · HSK 1~2 대화 4주차 · 15:24</div>
<div class="big" lang="zh-CN">你今年多大了？</div>
<table class="toc">
<tr><th>시작</th><td>상대에 따라 다른 나이 묻기 · 숫자 복습 · 월과 연도 읽기</td></tr>
<tr><th>LESSON 1</th><td>새 친구 · 사촌 동생 (多大了 · 一样大 · 比 · 几月)</td></tr>
<tr><th>LESSON 2</th><td>가족 모임 · 옛 이웃 할머니 (年纪·岁数 · 看起来 · 过得真快 · 还没有)</td></tr>
<tr><th>LESSON 3</th><td>입학 등록 · 형제자매 (几岁 · 有 · 比…大几岁 · 有点儿)</td></tr>
<tr><th>LESSON 4</th><td>생일 파티 · 면접 (生日快乐 · 什么时候 · 是…的 · 연도)</td></tr>
<tr><th>LESSON 5</th><td>아기 · 퇴직 이야기 (个月 · 会…了 · 快要…了 · 以后)</td></tr>
<tr><th>부록</th><td>정답 · 나이와 생일 표현 총정리 · 단어장</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_chinese → 11월 19일 모임 (문장을 누르면 그 부분부터 재생 · 병음과 한국어 번역 보기)<br>
각 레슨 구성: 오늘의 목표 → 영상 속 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기</div></div>
<div class="stripe"></div></section>''')

# ---------- 시작 ----------
P.append('<section class="lesson"><div class="hd"><div class="k">开始 · 시작</div><h1>시작하기 전에: 나이 묻기</h1></div>'
 + box("이번 주는 이런 영상이에요", "<p>10가지 장면이 모두 <b>나이와 생일</b> 이야기예요. 친구, 어린 동생, 삼촌, 할머니, 아기까지 <b>상대에 따라 나이 묻는 말이 달라져요.</b> 3주차에 배운 숫자 1~99를 실컷 써먹을 수 있어요!</p>", "g")
 + h("나이 묻기", "누구에게 묻나요?") + f'''
<table class="t"><tr><th>상대</th><th>질문</th><th>대답 예</th></tr>
<tr><td>어린아이 (10살 아래)</td><td>{Z("你几岁了？")}</td><td>{Z("我六岁了。")}</td></tr>
<tr><td>친구·또래·아랫사람</td><td>{Z("你今年多大了？")}</td><td>{Z("我今年十六岁。")}</td></tr>
<tr><td>어른 (삼촌·할머니)</td><td>{Z("您多大年纪了？ / 您多大岁数了？")}</td><td>{Z("我今年七十岁了。")}</td></tr>
<tr><td>아기</td><td>{Z("宝宝多大了？")}</td><td>{Z("她八个月了。")}</td></tr></table>
<p class="sm">※ 几는 10보다 작은 수를 짐작할 때, 多大는 그 밖의 나이에 써요. 어른께는 你 대신 您!</p>
''' + h("날짜 말하기", "월 · 연도 · 올해와 작년")
 + '<div class="two">' + box("월 = 숫자 + 月", f'<p>{Z("一月 二月 三月 … 十二月")}<br>{Z("你几月生日？")} → {Z("我三月生日。")}<br>{Z("九月份")} 9월 (份을 붙여도 같아요)</p>')
 + box("연도 = 숫자를 하나씩 + 年", f'<p>2001 → {Z("二零零一年")} èr líng líng yī nián<br>1998 → {Z("一九九八年")}<br>{Z("去年 · 今年 · 明年")} 작년 · 올해 · 내년<br>{Z("上个月 · 这个月 · 下个月")} 지난달 · 이번 달 · 다음 달</p>') + "</div>"
 + h("10가지 장면", "이번 영상에 나오는 대화")
 + '<table class="t scenes">' + "".join(
     f'<tr><td>대화 {i+1}</td><td>{fmt(dstart(i))}</td><td>{zh(D[i]["lines"][0][2])}</td><td>{e(D[i]["lines"][0][4])}</td></tr>' for i in range(10)) + "</table>"
 + "</section>")

# ---------- LESSON 1 ----------
P.append(lesson(1, 0, "학교에서 새 친구 · 어린 사촌 동생", [
    "<b>你今年多大了？</b>로 나이를 묻고 <b>我今年…岁</b>로 대답할 수 있다.",
    "<b>一样大</b>와 <b>比</b>로 나이를 비교할 수 있다.",
    "<b>你几月生日？</b>로 생일이 몇 월인지 물을 수 있다."])
 + h("문법", "多大了 · 一样大 · 比 · 几月")
 + '<div class="two">' + box("① 今年 + 多大了？", f'<p>{Z("你今年多大了？")} 올해 몇 살이야?<br>→ {Z("我今年十六岁。")} 올해 열여섯이야.<br>{Z("你现在多大了？")} 이제 몇 살이야?</p><p class="sm">끝의 了 = "이제 (벌써) ~살이 됐다"는 느낌</p>')
 + box("② 我们一样大 = 우리 동갑이야", f'<p>{Z("我也是十六岁。")} 나도 열여섯이야.<br>→ {Z("我们一样大。")} 우리 동갑이네.</p><p class="sm">一样 yíyàng = 같다 (一 + 4성 → yí)</p>') + "</div>"
 + '<div class="two">' + box("③ A 比 B + 大/小 (+ 얼마나)", f'<p>{Z("你比我小一点儿。")} 네가 나보다 조금 어리네.<br>{Z("你比我大很多。")} 누나가 나보다 훨씬 많네.<br>{Z("我大你十二岁。")} 내가 너보다 열두 살 많아.</p><p class="sm">比 문장에는 很을 안 써요. ✗ 你比我很大</p>')
 + box("④ 几月生日？ = 생일이 몇 월?", f'<p>{Z("你几月生日？")} → {Z("我三月生日。")}<br>{Z("你什么时候过生日？")} 생일이 언제야?<br>→ {Z("我下个月过生日。")} 다음 달이야.</p>') + "</div>"
 + box("⑤ 동사 + 得 + 真快 · 可以 + 동사 + 了", f'<p>{Z("你长得真快！")} 정말 빨리 컸네! · {Z("我可以吃蛋糕了！")} 케이크 먹을 수 있겠다!</p>', "g")
 + h("단어", "대화 1·2 핵심 단어") + words(0, 1)
 + h("연습 A", "알맞은 말을 골라 넣으세요. (多大 · 一样 · 比 · 几)")
 + ol([f'你今年 {BS} 了？', f'我们 {BS} 大。', f'你 {BS} 我小一点儿。', f'你 {BS} 月生日？'])
 + h("연습 B", "중국어로 옮겨 보세요.")
 + ol([f'저는 올해 ○살이에요. (내 나이로) → {B}', f'제 생일은 3월이에요. → {B}', f'누나가 나보다 훨씬 많네. → {B}'])
 + h("말하기", "영상 속 사람에게 내 이야기로 대답해 보세요")
 + say(("李红", "你今年多大了？", "올해 몇 살이야?"), ("王东", "你几月生日？", "생일이 몇 월이야?"))
 + "</section>")

# ---------- LESSON 2 ----------
P.append(lesson(2, 2, "가족 모임 · 옛 이웃 할머니", [
    "어른께 <b>您多大年纪了？ / 您多大岁数了？</b>로 공손하게 나이를 여쭐 수 있다.",
    "<b>您看起来很年轻 · 您身体真好</b>로 어른을 칭찬할 수 있다.",
    "<b>还没有 · 才</b>로 '아직 ~안 했어요'를 말할 수 있다."])
 + h("문법", "어른께 묻기 · 看起来 · 得 · 还没有")
 + '<div class="two">' + box("① 어른의 나이 = 年纪 · 岁数", f'<p>{Z("叔叔，您今年多大年纪了？")}<br>{Z("奶奶，您今年多大岁数了？")}<br>→ {Z("我今年七十岁了。")} 올해 일흔이란다.</p><p class="sm">어른께 ✗ 你几岁了? — 아이 대하듯 들려요!</p>')
 + box("② 看起来 + 형용사 = ~해 보인다", f'<p>{Z("您看起来很年轻。")} 젊어 보이세요.<br>{Z("您身体真好！")} 정말 정정하세요!<br>{Z("年轻真好啊！")} 젊어서 좋구나!</p>') + "</div>"
 + '<div class="two">' + box("③ 동사 + 得 + 정도", f'<p>{Z("时间过得真快。")} 시간이 정말 빨리 가네.<br>{Z("你长得真快！")} 정말 빨리 컸구나!</p><p class="sm">得 de는 "어떻게 ~하는지"를 뒤에서 설명해요.</p>')
 + box("④ 还没有 · 才", f'<p>{Z("你今年生日过了吗？")} 올해 생일 지났니?<br>→ {Z("还没有，下个月才过。")} 아직이요, 다음 달에야 돼요.</p><p class="sm">才 = (생각보다 늦게) ~에야</p>') + "</div>"
 + box("⑤ 去 + 장소 + 동사 두 번 · 提前祝你…", f'<p>{Z("我去公园走走。")} 공원에 좀 걸으러 가. (走走 = 가볍게 좀 걷다) · {Z("那提前祝你生日快乐！")} 그럼 미리 생일 축하해!</p>', "g")
 + h("단어", "대화 3·4 핵심 단어") + words(2, 3)
 + h("연습 A", "알맞은 말을 넣으세요. (看起来 · 得 · 还没有 · 才)")
 + ol([f'您 {BS} 很年轻。', f'时间过 {BS} 真快。', f'你生日过了吗？ — {BS}。', f'下个月 {BS} 过。'])
 + h("연습 B", "누구에게 하는 질문일까요? 짝을 지어 보세요.")
 + '<table class="t match"><tr><td>① 할머니께</td><td>ⓐ 宝宝多大了？</td></tr><tr><td>② 여섯 살 아이에게</td><td>ⓑ 你几岁了？</td></tr><tr><td>③ 같은 반 친구에게</td><td>ⓒ 您多大岁数了？</td></tr><tr><td>④ 아기 엄마에게</td><td>ⓓ 你今年多大了？</td></tr></table>'
 + h("말하기", "삼촌과 할머니께 대답해 보세요")
 + say(("叔叔", "你今年多大了？", "올해 몇 살 됐니?"), ("叔叔", "你今年生日过了吗？", "올해 생일 지났니?"))
 + "</section>")

# ---------- LESSON 3 ----------
P.append(lesson(3, 4, "아이 입학 등록 · 형제자매 나이 차이", [
    "<b>孩子多大了？ · 你几岁了？</b>로 아이 나이를 물을 수 있다.",
    "<b>你有兄弟姐妹吗？ 我有一个哥哥</b>로 가족을 말할 수 있다.",
    "<b>他比我大四岁 = 他大我四岁</b>로 나이 차이를 말할 수 있다."])
 + h("문법", "有 · 比 + 차이 · 有点儿")
 + '<div class="two">' + box("① 有 = 있다 · 没有 = 없다", f'<p>{Z("你有兄弟姐妹吗？")} 형제자매 있어요?<br>→ {Z("有，我有一个哥哥。")} 네, 오빠(형)가 한 명 있어요.<br>→ {Z("没有。")} 없어요.</p><p class="sm">사람 세기: 一个 yí ge · 两个 liǎng ge</p>')
 + box("② 나이 차이 = 比 + 大/小 + 숫자 + 岁", f'<p>{Z("他比你大几岁？")} 당신보다 몇 살 많아요?<br>→ {Z("他比我大四岁。")} = {Z("他大我四岁。")}<br>{Z("她比我小四岁。")} 저보다 네 살 어려요.</p>') + "</div>"
 + '<div class="two">' + box("③ 孩子多大了？ / 你几岁了？", f'<p>{Z("请问孩子多大了？")} 아이가 몇 살이에요?<br>{Z("小宝，你几岁了？")} 샤오바오, 몇 살이니?<br>→ {Z("他六岁了。")}</p>')
 + box("④ 有点儿 + 형용사 = 좀 ~하다", f'<p>{Z("他有点儿害羞。")} 애가 좀 수줍음을 타요.<br>→ {Z("没关系。")} 괜찮아요.</p><p class="sm">有点儿은 주로 아쉽거나 곤란한 느낌에 써요.</p>') + "</div>"
 + box("⑤ 给 + 사람 + 동사 · 都", f'<p>{Z("我想给孩子报名。")} 아이 등록을 하고 싶어요. · {Z("都是四岁。")} 둘 다 네 살 차이예요.</p>', "g")
 + h("단어", "대화 5·6 핵심 단어") + words(4, 5)
 + h("연습 A", "比를 써서 문장을 만들어 보세요.")
 + ol([f'哥哥 30살 · 나 26살 → {B}', f'妹妹 20살 · 나 24살 → {B}', f'나 22살 · 弟弟 10살 → {B}'])
 + h("연습 B", "내 가족 이야기로 대답해 보세요.")
 + ol([f'你有兄弟姐妹吗？ → {B}', f'他/她比你大几岁？ → {B}'])
 + h("말하기", "친구의 질문에 대답해 보세요")
 + say(("친구", "你有兄弟姐妹吗？", "형제자매 있어요?"), ("친구", "他比你大几岁？", "당신보다 몇 살 많아요?"))
 + "</section>")

# ---------- LESSON 4 ----------
P.append(lesson(4, 6, "생일 파티 · 면접에서", [
    "<b>生日快乐！</b>로 축하하고 <b>你什么时候生日？</b>로 생일을 물을 수 있다.",
    "<b>你是哪年出生的？ 我是…年出生的</b>로 태어난 해를 말할 수 있다.",
    "연도를 중국어로 읽을 수 있다."])
 + h("문법", "생일 · 是…的 · 연도")
 + '<div class="two">' + box("① 生日快乐！ = 생일 축하해!", f'<p>{Z("生日快乐！")} → {Z("谢谢！")}<br>{Z("你今天几岁了？")} 오늘로 몇 살이 됐어?<br>→ {Z("我今天二十一岁了。")}</p><p class="sm">了 = 이제 그렇게 됐다 (변화) · {Z("你可以喝酒了！")}</p>')
 + box("② 什么时候 = 언제", f'<p>{Z("你什么时候生日？")} 생일이 언제야?<br>→ {Z("我下个月过生日。")}<br>{Z("那我比你大一个月。")} 그럼 내가 한 달 형이네.</p>') + "</div>"
 + '<div class="two">' + box("③ 是 + 언제 + 동사 + 的", f'<p>{Z("你是哪年出生的？")} 몇 년생이에요?<br>→ {Z("我是二零零一年出生的。")} 2001년생이에요.<br>{Z("我去年毕业的。")} 작년에 졸업했어요. (是 생략 가능)</p><p class="sm">이미 일어난 일의 "언제"를 강조할 때 써요.</p>')
 + box("④ 연도는 숫자를 하나씩", f'<p>{Z("二零零一年")} 2001년<br>{Z("一九九五年")} 1995년<br>{Z("二零二六年")} 2026년</p><p class="sm">0은 零 líng</p>') + "</div>"
 + box("⑤ 毕业了吗？ — 毕业了 · 你是我的大哥！", f'<p>{Z("你大学毕业了吗？")} 대학 졸업했어요? → {Z("毕业了。")} 졸업했어요. · {Z("你是我的大哥！")} 네가 내 형님이다! (농담)</p>', "g")
 + h("단어", "대화 7·8 핵심 단어") + words(6, 7)
 + h("연습 A", "연도를 중국어로 써 보세요.")
 + ol([f'1998 → {BS}', f'2003 → {BS}', f'2026 → {BS}'])
 + h("연습 B", "是…的로 대답해 보세요.")
 + ol([f'你是哪年出生的？ (1995년) → {B}', f'你是什么时候毕业的？ (작년) → {B}'])
 + h("말하기", "면접관과 친구에게 대답해 보세요")
 + say(("면접관", "你是哪年出生的？", "몇 년생이에요?"), ("친구", "你什么时候过生日？", "생일이 언제야?"))
 + "</section>")

# ---------- LESSON 5 ----------
P.append(lesson(5, 8, "아기 나이 묻기 · 정년퇴직 이야기", [
    "<b>宝宝多大了？ 她八个月了</b>로 아기 나이(개월)를 말할 수 있다.",
    "<b>会…了 · 还不会</b>로 이제 할 수 있게 된 일을 말할 수 있다.",
    "<b>快要…了 · …以后</b>로 곧 일어날 일과 그 후의 계획을 말할 수 있다."])
 + h("문법", "个月 · 会…了 · 快要…了 · 以后")
 + '<div class="two">' + box("① 숫자 + 个月 = ~개월", f'<p>{Z("宝宝多大了？")} 아기가 몇 개월이에요?<br>→ {Z("她八个月了。")} 8개월 됐어요.</p><p class="sm">月 앞에 个가 있으면 기간(8개월), 없으면 달 이름(八月 8월)!</p>')
 + box("② 会 + 동사 + 了 = 이제 ~할 줄 알게 됐다", f'<p>{Z("她会走了吗？")} 이제 걸어요?<br>→ {Z("还不会，但是会爬了。")} 아직이요, 그래도 기어다녀요.</p>') + "</div>"
 + '<div class="two">' + box("③ 快要 + 동사 + 了 = 곧 ~하다", f'<p>{Z("你快要退休了吧？")} 곧 퇴직하겠네?<br>→ {Z("是的，还有两年。")} 응, 2년 남았어.<br>{Z("我快要过生日了。")} 곧 내 생일이야.</p>')
 + box("④ 동사 + 以后 = ~한 후에", f'<p>{Z("退休以后你想做什么？")} 퇴직하면 뭐 하고 싶어?<br>→ {Z("我想去旅游，看看中国。")} 여행하면서 중국 구경하고 싶어.</p><p class="sm">看看 = 좀 보다 (동사 두 번 → 가볍게)</p>') + "</div>"
 + box("⑤ 老 + 성 / 小 + 성", f'<p>{Z("老李")} 나이 지긋한 리 씨 · {Z("小张")} 젊은 장 군 — 친한 사이에서 성 앞에 붙여 불러요. · {Z("六十岁就可以退休了。")} 예순이면 퇴직할 수 있지.</p>', "g")
 + h("단어", "대화 9·10 핵심 단어") + words(8, 9)
 + h("연습 A", "알맞은 말을 넣으세요. (会 · 快要 · 以后 · 还有)")
 + ol([f'她 {BS} 爬了。', f'你 {BS} 退休了吧？', f'退休 {BS} 你想做什么？', f'{BS} 两年。'])
 + h("연습 B", "중국어로 옮겨 보세요.")
 + ol([f'곧 제 생일이에요. → {B}', f'졸업한 후에 여행하고 싶어요. → {B}'])
 + h("최종 미션", "짝 인터뷰: 나이와 생일")
 + f'''<table class="t mine"><tr><th>질문</th><th>패턴</th><th>짝의 대답</th></tr>
<tr><td>① 나이</td><td>{Z("你今年多大了？")}</td><td></td></tr>
<tr><td>② 생일</td><td>{Z("你几月生日？ / 你什么时候过生日？")}</td><td></td></tr>
<tr><td>③ 태어난 해</td><td>{Z("你是哪年出生的？")}</td><td></td></tr>
<tr><td>④ 형제자매</td><td>{Z("你有兄弟姐妹吗？")}</td><td></td></tr>
<tr><td>⑤ 나이 차이</td><td>{Z("他/她比你大几岁？")}</td><td></td></tr>
<tr><td>⑥ 앞으로</td><td>{Z("…以后你想做什么？")}</td><td></td></tr></table>'''
 + box("예시", f'<p>{Z("A: 你今年多大了？ B: 我今年三十岁。你呢？ A: 我也三十岁，我们一样大！ B: 你几月生日？ A: 我五月生日。 B: 那你比我小一点儿。我三月生日。 A: 你有兄弟姐妹吗？ B: 有，我有一个妹妹，她比我小两岁。")}</p>')
 + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>상대에 맞게 나이를 물을 수 있다. (几岁 · 多大 · 多大年纪/岁数)</li><li>比 · 一样大로 나이를 비교할 수 있다.</li><li>생일이 몇 월인지, 언제인지 묻고 답할 수 있다.</li><li>연도를 읽고 是…的로 태어난 해를 말할 수 있다.</li><li>会…了 · 快要…了 · 以后를 쓸 수 있다.</li><li>생일 축하 인사(生日快乐)를 할 수 있다.</li></ul>'
 + "</section>")

# ---------- 부록 ----------
P.append(f'''<section class="lesson"><div class="hd"><div class="k">附录 A</div><h1>정답</h1></div><div class="ans-list">
<p><b>Lesson 1</b> A: 1 多大 · 2 一样 · 3 比 · 4 几 &nbsp;|&nbsp; B: 1 我今年○岁。 · 2 我三月生日。 · 3 你比我大很多。</p>
<p><b>Lesson 2</b> A: 1 看起来 · 2 得 · 3 还没有 · 4 才 &nbsp;|&nbsp; B: ①ⓒ ②ⓑ ③ⓓ ④ⓐ</p>
<p><b>Lesson 3</b> A: 1 哥哥比我大四岁。 · 2 妹妹比我小四岁。 · 3 我比弟弟大十二岁。 &nbsp;|&nbsp; B: 예) 有，我有一个姐姐。 · 她比我大两岁。</p>
<p><b>Lesson 4</b> A: 1 一九九八年 · 2 二零零三年 · 3 二零二六年 &nbsp;|&nbsp; B: 1 我是一九九五年出生的。 · 2 我是去年毕业的。</p>
<p><b>Lesson 5</b> A: 1 会 · 2 快要 · 3 以后 · 4 还有 &nbsp;|&nbsp; B: 1 我快要过生日了。 · 2 毕业以后我想去旅游。</p>
</div>
<div class="hd" style="margin-top:26px"><div class="k">附录 B</div><h1>나이와 생일 표현 총정리</h1></div>
<table class="t"><tr><th>하고 싶은 말</th><th>질문</th><th>대답</th></tr>
<tr><td>나이 (또래)</td><td>{Z("你今年多大了？")}</td><td>{Z("我今年二十五岁。")}</td></tr>
<tr><td>나이 (아이)</td><td>{Z("你几岁了？")}</td><td>{Z("我六岁了。")}</td></tr>
<tr><td>나이 (어른)</td><td>{Z("您多大年纪了？ / 您多大岁数了？")}</td><td>{Z("我今年七十岁了。")}</td></tr>
<tr><td>나이 (아기)</td><td>{Z("宝宝多大了？")}</td><td>{Z("她八个月了。")}</td></tr>
<tr><td>비교</td><td>{Z("他比你大几岁？")}</td><td>{Z("他比我大四岁。 / 我们一样大。")}</td></tr>
<tr><td>생일</td><td>{Z("你几月生日？ / 你什么时候过生日？")}</td><td>{Z("我三月生日。 / 我下个月过生日。")}</td></tr>
<tr><td>태어난 해</td><td>{Z("你是哪年出生的？")}</td><td>{Z("我是二零零一年出生的。")}</td></tr>
<tr><td>축하</td><td>{Z("生日快乐！ / 提前祝你生日快乐！")}</td><td>{Z("谢谢！")}</td></tr>
<tr><td>칭찬 (어른께)</td><td>{Z("您看起来很年轻！ / 您身体真好！")}</td><td>{Z("谢谢。")}</td></tr></table>
</section>''')

voc = ['<section class="lesson"><div class="hd"><div class="k">附录 C</div><h1>단어장</h1><div class="s">사이트의 \'단어장\'과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="2">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span>{zp(z, py)}</td><td>{e(ko)}</td></tr>' for z, py, ko in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))


CSS = open(f"{work}/../book.css", encoding="utf-8").read() + open(f"{work}/../book_zh.css", encoding="utf-8").read()
CSS += ".lesson .dlg .dl{padding:2px 0}"  # 대화가 길어서 조금 촘촘하게
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>중국어 생활 대화 교재 4주차</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
