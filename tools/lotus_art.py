#!/usr/bin/env python3
"""The lotus: the birth chart as twelve petals, and the dasha as the petals opening one at a time.

Sumant, 19 Nov 2026, 1:57 PM: "the natal chart is you. Different houses are different petals of you ... wisdom, emotion, courage,
wealth, prosperity, happiness, peace ... When Dasha comes, Dasha brings forth. That petal is now getting built up, and then that
petal is built up, and Dasha takes over in the end ... create a visual image like me, how can be shown, and then we can update
emergent Dasha visuals ... you are a lotus and life is ... developing your one petal at a time."

Panels 3 and 4 and the film are drawn on one person's chart. Every date and house comes from the Your 2027 engine through a
facts file that is kept out of this public repo (LOTUS_FACTS; the first draft, 19 Nov 2026, used Sumant's own chart), and the
pictures are written outside the repo too (LOTUS_OUT). The facts file holds: lagna, now, birth_year, natal {graha: house, rules},
chapters [{lord, start_y, end_y, frac, start, end, seasons [{lord, start, end, now}] on the running one}].
Petals sit where the Sky Clock's rooms sit: petal 12 at the top, petal 1 at one o'clock, clockwise.
Opened 19 Nov 2026: the four aims by house (dharma 1 5 9, artha 2 6 10, kama 3 7 11, moksha 4 8 12): en.wikipedia.org/wiki/Bhāva.
BPHS 48.2 reads a dasha by the house its lord rules (enjoylearningsanskrit.com/scriptures/parashara/chapter-48/verse-2).
"And the petal where it sits" is the usual practice, and Sutram's way of drawing it.

    python3 lotus_build.py            # four panels and a sheet
    python3 lotus_build.py --film     # and the film
"""
import sys, os, json, subprocess, shutil
sys.path.insert(0, '/home/claude/sutram-social/tools')
import look as L
from playwright.sync_api import sync_playwright
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); P = L.PAL['day']
OUT = os.environ.get('LOTUS_OUT', '/home/claude/_private/lotus/out')                  # pictures of a real chart stay out of the public repo
F = json.load(open(os.environ.get('LOTUS_FACTS', '/home/claude/_private/lotus_facts.json')))
AIM = {'purpose': '#E8C56E', 'means': '#9DB59A', 'desire': '#DDA088', 'release': '#A9C3DB'}
AIMS = ['purpose', 'means', 'desire', 'release']                       # houses 1 5 9, 2 6 10, 3 7 11, 4 8 12
PETAL = {1: ('Self', 'your body, your name, how you show up'), 2: ('Wealth', 'income, savings, family table, your voice'),
         3: ('Courage', 'skills, effort, siblings, short trips'), 4: ('Happiness', 'home, mother, property, peace of mind'),
         5: ('Creativity', 'ideas, children, romance, play'), 6: ('Service', 'daily work, routines, debts, rivals'),
         7: ('Partnership', 'spouse, clients, deals, the public'), 8: ('Depth', 'shared money, sudden turns, what is hidden'),
         9: ('Wisdom', 'mentors, beliefs, father, long travel, luck'), 10: ('Calling', 'public role, reputation, your work in the world'),
         11: ('Prosperity', 'income from your work, friends, wishes that land'), 12: ('Peace', 'sleep, retreat, far lands, letting go')}
ROLE = {'Sun': 'the king', 'Moon': 'the mother', 'Mars': 'the soldier', 'Mercury': 'the messenger', 'Jupiter': 'the teacher', 'Venus': 'the lover', 'Saturn': 'the auditor', 'Rahu': 'the magician', 'Ketu': 'the monk'}
opens = lambda g: sorted(set(F['natal'][g]['rules'] + [F['natal'][g]['house']]))
names = lambda hs: ', '.join(PETAL[h][0] for h in hs)
def also(hs): n = [PETAL[h][0] for h in hs]; return n[0] if len(n) == 1 else ', '.join(n[:-1]) + ' and ' + n[-1]
CH = F['chapters'][:9]                                                               # one full round, from the chapter of birth
NOW = next(c for c in CH if 'seasons' in c); SEA = next(s for s in NOW['seasons'] if s['now']); NXT = NOW['seasons'][NOW['seasons'].index(SEA) + 1]
DATA = dict(aim=AIM, petal={h: dict(name=PETAL[h][0], aim=AIMS[(h - 1) % 4]) for h in PETAL}, paper=P['bg'] if isinstance(P['bg'], str) and P['bg'].startswith('#') else '#FBF7EF',
            ink=P['ink'], ink2=P['ink2'], mute=P['mute'], brass=P['brass'], terra=P['terra'], flame=L.FLAME,
            chapters=[dict(lord=c['lord'], y0=max(c['start_y'], F['birth_year']), y1=c['end_y'], opens=opens(c['lord']), frac=c['frac']) for c in CH], now=CH.index(NOW), season=opens(SEA['lord']))
JS = r"""
const D = %DATA%, NS = 'http://www.w3.org/2000/svg';
function E(tag, a, parent){ const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); if (parent) parent.appendChild(e); return e; }
const PATH = 'M-4.2,-23 C-8,-38 -17.6,-50 -17.6,-66 C-17.6,-79 -6.5,-88 0,-104 C6.5,-88 17.6,-79 17.6,-66 C17.6,-50 8,-38 4.2,-23 Q0,-20.5 -4.2,-23 Z';
const INNER = 'M-2.6,-20 C-5.2,-27 -8,-33 -8,-40 C-8,-46.5 -3.2,-50 0,-58 C3.2,-50 8,-46.5 8,-40 C8,-33 5.2,-27 2.6,-20 Z';
/* st[h] = {grow: 0..1, tone: 0..1 (how strong the colour is), ring: 'chapter' | 'season' | null}; labels: 'all' | list of houses | null */
function lotus(svg, st, o){
  o = o || {}; while (svg.firstChild) svg.removeChild(svg.firstChild);
  const pad = o.labels ? 66 : 4; svg.setAttribute('viewBox', [-108 - pad, -108 - (o.labels ? 26 : 4), 216 + 2 * pad, 216 + (o.labels ? 52 : 8)].join(' '));
  const defs = E('defs', {}, svg), f = E('filter', {id: 'glow' + (o.id || ''), x: '-40%', y: '-40%', width: '180%', height: '180%'}, defs); E('feGaussianBlur', {stdDeviation: 3.2}, f);
  E('circle', {r: 107.5, fill: 'none', stroke: D.brass, 'stroke-width': .45, opacity: .34}, svg);
  const order = [...Array(12).keys()].map(i => i + 1).sort((a, b) => ((st[a] || {}).ring ? 1 : 0) - ((st[b] || {}).ring ? 1 : 0));
  order.forEach(h => { const s = st[h] || {grow: 0, tone: 0}, col = D.aim[D.petal[h].aim], g = E('g', {transform: 'rotate(' + (h * 30) + ')'}, svg);
    E('path', {d: PATH, fill: col, 'fill-opacity': .1, stroke: D.brass, 'stroke-width': .7, 'stroke-opacity': .5}, g);
    if (s.grow > 0.001){ const k = .42 + .58 * s.grow, tr = 'translate(0,-23) scale(' + k.toFixed(4) + ') translate(0,23)';
      if (s.ring === 'chapter') E('path', {d: PATH, transform: tr, fill: col, opacity: .55, filter: 'url(#glow' + (o.id || '') + ')'}, g);
      E('path', {d: PATH, transform: tr, fill: col, 'fill-opacity': (.3 + .7 * s.tone).toFixed(3)}, g);
      E('path', {d: 'M0,-58 L0,-93', transform: tr, stroke: '#FFFDF8', 'stroke-width': .7, 'stroke-opacity': .45, 'stroke-linecap': 'round'}, g); }
    if (s.ring === 'chapter') E('path', {d: PATH, fill: 'none', stroke: D.terra, 'stroke-width': 2.1, 'stroke-linejoin': 'round'}, g);
    if (s.ring === 'season'){ E('path', {d: PATH, fill: 'none', stroke: D.brass, 'stroke-width': 1.5, 'stroke-dasharray': '3.2 2.6'}, g); E('circle', {cx: 0, cy: -104, r: 4.6, fill: '#FFFDF8', stroke: D.brass, 'stroke-width': 1.6}, g); }
  });
  for (let h = 0; h < 12; h++) E('path', {d: INNER, transform: 'rotate(' + (h * 30 + 15) + ')', fill: '#FFFDF8', 'fill-opacity': .86, stroke: D.brass, 'stroke-width': .6, 'stroke-opacity': .6}, svg);
  E('circle', {r: 17.5, fill: '#FFFDF8', stroke: D.brass, 'stroke-width': .9}, svg);
  const fl = E('g', {transform: 'translate(-7.4 -10.2) scale(.148)'}, svg); E('path', {d: D.flame, fill: D.terra}, fl);
  if (o.labels){ for (let h = 1; h <= 12; h++){ const a = h * 30 * Math.PI / 180, sx = Math.sin(a), cy = -Math.cos(a), rl = 114, on = o.labels === 'all' || o.labels.includes(h);
      const t = E('text', {x: (rl * sx).toFixed(1), y: (rl * cy + (cy > .5 ? 9 : cy < -.5 ? -1 : 4)).toFixed(1), 'text-anchor': Math.abs(sx) < .3 ? 'middle' : sx > 0 ? 'start' : 'end', 'font-family': "'Cormorant Garamond', serif", 'font-weight': 600, 'font-size': on ? 12.5 : 11.5, fill: on ? D.ink : D.mute, 'fill-opacity': on ? 1 : .85}, svg);
      const n = E('tspan', {'font-family': 'Inter, sans-serif', 'font-size': 6.6, 'font-weight': 600, fill: D.brass, dy: -.6}, t); n.textContent = h + '  '; const w = E('tspan', {dy: .6}, t); w.textContent = D.petal[h].name; } }
}
"""
JS = JS.replace('%DATA%', json.dumps(DATA))
CSSX = f"""<style>.lot{{display:block}} .aims{{display:grid;grid-template-columns:repeat(4,auto);gap:10px 34px;justify-content:center;margin-top:26px}}
.aims div{{display:flex;flex-direction:column;align-items:center;gap:6px;font:600 25px/1.1 Inter;color:{P['ink']}}} .aims i{{width:20px;height:20px;border-radius:50%}} .aims span{{font:500 21px/1 Inter;color:{P['mute']};letter-spacing:.08em}}
.hold{{display:grid;grid-template-columns:1fr 1fr;gap:6px 44px;width:936px;text-align:left;margin-top:30px}} .hold .r{{display:grid;grid-template-columns:44px 1fr;gap:12px;align-items:start;padding:15px 0;border-top:1.5px solid {P['line']}}}
.hold .n{{font:600 22px/1 Inter;color:{P['brass']};padding-top:11px;display:flex;align-items:center;gap:8px}} .hold .n i{{width:13px;height:13px;border-radius:50%}}
.hold b{{display:block;font:600 41px/1.05 'Cormorant Garamond';color:{P['ink']}}} .hold span{{display:block;font:400 24.5px/1.32 Inter;color:{P['ink2']};margin-top:5px}}
.cap{{width:900px;text-align:left;margin-top:14px}} .cap .r{{display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:baseline;padding:12px 4px;border-top:1.5px solid {P['line']}}}
.cap .k{{font:600 20px/1.2 Inter;letter-spacing:.2em;text-transform:uppercase;color:{P['terra']}}} .cap b{{font:600 40px/1.05 'Cormorant Garamond';color:{P['ink']}}} .cap span{{display:block;font:400 28px/1.32 Inter;color:{P['ink2']};margin-top:4px}}
.grid9{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px 14px;width:936px;margin-top:14px}} .grid9 .c{{display:flex;flex-direction:column;align-items:center;text-align:center}}
.grid9 b{{font:600 37px/1.05 'Cormorant Garamond';color:{P['ink']};margin-top:2px}} .grid9 .y{{font:500 21px/1.2 Inter;color:{P['mute']};margin-top:4px}} .grid9 .p{{font:600 21.5px/1.25 Inter;color:{P['terra']};margin-top:5px;max-width:290px}}
.grid9 .now b{{color:{P['terra']}}} .tagnow{{font:600 15px/1 Inter;letter-spacing:.2em;color:#fff;background:{P['terra']};border-radius:999px;padding:5px 10px;margin-left:8px;vertical-align:6px}}</style>"""
T = lambda s, size=88: f'<div class="t" style="font-size:{size}px">{s}</div>'
SUB = lambda s, size=44: f'<div class="sub" style="margin-top:14px;font-size:{size}px">{s}</div>'
LAB = lambda s: f'<div class="lab" style="font-size:23px;margin-bottom:16px">{s}</div>'
SRC = lambda s: f'<div class="src" style="margin-top:6px;font-size:18.5px">{s}</div>'
def state_now():
    st = {}
    for i, c in enumerate(DATA['chapters'][:DATA['now'] + 1]):
        for h in c['opens']:
            cur = i == DATA['now']; old = st.get(h, dict(grow=0, tone=0, ring=None))
            st[h] = dict(grow=max(old['grow'], c['frac'] if cur else 1), tone=1 if cur else max(old['tone'], .62), ring='chapter' if cur else old['ring'])
    for h in DATA['season']:
        if st.get(h, {}).get('ring') != 'chapter': st[h] = dict(st.get(h, dict(grow=0, tone=0)), ring='season')
    return st
def panels():
    full = {h: dict(grow=1, tone=.9, ring=None) for h in range(1, 13)}
    p1 = (CSSX + LAB('Your birth chart') + T('You are a lotus', 98) + SUB('Twelve houses, twelve petals of you')
          + '<svg class="lot" id="L" width="900" height="640" style="margin-top:8px"></svg>'
          + '<div class="aims">' + ''.join(f'<div><i style="background:{AIM[a]}"></i>{n}<span>{h}</span></div>' for a, n, h in (('purpose', 'Purpose', '1 · 5 · 9'), ('means', 'Means', '2 · 6 · 10'), ('desire', 'Desire', '3 · 7 · 11'), ('release', 'Release', '4 · 8 · 12'))) + '</div>')
    j1 = JS + f"lotus(document.getElementById('L'), {json.dumps(full)}, {{labels: 'all'}});"
    rows = ''.join(f'<div class="r"><div class="n"><i style="background:{AIM[AIMS[(h - 1) % 4]]}"></i>{h}</div><div><b>{PETAL[h][0]}</b><span>{PETAL[h][1]}</span></div></div>' for h in (1, 7, 2, 8, 3, 9, 4, 10, 5, 11, 6, 12))
    p2 = CSSX + LAB('The twelve petals') + T('What each petal holds', 80) + f'<div class="hold">{rows}</div>'
    st = state_now(); lit = sorted(h for h, s in st.items() if s.get('ring'))
    g = NOW['lord']; s = SEA['lord']; n = NXT['lord']
    p3 = (CSSX + LAB('Your chart today · ' + F['now']) + T('The petals opening now', 80) + '<svg class="lot" id="L" width="900" height="584" style="margin-top:0"></svg>'
          + SRC('A graha opens the petals it rules and the petal it sits in') + '<div class="cap">'
          + f'<div class="r"><div class="k">Chapter</div><div><b>{g}, {ROLE[g]}</b><span>{NOW["start_y"]} to {NOW["end_y"]}. It builds {also(opens(g))}.</span></div></div>'
          + f'<div class="r"><div class="k">Season</div><div><b>{s}, {ROLE[s]}</b><span>Until {SEA["end"]}. It tends {also(opens(s))}.</span></div></div>'
          + f'<div class="r"><div class="k">Next</div><div><b>{n}, {ROLE[n]}</b><span>From {NXT["start"]}. It tends {also(opens(n))}.</span></div></div></div>')
    j3 = JS + f"lotus(document.getElementById('L'), {json.dumps(st)}, {{labels: {json.dumps(lit)}}});"
    cells = ''; calls = ''
    for i, c in enumerate(DATA['chapters']):
        stc = {h: dict(grow=(c['frac'] if i == DATA['now'] else 1), tone=1 if i <= DATA['now'] else .55, ring='chapter' if i == DATA['now'] else None) for h in c['opens']}
        cells += (f'<div class="c{" now" if i == DATA["now"] else ""}"><svg class="lot" id="m{i}" width="160" height="160"></svg><b>{c["lord"]}{"<span class=tagnow>NOW</span>" if i == DATA["now"] else ""}</b>'
                  f'<div class="y">{"Birth" if i == 0 else c["y0"]} to {c["y1"]}</div><div class="p">{names(c["opens"])}</div></div>')
        calls += f"lotus(document.getElementById('m{i}'), {json.dumps(stc)}, {{id: 'm{i}'}});"
    p4 = (CSSX + LAB('Your life in chapters') + T('One petal at a time', 80) + f'<div class="grid9">{cells}</div>'
          + f'<div class="sub" style="margin-top:14px;font-size:35px;max-width:900px">Inside each chapter, shorter seasons give every other petal its turn</div>')
    return [(p1, j1), (p2, ''), (p3, j3), (p4, JS + calls)]
FILM = r"""
const svg = document.getElementById('L'), cap = document.getElementById('cap'), yr = document.getElementById('yr'), sub = document.getElementById('sub');
const sm = (a, b, t) => { t = Math.min(1, Math.max(0, (t - a) / (b - a))); return t * t * (3 - 2 * t); };
const C = D.chapters, ROLE = %ROLE%, N = D.now;
// each chapter gets a slot on the film's clock: [start, end] in seconds; a hold after "now"
const slot = []; let t0 = 1.0; C.forEach((c, i) => { const d = i <= N ? 1.25 : .62; slot.push([t0, t0 + d]); t0 += d; if (i === N) t0 += 2.3; });
const END = t0;
window.__len = END + 2.4;
window.__fab = function(t){
  const st = {}; let cur = -1;
  C.forEach((c, i) => { const g = sm(slot[i][0], slot[i][1], t) * (i === N ? c.frac : 1); if (t >= slot[i][0]) cur = i;
    c.opens.forEach(h => { if (g > 0){ const o = st[h] || {grow: 0, tone: 0, ring: null}; st[h] = {grow: Math.max(o.grow, g), tone: Math.max(o.tone, i <= N ? .95 : .6), ring: o.ring}; } }); });
  const hold = t >= slot[N][1] && t < slot[N][1] + 2.3, done = t >= END;
  if (cur >= 0 && !done){ const live = t < slot[cur][1] + (cur === N ? 2.3 : 0); if (live) C[cur].opens.forEach(h => { if (st[h]) st[h].ring = 'chapter'; }); }
  if (hold) D.season.forEach(h => { if (st[h] && st[h].ring !== 'chapter') st[h].ring = 'season'; });
  if (done){ const k = sm(END, END + 1.2, t); for (let h = 1; h <= 12; h++){ const o = st[h] || {grow: 0, tone: 0}; st[h] = {grow: Math.max(o.grow, k), tone: Math.max(o.tone, .9 * k), ring: null}; } }
  lotus(svg, st, {labels: cur >= 0 && !done ? C[cur].opens.concat(hold ? D.season : []) : (done ? 'all' : [])});
  if (cur < 0){ yr.textContent = ''; cap.textContent = 'Twelve petals, still closed'; sub.textContent = ''; }
  else if (done){ yr.textContent = ''; cap.textContent = 'You are a lotus'; sub.textContent = 'Life opens it one petal at a time'; }
  else { const c = C[cur], f = Math.min(1, Math.max(0, (t - slot[cur][0]) / (slot[cur][1] - slot[cur][0]))) * (cur === N ? c.frac : 1);
    yr.textContent = hold ? 'Today' : String(Math.round(c.y0 + (c.y1 - c.y0) * f));
    cap.textContent = c.lord + ', ' + ROLE[c.lord]; sub.textContent = (cur > N ? 'Ahead: ' : hold ? 'This chapter builds ' : 'Builds ') + c.opens.map(h => D.petal[h].name).join(', '); }
};
window.__fab(0);
"""
def film_page():
    inner = (CSSX + LAB('Your life in chapters') + T('One petal at a time', 76) + '<svg class="lot" id="L" width="936" height="690" style="margin-top:8px"></svg>'
             + f'<div id="yr" style="font:600 30px/1 Inter;letter-spacing:.3em;color:{P["brass"]};height:34px;margin-top:6px"></div>'
             + f'<div id="cap" class="t" style="font-size:64px;margin-top:10px;height:70px"></div><div id="sub" class="sub" style="font-size:38px;margin-top:10px;height:50px"></div>')
    return inner, JS + FILM.replace('%ROLE%', json.dumps(ROLE))
def shoot(film=False):
    os.makedirs(OUT, exist_ok=True); outs = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=2)
        for i, (inner, js) in enumerate(panels(), 1):
            fn = f'{OUT}/_p{i}.html'; open(fn, 'w').write(L.page(P, 'Sutram · The lotus', inner, 7 + i * 13, 'arcs', 'word', js)); pg.goto('file://' + fn); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            ov = pg.evaluate("()=>{const b=document.querySelector('.body');return b.scrollHeight-b.clientHeight}")
            raw = f'{OUT}/_raw.png'; pg.screenshot(path=raw); o = f'{OUT}/lotus-{i}.jpg'; Image.open(raw).convert('RGB').resize((1080, 1350), Image.LANCZOS).save(o, quality=93, optimize=True); outs.append(o); os.remove(raw); os.remove(fn)
            print('panel', i, 'overflow', ov)
        b.close()
        if film:
            b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
            inner, js = film_page(); fn = f'{OUT}/_film.html'; open(fn, 'w').write(L.page(P, 'Sutram · The lotus', inner, 61, 'arcs', 'word', js)); pg.goto('file://' + fn); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            n = int(pg.evaluate('window.__len') * 30); tmp = f'{OUT}/_frames/'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
            for f in range(n): pg.evaluate('(t)=>window.__fab(t)', f / 30); pg.screenshot(path=tmp + f'f{f:04d}.jpg', type='jpeg', quality=92)
            part = f'{OUT}/_lotus.part.mp4'
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', tmp + 'f%04d.jpg', '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000', '-shortest', '-vf', 'format=yuv420p',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-r', '30', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', part], check=True)
            os.replace(part, f'{OUT}/lotus-one-petal-at-a-time.mp4'); print('film', n, 'frames')
            # a strip of frames to look at
            pick = [int(n * k / 7) for k in range(8)]; sheet = Image.new('RGB', (8 * 270 + 9 * 8, 338 + 16), '#E9E1D3')
            for k, f in enumerate(pick): sheet.paste(Image.open(tmp + f'f{min(f, n - 1):04d}.jpg').resize((270, 338), Image.LANCZOS), (8 + k * 278, 8))
            sheet.save(f'{OUT}/_film_strip.jpg', quality=88); shutil.rmtree(tmp, ignore_errors=True); os.remove(fn); b.close()
    sheet = Image.new('RGB', (2 * 1080 + 3 * 36, 2 * 1350 + 3 * 36), '#E9E1D3')
    for k, o in enumerate(outs): sheet.paste(Image.open(o), (36 + (k % 2) * 1116, 36 + (k // 2) * 1386))
    sheet.resize((sheet.width * 2 // 3, sheet.height * 2 // 3), Image.LANCZOS).save(f'{OUT}/lotus-draft.jpg', quality=90, optimize=True)
    sheet.resize((sheet.width // 3, sheet.height // 3), Image.LANCZOS).save(f'{OUT}/_small.jpg', quality=85)
if __name__ == '__main__': shoot('--film' in sys.argv)
