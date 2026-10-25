// 공통 도우미: 날짜(한국 시간 기준)·HTML 이스케이프·모임 목록 불러오기
const CS = (() => {
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const todayKST = () => new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Seoul" }).format(new Date()); // YYYY-MM-DD
  const WD = ["일", "월", "화", "수", "목", "금", "토"];
  const parts = d => { const [y, m, dd] = d.split("-").map(Number); return { y, m, d: dd, wd: WD[new Date(Date.UTC(y, m - 1, dd)).getUTCDay()] }; };
  const fmtDate = d => { const p = parts(d); return `${p.m}월 ${p.d}일 (${p.wd})`; };
  // 모임 당일은 정해진 시각(기본 낮 12시, 한국 시간)까지 '오늘 모임'으로 보여 주고, 그 뒤에는 다음 모임을 공지해요.
  const hourKST = () => +new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Seoul", hour: "2-digit", hour12: false }).format(new Date());
  // 저녁 모임이면 meetings.json의 defaults.switchHour(예: 22)로 바꿀 수 있어요.
  let switchHour = 12;
  const isUpcoming = (d, today) => d > today || (d === today && hourKST() < switchHour);
  const daysBetween = (a, b) => Math.round((Date.parse(b) - Date.parse(a)) / 864e5);
  const PFX = "zh_"; // 같은 주소(lkj640.github.io)의 스페인어 사이트와 저장 값이 섞이지 않게
  const store = {
    get(k, def) { try { const v = localStorage.getItem(PFX + k); return v === null ? def : JSON.parse(v); } catch { return def; } },
    set(k, v) { try { localStorage.setItem(PFX + k, JSON.stringify(v)); } catch {} },
  };
  async function load() {
    const r = await fetch("meetings.json", { cache: "no-cache" });
    const j = await r.json();
    j.meetings.sort((a, b) => a.date.localeCompare(b.date));
    if (j.defaults && j.defaults.switchHour != null) switchHour = j.defaults.switchHour;
    return j;
  }
  // 병음을 한자 한 글자마다 하나씩 위에 얹어요(<ruby>). 글자 수와 음절 수가 안 맞으면 null.
  const SYL = /^(?:er|(?:zh|ch|sh|[bpmfdtnlgkhjqxrzcsyw])?(?:iang|iong|uang|ueng|iao|ian|ing|uai|uan|ang|eng|ong|van|ai|ei|ao|ou|an|en|ia|ie|iu|in|ua|uo|ui|un|ue|ve|vn|a|o|e|i|u|v))$/;
  const base = c => c.normalize("NFD").replace(/u\u0308/i, "v")[0].toLowerCase();
  const toned = c => /[\u0300\u0301\u0304\u030c]/.test(c.normalize("NFD"));
  function sylls(w) {
    const ch = [...w.normalize("NFC")], b = ch.map(base).join(""), out = [];
    const go = i => {
      if (i === b.length) return true;
      for (let n = Math.min(6, b.length - i); n > 0; n--) {
        const s = b.slice(i, i + n);
        // 단어 중간 음절은 자음으로 시작(아니면 병음에 ' 가 붙어요), 끝의 r은 儿화
        const ok = (i > 0 && s === "r" && i + n === b.length) || (SYL.test(s) && (i === 0 || !/^[aoeiuv]/.test(s)));
        if (!ok || ch.slice(i, i + n).filter(toned).length > 1) continue;
        out.push(ch.slice(i, i + n).join(""));
        if (go(i + n)) return true;
        out.pop();
      }
      return false;
    };
    return go(0) ? out : null;
  }
  function ruby(zh, py) {
    const words = String(py || "").match(/[a-zA-Z\u00c0-\u024f\u0300-\u036f]+/g) || [], ps = [];
    for (const w of words) { const s = sylls(w); if (!s) return null; ps.push(...s); }
    const chars = [...String(zh || "")];
    if (!ps.length || chars.filter(c => /\p{Script=Han}/u.test(c)).length !== ps.length) return null;
    let k = 0;
    return chars.map(c => /\p{Script=Han}/u.test(c) ? `<ruby>${esc(c)}<rt>${esc(ps[k++])}</rt></ruby>` : esc(c)).join("");
  }
  const lab = m => m.label || (m.ep != null ? `Ep.${m.ep}` : "");
  return { lab, esc, ruby, todayKST, fmtDate, daysBetween, isUpcoming, store, load };
})();
