"""병음을 한자 한 글자마다 하나씩 위에 얹어요(<ruby>). assets/common.js의 ruby()와 같은 규칙이에요."""
import html, re, unicodedata

SYL = re.compile(r"(?:er|(?:zh|ch|sh|[bpmfdtnlgkhjqxrzcsyw])?(?:iang|iong|uang|ueng|iao|ian|ing|uai|uan|ang|eng|ong|van|ai|ei|ao|ou|an|en|ia|ie|iu|in|ua|uo|ui|un|ue|ve|vn|a|o|e|i|u|v))")
HAN = re.compile(r"[㐀-鿿豈-﫿]")
e = lambda s: html.escape(s, quote=False)


def base(c):
    d = unicodedata.normalize("NFD", c)
    return "v" if d[:2].lower() == "ü" else d[0].lower()


def toned(c): return bool(re.search("[̀́̄̌]", unicodedata.normalize("NFD", c)))


def sylls(w):
    ch = list(unicodedata.normalize("NFC", w)); b = "".join(map(base, ch)); out = []
    def go(i):
        if i == len(b): return True
        for n in range(min(6, len(b) - i), 0, -1):
            s = b[i:i + n]
            # 단어 중간 음절은 자음으로 시작(아니면 병음에 ' 가 붙어요), 끝의 r은 儿화
            ok = (i > 0 and s == "r" and i + n == len(b)) or (SYL.fullmatch(s) and (i == 0 or s[0] not in "aoeiuv"))
            if not ok or sum(map(toned, ch[i:i + n])) > 1: continue
            out.append("".join(ch[i:i + n]))
            if go(i + n): return True
            out.pop()
        return False
    return out if go(0) else None


def ruby(zh, py):
    """글자 수와 음절 수가 안 맞으면 None"""
    ps = []
    for w in re.findall(r"[A-Za-zÀ-ɏ̀-ͯ]+", py or ""):
        s = sylls(w)
        if s is None: return None
        ps += s
    if not ps or len(HAN.findall(zh)) != len(ps): return None
    it = iter(ps)
    return "".join(f"<ruby>{e(c)}<rt>{e(next(it))}</rt></ruby>" if HAN.match(c) else e(c) for c in zh)


def zp(zh, py, tag="span"):
    """한자 위에 병음. 맞출 수 없으면 한자 아래에 병음 한 줄."""
    r = ruby(zh, py)
    if r: return f'<{tag} class="zh rb" lang="zh-CN">{r}</{tag}>'
    return f'<{tag} class="zh" lang="zh-CN">{e(zh)}</{tag}>' + (f'<i class="py">{e(py)}</i>' if py else "")
