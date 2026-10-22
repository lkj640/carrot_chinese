"""1주차 인사하기 교재(workbook.html) 만들기 → Chrome으로 PDF 출력.
python3 tools/2026-10-29/build_book.py tools/2026-10-29 meetings/2026-10-29/workbook.html
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
def dend(i): return D[i + 1]["lines"][0][1] if i + 1 < len(D) else 15 * 60 + 8

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
    rows = []
    for k in (i, j):
        for s, t, z, py, ko in D[k]["lines"]:
            if s == "V":
                rows.append((z, py, ko))
    tr = "".join(f'<tr><td class="wz">{zh(z)}</td><td class="wp">{e(py)}</td><td>{e(ko)}</td></tr>' for z, py, ko in rows)
    return '<table class="t words"><tr><th>단어</th><th>병음</th><th>뜻</th></tr>' + tr + "</table>"

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

P = []
# ---------- 표지 ----------
P.append(f'''<section class="cover"><div class="stripe"></div>
<div class="ct"><h1>왕초보 중국어<br>인사하기 교재</h1>
<div class="cs">Learn Chinese with Pipo · HSK 1~2 대화 1주차 · 15:08</div>
<div class="big" lang="zh-CN">你好！早上好！</div>
<table class="toc">
<tr><th>시작</th><td>성조와 병음 · 성조가 바뀌는 글자 · 인사 공식</td></tr>
<tr><th>LESSON 1</th><td>아침 인사 · 새 이웃과 첫인사 (吗 · 呢 · 也 · 叫)</td></tr>
<tr><th>LESSON 2</th><td>오랜만의 인사 · 가족과 저녁 인사 (在 · 想 · 累不累)</td></tr>
<tr><th>LESSON 3</th><td>주말 인사 · 첫 출근 인사 (就 · 的 · 是…的)</td></tr>
<tr><th>LESSON 4</th><td>선생님·어른께 인사 (您 · 做完了 · 吧)</td></tr>
<tr><th>LESSON 5</th><td>우연히 만났을 때 · 밤에 헤어질 때 (该…了 · 给)</td></tr>
<tr><th>부록</th><td>정답 · 인사말 총정리 · 단어장</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_chinese → 10월 29일 모임 (문장을 누르면 그 부분부터 재생 · 병음과 한국어 번역 보기)<br>
각 레슨 구성: 오늘의 목표 → 영상 속 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기</div></div>
<div class="stripe"></div></section>''')

# ---------- 시작 ----------
P.append('<section class="lesson"><div class="hd"><div class="k">开始 · 시작</div><h1>시작하기 전에: 성조와 병음</h1></div>'
 + box("이 교재로 공부하는 방법", "<p>① 대화를 먼저 읽고 → ② 사이트의 '듣기'에서 문장을 눌러 듣고 → ③ <b>'현재 문장 반복'</b>으로 따라 말하고 → ④ 연습 문제를 풀어요. 사이트에서 <b>병음</b>을 끄고 한자만 보며 읽어 보는 것도 좋은 연습이에요.</p>", "g")
 + h("성조", "중국어의 4가지 성조 + 경성") + '''
<table class="t tone"><tr><th>성조</th><th>표기</th><th>소리 내는 법</th><th>예</th></tr>
<tr><td>1성</td><td><b>ā</b></td><td>높고 평평하게 쭉 — "아~"</td><td><span class="zh" lang="zh-CN">妈</span> mā 엄마</td></tr>
<tr><td>2성</td><td><b>á</b></td><td>중간에서 위로 올리기 — "아?"</td><td><span class="zh" lang="zh-CN">麻</span> má 삼, 마비되다</td></tr>
<tr><td>3성</td><td><b>ǎ</b></td><td>낮게 내렸다가 살짝 올리기 (보통은 낮게만)</td><td><span class="zh" lang="zh-CN">马</span> mǎ 말</td></tr>
<tr><td>4성</td><td><b>à</b></td><td>위에서 아래로 뚝 — "아!"</td><td><span class="zh" lang="zh-CN">骂</span> mà 꾸짖다</td></tr>
<tr><td>경성</td><td><b>a</b></td><td>짧고 가볍게, 표시 없음</td><td><span class="zh" lang="zh-CN">吗</span> ma ~까? · <span class="zh" lang="zh-CN">谢谢</span> xièxie</td></tr></table>
''' + h("성조 변화", "이번 영상에서 꼭 알아야 할 3가지") + '''
<table class="t"><tr><th>규칙</th><th>원래</th><th>실제 소리</th><th>영상 속 예</th></tr>
<tr><td>3성 + 3성 → <b>2성</b> + 3성</td><td>nǐ hǎo</td><td><b>ní</b> hǎo</td><td><span class="zh" lang="zh-CN">你好 · 很好 · 也很好</span></td></tr>
<tr><td><b>不</b> + 4성 → bú</td><td>bù</td><td><b>bú</b> kèqi</td><td><span class="zh" lang="zh-CN">不客气 · 不会 · 不太忙 · 好久不见</span></td></tr>
<tr><td><b>一</b> + 4성 → yí · 그 밖 → yì</td><td>yī</td><td><b>yí</b>huìr · <b>yì</b>qǐ</td><td><span class="zh" lang="zh-CN">一会儿 · 一定 · 一起</span></td></tr></table>
<p class="sm">※ 이 교재와 사이트의 병음은 不·一의 바뀐 성조를 그대로 적었어요. 3성+3성은 원래 성조로 적고, 읽을 때만 바꿔요.</p>
''' + h("발음", "한국 사람이 헷갈리는 병음") + '''
<table class="t"><tr><th>병음</th><th>소리</th><th>예</th></tr>
<tr><td><b>zh · ch · sh · r</b></td><td>혀끝을 말아 올려서 — 즈·츠·스·르</td><td><span class="zh" lang="zh-CN">桌子</span> zhuōzi · <span class="zh" lang="zh-CN">吃</span> chī · <span class="zh" lang="zh-CN">是</span> shì · <span class="zh" lang="zh-CN">认识</span> rènshi</td></tr>
<tr><td><b>z · c · s</b></td><td>혀를 펴고 — 쯔·츠·쓰</td><td><span class="zh" lang="zh-CN">再见</span> zàijiàn · <span class="zh" lang="zh-CN">菜</span> cài · <span class="zh" lang="zh-CN">四</span> sì</td></tr>
<tr><td><b>j · q · x</b></td><td>지·치·시 (뒤에 i·ü만 와요)</td><td><span class="zh" lang="zh-CN">见</span> jiàn · <span class="zh" lang="zh-CN">请</span> qǐng · <span class="zh" lang="zh-CN">谢谢</span> xièxie</td></tr>
<tr><td><b>ü</b> (j·q·x 뒤에선 u로 적음)</td><td>입술을 둥글게 하고 "이" — 위</td><td><span class="zh" lang="zh-CN">愉快</span> yúkuài · <span class="zh" lang="zh-CN">去</span> qù</td></tr>
<tr><td><b>-r</b> (儿화)</td><td>끝에 혀를 말아요</td><td><span class="zh" lang="zh-CN">一会儿</span> yíhuìr · <span class="zh" lang="zh-CN">有点儿</span> yǒudiǎnr</td></tr></table>
''' + h("인사 공식", "누구에게든 + 好！")
 + '<div class="two">' + box("사람 + 好", '<p><span class="zh" lang="zh-CN">你好！</span> 안녕! · <span class="zh" lang="zh-CN">您好！</span> 안녕하세요(높임)<br><span class="zh" lang="zh-CN">老师好！</span> 선생님 안녕하세요 · <span class="zh" lang="zh-CN">阿姨好！</span> 아주머니 안녕하세요</p>')
 + box("때 + 好", '<p><span class="zh" lang="zh-CN">早上好！ / 早！</span> 아침 인사<br><span class="zh" lang="zh-CN">下午好！</span> 오후 인사 · <span class="zh" lang="zh-CN">晚上好！</span> 저녁 인사<br><span class="zh" lang="zh-CN">晚安！</span> 잘 자요 (밤에 헤어질 때)</p>') + "</div>"
 + h("10가지 장면", "이번 영상에 나오는 대화")
 + '<table class="t scenes">' + "".join(
     f'<tr><td>대화 {i+1}</td><td>{fmt(dstart(i))}</td><td>{zh(D[i]["lines"][0][2])}</td><td>{e(D[i]["lines"][0][4])}</td></tr>' for i in range(10)) + "</table>"
 + "</section>")

# ---------- LESSON 1 ----------
P.append(lesson(1, 0, "아침 인사 · 새 이웃과 첫인사", [
    "<b>早上好！</b>로 아침 인사를 하고 <b>一会儿见！</b>으로 헤어질 수 있다.",
    "<b>…吗？</b>로 묻고 <b>你呢？</b>로 되물을 수 있다.",
    "<b>我叫…</b>로 이름을 말하고 <b>很高兴认识你</b>로 인사할 수 있다."])
 + h("문법", "질문은 끝에 吗, 되물을 땐 呢")
 + '<div class="two">' + box("① 문장 + 吗？ = ~예요?", '<p><span class="zh" lang="zh-CN">你吃早饭了吗？</span> 아침 먹었어?<br><span class="zh" lang="zh-CN">你是新搬来的吗？</span> 새로 이사 왔어요?</p><p class="sm">평서문 끝에 吗만 붙이면 질문이 돼요. 어순은 그대로!</p>')
 + box("② 你呢？ = 너는?", '<p><span class="zh" lang="zh-CN">吃了，你呢？</span> 먹었어, 너는?<br><span class="zh" lang="zh-CN">我叫李美。你呢？</span> 저는 리메이예요. 당신은요?</p><p class="sm">같은 질문을 상대에게 돌려줄 때 써요.</p>') + "</div>"
 + '<div class="two">' + box("③ 也 = ~도", '<p><span class="zh" lang="zh-CN">我也吃了。</span> 나도 먹었어.<br><span class="zh" lang="zh-CN">我也很高兴认识你。</span> 저도 만나서 반가워요.</p><p class="sm">也는 항상 <b>동사·형용사 앞</b>에 와요. ✗ 也我</p>')
 + box("④ 叫 + 이름 = 이름이 ~예요", '<p><span class="zh" lang="zh-CN">你叫什么名字？</span> 이름이 뭐예요?<br><span class="zh" lang="zh-CN">我叫王明。</span> 저는 왕밍이에요.</p><p class="sm">什么 shénme = 무엇 · 名字 míngzi = 이름</p>') + "</div>"
 + box("⑤ 동사 + 了 = ~했어요 (완료)", '<p><span class="zh" lang="zh-CN">吃了。</span> 먹었어. · <span class="zh" lang="zh-CN">我七点就到了。</span> 7시에 벌써 왔어.</p>', "g")
 + h("단어", "대화 1·2 핵심 단어") + words(0, 1)
 + h("연습 A", "알맞은 말을 골라 넣으세요. (吗 · 呢 · 也 · 叫)")
 + ol([f'你今天来得很早 {BS}？', f'我吃了，你 {BS}？', f'我 {BS} 很高兴认识你。', f'我 {BS} 李美。'])
 + h("연습 B", "중국어로 옮겨 보세요.")
 + ol([f'좋은 아침! → {B}', f'만나서 반가워요. → {B}', f'이름이 뭐예요? → {B}', f'이따 봐! → {B}'])
 + h("말하기", "영상 속 사람에게 내 이름으로 대답해 보세요")
 + say(("王明", "你叫什么名字？", "이름이 뭐예요?"), ("朋友", "你吃早饭了吗？", "아침 먹었어?"))
 + "</section>")

# ---------- LESSON 2 ----------
P.append(lesson(2, 2, "오랜만의 인사 · 가족과 저녁 인사", [
    "<b>好久不见！你最近好吗？</b>로 안부를 물을 수 있다.",
    "<b>在 + 동사</b>로 지금 하는 일을, <b>想 + 동사</b>로 하고 싶은 일을 말할 수 있다.",
    "<b>累不累？</b>처럼 '형용사 + 不 + 형용사'로 물을 수 있다."])
 + h("문법", "지금 하는 일 · 하고 싶은 일")
 + '<div class="two">' + box("① 在 + 동사 = ~하고 있어요", '<p><span class="zh" lang="zh-CN">你在忙什么？</span> 뭐 하느라 바빠요?<br><span class="zh" lang="zh-CN">我在学习。</span> 공부하고 있어요.</p>')
 + box("② 想 + 동사 = ~하고 싶어요", '<p><span class="zh" lang="zh-CN">你想喝点什么？</span> 뭐 좀 마실래요?<br><span class="zh" lang="zh-CN">我想喝咖啡。</span> 커피 마시고 싶어요.</p><p class="sm">点 = 一点(儿) 조금</p>') + "</div>"
 + '<div class="two">' + box("③ 累不累？ = 피곤해, 안 피곤해?", '<p>형용사·동사를 <b>긍정 + 不 + 긍정</b>으로 붙이면 吗 없이도 질문이 돼요.<br><span class="zh" lang="zh-CN">累不累？ = 累吗？</span><br><span class="zh" lang="zh-CN">忙不忙？ 好不好？</span></p>')
 + box("④ 了 ↔ 还没有", '<p><span class="zh" lang="zh-CN">你吃晚饭了吗？</span> 저녁 먹었니?<br>→ <span class="zh" lang="zh-CN">吃了。</span> 먹었어요. / <span class="zh" lang="zh-CN">还没有。</span> 아직이요.</p>') + "</div>"
 + box("⑤ 제안하는 吧 · 조금 有点儿", '<p><span class="zh" lang="zh-CN">我们一起坐吧。</span> 같이 앉아요. · <span class="zh" lang="zh-CN">先去洗手吧。</span> 먼저 손 씻고 와.<br><span class="zh" lang="zh-CN">有点儿累。</span> 조금 피곤해요. (有点儿 + 형용사 = 좀 ~하다, 주로 아쉬운 느낌)</p>', "g")
 + h("단어", "대화 3·4 핵심 단어") + words(2, 3)
 + h("연습 A", "질문에 대답해 보세요.")
 + ol([f'你最近好吗？ → {B}', f'你在忙什么？ (공부하는 중) → {B}', f'你想喝点什么？ (커피) → {B}', f'你吃晚饭了吗？ (아직) → {B}'])
 + h("연습 B", "'형용사 + 不 + 형용사' 질문으로 바꾸세요.")
 + ol([f'你累吗？ → {B}', f'你忙吗？ → {B}', f'咖啡好喝吗？ → {B}'])
 + h("말하기", "오랜만에 만난 친구에게 대답해 보세요")
 + say(("朋友", "好久不见！你最近好吗？", "오랜만이야! 요즘 잘 지내?"), ("朋友", "你在忙什么？", "요즘 뭐 하느라 바빠?"))
 + "</section>")

# ---------- LESSON 3 ----------
P.append(lesson(3, 4, "주말 인사 · 첫 출근 인사", [
    "<b>周末愉快！ 回头见！</b>으로 주말 인사를 할 수 있다.",
    "<b>我是新来的。请多关照。</b>로 새 자리에서 인사할 수 있다.",
    "<b>就</b>(벌써)와 <b>的</b>(~의)를 쓸 수 있다."])
 + h("문법", "就 · 的 · 是…的")
 + '<div class="two">' + box("① 시간 + 就 = 벌써(일찍) ~했다", '<p><span class="zh" lang="zh-CN">六点就起了。</span> 6시에 벌써 일어났어.<br><span class="zh" lang="zh-CN">这么早就起床了？</span> 이렇게 일찍 일어났어?</p><p class="sm">这么 + 형용사 = 이렇게 ~하다</p>')
 + box("② 사람 + 的 + 물건 = ~의", '<p><span class="zh" lang="zh-CN">你的狗</span> 너의 개 · <span class="zh" lang="zh-CN">你的桌子</span> 당신의 책상<br><span class="zh" lang="zh-CN">小明的同学</span> 샤오밍의 반 친구</p>') + "</div>"
 + '<div class="two">' + box("③ 是…的 = (언제·어떻게) ~한 거예요", '<p><span class="zh" lang="zh-CN">我是新来的。</span> 저는 새로 온 사람이에요.<br><span class="zh" lang="zh-CN">我昨天搬来的。</span> 어제 이사 왔어요. (是 생략)</p>')
 + box("④ 有 + 명사 + 就… = ~있으면 바로…", '<p><span class="zh" lang="zh-CN">有问题就问我。</span> 궁금한 게 있으면 저한테 물어보세요.<br><span class="zh" lang="zh-CN">有什么事可以找我。</span> 무슨 일 있으면 저를 찾으세요.</p>') + "</div>"
 + box("새 자리에서 쓰는 인사 세트", '<p><span class="zh" lang="zh-CN">你好！我是新来的。我叫○○。请多关照！</span><br>안녕하세요! 새로 왔어요. ○○라고 해요. 잘 부탁드려요!<br>→ 대답: <span class="zh" lang="zh-CN">欢迎加入我们！ 请多关照！</span></p>', "g")
 + h("단어", "대화 5·6 핵심 단어") + words(4, 5)
 + h("연습 A", "빈칸을 채우세요.")
 + ol([f'六点 {BS} 起了。 (6시에 벌써 일어났어.)', f'这是你 {BS} 桌子。 (이게 당신 책상이에요.)', f'我是新来 {BS}。 (저는 새로 왔어요.)', f'有问题 {BS} 问我。 (궁금하면 바로 물어봐요.)'])
 + h("연습 B", "상황에 맞는 말을 고르세요.")
 + '<table class="t match"><tr><td>① 주말에 헤어질 때</td><td>ⓐ 请多关照！</td></tr><tr><td>② 친구 강아지를 봤을 때</td><td>ⓑ 周末愉快！</td></tr><tr><td>③ 회사에 처음 왔을 때</td><td>ⓒ 真厉害！</td></tr><tr><td>④ 친구가 새벽에 일어났다고 할 때</td><td>ⓓ 你的狗很可爱。</td></tr></table>'
 + h("말하기", "새 동료에게 나를 소개해 보세요")
 + say(("刘娟", "你好！欢迎加入我们！你叫什么？", "안녕하세요! 환영해요! 이름이 뭐예요?"))
 + "</section>")

# ---------- LESSON 4 ----------
P.append(lesson(4, 6, "선생님·어른께 인사", [
    "<b>您</b>과 <b>호칭 + 好</b>로 어른께 공손하게 인사할 수 있다.",
    "<b>做完了</b>처럼 '동사 + 完'으로 다 했다고 말할 수 있다.",
    "<b>…吧？</b>로 짐작해서 확인할 수 있다."])
 + h("문법", "높임말 · 다 했어요 · 확인하는 吧")
 + '<div class="two">' + box("① 你 → 您 (높임)", '<p><span class="zh" lang="zh-CN">老师，您身体好吗？</span> 선생님, 건강하시죠?<br><span class="zh" lang="zh-CN">好的，谢谢您！</span> 네, 감사합니다!</p><p class="sm">선생님·친구 부모님·처음 보는 어른께는 您을 써요.</p>')
 + box("② 호칭 + 好", '<p><span class="zh" lang="zh-CN">老师好！</span> 선생님 안녕하세요<br><span class="zh" lang="zh-CN">阿姨好！</span> 아주머니 안녕하세요<br><span class="zh" lang="zh-CN">叔叔好！</span> 아저씨 안녕하세요 (보너스)</p>') + "</div>"
 + '<div class="two">' + box("③ 동사 + 完 = 다 ~했다", '<p><span class="zh" lang="zh-CN">作业做完了吗？</span> 숙제 다 했니?<br>→ <span class="zh" lang="zh-CN">做完了。</span> 다 했어요.<br><span class="zh" lang="zh-CN">吃完了 · 看完了</span> 다 먹었다 · 다 봤다</p>')
 + box("④ …吧？ = ~지? (짐작 확인)", '<p><span class="zh" lang="zh-CN">你是小明的同学吧？</span> 샤오밍 반 친구지?<br>문장 끝 吧: 확인(…지?) · 제안(…하자) · 권유(…하렴)<br><span class="zh" lang="zh-CN">喝点水吧。</span> 물 좀 마시렴.</p>') + "</div>"
 + box("⑤ 약속하기: 不会…的 / 부탁하기: 请 + 동사", '<p><span class="zh" lang="zh-CN">我不会迟到的。</span> 늦지 않을게요. · <span class="zh" lang="zh-CN">请坐。</span> 앉으세요. · <span class="zh" lang="zh-CN">快进来。</span> 어서 들어와.</p>', "g")
 + h("단어", "대화 7·8 핵심 단어") + words(6, 7)
 + h("연습 A", "공손한 말로 바꾸세요. (你 → 您)")
 + ol([f'你好！ → {B}', f'谢谢你！ → {B}', f'你身体好吗？ → {B}'])
 + h("연습 B", "'동사 + 完了'로 대답하세요.")
 + ol([f'作业做完了吗？ → {B}', f'饭吃完了吗？ → {B}'])
 + h("말하기", "친구 집에 놀러 갔어요. 친구 어머니께 대답해 보세요")
 + say(("阿姨", "你好！快进来。", "어서 와! 들어오렴."), ("阿姨", "你是小明的同学吧？", "샤오밍 반 친구지?"), ("阿姨", "喝点水吧。", "물 좀 마시렴."))
 + "</section>")

# ---------- LESSON 5 ----------
P.append(lesson(5, 8, "우연히 만났을 때 · 밤에 헤어질 때", [
    "<b>好巧啊！</b>로 반가움을 표현하고 <b>你家人都好吗？</b>로 안부를 물을 수 있다.",
    "<b>我该回家了。</b>로 자리를 마무리할 수 있다.",
    "<b>晚安 · 明天见 · 路上小心</b>으로 밤 인사를 할 수 있다."])
 + h("문법", "该…了 · 给 · 都 · 不太")
 + '<div class="two">' + box("① 该 + 동사 + 了 = 이제 ~해야겠다", '<p><span class="zh" lang="zh-CN">我该回家了。</span> 이제 집에 가야겠어.<br><span class="zh" lang="zh-CN">时间不早了。</span> 시간이 늦었네. (不早 = 이르지 않다)</p>')
 + box("② 给 + 사람 + 동사 = ~에게 …하다", '<p><span class="zh" lang="zh-CN">回去给我发消息。</span> 집에 가면 나한테 메시지 보내.<br><span class="zh" lang="zh-CN">我打电话给你。</span> 내가 너한테 전화할게. (= 我给你打电话)</p>') + "</div>"
 + '<div class="two">' + box("③ 都 = 모두", '<p><span class="zh" lang="zh-CN">你家人都好吗？</span> 가족들 다 잘 지내?<br><span class="zh" lang="zh-CN">都很好。</span> 다들 잘 지내.</p>')
 + box("④ 不太 + 형용사 = 별로 ~하지 않다", '<p><span class="zh" lang="zh-CN">还好，不太忙。</span> 그럭저럭, 별로 안 바빠.<br><span class="zh" lang="zh-CN">好巧啊！</span> (好 + 형용사 + 啊!) 정말 공교롭다!</p>') + "</div>"
 + box("밤 인사 세트", '<p><span class="zh" lang="zh-CN">时间不早了，我该回家了。今天很开心！路上小心。明天见！晚安！</span></p>', "g")
 + h("단어", "대화 9·10 핵심 단어") + words(8, 9)
 + h("연습 A", "알맞은 말을 넣으세요. (该 · 给 · 都 · 不太)")
 + ol([f'我 {BS} 回家了。', f'回去 {BS} 我发消息。', f'你家人 {BS} 好吗？', f'还好，{BS} 忙。'])
 + h("연습 B", "순서대로 배열해 대화를 완성하세요.")
 + '<p class="fillp"><span class="zh" lang="zh-CN">ⓐ 明天见！ &nbsp; ⓑ 时间不早了。 &nbsp; ⓒ 是啊，我该回家了。 &nbsp; ⓓ 路上小心。</span><br>→ ( ) → ( ) → ( ) → ( )</p>'
 + h("최종 미션", "나만의 인사 대화 만들기")
 + '''<table class="t mine"><tr><th>순서</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>① 만나기</td><td><span class="zh" lang="zh-CN">你好！ / 早上好！ / 好久不见！</span></td><td></td></tr>
<tr><td>② 안부</td><td><span class="zh" lang="zh-CN">你最近好吗？ 我很好，你呢？</span></td><td></td></tr>
<tr><td>③ 이름</td><td><span class="zh" lang="zh-CN">我叫…。很高兴认识你。</span></td><td></td></tr>
<tr><td>④ 지금 하는 일</td><td><span class="zh" lang="zh-CN">我在学习中文。</span></td><td></td></tr>
<tr><td>⑤ 헤어지기</td><td><span class="zh" lang="zh-CN">我该走了。再见！ / 回头见！</span></td><td></td></tr></table>'''
 + box("예시", '<p><span class="zh" lang="zh-CN">A: 你好！好久不见！ B: 好久不见！你最近好吗？ A: 我很好，你呢？ B: 我也很好。你在忙什么？ A: 我在学习中文。 B: 太好了！加油！ A: 谢谢！我该走了。回头见！ B: 回头见！</span></p><p class="sm">学习中文 xuéxí Zhōngwén 중국어를 공부하다 · 走 zǒu 가다, 떠나다</p>')
 + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>아침·오후·밤에 맞는 인사를 할 수 있다.</li><li>처음 만난 사람에게 이름을 말하고 반갑다고 할 수 있다.</li><li>吗·呢·累不累로 질문할 수 있다.</li><li>선생님·어른께 您으로 공손하게 인사할 수 있다.</li><li>상황에 맞게 헤어지는 인사를 고를 수 있다. (再见 · 一会儿见 · 回头见 · 明天见 · 晚安)</li><li>성조 변화(你好 · 不客气 · 一会儿)를 지켜 읽을 수 있다.</li></ul>'
 + "</section>")

# ---------- 부록 ----------
P.append('''<section class="lesson"><div class="hd"><div class="k">附录 A</div><h1>정답</h1></div><div class="ans-list">
<p><b>Lesson 1</b> A: 1 吗 · 2 呢 · 3 也 · 4 叫 &nbsp;|&nbsp; B: 1 早上好！ · 2 很高兴认识你。 · 3 你叫什么名字？ · 4 一会儿见！</p>
<p><b>Lesson 2</b> A: 1 我很好(，你呢？) · 2 我在学习。 · 3 我想喝咖啡。 · 4 还没有。 &nbsp;|&nbsp; B: 1 你累不累？ · 2 你忙不忙？ · 3 咖啡好喝不好喝？(好不好喝？)</p>
<p><b>Lesson 3</b> A: 1 就 · 2 的 · 3 的 · 4 就 &nbsp;|&nbsp; B: ①ⓑ ②ⓓ ③ⓐ ④ⓒ</p>
<p><b>Lesson 4</b> A: 1 您好！ · 2 谢谢您！ · 3 您身体好吗？ &nbsp;|&nbsp; B: 1 做完了。 · 2 吃完了。</p>
<p><b>Lesson 5</b> A: 1 该 · 2 给 · 3 都 · 4 不太 &nbsp;|&nbsp; B: ⓑ → ⓒ → ⓓ → ⓐ</p>
</div>
<div class="hd" style="margin-top:26px"><div class="k">附录 B</div><h1>인사말 총정리</h1></div>
<table class="t"><tr><th>상황</th><th>만날 때</th><th>헤어질 때</th></tr>
<tr><td>아침</td><td><span class="zh" lang="zh-CN">早上好！ 早！</span></td><td><span class="zh" lang="zh-CN">一会儿见！</span> 이따 봐</td></tr>
<tr><td>오후</td><td><span class="zh" lang="zh-CN">下午好！</span></td><td><span class="zh" lang="zh-CN">回头见！ 回头聊！</span> 나중에 봐/얘기해</td></tr>
<tr><td>저녁·밤</td><td><span class="zh" lang="zh-CN">晚上好！</span></td><td><span class="zh" lang="zh-CN">明天见！ 晚安！ 路上小心。</span></td></tr>
<tr><td>처음 만날 때</td><td><span class="zh" lang="zh-CN">你好！很高兴认识你。</span></td><td><span class="zh" lang="zh-CN">再见！</span></td></tr>
<tr><td>오랜만에</td><td><span class="zh" lang="zh-CN">好久不见！你最近好吗？</span></td><td><span class="zh" lang="zh-CN">有时间一起吃饭吧！</span></td></tr>
<tr><td>어른께</td><td><span class="zh" lang="zh-CN">老师好！ 阿姨好！ 您好！</span></td><td><span class="zh" lang="zh-CN">老师再见！ 谢谢您！</span></td></tr>
<tr><td>새 자리에서</td><td><span class="zh" lang="zh-CN">我是新来的。请多关照！</span></td><td><span class="zh" lang="zh-CN">周末愉快！</span> 즐거운 주말!</td></tr></table>
</section>''')

voc = ['<section class="lesson"><div class="hd"><div class="k">附录 C</div><h1>단어장</h1><div class="s">사이트의 \'단어장\'과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="3">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span>{zh(z)}</td><td class="wp">{e(py)}</td><td>{e(ko)}</td></tr>' for z, py, ko in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))

CSS = open(f"{work}/../book.css", encoding="utf-8").read() + open(f"{work}/../book_zh.css", encoding="utf-8").read()
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>중국어 인사하기 교재 1주차</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
