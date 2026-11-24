"""Two drawings for the day and night look (tools/look.py), made 24 Nov 2026 for the first post under rules_23nov
(Rahu and Ketu change signs, Sun 29 Nov): a wheel of the twelve signs, and the sky laid flat with the two paths.

zodiac(P, size, ...)  the twelve signs as a ring, Aries in the middle at the top, going clockwise.
    Rahu and Ketu can stand inside it (given by sidereal longitude) with the line between them through the middle,
    their old place can show as a dashed ghost with an arrow, houses can be counted from a Moon sign, some houses ringed.
    mode 'shift': the two fade back to the old place and walk backward to the new one.
    mode 'count': the houses are counted one by one from the Moon sign, then the rings, then Rahu and Ketu.
strip(P, size, ...)  the sky around Earth laid flat: the Sun's path as a straight line, the Moon's path as a wave that
    crosses it twice, at Rahu (going up) and at Ketu (going down). The Sun waits at Rahu.
    mode 'orbit': the Moon runs once along its path; at Rahu it hides the Sun, at Ketu, full and across from the Sun, it darkens.

Every drawing is made in its finished state, which is the still; MOTION (appended to the page by tools/render_look.py)
moves it and comes back to that state at the end of the 8 s loop."""
import math

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
NODE = {'rahu': {'day': '#7D90C4', 'night': '#A9B9D6'}, 'ketu': {'day': '#D9824F', 'night': '#E09460'}}
SUN = '#F29A5C'; SUN_LINE = '#E9874A'


def _xy(r, th):
    """clock angle th in degrees (0 = top, clockwise) to SVG x, y"""
    a = math.radians(th); return r * math.sin(a), -r * math.cos(a)


def _clock(lon):
    """sidereal longitude to clock angle: Aries 0 to 30 is centred on the top"""
    return (lon - 15) % 360


def _wedge(r0, r1, a0, a1):
    x0, y0 = _xy(r1, a0); x1, y1 = _xy(r1, a1); x2, y2 = _xy(r0, a1); x3, y3 = _xy(r0, a0)
    return f'M{x0:.2f},{y0:.2f} A{r1},{r1} 0 0 1 {x1:.2f},{y1:.2f} L{x2:.2f},{y2:.2f} A{r0},{r0} 0 0 0 {x3:.2f},{y3:.2f} Z'


def node_marker(kind, x, y, P, r=8.0, cls='', op=1.0, ghost=False, extra=''):
    """Rahu or Ketu as a shadow point: a dark disc with a coloured rim, like the node orbs of the Thread renderer"""
    rim = NODE[kind][P['name']]; disc = '#14110E' if P['name'] == 'day' else '#070504'
    if ghost:
        return (f'<g class="{cls}" transform="translate({x:.2f} {y:.2f})" opacity="{op}" {extra}>'
                f'<circle r="{r}" fill="none" stroke="{rim}" stroke-width="1.4" stroke-dasharray="2.4 2.2"/></g>')
    return (f'<g class="{cls}" transform="translate({x:.2f} {y:.2f})" opacity="{op}" {extra}>'
            f'<circle r="{r * 1.7:.2f}" fill="{rim}" opacity=".17"/><circle r="{r}" fill="{disc}"/>'
            f'<circle r="{r}" fill="none" stroke="{rim}" stroke-width="1.7"/><circle r="{r - 2.6:.2f}" fill="none" stroke="{rim}" stroke-opacity=".28" stroke-width=".7"/></g>')


def _tag(name, x, y, P, size, cls='zt', extra=''):
    return (f'<text class="{cls}" {extra} x="{x:.2f}" y="{y:.2f}" text-anchor="middle" font-family="Cormorant Garamond" font-style="italic" '
            f'font-weight="600" font-size="{size}" fill="{P["ink"]}">{name}</text>')


def zodiac(P, size=760, rahu=None, ketu=None, rahu_from=None, ketu_from=None, count_from=None, good=(), lit=(), mode='',
           labels=True, name_size=10.6, num_size=15.0, node_r=8.0, node_at=None, moon=False, tags=True, tag_size=10.5, inner=''):
    """size in px. rahu, ketu, rahu_from, ketu_from: sidereal longitudes. count_from: index of the Moon sign (Aries 0).
    good: house numbers to ring. lit: sign indices drawn warm. node_at: radius where Rahu and Ketu stand."""
    R1, R0 = 100.0, 72.0; gap = 1.1; o = []; uid = f'{int(size)}{len(lit)}{count_from}{mode}'
    warm = '#FFF1D2' if P['name'] == 'day' else 'rgba(217,165,122,.18)'
    base = '#FFFFFF' if P['name'] == 'day' else 'rgba(255,240,214,.05)'
    for k, s in enumerate(SIGNS):
        a0 = k * 30 - 15 + gap / 2; a1 = k * 30 + 15 - gap / 2
        o.append(f'<path class="zs" data-k="{k}" d="{_wedge(R0, R1, a0, a1)}" fill="{base}" stroke="{P["line"]}" stroke-width="1.1"/>')
        o.append(f'<path class="zh" data-k="{k}" d="{_wedge(R0, R1, a0, a1)}" fill="{warm}" stroke="{P["brass"]}" stroke-opacity=".75" stroke-width="1.4" opacity="{1 if k in lit else 0}"/>')
    if labels:
        defs = []
        for k, s in enumerate(SIGNS):
            c = k * 30; bottom = 90 < c < 270; fs = name_size * (.84 if len(s) > 9 else .9 if len(s) > 7 else 1)
            rr = (R0 + R1) / 2 + (fs * .32 if bottom else -fs * .32)
            if bottom:
                x0, y0 = _xy(rr, c + 14.6); x1, y1 = _xy(rr, c - 14.6); d = f'M{x0:.2f},{y0:.2f} A{rr:.2f},{rr:.2f} 0 0 0 {x1:.2f},{y1:.2f}'
            else:
                x0, y0 = _xy(rr, c - 14.6); x1, y1 = _xy(rr, c + 14.6); d = f'M{x0:.2f},{y0:.2f} A{rr:.2f},{rr:.2f} 0 0 1 {x1:.2f},{y1:.2f}'
            pid = f'zp{k}_{uid}'; defs.append(f'<path id="{pid}" d="{d}" fill="none"/>')
            col = P['ink'] if k in lit else P['ink2']; wt = 700 if k in lit else 600
            o.append(f'<text class="zn" data-k="{k}" font-family="Cormorant Garamond" font-weight="{wt}" font-size="{fs:.2f}" fill="{col}">'
                     f'<textPath href="#{pid}" startOffset="50%" text-anchor="middle">{s}</textPath></text>')
        o.insert(0, '<defs>' + ''.join(defs) + '</defs>')
    if count_from is not None:
        rn = 57.5
        for h in range(1, 13):
            k = (count_from + h - 1) % 12; x, y = _xy(rn, k * 30)
            if h in good:
                o.append(f'<circle class="zg" data-h="{h}" cx="{x:.2f}" cy="{y:.2f}" r="{num_size * .74:.2f}" fill="{"#FFF6DA" if P["name"] == "day" else "rgba(217,165,122,.16)"}" '
                         f'stroke="{P["brass"]}" stroke-width="1.5"/>')
            o.append(f'<text class="zc" data-h="{h}" x="{x:.2f}" y="{y + num_size * .34:.2f}" text-anchor="middle" font-family="Cormorant Garamond" font-weight="600" '
                     f'font-size="{num_size}" fill="{P["terra"] if h in good else P["ink"]}">{h}</text>')
    rn_node = node_at or (34.0 if count_from is not None else 50.0)
    if rahu is not None:
        ketu = rahu + 180 if ketu is None else ketu
        ar, ak = _clock(rahu), _clock(ketu)
        fr = _clock(rahu_from) if rahu_from is not None else ar
        fk = _clock(rahu_from + 180 if ketu_from is None else ketu_from) if rahu_from is not None else ak
        if rahu_from is not None:
            for kind, a_from, a_to in (('rahu', fr, ar), ('ketu', fk, ak)):
                gx, gy = _xy(rn_node, a_from); o.append(node_marker(kind, gx, gy, P, node_r, cls='zgh', op=.8, ghost=True))
                ra = rn_node + node_r * 1.9; da = (a_to - a_from + 540) % 360 - 180; sg = 1 if da > 0 else -1
                s0 = a_from + 6 * sg; s1 = a_to - 8 * sg
                x0, y0 = _xy(ra, s0); x1, y1 = _xy(ra, s1); tx, ty = _xy(ra, s1 - 2.5 * sg)
                hx, hy = x1 - tx, y1 - ty; L = math.hypot(hx, hy) or 1; hx, hy = hx / L, hy / L; px, py = -hy, hx; hs = 3.3
                o.append(f'<g class="zar"><path d="M{x0:.2f},{y0:.2f} A{ra:.2f},{ra:.2f} 0 0 {1 if sg > 0 else 0} {x1:.2f},{y1:.2f}" fill="none" stroke="{P["terra"]}" stroke-width="1.6" stroke-linecap="round"/>'
                         f'<path d="M{x1 + hx * hs:.2f},{y1 + hy * hs:.2f} L{x1 - hx * hs + px * hs:.2f},{y1 - hy * hs + py * hs:.2f} L{x1 - hx * hs - px * hs:.2f},{y1 - hy * hs - py * hs:.2f} Z" fill="{P["terra"]}"/></g>')
        rx_, ry_ = _xy(rn_node, ar); kx, ky = _xy(rn_node, ak)
        o.append(f'<line class="zax" x1="{rx_:.2f}" y1="{ry_:.2f}" x2="{kx:.2f}" y2="{ky:.2f}" stroke="{P["brass"]}" stroke-width="1.3" stroke-dasharray="1 3.2" stroke-linecap="round"/>')
        o.append(f'<circle cx="0" cy="0" r="2.3" fill="{P["brass"]}"/>')
        for kind, x, y, a, f in (('rahu', rx_, ry_, ar, fr), ('ketu', kx, ky, ak, fk)):
            gy = _xy(rn_node, f)[1]   # the name goes on the side away from the ghost, so the arrow stays clear
            dy = -(node_r + tag_size * .55) if (rahu_from is not None and gy > y + 1) else node_r + tag_size * 1.05
            meta = f'data-a="{a:.3f}" data-f="{f:.3f}" data-r="{rn_node}" data-dy="{dy:.2f}"'
            o.append(node_marker(kind, x, y, P, node_r, cls='zm', extra=meta))
            if tags: o.append(_tag(kind.capitalize(), x, y + dy, P, tag_size, extra=f'data-k="{kind}"'))
    if moon and count_from is not None:
        mx, my = _xy(rn_node, count_from * 30)
        o.append(f'<g class="zmoon" transform="translate({mx:.2f} {my:.2f})"><circle r="{node_r + 1:.1f}" fill="#FBF3E2" stroke="{P["brass"]}" stroke-width="1.2"/>'
                 f'<path d="M-2.4,-6 A6.4,6.4 0 1 0 -2.4,6 A5,5 0 1 1 -2.4,-6 Z" fill="{P["brass"]}" opacity=".6"/></g>')
        if tags: o.append(_tag('your Moon', mx, my + node_r + tag_size * 1.05, P, tag_size * .9))
    V = 106
    mid = f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);line-height:0">{inner}</div>' if inner else ''
    return (f'<div class="zodw" data-mode="{mode}" style="position:relative;flex:0 0 auto;width:{size:.1f}px;height:{size:.1f}px">'
            f'<svg viewBox="{-V} {-V} {2 * V} {2 * V}" width="{size:.1f}" height="{size:.1f}" style="display:block;overflow:visible;font-variant-numeric:lining-nums">{"".join(o)}</svg>{mid}</div>')


def strip(P, size=920, mode='', amp=32.0, labels=True, tag_size=9.5):
    """the sky laid flat, 220 units wide: Rahu a quarter of the way along, Ketu three quarters"""
    W = 220.0; xR, xK = -W / 4, W / 4; y = lambda x: -amp * math.sin(2 * math.pi * (x - xR) / W)
    mc = '#7686A8' if P['name'] == 'day' else '#C9D3E6'; o = []
    o.append(f'<line x1="{-W / 2}" y1="0" x2="{W / 2}" y2="0" stroke="{SUN_LINE}" stroke-width="2.6" stroke-linecap="round"/>')
    pts = ' '.join(f'{x:.2f},{y(x):.2f}' for x in (-W / 2 + W * k / 240 for k in range(241)))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{mc}" stroke-width="2.6" stroke-linecap="round"/>')
    for x in (-W / 2, W / 2):   # the two ends are the same place in the sky
        o.append(f'<circle cx="{x}" cy="0" r="1.6" fill="{SUN_LINE}"/>')
    o.append(node_marker('rahu', xR, 0, P, 5.6, cls='pn')); o.append(node_marker('ketu', xK, 0, P, 5.6, cls='pn'))
    if labels:
        o.append(_tag('Rahu', xR, -15.5, P, tag_size + 2))
        o.append(_tag('Ketu', xK - 4, 15, P, tag_size + 2).replace('text-anchor="middle"', 'text-anchor="end"'))
        small = lambda x, yy, t, col: (f'<text x="{x:.2f}" y="{yy:.2f}" text-anchor="middle" font-family="Inter" font-weight="600" '
                                       f'font-size="{tag_size * .72:.2f}" letter-spacing=".9" fill="{col}">{t}</text>')
        pill = lambda x, yy, t, col: (f'<rect x="{x - len(t) * tag_size * .27:.2f}" y="{yy - tag_size * .62:.2f}" width="{len(t) * tag_size * .54:.2f}" height="{tag_size * 1.24:.2f}" rx="{tag_size * .62:.2f}" '
                                      f'fill="{P["paper"]}" stroke="{col}" stroke-opacity=".55" stroke-width=".8"/>' + small(x, yy + tag_size * .25, t, col))
        o.append(pill(0, 0, 'THE SUN’S PATH', '#C9652E'))
        o.append(small(0, -amp - 7, 'THE MOON’S PATH', '#5E6E91' if P['name'] == 'day' else mc))
        o.append(small(0, amp + 13, 'THE SKY ALL AROUND US, LAID FLAT', P['mute']))
        o.append(f'<text class="pe1" x="{xR + 5:.2f}" y="15" text-anchor="start" font-family="Cormorant Garamond" font-style="italic" font-weight="600" font-size="{tag_size + 1}" fill="{P["terra"]}" opacity=".8">eclipse of the Sun</text>')
        o.append(f'<text class="pe2" x="{xK - 4:.2f}" y="{26:.2f}" text-anchor="end" font-family="Cormorant Garamond" font-style="italic" font-weight="600" font-size="{tag_size + 1}" fill="{P["terra"]}" opacity="0">eclipse of the Moon</text>')
    xs = xR; x0 = xR - 6.0; u0 = (x0 + W / 2) / W   # the still: the dark new Moon half over the Sun at Rahu
    lit0 = (1 - math.cos(2 * math.pi * (x0 - xs) / W)) / 2; c0 = [round(a + (b - a) * lit0) for a, b in zip((52, 47, 42), (244, 239, 230))]
    o.append(f'<g class="psun" transform="translate({xs:.2f} 0)"><circle r="12" fill="{SUN}" opacity=".2"/><circle r="7.6" fill="{SUN}"/>'
             f'<circle r="7.6" fill="none" stroke="#C9521F" stroke-opacity=".5" stroke-width=".8"/></g>')
    o.append(f'<g class="pmoon" data-u0="{u0:.4f}" data-w="{W}" data-amp="{amp}" data-xr="{xR}" data-xk="{xK}" data-xs="{xs}" transform="translate({x0:.2f} {y(x0):.2f})">'
             f'<circle class="pmd" r="7.2" fill="rgb({c0[0]},{c0[1]},{c0[2]})" stroke="{P["ink2"]}" stroke-opacity=".45" stroke-width=".8"/></g>')
    VX, VY = 118, amp + 18
    h = size * 2 * VY / (2 * VX)
    return (f'<div class="pathw" data-mode="{mode}" style="position:relative;flex:0 0 auto;width:{size:.1f}px;height:{h:.1f}px">'
            f'<svg viewBox="{-VX} {-VY} {2 * VX} {2 * VY}" width="{size:.1f}" height="{h:.1f}" style="display:block;overflow:visible;font-variant-numeric:lining-nums">{"".join(o)}</svg></div>')


MOTION = r"""(function(){
const sm=(a,b,t)=>{t=Math.min(1,Math.max(0,(t-a)/(b-a)));return t*t*(3-2*t)};
const pt=(r,a)=>{a=a*Math.PI/180;return [r*Math.sin(a),-r*Math.cos(a)]};
const lerpA=(a,b,p)=>{let d=((b-a+540)%360)-180;return a+d*p};
const zods=[...document.querySelectorAll('.body .zodw')].map(Z=>({mode:Z.dataset.mode,m:[...Z.querySelectorAll('.zm')],tg:[...Z.querySelectorAll('.zt')],ax:Z.querySelector('.zax'),
  gh:[...Z.querySelectorAll('.zgh')],ar:[...Z.querySelectorAll('.zar')],h:[...Z.querySelectorAll('.zh')],n:[...Z.querySelectorAll('.zc')],g:[...Z.querySelectorAll('.zg')],
  lit0:[...Z.querySelectorAll('.zh')].filter(e=>+e.getAttribute('opacity')>0).map(e=>+e.dataset.k)}));
function place(Z,at,op){   // put Rahu and Ketu (and their names and the line) at clock angles at[0], at[1]
  const xy=Z.m.map((e,i)=>{const r=+e.dataset.r;const [x,y]=pt(r,at[i]);e.setAttribute('transform',`translate(${x.toFixed(2)} ${y.toFixed(2)})`);e.setAttribute('opacity',op.toFixed(3));
   const tg=Z.tg.find(g=>g.dataset.k===(i?'ketu':'rahu'));if(tg){tg.setAttribute('x',x.toFixed(2));tg.setAttribute('y',(y+ +e.dataset.dy).toFixed(2));tg.setAttribute('opacity',op.toFixed(3));}return [x,y];});
  if(Z.ax&&xy.length===2){Z.ax.setAttribute('x1',xy[0][0].toFixed(2));Z.ax.setAttribute('y1',xy[0][1].toFixed(2));Z.ax.setAttribute('x2',xy[1][0].toFixed(2));Z.ax.setAttribute('y2',xy[1][1].toFixed(2));Z.ax.setAttribute('opacity',op.toFixed(3));}}
function zod(Z,t){
 if(Z.mode==='shift'){   // still: the new places. 1.2-1.7 s fade out, 1.9-2.4 s fade in at the old places, 2.4-6.2 s walk backward, 6.2-6.9 s ghosts and arrows return
  const out=sm(1.2,1.7,t)-sm(1.9,2.4,t), p=sm(2.4,6.2,t);
  place(Z,Z.m.map(e=>t<1.9?+e.dataset.a:lerpA(+e.dataset.f,+e.dataset.a,p)),1-out);
  const marks=t<1.9?1-sm(1.2,1.7,t):sm(6.2,6.9,t); Z.ar.forEach(e=>e.setAttribute('opacity',marks.toFixed(3))); Z.gh.forEach(e=>e.setAttribute('opacity',(.8*marks).toFixed(3)));
  const lit=t<1.9?1-sm(1.2,1.7,t):p; Z.h.forEach(e=>{if(Z.lit0.includes(+e.dataset.k))e.setAttribute('opacity',lit.toFixed(3));});}
 if(Z.mode==='count'){   // still: all there. 0.5-1.0 s it clears; from 1.3 s it counts 1 to 12 from the Moon; 4.9 s the rings; 5.7 s Rahu and Ketu
  const clear=sm(.5,1.0,t), keep=v=>(1-clear+Math.min(clear,v)).toFixed(3);
  Z.n.forEach(e=>{const h=+e.dataset.h;e.setAttribute('opacity',keep(sm(1.3+(h-1)*.28,1.5+(h-1)*.28,t)));});
  Z.g.forEach(e=>e.setAttribute('opacity',keep(sm(4.9,5.4,t))));
  const nodes=sm(5.7,6.3,t); Z.m.concat(Z.tg.filter(g=>g.dataset.k)).forEach(e=>e.setAttribute('opacity',keep(nodes))); if(Z.ax)Z.ax.setAttribute('opacity',keep(nodes));
  Z.h.forEach(e=>{if(Z.lit0.includes(+e.dataset.k))e.setAttribute('opacity',keep(nodes));});}
}
const mix=(c0,c1,p)=>`rgb(${c0.map((v,i)=>Math.round(v+(c1[i]-v)*p)).join(',')})`;
const pws=[...document.querySelectorAll('.body .pathw')].map(W=>{const m=W.querySelector('.pmoon');return m?{mode:W.dataset.mode,m,d:m.querySelector('.pmd'),u0:+m.dataset.u0,w:+m.dataset.w,amp:+m.dataset.amp,
  xr:+m.dataset.xr,xk:+m.dataset.xk,xs:+m.dataset.xs,s:W.querySelector('.psun'),e1:[...W.querySelectorAll('.pe1')],e2:[...W.querySelectorAll('.pe2')]}:null}).filter(Boolean);
function pw(W,t){   // the Moon runs once along its path in 8 s, left to right, starting from the still
 if(W.mode!=='orbit')return;
 const u=(W.u0+t/8)%1, x=-W.w/2+W.w*u, y=-W.amp*Math.sin(2*Math.PI*(x-W.xr)/W.w);
 W.m.setAttribute('transform',`translate(${x.toFixed(2)} ${y.toFixed(2)})`);
 const lit=(1-Math.cos(2*Math.PI*(x-W.xs)/W.w))/2, red=Math.max(0,1-Math.abs(x-W.xk)/11), cover=Math.max(0,1-Math.abs(x-W.xs)/12);
 W.d.setAttribute('fill',red>0?mix([244,239,230],[150,62,44],red):mix([52,47,42],[244,239,230],lit));
 if(W.s)W.s.setAttribute('opacity',(1-.25*cover).toFixed(3));
 W.e1.forEach(e=>e.setAttribute('opacity',Math.min(1,cover*1.6).toFixed(3))); W.e2.forEach(e=>e.setAttribute('opacity',Math.min(1,red*1.6).toFixed(3)));}
const prev=window.__fab; window.__fab=function(t){if(prev)prev(t); zods.forEach(Z=>zod(Z,t)); pws.forEach(W=>pw(W,t));};
window.__fab(0);})();"""
