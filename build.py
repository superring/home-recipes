#!/usr/bin/env python3
"""Build index.html (the dish picker page) from recipes/*.md."""
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
RECIPES = ROOT / "recipes"
OUT = ROOT / "index.html"


def parse(md: Path) -> dict:
    text = md.read_text(encoding="utf-8")
    r = {"slug": md.stem, "oid": hashlib.md5(md.stem.encode()).hexdigest()[:16],
         "tags": [], "time": "", "source": "", "intro": "",
         "cover": "", "ingredients": [], "steps": [], "tips": ""}
    r["title"] = re.search(r"^# (.+)$", text, re.M).group(1).strip()
    m = re.search(r"^标签[:：]\s*(.+)$", text, re.M)
    if m:
        r["tags"] = [t.strip() for t in re.split(r"[,，、\s]+", m.group(1)) if t.strip()]
    m = re.search(r"^用时[:：]\s*(.+)$", text, re.M)
    if m:
        r["time"] = m.group(1).strip()
    m = re.search(r"^来源[:：]\s*\[.*?\]\((.+?)\)", text, re.M)
    if m:
        r["source"] = m.group(1)
    m = re.search(r"!\[[^\]]*\]\(\.\./(images/[^)]+)\)", text)
    if m:
        r["cover"] = m.group(1)

    sections = re.split(r"^## ", text, flags=re.M)
    head = sections[0]
    paras = [p.strip() for p in head.split("\n\n")
             if p.strip() and not p.startswith("#")
             and not re.match(r"^(标签|用时|来源)[:：]", p.strip())]
    r["intro"] = paras[0] if paras else ""
    for sec in sections[1:]:
        name, _, body = sec.partition("\n")
        name = name.strip()
        if name.startswith("材料"):
            r["ingredients"] = [l[2:].strip() for l in body.splitlines() if l.startswith("- ")]
            m = re.search(r"（(.+?)）", name)
            r["serves"] = m.group(1) if m else ""
        elif name.startswith("做法"):
            r["steps"] = [re.sub(r"^\d+\.\s*", "", l).strip()
                          for l in body.splitlines() if re.match(r"^\d+\.", l)]
        elif name.startswith("小贴士"):
            r["tips"] = body.strip()
    return r


def build():
    recipes = [parse(p) for p in sorted(RECIPES.glob("*.md"))]
    recipes.sort(key=lambda r: ("自家拿手" not in r["tags"], r["title"]))
    data = json.dumps(recipes, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__DATA__", data)
    OUT.write_text(html, encoding="utf-8")
    print(f"{len(recipes)} recipes -> {OUT.name}")


TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>今晚吃什么</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap">
<style>
:root{
  --bg:#F7F2EA; --surface:#FFFDFA; --ink:#2A2320; --muted:#8B7E72; --line:#E6DDD0;
  --accent:#C4432F; --accent-ink:#FFF7F4; --veg:#5F7A4C; --chip:#EFE7DB; --chip-on:#2A2320;
  --shadow:0 1px 2px rgba(60,40,20,.06),0 8px 24px rgba(60,40,20,.08);
  color-scheme:light dark;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#1C1815; --surface:#26211D; --ink:#F1E9DF; --muted:#A3968A; --line:#3A322B;
    --accent:#E0644F; --accent-ink:#1C1815; --veg:#9DB57E; --chip:#2F2925; --chip-on:#F1E9DF;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35);
  }
}
:root[data-theme="dark"]{
  --bg:#1C1815; --surface:#26211D; --ink:#F1E9DF; --muted:#A3968A; --line:#3A322B;
  --accent:#E0644F; --accent-ink:#1C1815; --veg:#9DB57E; --chip:#2F2925; --chip-on:#F1E9DF;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35);
}
*{box-sizing:border-box}
html,body{margin:0}
body{overflow-x:hidden;background:var(--bg);color:var(--ink);font:16px/1.55 "Noto Sans SC",-apple-system,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;-webkit-font-smoothing:antialiased;padding-bottom:calc(96px + env(safe-area-inset-bottom))}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
button:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.serif{font-family:"Noto Serif SC","Songti SC","STSong",serif}

header{position:sticky;top:0;z-index:5;background:var(--bg);padding:18px 16px 10px;border-bottom:1px solid var(--line)}
.top{display:flex;align-items:baseline;justify-content:space-between;gap:12px}
.top>*{min-width:0}
h1{margin:0;font-size:26px;font-weight:700;letter-spacing:.02em;white-space:nowrap}
h1 small{font-family:"Noto Sans SC",sans-serif;font-size:12px;font-weight:500;color:var(--muted);margin-left:8px;letter-spacing:.08em}
.dice{display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:500;color:var(--accent);padding:6px 10px;border:1px solid var(--accent);border-radius:999px;white-space:nowrap}
.dice:active{transform:scale(.97)}
.search{margin-top:12px;display:flex;align-items:center;gap:8px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:8px 12px}
.search svg{flex:none;color:var(--muted)}
.search input{flex:1;border:0;background:none;font:inherit;color:inherit;min-width:0}
.search input::placeholder{color:var(--muted)}
.chips{display:flex;gap:8px;overflow-x:auto;margin:10px -16px 0;padding:2px 16px 4px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chip{flex:none;font-size:13px;font-weight:500;padding:6px 12px;border-radius:999px;background:var(--chip);color:var(--ink)}
.chip[aria-pressed="true"]{background:var(--chip-on);color:var(--bg)}

main{padding:14px 16px 0}
.count{font-size:12px;color:var(--muted);letter-spacing:.06em;margin:0 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px}
.card{min-width:0;width:100%;background:var(--surface);border-radius:14px;overflow:hidden;box-shadow:var(--shadow);text-align:left;display:flex;flex-direction:column;position:relative;transition:transform .12s}
.card:active{transform:scale(.98)}
.card .ph{aspect-ratio:4/3;background:var(--chip);width:100%;object-fit:cover;display:block}
.card .body{padding:10px 12px 12px;display:flex;flex-direction:column;gap:6px;flex:1}
.card h2{margin:0;font-size:16px;font-weight:700;line-height:1.35;text-wrap:balance}
.card .meta{display:flex;flex-wrap:wrap;gap:6px;font-size:11px;color:var(--muted);margin-top:auto}
.card .meta span{background:var(--chip);border-radius:6px;padding:2px 6px}
.card .meta .home{color:var(--accent)}
.card .meta .time{background:none;padding-left:0}
.card .heart{position:absolute;top:8px;right:8px;width:34px;height:34px;border-radius:50%;background:rgba(255,253,250,.9);display:grid;place-items:center;color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,.2)}
.card.picked .heart{background:var(--accent);color:var(--accent-ink)}
.card.picked{outline:2px solid var(--accent);outline-offset:-2px}
.empty{grid-column:1/-1;text-align:center;color:var(--muted);padding:40px 0}

.bar{position:fixed;left:0;right:0;bottom:0;z-index:6;background:var(--surface);border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));box-shadow:0 -6px 20px rgba(60,40,20,.08);transform:translateY(110%);transition:transform .2s;max-height:45vh;overflow-y:auto}
.bar.show{transform:none}
.bar-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:8px}
.bar-head b{font-size:12px;color:var(--muted);letter-spacing:.06em;font-weight:500}
.bar-doneall{flex:none;color:var(--accent);font-size:13px;font-weight:600;padding:4px 2px}
.bar-chips{display:flex;flex-wrap:wrap;gap:8px}
.bar-chip{display:inline-flex;align-items:center;gap:8px;background:var(--chip);border-radius:999px;padding:6px 6px 6px 14px;font-size:14px;font-weight:500;max-width:100%}
.bar-chip span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bar-chip button{flex:none;width:24px;height:24px;border-radius:50%;background:var(--accent);color:var(--accent-ink);display:grid;place-items:center}
@media (prefers-reduced-motion:reduce){.bar,.card{transition:none}}

.sheet{position:fixed;inset:0;z-index:10;background:var(--bg);overflow-y:auto;display:none}
.sheet.open{display:block}
.sheet .hero{position:relative;aspect-ratio:4/3;max-height:52vh;background:var(--chip)}
.sheet .hero img{width:100%;height:100%;object-fit:cover;display:block}
.sheet .back{position:absolute;top:calc(12px + env(safe-area-inset-top));left:12px;width:38px;height:38px;border-radius:50%;background:rgba(255,253,250,.92);color:#2A2320;display:grid;place-items:center;box-shadow:0 1px 3px rgba(0,0,0,.25)}
.sheet .inner{padding:18px 20px 40px;max-width:680px;margin:0 auto}
.sheet h2{margin:0 0 6px;font-size:24px;line-height:1.3;text-wrap:balance}
.sheet .sub{color:var(--muted);font-size:13px;display:flex;flex-wrap:wrap;gap:6px 12px;margin-bottom:12px}
.sheet .sub a{color:var(--muted)}
.sheet p.intro{margin:0 0 16px;color:var(--ink)}
.sheet h3{font-size:13px;letter-spacing:.12em;color:var(--muted);font-weight:500;margin:22px 0 8px;text-transform:uppercase}
.ings{display:grid;grid-template-columns:1fr 1fr;gap:4px 16px;margin:0;padding:0;list-style:none}
.ings li{display:flex;justify-content:space-between;gap:8px;padding:6px 0;border-bottom:1px dashed var(--line);font-size:15px}
.ings li span:last-child{color:var(--muted);text-align:right;flex:none;max-width:50%}
.steps{margin:0;padding:0;list-style:none;counter-reset:s}
.steps li{position:relative;padding:8px 0 8px 36px;counter-increment:s;border-bottom:1px solid var(--line)}
.steps li::before{content:counter(s);position:absolute;left:0;top:9px;width:24px;height:24px;border-radius:50%;background:var(--chip);color:var(--ink);font-size:12px;font-weight:700;display:grid;place-items:center;font-variant-numeric:tabular-nums}
.tips{background:var(--surface);border-left:3px solid var(--veg);padding:10px 14px;border-radius:0 10px 10px 0;white-space:pre-line;font-size:14px}
.sheet .pick{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;margin-top:26px;padding:14px;border-radius:14px;border:1.5px solid var(--accent);color:var(--accent);font-weight:700;font-size:16px}
.sheet .pick.on{background:var(--accent);color:var(--accent-ink)}
.toast{position:fixed;left:50%;bottom:calc(110px + env(safe-area-inset-bottom));transform:translateX(-50%);background:var(--ink);color:var(--bg);padding:10px 16px;border-radius:999px;font-size:14px;opacity:0;pointer-events:none;transition:opacity .2s;z-index:20;white-space:nowrap}
.toast.show{opacity:1}
</style>
</head>
<body>
<header>
  <div class="top">
    <h1 class="serif">今晚吃什么<small>拿手好菜</small></h1>
    <button class="dice" id="dice" type="button" aria-label="随机挑一道">🎲 随机一道</button>
  </div>
  <label class="search">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input id="q" type="search" placeholder="搜菜名或食材，比如“牛肉”" autocomplete="off">
  </label>
  <div class="chips" id="chips"></div>
</header>

<main>
  <p class="count" id="count"></p>
  <div class="grid" id="grid"></div>
</main>

<div class="bar" id="bar"><div id="barInner"></div></div>

<div class="sheet" id="sheet" role="dialog" aria-modal="true"></div>
<div class="toast" id="toast"></div>

<script id="data" type="application/json">__DATA__</script>
<script>
const R = JSON.parse(document.getElementById('data').textContent);
const byId = Object.fromEntries(R.map(r => [r.slug, r]));
const slugByOid = Object.fromEntries(R.map(r => [r.oid, r.slug]));
const TAGS = ['全部','自家拿手','荤菜','素菜','汤','主食','快手'];
let tag = '全部', q = '';
let orders = new Set();
let ordersAt = {};
let dbCol = null;

const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function renderChips(){
  $('#chips').innerHTML = TAGS.map(t => `<button class="chip" type="button" aria-pressed="${t===tag}" data-t="${t}">${t}</button>`).join('');
}
function filtered(){
  const s = q.trim().toLowerCase();
  return R.filter(r => (tag==='全部' || r.tags.includes(tag)) &&
    (!s || r.title.toLowerCase().includes(s) || r.ingredients.some(i => i.toLowerCase().includes(s))));
}
function renderGrid(){
  const list = filtered();
  $('#count').textContent = `${list.length} 道菜`;
  $('#grid').innerHTML = list.length ? list.map(r => `
    <button class="card ${orders.has(r.slug)?'picked':''}" type="button" data-s="${r.slug}">
      ${r.cover ? `<img class="ph" src="${esc(r.cover)}" alt="" loading="lazy">` : `<div class="ph"></div>`}
      <span class="heart" data-heart="${r.slug}" aria-label="${orders.has(r.slug)?'取消点单':'点这道菜'}">${heart(orders.has(r.slug))}</span>
      <div class="body">
        <h2 class="serif">${esc(r.title)}</h2>
        <div class="meta">
          ${r.tags.includes('自家拿手') ? '<span class="home">自家拿手</span>' : ''}
          ${r.tags.filter(t => t!=='自家拿手').map(t => `<span>${esc(t)}</span>`).join('')}
          ${r.time ? `<span class="time">${esc(r.time)}</span>` : ''}
        </div>
      </div>
    </button>`).join('') : `<div class="empty">没找到，换个词试试</div>`;
}
function heart(on){
  return `<svg width="18" height="18" viewBox="0 0 24 24" fill="${on?'currentColor':'none'}" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 21s-7-4.6-9.3-9A5.3 5.3 0 0 1 12 6.2 5.3 5.3 0 0 1 21.3 12C19 16.4 12 21 12 21z"/></svg>`;
}
function renderBar(){
  const list = [...orders].filter(s => byId[s]).sort((a,b) => (ordersAt[a]||0) - (ordersAt[b]||0));
  $('#bar').classList.toggle('show', list.length > 0);
  $('#barInner').innerHTML = list.length ? `
    <div class="bar-head"><b>已点 ${list.length} 道</b>${list.length>1 ? '<button class="bar-doneall" id="doneAll" type="button">全部做完</button>' : ''}</div>
    <div class="bar-chips">${list.map(s => `
      <span class="bar-chip"><span>${esc(byId[s].title)}</span><button data-done="${s}" type="button" aria-label="做完，取消点单">✓</button></span>`).join('')}</div>
  ` : '';
}
async function toggle(slug){
  const has = orders.has(slug);
  if (dbCol) {
    try {
      if (has) await dbCol.doc(byId[slug].oid).delete();
      else await dbCol.doc(byId[slug].oid).set({ title: byId[slug].title, at: Date.now() });
    } catch (e) { toast('同步失败，请重试'); }
    return; // UI updates from the onSnapshot echo
  }
  if (has) orders.delete(slug); else orders.add(slug);
  ordersAt[slug] = Date.now();
  saveLocal();
  renderGrid(); renderBar();
  const b = $('#sheet .pick'); if (b && b.dataset.s===slug) b.replaceWith(pickBtn(slug));
}
function pickBtn(slug){
  const on = orders.has(slug);
  const b = document.createElement('button');
  b.className = 'pick' + (on?' on':''); b.type='button'; b.dataset.s = slug;
  b.innerHTML = heart(on) + (on ? '已点 · 做好了点这里取消' : '点这道菜');
  b.onclick = () => toggle(slug);
  return b;
}
function saveLocal(){
  try { localStorage.setItem('orders', JSON.stringify([...orders])); } catch (e) {}
}
async function initSync(){
  try {
    if (window.claude && typeof window.claude.use === 'function') {
      const db = await window.claude.use('db');
      if (db) {
        dbCol = db.collection('orders');
        dbCol.onSnapshot(snap => {
          const known = snap.docs.filter(d => slugByOid[d.id]);
          orders = new Set(known.map(d => slugByOid[d.id]));
          ordersAt = Object.fromEntries(known.map(d => [slugByOid[d.id], (d.data()||{}).at || 0]));
          const openSlug = $('#sheet').classList.contains('open') && $('#sheet .pick')?.dataset.s;
          renderGrid(); renderBar();
          if (openSlug) { const b = $('#sheet .pick'); if (b) b.replaceWith(pickBtn(openSlug)); }
        }, () => { dbCol = null; loadLocal(); toast('无法同步点单，仅保存在本机'); });
        return;
      }
    }
  } catch (e) {}
  loadLocal();
}
function loadLocal(){
  try { orders = new Set(JSON.parse(localStorage.getItem('orders') || '[]').filter(s => byId[s])); } catch (e) { orders = new Set(); }
  renderGrid(); renderBar();
}
$('#bar').addEventListener('click', e => {
  const d = e.target.closest('[data-done]'); if (d) { toggle(d.dataset.done); return; }
  if (e.target.closest('#doneAll')) {
    const slugs = [...orders];
    if (dbCol) slugs.forEach(s => dbCol.doc(byId[s].oid).delete().catch(() => {}));
    else { orders.clear(); saveLocal(); renderGrid(); renderBar(); }
  }
});
function openSheet(slug){
  const r = byId[slug];
  const sh = $('#sheet');
  sh.innerHTML = `
    <div class="hero">${r.cover ? `<img src="${esc(r.cover)}" alt="${esc(r.title)}">` : ''}
      <button class="back" type="button" aria-label="返回"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg></button>
    </div>
    <div class="inner">
      <h2 class="serif">${esc(r.title)}</h2>
      <div class="sub">
        ${r.serves ? `<span>${esc(r.serves)}</span>` : ''}
        ${r.time ? `<span>约 ${esc(r.time)}</span>` : ''}
        ${r.source ? `<a href="${esc(r.source)}" target="_blank" rel="noopener">原菜谱 ↗</a>` : ''}
      </div>
      ${r.intro ? `<p class="intro">${esc(r.intro)}</p>` : ''}
      <h3>材料</h3>
      <ul class="ings">${r.ingredients.map(i => { const m = i.match(/^(.+?)\s+(\S+)$/); return m ? `<li><span>${esc(m[1])}</span><span>${esc(m[2])}</span></li>` : `<li><span>${esc(i)}</span></li>`; }).join('')}</ul>
      <h3>做法</h3>
      <ol class="steps">${r.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol>
      ${r.tips ? `<h3>小贴士</h3><div class="tips">${esc(r.tips)}</div>` : ''}
    </div>`;
  sh.querySelector('.inner').appendChild(pickBtn(slug));
  sh.querySelector('.back').onclick = closeSheet;
  sh.classList.add('open'); sh.scrollTop = 0;
  document.body.style.overflow = 'hidden';
  history.pushState({sheet:slug}, '');
}
function closeSheet(){
  $('#sheet').classList.remove('open');
  document.body.style.overflow = '';
  if (history.state && history.state.sheet) history.back();
}
window.addEventListener('popstate', () => { if ($('#sheet').classList.contains('open')) { $('#sheet').classList.remove('open'); document.body.style.overflow=''; } });

function toast(msg){ const t = $('#toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('show'), 1800); }

$('#chips').addEventListener('click', e => { const b = e.target.closest('.chip'); if (!b) return; tag = b.dataset.t; renderChips(); renderGrid(); });
$('#q').addEventListener('input', e => { q = e.target.value; renderGrid(); });
$('#grid').addEventListener('click', e => {
  const h = e.target.closest('[data-heart]'); if (h) { e.stopPropagation(); toggle(h.dataset.heart); return; }
  const c = e.target.closest('.card'); if (c) openSheet(c.dataset.s);
});
$('#dice').onclick = () => { const l = filtered(); if (!l.length) return; openSheet(l[Math.floor(Math.random()*l.length)].slug); };

renderChips(); renderGrid();
initSync();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
