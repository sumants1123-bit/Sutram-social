#!/usr/bin/env python3
"""Render a Sutram post in the day (cream) or night (dark) look of tools/look.py from a JSON spec.

    python3 tools/render_look.py specs/<id>.json [--motion] [--border arcs|mandala|frame|braid] [--foot word|seal|kolam|thread]

Sumant, 18 Nov 2026, on "How a gemstone works": "I absolutely love this design, the post, the visual, the animation, the
colors, the font size ... zero changes", and "this light theme, I love it. I want to have more posts around this light theme."
This is that look for the regular posts. The spec keeps the words of the Thread posts he praised on 16 Nov
(a small label, a title, a few short lines, a short list, a source), so tools/buffer_assets.py reads it unchanged.

Spec: {"id", "look": "day" | "night", "kicker", "border"?, "foot"?, "slides": [...]}
Slide types
  cover  orbs or art, title, subtitle, motion ("meet": the first graha walks in; "rise": the grahas rise; default: they breathe)
         any slide with "motion" also gets an mp4; a wheel moves by its own "mode" ("sweep" or "pick", tools/look_art.py)
  text   orbs?, label, title, body [lines], closing, note
  cast   label, title, items [{orbs or art, head, line, sub?}] cards with a graha or a drawing beside each
  grid   label, title, cols (2), cells [[label, head, line, lit?]], cellorbs?, closing, note
  rows   label, title, items [[key, line]]                    a number as key makes a numbered list
  stack  label, title, items [[label, line]]                  plain cards
  quote  label, quote, source, body
  any slide may add "sanskrit": a verse's own words in the italic serif under its title or quote
  cta    orbs?, title, subtitle, link (drawn in a ring, for a page to visit), lines, next
Writes posts/<id>/<id>-<n>.jpg, <id>-overview.jpg and, with --motion, <id>-1.mp4 (8 s loop; the first frame is the still).
A slide that does not fit is scaled down in steps; anything below .92 is reported and should be cut or split."""
import json, os, sys, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import look as L
import look_art as A
import render_thread as R
from playwright.sync_api import sync_playwright
from PIL import Image


def esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace("'", '’').replace('\n', '<br>')


def orb_box(o, P, s=1.0):
    """one graha from the Thread renderer, in a box as wide as its disc so rows and cards can place it"""
    r = o.get('r', 60) * s; q = dict(o); q['r'] = r
    if q.get('kind') == 'sun': q.setdefault('rings', False)
    svg = re.sub(r'style="display:block;margin:[^"]*"', 'style="display:block"', R.orb(q), count=1)
    k = 1.5 if o.get('kind') == 'saturn' else 1.0
    sh = 'filter:drop-shadow(0 12px 18px rgba(30,42,68,.20));' if P['name'] == 'day' else ''
    box = 2 * r + 20 * s
    return (f'<div class="orbw" style="position:relative;flex:0 0 auto;width:{box * k:.1f}px;height:{box:.1f}px;{sh}">'
            f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);line-height:0">{svg}</div></div>')


def art_html(a, P, s=1.0):
    """a drawing from tools/look_art.py: {"kind": "wheel", "size", "lit", "pick", "quarters", "dot", "mode", "moon": radius of a Moon in the middle}"""
    if a['kind'] == 'wheel':
        inner = orb_box({'kind': 'moon', 'r': a['moon']}, P, s) if a.get('moon') else ''
        return A.wheel(P, a.get('size', 520) * s, a.get('lit'), a.get('mode', ''), a.get('pick'), a.get('quarters', False), a.get('dot', False), inner, a.get('hole', .6))
    raise ValueError(a['kind'])


def orbs_row(orbs, P, s=1.0, gap=34):
    return f'<div style="display:flex;align-items:center;justify-content:center;gap:{gap * s:.1f}px">{"".join(orb_box(o, P, s) for o in orbs)}</div>'


def slide_html(sp, P, s=1.0):
    F = lambda px: f'{px * s:.1f}px'
    t = sp['type']; H = []
    art = orbs_row(sp['orbs'], P, s, sp.get('orbgap', 34)) if sp.get('orbs') else (f'<div style="display:flex;justify-content:center">{art_html(sp["art"], P, s)}</div>' if sp.get('art') else '')
    if t == 'cover':
        if art: H.append(f'<div class="art" style="margin-bottom:{F(40)}">{art}</div>')
        H.append(f'<div class="t" style="font-size:{F(sp.get("titlesize", 108))}">{esc(sp["title"])}</div>')
        if sp.get('subtitle'): H.append(f'<div class="sub" style="margin-top:{F(24)};font-size:{F(sp.get("subsize", 50))}">{esc(sp["subtitle"])}</div>')
        return ''.join(H)
    if art: H.append(f'<div class="art" style="margin-bottom:{F(30)}">{art}</div>')
    if sp.get('label'): H.append(f'<div class="lab" style="font-size:{F(23)}">{esc(sp["label"])}</div>')
    if sp.get('title'):
        n = max(len(x) for x in str(sp['title']).split('\n'))
        size = sp.get('titlesize') or (90 if n <= 18 else 78 if n <= 24 else 68)
        H.append(f'<div class="t" style="font-size:{F(size)};margin-top:{F(18 if sp.get("label") else 0)}">{esc(sp["title"])}</div>')
    if t == 'cta' and sp.get('subtitle'): H.append(f'<div class="sub" style="margin-top:{F(24)};font-size:{F(50)}">{esc(sp["subtitle"])}</div>')
    if t == 'quote':
        H.append(f'<div class="t" style="font-style:italic;font-weight:500;font-size:{F(sp.get("quotesize", 68))};line-height:1.12;margin-top:{F(26)}">“{esc(sp["quote"])}”</div>')
        if sp.get('source'): H.append(f'<div class="src" style="margin-top:{F(24)};font-size:{F(20)}">{esc(sp["source"])}</div>')
    if sp.get('sanskrit'):   # 20 Nov 2026: a verse's own words, in the italic serif under the title or quote
        H.append(f'<div class="sub" style="margin-top:{F(22)};font-size:{F(sp.get("sanskritsize", 40))}">{esc(sp["sanskrit"])}</div>')
    if t == 'cast':
        cards = ''
        for it in sp['items']:
            ic = orbs_row(it['orbs'], P, s, 6) if it.get('orbs') else (art_html(it['art'], P, s) if it.get('art') else '')
            sub = f'<div style="font:600 {F(sp.get("subsize", 22))}/1.35 Inter;letter-spacing:.04em;color:{P["terra"]};margin-top:{F(10)}">{esc(it["sub"])}</div>' if it.get('sub') else ''
            cards += (f'<div class="card" style="display:grid;grid-template-columns:{F(sp.get("iconw", 132))} 1fr;gap:{F(24)};align-items:center;padding:{F(24)} {F(30)};text-align:left">'
                      f'<div style="display:flex;justify-content:center">{ic}</div><div><div class="t" style="font-size:{F(sp.get("headsize", 54))}">{esc(it["head"])}</div>'
                      f'<div style="font:400 {F(sp.get("linesize", 33))}/1.4 Inter;color:{P["ink2"]};margin-top:{F(8)}">{esc(it["line"])}</div>{sub}</div></div>')
        H.append(f'<div style="display:flex;flex-direction:column;gap:{F(22)};width:930px;margin-top:{F(32)}">{cards}</div>')
    if t == 'grid':
        cols = sp.get('cols', 2); co = sp.get('cellorbs') or []; cells = ''
        lit = 'background:#FFF6DA;border-color:#EAD08A;' if P['name'] == 'day' else 'background:rgba(217,165,122,.14);border-color:rgba(217,165,122,.5);'
        for k, c in enumerate(sp['cells']):
            ob = f'<div style="display:flex;justify-content:center;margin-bottom:{F(8)}">{orb_box(co[k], P, s)}</div>' if k < len(co) else ''
            cells += (f'<div class="card" style="padding:{F(sp.get("cellpad", 20))} {F(12)};{lit if len(c) > 3 and c[3] else ""}">{ob}'
                      f'<div style="font:600 {F(sp.get("celllab", 19))}/1.2 Inter;letter-spacing:.2em;text-transform:uppercase;color:{P["terra"]}">{esc(c[0])}</div>'
                      f'<div class="t" style="font-size:{F(sp.get("cellsize", 50))};margin-top:{F(8)}">{esc(c[1])}</div>'
                      + (f'<div style="font:400 {F(sp.get("celltext", 28))}/1.3 Inter;color:{P["ink2"]};margin-top:{F(6)}">{esc(c[2])}</div>' if len(c) > 2 and c[2] else '') + '</div>')
        H.append(f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:{F(18)};width:920px;margin-top:{F(30)}">{cells}</div>')
    if t == 'rows':
        numbered = all(str(a).isdigit() for a, _ in sp['items']); rows = ''
        for a, b in sp['items']:
            if numbered:
                rows += (f'<div style="display:grid;grid-template-columns:{F(44)} 1fr;gap:{F(18)};align-items:baseline;padding:{F(20)} 4px;border-top:1.5px solid {P["line"]}">'
                         f'<div class="t" style="font-size:{F(40)};color:{P["terra"]}">{esc(a)}</div><div style="font:400 {F(40)}/1.38 Inter;color:{P["ink"]}">{esc(b)}</div></div>')
            else:
                rows += (f'<div style="display:grid;grid-template-columns:{F(sp.get("keyw", 210))} 1fr;gap:{F(22)};align-items:baseline;padding:{F(20)} 4px;border-top:1.5px solid {P["line"]}">'
                         f'<div class="t" style="font-size:{F(46)};color:{P["terra"]}">{esc(a)}</div><div style="font:400 {F(36)}/1.38 Inter;color:{P["ink"]}">{esc(b)}</div></div>')
        H.append(f'<div style="width:900px;text-align:left;margin-top:{F(30)}">{rows}</div>')
    if t == 'stack':
        cards = ''.join(f'<div class="card" style="padding:{F(22)} {F(30)};text-align:left"><div style="font:600 {F(20)}/1.2 Inter;letter-spacing:.2em;text-transform:uppercase;color:{P["terra"]}">{esc(a)}</div>'
                        f'<div class="t" style="font-size:{F(sp.get("linesize", 44))};line-height:1.12;margin-top:{F(8)}">{esc(b)}</div></div>' for a, b in sp['items'])
        H.append(f'<div style="display:flex;flex-direction:column;gap:{F(18)};width:920px;margin-top:{F(30)}">{cards}</div>')
    if sp.get('body'):
        H.append(''.join(f'<div class="p" style="font-size:{F(sp.get("bodysize", 40))};margin-top:{F(30 if k == 0 else 18)};max-width:880px">{esc(l)}</div>' for k, l in enumerate(sp['body'])))
    if t == 'cta':
        if sp.get('link'): H.append(f'<div style="display:inline-block;font:600 {F(46)}/1 Inter;color:{P["ink"]};margin-top:{F(44)};padding:{F(24)} {F(48)};border:2.5px solid {P["ink"]};border-radius:999px">{esc(sp["link"])}</div>')
        H.append(''.join(f'<div style="font:500 {F(36)}/1.45 Inter;color:{P["ink"]};margin-top:{F(40 if k == 0 else 6)}">{esc(l)}</div>' for k, l in enumerate(sp.get('lines', []))))
        if sp.get('next'): H.append(f'<div class="src" style="margin-top:{F(32)};font-size:{F(20)}">{esc(sp["next"])}</div>')
    if sp.get('closing'): H.append(f'<div class="sub" style="margin-top:{F(34)};font-size:{F(sp.get("closingsize", 46))};max-width:880px">{esc(sp["closing"])}</div>')
    if sp.get('note'): H.append(f'<div class="src" style="margin-top:{F(26)};font-size:{F(19)}">{esc(sp["note"])}</div>')
    return ''.join(H)


MOTION = r"""(function(){
const TAU=2*Math.PI, MODE=%MODE%, sm=(a,b,t)=>{t=Math.min(1,Math.max(0,(t-a)/(b-a)));return t*t*(3-2*t)};
const orbs=[...document.querySelectorAll('.body .orbw')];
const dust=[...document.querySelectorAll('.dst')].map((c,i)=>({c,o:+c.getAttribute('opacity'),k:1+i%3,p:i*1.37}));
const beads=[...document.querySelectorAll('.ab')].map((c,i)=>({c,q:c.dataset.arc.split(',').map(Number),p:i*.9}));
const ring=[...document.querySelectorAll('.mb')].map((c,i)=>({c,q:c.dataset.ring.split(',').map(Number),p:i*1.1}));
const wheels=[...document.querySelectorAll('.body .wheel')].map(W=>({mode:W.dataset.mode,ws:[...W.querySelectorAll('.wg')],pk:W.querySelector('.pk'),pke:W.querySelector('.pke'),qt:[...W.querySelectorAll('.qt')],mv:W.querySelector('.mv')}));
const bump=(a,d,t)=>t>a&&t<a+d?Math.sin(Math.PI*(t-a)/d):0;
function wheel(W,t){
 if(W.mode==='sweep'){   // all dim, the 27 light up in turn, then each nature glows in turn
  const dim=sm(.2,.9,t);
  W.ws.forEach(g=>{const i=+g.dataset.i,c=+g.dataset.c;const back=sm(1.0+i*.095,1.3+i*.095,t);let op=1-.74*(dim-Math.min(dim,back));
   let own=bump(4.0+c*.48,.46,t),other=0;for(let k=0;k<7;k++)if(k!==c)other=Math.max(other,bump(4.0+k*.48,.46,t));
   op*=1-.6*other;g.setAttribute('opacity',op.toFixed(3));g.setAttribute('transform',`scale(${(1+.07*own+.05*bump(1.0+i*.095,.3,t)).toFixed(4)})`);});}
 if(W.mode==='pick'){    // the Moon goes once round its road and stops; the star lights; it splits in four
  const off=sm(.2,.8,t),on=sm(4.0,4.6,t),lit=1-off+Math.min(off,on);
  if(W.pk)W.pk.setAttribute('opacity',(.26+.74*lit).toFixed(3));if(W.pke)W.pke.style.opacity=lit.toFixed(3);
  const q=1-off+Math.min(off,sm(4.8,5.4,t));W.qt.forEach(l=>l.style.opacity=q.toFixed(3));
  if(W.mv){const a=(+W.mv.dataset.a+360*sm(1.0,4.0,t))*Math.PI/180,r=+W.mv.dataset.r;W.mv.setAttribute('cx',(r*Math.cos(a)).toFixed(2));W.mv.setAttribute('cy',(r*Math.sin(a)).toFixed(2));}}}
window.__fab=function(t){const w=TAU*t/8;
 wheels.forEach(W=>wheel(W,t));
 dust.forEach(s=>s.c.setAttribute('opacity',(s.o*(.6+.4*Math.cos(w*s.k+s.p))/(.6+.4*Math.cos(s.p))).toFixed(3)));
 beads.forEach(b=>{const u=b.q[6]+.05*(Math.sin(w+b.p)-Math.sin(b.p));const [x0,y0,cx,cy,x1,y1]=b.q;
  b.c.setAttribute('cx',((1-u)*(1-u)*x0+2*(1-u)*u*cx+u*u*x1).toFixed(2));b.c.setAttribute('cy',((1-u)*(1-u)*y0+2*(1-u)*u*cy+u*u*y1).toFixed(2));});
 ring.forEach(b=>{const a=(b.q[3]+5*(Math.sin(w+b.p)-Math.sin(b.p)))*Math.PI/180;b.c.setAttribute('cx',(b.q[0]+b.q[2]*Math.cos(a)).toFixed(2));b.c.setAttribute('cy',(b.q[1]+b.q[2]*Math.sin(a)).toFixed(2));});
 const away=sm(.2,1.1,t)-sm(1.7,5.0,t);
 orbs.forEach((o,i)=>{let dx=0,dy=0;const k=1+.016*(Math.sin(w+i*1.3)-Math.sin(i*1.3));
  if(MODE==='meet'&&i===0)dx=-170*away; if(MODE==='rise')dy=54*away;
  o.style.transform=`translate(${dx.toFixed(2)}px,${dy.toFixed(2)}px) scale(${k.toFixed(4)})`;o.style.opacity=(MODE==='rise'?1-.55*away:1).toFixed(3);});};
window.__fab(0);})();"""


def render(spec_path, motion=False, border=None, foot=None):
    spec = json.load(open(spec_path)); pid = spec['id']; P = L.PAL[spec.get('look', 'day')]
    border = border or spec.get('border', 'arcs'); foot = foot or spec.get('foot', 'word')
    out = os.path.join(REPO, 'posts', pid); os.makedirs(out, exist_ok=True); outs = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=2)
        for i, sp in enumerate(spec['slides'], 1):
            kicker = sp.get('kicker', spec.get('kicker', 'Sutram')); seed = i * 13 + len(pid)
            for s in (1, .96, .92, .88, .84, .8, .76):
                html = L.page(P, esc(kicker), slide_html(sp, P, s), seed, border, foot)
                fn = os.path.join(out, f'_s{i}.html'); open(fn, 'w').write(html); pg.goto('file://' + fn); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
                ov = pg.evaluate("()=>{const b=document.querySelector('.body');return b.scrollHeight-b.clientHeight}")
                if ov <= 0: break
            if s < .92 or ov > 0: print(f'  ! {pid} slide {i}: scale {s}, overflow {ov}px: cut or split it')
            raw = os.path.join(out, f'_raw{i}.png'); pg.screenshot(path=raw)
            o = os.path.join(out, f'{pid}-{i}.jpg'); Image.open(raw).convert('RGB').resize((1080, 1350), Image.LANCZOS).save(o, quality=93, optimize=True, progressive=True); outs.append(o)
            os.remove(raw)
            if motion and (i == 1 or sp.get('motion')):
                mode = json.dumps(sp.get('motion', 'breathe'))
                open(fn, 'w').write(html.replace('</body>', f'<script>{MOTION.replace("%MODE%", mode)}</script></body>')); pg.goto('file://' + fn); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
                tmp = os.path.join(out, '_frames') + '/'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
                for f in range(240):
                    pg.evaluate('(t)=>window.__fab(t)', f / 30); pg.screenshot(path=tmp + f'f{f:04d}.jpg', type='jpeg', quality=92)
                part = os.path.join(out, f'_{pid}-{i}.part.mp4')
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', tmp + 'f%04d.jpg', '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000', '-shortest',
                                '-vf', 'scale=1080:1350:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-profile:v', 'high', '-level', '4.1', '-g', '30', '-keyint_min', '30',
                                '-sc_threshold', '0', '-bf', '2', '-flags', '+cgop', '-r', '30', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'aac', '-b:a', '96k', '-ar', '48000',
                                '-movflags', '+faststart', part], check=True)
                os.replace(part, os.path.join(out, f'{pid}-{i}.mp4')); shutil.rmtree(tmp, ignore_errors=True)
            os.remove(fn)
        b.close()
    n = len(outs); cols = min(4, n); rows = (n + cols - 1) // cols
    sheet = Image.new('RGB', (24 + cols * 384, 24 + rows * 474), (236, 230, 218) if P['name'] == 'day' else (5, 4, 3))
    for k, o in enumerate(outs):
        r, c = divmod(k, cols); sheet.paste(Image.open(o).resize((360, 450), Image.LANCZOS), (24 + c * 384, 24 + r * 474))
    sheet.save(os.path.join(out, f'{pid}-overview.jpg'), quality=88)
    print(pid, '->', n, 'slides', '+ moving cover' if motion else '')
    return outs


if __name__ == '__main__':
    a = sys.argv[1:]; opt = lambda k: a[a.index(k) + 1] if k in a else None
    for f in [x for x in a if x.endswith('.json')]: render(f, '--motion' in a, opt('--border'), opt('--foot'))
