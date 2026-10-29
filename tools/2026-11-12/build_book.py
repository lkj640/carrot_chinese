"""3주차 짧은 생활 대화 ① 교재(workbook.html) 만들기 → Chrome으로 PDF 출력.
python3 tools/2026-11-12/build_book.py tools/2026-11-12 meetings/2026-11-12/workbook.html
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
def dend(i): return D[i + 1]["lines"][0][1] if i + 1 < len(D) else 14 * 60 + 16

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
<div class="ct"><h1>왕초보 중국어<br>생활 대화 교재 ①</h1>
<div class="cs">Learn Chinese with Pipo · HSK 1~2 대화 3주차 · 14:16</div>
<div class="big" lang="zh-CN">请问你贵姓？</div>
<table class="toc">
<tr><th>시작</th><td>1·2주차 복습 · 이름 묻는 세 가지 방법 · 숫자 1~99</td></tr>
<tr><th>LESSON 1</th><td>새 반 친구 · 카페에서 (认识你很高兴 · 很 + 형용사 · 也)</td></tr>
<tr><th>LESSON 2</th><td>첫 출근 · 공원에서 (贵姓 · 姓과 叫 · 可以…吗 · 常)</td></tr>
<tr><th>LESSON 3</th><td>학교 등록처 · 도서관 (多大了 · 岁 · …对吗 · 在 + 동사 · 有人)</td></tr>
<tr><th>LESSON 4</th><td>생일 파티 · 새 이웃 (好像 · 谁的 · 都 · 是…的 · 一个人)</td></tr>
<tr><th>LESSON 5</th><td>언어 교환 · 버스 정류장 (来 + 동사 · 去 + 장소 + 동사 · 了 · 吧)</td></tr>
<tr><th>부록</th><td>정답 · 처음 만났을 때 쓰는 말 총정리 · 단어장</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_chinese → 11월 12일 모임 (문장을 누르면 그 부분부터 재생 · 병음과 한국어 번역 보기)<br>
각 레슨 구성: 오늘의 목표 → 영상 속 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기</div></div>
<div class="stripe"></div></section>''')

# ---------- 시작 ----------
P.append('<section class="lesson"><div class="hd"><div class="k">开始 · 시작</div><h1>시작하기 전에: 처음 만난 사람과 이야기하기</h1></div>'
 + box("이번 주는 이런 영상이에요", "<p>1주차(인사)와 2주차(자기소개)에서 배운 표현이 <b>10가지 생활 장면</b>에 다시 나와요. 새로운 건 <b>성 묻기(贵姓)·나이 묻기(多大了)·자리 묻기(有人吗)</b> 정도라 복습하기 딱 좋아요. 사이트의 '듣기'에서 <b>'현재 문장 반복'</b>으로 따라 말해 보세요.</p>", "g")
 + h("복습", "1·2주차에서 배운 말, 이번 영상에도 나와요") + f'''
<table class="t"><tr><th>표현</th><th>뜻</th><th>이번 영상 속 장면</th></tr>
<tr><td>{Z("你叫什么名字？ · 我叫…")}</td><td>이름이 뭐예요? · 저는 …예요</td><td>거의 모든 대화</td></tr>
<tr><td>{Z("你是中国人吗？")}</td><td>중국 사람이에요?</td><td>대화 2 카페</td></tr>
<tr><td>{Z("你是新搬来的吗？")}</td><td>새로 이사 왔어요?</td><td>대화 8 이웃 (1주차 대화 2와 같아요!)</td></tr>
<tr><td>{Z("会一点儿 · 我们可以一起学习")}</td><td>조금 해요 · 같이 공부하면 되겠네요</td><td>대화 6 도서관 · 대화 9 언어 교환</td></tr>
<tr><td>{Z("有什么需要帮忙的，可以找我")}</td><td>도움이 필요하면 저를 찾아요</td><td>대화 8 이웃</td></tr></table>
''' + h("이름 묻기", "상대와 상황에 따라 세 가지")
 + '<div class="two">' + box("친구·또래에게", f'<p>{Z("你叫什么名字？")}<br>{Z("你叫什么？")} (더 짧게)<br>→ {Z("我叫王明。")}</p>')
 + box("처음 보는 어른·직장에서", f'<p>{Z("请问你贵姓？ / 您贵姓？")}<br>→ {Z("我姓刘。")} 류씨예요.</p><p class="sm">贵 = 귀하다. 성만 물어요. 대답에는 贵를 안 써요! ✗ 我贵姓刘</p>')
 + box("공손하게 말 걸기", f'<p>{Z("请问，你叫什么名字？")}<br>{Z("我可以问一下吗？")} 뭐 좀 물어봐도 돼요?</p>') + "</div>"
 + h("숫자", "1~99 세기 (나이 말하기 준비)") + f'''
<table class="t"><tr><th>1~10</th><td>{Z("一 二 三 四 五 六 七 八 九 十")}<br><span class="sm">yī èr sān sì wǔ liù qī bā jiǔ shí</span></td></tr>
<tr><th>11~19</th><td>十 + 숫자: {Z("十一")} 11 · {Z("十九")} 19</td></tr>
<tr><th>20~99</th><td>숫자 + 十 + 숫자: {Z("二十")} 20 · {Z("二十五")} 25 · {Z("九十九")} 99</td></tr></table>
'''
 + h("10가지 장면", "이번 영상에 나오는 대화")
 + '<table class="t scenes">' + "".join(
     f'<tr><td>대화 {i+1}</td><td>{fmt(dstart(i))}</td><td>{zh(D[i]["lines"][0][2])}</td><td>{e(D[i]["lines"][0][4])}</td></tr>' for i in range(10)) + "</table>"
 + "</section>")

# ---------- LESSON 1 ----------
P.append(lesson(1, 0, "새 반 친구 · 카페에서", [
    "<b>认识你很高兴</b>과 <b>很高兴认识你</b>로 반가움을 말할 수 있다.",
    "<b>你的名字很好听！</b>처럼 '很 + 형용사'로 칭찬할 수 있다.",
    "<b>我也是…</b>로 '나도 그래요'라고 말할 수 있다."])
 + h("문법", "반가워요 두 가지 · 很 + 형용사 · 也")
 + '<div class="two">' + box("① 반가워요 = 두 가지 모두 OK", f'<p>{Z("认识你很高兴。")} (너를 알게 되어 기뻐)<br>{Z("很高兴认识你。")} (기쁘다, 너를 알게 되어)</p><p class="sm">대답: {Z("我也很高兴。")} / {Z("我也是。")}</p>')
 + box("② 주어 + 很 + 형용사", f'<p>{Z("你的名字很好听。")} 이름이 예쁘네요.<br>{Z("你的名字很可爱。")} 이름이 귀엽네요.</p><p class="sm">형용사 앞에는 是를 쓰지 않아요. ✗ 名字是好听 · 很은 "아주"라는 뜻이 약해서 습관처럼 붙여요.</p>') + "</div>"
 + '<div class="two">' + box("③ 我也是 + 명사 = 저도 ~예요", f'<p>{Z("我也是中国人。")} 저도 중국 사람이에요.<br>짧게: {Z("我也是。")} 저도요.</p><p class="sm">也는 동사(是) 앞! ✗ 我是也</p>')
 + box("④ 新 + 명사 = 새 ~", f'<p>{Z("你是新学生吗？")} 새로 온 학생이야?<br>{Z("新同学 · 新朋友")} 새 반 친구 · 새 친구</p>') + "</div>"
 + box("⑤ 请问 = 공손하게 묻기 시작", f'<p>{Z("你好，请问你叫什么？")} 안녕하세요, 실례지만 이름이 뭐예요? · 대답할 때는 请问을 안 써요.</p>', "g")
 + h("단어", "대화 1·2 핵심 단어") + words(0, 1)
 + h("연습 A", "알맞은 말을 골라 넣으세요. (很 · 也 · 新 · 请问)")
 + ol([f'你的名字 {BS} 好听。', f'我 {BS} 是中国人。', f'你是 {BS} 学生吗？', f'你好，{BS} 你叫什么？'])
 + h("연습 B", "중국어로 옮겨 보세요.")
 + ol([f'만나서 반가워요. (두 가지로) → {B}', f'이름이 참 예쁘네요. → {B}', f'저도요. → {B}'])
 + h("말하기", "영상 속 사람에게 대답해 보세요")
 + say(("李美", "你叫什么名字？", "이름이 뭐야?"), ("张伟", "你是中国人吗？", "중국 사람이에요?"))
 + "</section>")

# ---------- LESSON 2 ----------
P.append(lesson(2, 2, "첫 출근 날 · 공원에서", [
    "<b>请问你贵姓？</b>으로 공손하게 성을 묻고 <b>我姓…</b>으로 대답할 수 있다.",
    "<b>姓</b>(성)과 <b>叫</b>(이름 전체)를 구분할 수 있다.",
    "<b>我可以…吗？</b>로 허락을 구하고 <b>常</b>으로 자주 하는 일을 말할 수 있다."])
 + h("문법", "贵姓 · 姓과 叫 · 可以…吗 · 常")
 + '<div class="two">' + box("① 姓 = 성 · 叫 = 이름 전체", f'<p>{Z("我姓周。")} 저는 저우씨예요.<br>{Z("我叫周杰。")} 저는 저우제예요.</p><p class="sm">중국 이름은 <b>성 + 이름</b>: 周 + 杰 · 刘 + 老师 = 류 선생님</p>')
 + box("② 请问你贵姓？ = 성함이?", f'<p>{Z("请问你贵姓？")} → {Z("我姓刘。")}<br>→ 되묻기: {Z("我姓刘。你呢？")}</p><p class="sm">대답할 때 ✗ 我贵姓刘 ✗ 我姓刘老师</p>') + "</div>"
 + '<div class="two">' + box("③ 我可以 + 동사 + 吗？ = ~해도 돼요?", f'<p>{Z("我可以问一下吗？")} 뭐 좀 물어봐도 돼요?<br>→ {Z("可以，请问。")} 그럼요, 물어보세요.</p><p class="sm">동사 + 一下 = 좀 ~하다 (가볍게): {Z("问一下 · 写一下")}</p>')
 + box("④ 常 + 동사 = 자주 ~하다", f'<p>{Z("你常来这里吗？")} 여기 자주 와요?<br>→ {Z("是的，我常来。")} 네, 자주 와요.</p>') + "</div>"
 + box("⑤ 이름 + 欢迎你！ · 谢谢 + 호칭", f'<p>{Z("周杰，欢迎你！")} 저우제 씨, 환영해요! · {Z("谢谢刘老师。")} 감사합니다, 류 선생님. · {Z("那很好。")} 그거 좋네요.</p>', "g")
 + h("단어", "대화 3·4 핵심 단어") + words(2, 3)
 + h("연습 A", "姓 또는 叫를 넣으세요.")
 + ol([f'请问你贵 {BS}？', f'我 {BS} 刘。', f'我 {BS} 周杰。', f'你 {BS} 什么名字？'])
 + h("연습 B", "( ) 안의 내용으로 대답해 보세요.")
 + ol([f'请问你贵姓？ (내 성으로) → {B}', f'我可以问一下吗？ (그럼요) → {B}', f'你常来这里吗？ (네, 자주 와요) → {B}'])
 + h("말하기", "새 회사 선배·공원에서 만난 사람에게 대답해 보세요")
 + say(("刘老师", "请问你贵姓？", "성함이 어떻게 되세요?"), ("林大明", "你常来这里吗？", "여기 자주 와요?"))
 + "</section>")

# ---------- LESSON 3 ----------
P.append(lesson(3, 4, "학교 등록처 · 도서관에서", [
    "<b>你多大了？</b>로 나이를 묻고 <b>我…岁</b>로 대답할 수 있다.",
    "<b>…，对吗？</b>로 확인하고 <b>对，没错</b>로 대답할 수 있다.",
    "<b>这里有人吗？</b>로 빈자리인지 묻고 <b>在 + 동사</b>로 지금 하는 일을 말할 수 있다."])
 + h("문법", "나이 · 확인 · 자리 · 지금 하는 일")
 + '<div class="two">' + box("① 你多大了？ = 몇 살이에요?", f'<p>{Z("你多大了？")} → {Z("我十九岁。")} 열아홉 살이에요.<br>{Z("我二十五岁。")} 스물다섯 살이에요.</p><p class="sm">나이를 말할 때는 是를 안 써도 돼요. 어린아이에게는 {Z("你几岁了？")}</p>')
 + box("② 문장 + ，对吗？ = ~맞죠?", f'<p>{Z("你姓赵，名字是小龙，对吗？")}<br>→ {Z("对，没错。")} 네, 맞아요.<br>→ {Z("不对。")} 아니요.</p>') + "</div>"
 + '<div class="two">' + box("③ 这里有人吗？ = 여기 자리 있어요?", f'<p>{Z("对不起，这里有人吗？")}<br>→ {Z("没有人，请坐。")} 비었어요. 앉으세요.<br>→ {Z("有人。")} 자리 있어요.</p><p class="sm">有의 부정은 没有 (✗ 不有)</p>')
 + box("④ 在 + 동사 = ~하고 있어요 (1주차 복습)", f'<p>{Z("你在看什么书？")} 무슨 책 읽고 있어요?<br>→ {Z("我在看中文书。")} 중국어 책 읽고 있어요.</p>') + "</div>"
 + box("⑤ 请 + 동사 + 一下 · 对了", f'<p>{Z("请写一下你的名字。")} 이름 좀 적어 주세요. · {Z("对了，我叫马强。")} 참, 저는 마창이에요. (화제를 바꿀 때)</p>', "g")
 + h("단어", "대화 5·6 핵심 단어") + words(4, 5)
 + h("연습 A", "( ) 안의 내용으로 대답해 보세요.")
 + ol([f'你多大了？ (스물두 살) → {B}', f'你姓王，对吗？ (네, 맞아요) → {B}', f'这里有人吗？ (비었어요. 앉으세요) → {B}', f'你在看什么书？ (중국어 책) → {B}'])
 + h("연습 B", "숫자를 중국어로 써 보세요.")
 + ol([f'15 → {BS}', f'30 → {BS}', f'48 → {BS}'])
 + h("말하기", "등록처 선생님과 도서관 옆자리 사람에게 대답해 보세요")
 + say(("선생님", "你多大了？", "몇 살이에요?"), ("马强", "你会说中文吗？", "중국어 할 줄 알아요?"))
 + "</section>")

# ---------- LESSON 4 ----------
P.append(lesson(4, 6, "생일 파티 · 새 이웃", [
    "<b>你是谁的朋友？</b>로 누구 친구인지 물을 수 있다.",
    "<b>好像</b>으로 '~인 것 같아요', <b>都</b>로 '모두'를 말할 수 있다.",
    "<b>你一个人住吗？</b>처럼 사는 모습을 묻고 대답할 수 있다."])
 + h("문법", "谁的 · 好像 · 都 · 是…的")
 + '<div class="two">' + box("① 谁 = 누구 · 谁的 = 누구의", f'<p>{Z("你是谁的朋友？")} 누구 친구예요?<br>→ {Z("我是小明的朋友。")} 샤오밍 친구예요.<br>{Z("我也是他的朋友。")} 저도 그의 친구예요.</p><p class="sm">谁는 shéi (shuí라고도 읽어요)</p>')
 + box("② 好像 = ~인 것 같다", f'<p>{Z("我们好像没见过。")} 우리 처음 보는 것 같네요.</p><p class="sm">동사 + 过 = ~한 적 있다 · 没 + 동사 + 过 = ~한 적 없다<br>{Z("见过 · 没见过")}</p>') + "</div>"
 + '<div class="two">' + box("③ 都 = 모두 (동사 앞)", f'<p>{Z("那我们都是朋友了。")} 그럼 우리 다 친구네요.<br>{Z("我们都是中国人。")} 우리는 모두 중국 사람이에요.</p><p class="sm">끝의 了 = 이제 그렇게 됐다 (변화)</p>')
 + box("④ 是…的 · 一个人", f'<p>{Z("我昨天搬来的。")} 어제 이사 왔어요. (언제 했는지 강조, 1주차 복습)<br>{Z("你一个人住吗？")} 혼자 살아요?<br>→ {Z("是的，我一个人住。")}</p>') + "</div>"
 + box("⑤ 很好记 · 很简单 · 这个名字很漂亮", f'<p>好 + 동사 = ~하기 쉽다: {Z("很好记的名字")} 외우기 쉬운 이름 · {Z("好听")} 듣기 좋다 · {Z("吴女士")} 우 여사님 (성 + 女士)</p>', "g")
 + h("단어", "대화 7·8 핵심 단어") + words(6, 7)
 + h("연습 A", "알맞은 말을 넣으세요. (谁 · 好像 · 都 · 一个人)")
 + ol([f'你是 {BS} 的朋友？', f'我们 {BS} 没见过。', f'我们 {BS} 是朋友了。', f'你 {BS} 住吗？'])
 + h("연습 B", "상황에 맞는 말을 고르세요.")
 + '<table class="t match"><tr><td>① 파티에서 처음 보는 사람에게</td><td>ⓐ 很好记的名字。</td></tr><tr><td>② 이름이 짧고 쉬울 때</td><td>ⓑ 有什么需要帮忙的，可以找我。</td></tr><tr><td>③ 새 이웃을 도와주고 싶을 때</td><td>ⓒ 我们好像没见过。</td></tr><tr><td>④ 둘 다 샤오밍 친구일 때</td><td>ⓓ 那我们都是朋友了。</td></tr></table>'
 + h("말하기", "파티와 새 동네에서 대답해 보세요")
 + say(("白雪", "你是谁的朋友？", "누구 친구예요?"), ("吴女士", "你一个人住吗？", "혼자 살아요?"))
 + "</section>")

# ---------- LESSON 5 ----------
P.append(lesson(5, 8, "언어 교환 모임 · 버스 정류장", [
    "<b>你是来学中文的吗？</b>처럼 '来 + 동사'로 무엇 하러 왔는지 물을 수 있다.",
    "<b>我去看朋友</b>처럼 '去 + (장소) + 동사'로 어디에 무엇 하러 가는지 말할 수 있다.",
    "<b>车来了 · 我们上车吧</b>로 상황을 알리고 제안할 수 있다."])
 + h("문법", "来·去 + 동사 · 了 · 吧")
 + '<div class="two">' + box("① 来 + 동사 = ~하러 오다", f'<p>{Z("你是来学中文的吗？")} 중국어 배우러 왔어요?<br>→ {Z("是的。")}</p><p class="sm">2주차 {Z("你也来锻炼吗？")} 운동하러 왔어요? 와 같은 모양</p>')
 + box("② 去 + 장소 / 去 + 동사", f'<p>{Z("你也去医院吗？")} 당신도 병원 가요?<br>{Z("我去看朋友。")} 친구 보러 가요.<br>{Z("这里是去医院的车站吗？")} 여기가 병원 가는 정류장이에요?</p>') + "</div>"
 + '<div class="two">' + box("③ 문장 끝 了 = 지금 그렇게 됐다", f'<p>{Z("车来了。")} 차가 왔어요.<br>{Z("那我们都是朋友了。")} 그럼 우리 이제 친구네요.</p>')
 + box("④ 吧 = ~하자 (제안)", f'<p>{Z("我们上车吧。")} 우리 타요.<br>{Z("我们一起学习吧。")} 같이 공부해요.</p>') + "</div>"
 + box("⑤ 외국 이름 → 중국어 이름", f'<p>{Z("我叫Anna。我的中文名字叫安娜。")} 저는 Anna예요. 중국어 이름은 안나예요. · 맞장구: {Z("这样啊。")} 그렇군요.</p>', "g")
 + h("단어", "대화 9·10 핵심 단어") + words(8, 9)
 + h("연습 A", "来 또는 去를 넣으세요.")
 + ol([f'你是 {BS} 学中文的吗？ (배우러 왔어요?)', f'我 {BS} 看朋友。 (친구 보러 가요.)', f'车 {BS} 了。 (차가 왔어요.)', f'你也 {BS} 医院吗？ (병원 가요?)'])
 + h("연습 B", "중국어로 옮겨 보세요.")
 + ol([f'우리 타요. → {B}', f'제 중국어 이름은 ○○예요. → {B}'])
 + h("최종 미션", "짝과 함께 '처음 만난 사람' 대화 만들기")
 + f'''<table class="t mine"><tr><th>순서</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>① 말 걸기</td><td>{Z("你好！请问… / 我可以问一下吗？")}</td><td></td></tr>
<tr><td>② 이름·성</td><td>{Z("你叫什么名字？ / 请问你贵姓？")}</td><td></td></tr>
<tr><td>③ 칭찬</td><td>{Z("你的名字很好听！")}</td><td></td></tr>
<tr><td>④ 나이·하는 일</td><td>{Z("你多大了？ / 你在看什么书？")}</td><td></td></tr>
<tr><td>⑤ 어디 가요?</td><td>{Z("你也去…吗？ 我去…。")}</td><td></td></tr>
<tr><td>⑥ 마무리</td><td>{Z("认识你很高兴！ 我们一起…吧。")}</td><td></td></tr></table>'''
 + box("예시", f'<p>{Z("A: 你好！请问你叫什么名字？ B: 我叫金民浩。你呢？ A: 我姓王，叫王丽。 B: 王丽，你的名字很好听！ A: 谢谢！你也去医院吗？ B: 是的，我去看朋友。 A: 这样啊。车来了！ B: 我们上车吧。认识你很高兴！")}</p>')
 + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>你叫什么名字와 请问你贵姓을 상황에 맞게 쓸 수 있다.</li><li>姓과 叫를 구분해서 대답할 수 있다.</li><li>나이를 묻고 1~99로 대답할 수 있다.</li><li>这里有人吗？로 빈자리를 물을 수 있다.</li><li>谁的朋友 · 好像 · 都를 쓸 수 있다.</li><li>来/去 + 동사로 무엇 하러 왔는지·가는지 말할 수 있다.</li></ul>'
 + "</section>")

# ---------- 부록 ----------
P.append(f'''<section class="lesson"><div class="hd"><div class="k">附录 A</div><h1>정답</h1></div><div class="ans-list">
<p><b>Lesson 1</b> A: 1 很 · 2 也 · 3 新 · 4 请问 &nbsp;|&nbsp; B: 1 认识你很高兴。/ 很高兴认识你。 · 2 你的名字很好听。 · 3 我也是。</p>
<p><b>Lesson 2</b> A: 1 姓 · 2 姓 · 3 叫 · 4 叫 &nbsp;|&nbsp; B: 1 我姓○。 · 2 可以，请问。 · 3 是的，我常来。</p>
<p><b>Lesson 3</b> A: 1 我二十二岁。 · 2 对，没错。 · 3 没有人，请坐。 · 4 我在看中文书。 &nbsp;|&nbsp; B: 1 十五 · 2 三十 · 3 四十八</p>
<p><b>Lesson 4</b> A: 1 谁 · 2 好像 · 3 都 · 4 一个人 &nbsp;|&nbsp; B: ①ⓒ ②ⓐ ③ⓑ ④ⓓ</p>
<p><b>Lesson 5</b> A: 1 来 · 2 去 · 3 来 · 4 去 &nbsp;|&nbsp; B: 1 我们上车吧。 · 2 我的中文名字叫○○。</p>
</div>
<div class="hd" style="margin-top:26px"><div class="k">附录 B</div><h1>처음 만났을 때 쓰는 말 총정리</h1></div>
<table class="t"><tr><th>하고 싶은 말</th><th>질문 · 말 걸기</th><th>대답</th></tr>
<tr><td>말 걸기</td><td>{Z("请问… / 我可以问一下吗？")}</td><td>{Z("可以，请问。")}</td></tr>
<tr><td>이름</td><td>{Z("你叫什么名字？")}</td><td>{Z("我叫○○。你呢？")}</td></tr>
<tr><td>성 (공손)</td><td>{Z("请问你贵姓？")}</td><td>{Z("我姓○。")}</td></tr>
<tr><td>나이</td><td>{Z("你多大了？")}</td><td>{Z("我十九岁。")}</td></tr>
<tr><td>확인</td><td>{Z("…，对吗？")}</td><td>{Z("对，没错。 / 不对。")}</td></tr>
<tr><td>빈자리</td><td>{Z("这里有人吗？")}</td><td>{Z("没有人，请坐。")}</td></tr>
<tr><td>누구 친구?</td><td>{Z("你是谁的朋友？")}</td><td>{Z("我是小明的朋友。")}</td></tr>
<tr><td>칭찬</td><td>{Z("你的名字很好听 / 很可爱 / 很漂亮！")}</td><td>{Z("谢谢你。")}</td></tr>
<tr><td>반가워요</td><td>{Z("认识你很高兴！")}</td><td>{Z("我也很高兴。 / 我也是。")}</td></tr></table>
</section>''')

voc = ['<section class="lesson"><div class="hd"><div class="k">附录 C</div><h1>단어장</h1><div class="s">사이트의 \'단어장\'과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="2">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span>{zp(z, py)}</td><td>{e(ko)}</td></tr>' for z, py, ko in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))


CSS = open(f"{work}/../book.css", encoding="utf-8").read() + open(f"{work}/../book_zh.css", encoding="utf-8").read()
CSS += ".lesson .dlg .dl{padding:2px 0}"  # 대화가 길어서 조금 촘촘하게
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>중국어 생활 대화 교재 3주차</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
