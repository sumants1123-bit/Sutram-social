"""Sutram post look, day and night (18 Nov 2026).
Sumant, 18 Nov 6:39 PM, on 'How a gemstone works': "I absolutely love this design ... zero changes". He asked for
a logo for the footer of every post, more posts in this light look, a feed that mixes dark and cream tiles, and
"mandala at the borders ... a minimal touch ... Indianish and unique". This module is that look in two palettes
(day = the gemstone post, night = its dark twin), three border ornaments and three footer marks to choose from."""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kolam
NM = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_modules')
CG = NM + '/@fontsource/cormorant-garamond/files/cormorant-garamond-latin-'
FONTS = ''.join(f"@font-face{{font-family:'Cormorant Garamond';font-weight:{w};font-style:{s};src:url('file://{CG}{w}-{s}.woff2')}}" for w, s in ((500, 'normal'), (600, 'normal'), (500, 'italic'), (600, 'italic')))
FONTS += f"@font-face{{font-family:Inter;font-weight:100 900;src:url('file://{NM}/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2')}}"
# 20 Nov 2026: the letters with marks used to write Sanskrit (ā ī ū ṛ ṣ ṭ ḍ ṇ ḥ ṃ ś) live in the latin-ext files. These faces
# only cover those letters (unicode-range), so every slide made before stays exactly as it was.
EXT = 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2C60-2C7F,U+A720-A7FF'
FONTS += ''.join(f"@font-face{{font-family:'Cormorant Garamond';font-weight:{w};font-style:{s};src:url('file://{NM}/@fontsource/cormorant-garamond/files/cormorant-garamond-latin-ext-{w}-{s}.woff2');unicode-range:{EXT}}}"
                 for w, s in ((500, 'normal'), (600, 'normal'), (500, 'italic'), (600, 'italic')))
FONTS += f"@font-face{{font-family:Inter;font-weight:100 900;src:url('file://{NM}/@fontsource-variable/inter/files/inter-latin-ext-wght-normal.woff2');unicode-range:{EXT}}}"

PAL = {
 'day': dict(name='day', ink='#1E2A44', ink2='#47536B', mute='#8B8577', brass='#A9813A', terra='#B4643F', line='#E4DCCB', card='#FFFFFF', cardsh='0 16px 36px rgba(30,42,68,.07)',
             orn='#A9813A', orn_op=.46, dot='#A9813A', flame='#B4643F', bead='#FFFDF8', paper='#FBF7EF',
             bg='radial-gradient(70% 45% at 12% 8%,rgba(246,211,190,.35),transparent 70%),radial-gradient(60% 40% at 92% 96%,rgba(207,224,239,.45),transparent 70%),radial-gradient(120% 80% at 50% 32%,#FFFDF8 0%,#FBF7EF 58%,#F4EDDF 100%)'),
 'night': dict(name='night', ink='#F4EAD3', ink2='rgba(244,234,211,.84)', mute='rgba(244,234,211,.52)', brass='#D9A57A', terra='#E7A070', line='rgba(217,165,122,.24)', card='rgba(255,240,214,.05)', cardsh='none',
               orn='#D9A57A', orn_op=.42, dot='#D9A57A', flame='#E7A070', bead='#F4EAD3', paper='#0D0A08',
               bg='radial-gradient(60% 38% at 50% 40%,rgba(150,88,44,.20) 0%,rgba(150,88,44,0) 100%),radial-gradient(70% 14% at 50% 100%,rgba(224,148,96,.09) 0%,rgba(224,148,96,0) 100%),radial-gradient(125% 95% at 50% 38%,#19120D 0%,#0D0A08 55%,#060504 100%)'),
}


def css(P):
    return f"""{FONTS}
*{{box-sizing:border-box}} body{{margin:0}}
.slide{{position:relative;width:1080px;height:1350px;overflow:hidden;color:{P['ink']};background:{P['bg']}}}
.kick{{position:absolute;top:66px;left:0;right:0;text-align:center;font:600 21px/1 Inter;letter-spacing:.36em;text-transform:uppercase;color:{P['brass']}}}
.foot{{position:absolute;bottom:46px;left:0;right:0;display:flex;flex-direction:column;align-items:center}}
.foot .s{{font:600 36px/1 'Cormorant Garamond';color:{P['ink']}}} .foot .u{{font:600 15px/1 Inter;letter-spacing:.34em;color:{P['mute']};margin-top:10px}}
.body{{position:absolute;top:128px;bottom:176px;left:72px;right:72px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}}
.lab{{font:600 23px/1.25 Inter;letter-spacing:.26em;text-transform:uppercase;color:{P['terra']}}}
.t{{font-family:'Cormorant Garamond';font-weight:600;font-variant-numeric:lining-nums;color:{P['ink']};line-height:1.02;letter-spacing:-.005em;text-wrap:balance}}
.h1{{font-size:118px}} .h2{{font-size:90px}} .h3{{font-size:72px}}
.sub{{font:italic 500 46px/1.18 'Cormorant Garamond';font-variant-numeric:lining-nums;color:{P['terra']};text-wrap:balance}}
.p{{font:400 40px/1.42 Inter;color:{P['ink2']};text-wrap:pretty}}
.card{{background:{P['card']};border:1.5px solid {P['line']};border-radius:30px;box-shadow:{P['cardsh']}}}
.card div{{text-wrap:pretty}}
.src{{font:600 19px/1.3 Inter;letter-spacing:.2em;text-transform:uppercase;color:{P['mute']}}}
"""


# ------------------------------------------------------------------ marks
FLAME = 'M50,128 C22,128 6,108 11,82 C15,58 38,44 43,3 C57,22 62,37 58,54 C66,50 72,42 74,30 C91,52 94,75 89,91 C84,113 70,128 50,128 Z'


def flame(x, y, h, col, cls='flame'):
    """the flame of Sutram's mark, h tall, standing on (x, y)"""
    s = h / 128
    return f'<g class="{cls}" data-x="{x}" data-y="{y}" transform="translate({x - 50 * s:.2f} {y - 128 * s:.2f}) scale({s:.4f})"><path d="{FLAME}" fill="{col}"/></g>'


def petal(r, w, ang):
    """a pointed lotus petal from the centre to r, turned by ang degrees"""
    d = f'M0,0 C{.22 * r:.1f},{-w:.1f} {.66 * r:.1f},{-w:.1f} {r:.1f},0 C{.66 * r:.1f},{w:.1f} {.22 * r:.1f},{w:.1f} 0,0 Z'
    return f'<path class="pet" d="{d}" transform="rotate({ang})"/>'


def mark_seal(size, P, sw=None):
    """A: the mark Sumant already uses (the chart square with its diagonals, three petals and the flame), as fine line"""
    R = 50; sw = sw or 3.2; c = P['orn']
    o = [f'<svg class="mk seal" viewBox="-70 -78 140 148" width="{size * 140 / 148:.1f}" height="{size}" style="overflow:visible">',
         f'<g fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round">',
         f'<rect class="sq" x="{-R}" y="{-R}" width="{2 * R}" height="{2 * R}"/><path class="dg" d="M{-R},{-R} L{R},{R} M{R},{-R} L{-R},{R}"/></g>',
         f'<g fill="{P["paper"]}" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round">{petal(64, 27, 180)}{petal(64, 27, 0)}{petal(64, 27, 90)}</g>',
         flame(0, 4, 78, P['flame']), '</svg>']
    return ''.join(o)


KOLAM_WALLS = (((0, 0), (0, 1)), ((0, 1), (0, 2)), ((2, 0), (2, 1)), ((2, 1), (2, 2)))


def mark_kolam(size, P, sw=7.5, colour=False):
    """B: nine dots, one unbroken thread (a kolam); the middle dot is the flame"""
    d, n = kolam.path(KOLAM_WALLS, 100, 0, 0); assert n == 1
    cols = ['#B9B4AE', '#C2643A', '#6C8F6A', '#D8B25A', None, '#E9E2D2', '#4B5C8C', '#8A6A4A', '#77706A']
    dots = ''
    for k, (x, y) in enumerate(kolam.dots(100, 0, 0)):
        if k == 4: continue
        dots += f'<circle class="kd" data-x="{x}" data-y="{y}" cx="{x}" cy="{y}" r="9" fill="{(cols[k] if colour else P["dot"])}"/>'
    return (f'<svg class="mk kolam" viewBox="-12 -12 324 324" width="{size}" height="{size}" style="overflow:visible">'
            f'<path class="thr" d="{d}" fill="none" stroke="{P["orn"]}" stroke-width="{sw}" stroke-linejoin="round" pathLength="1000"/>{dots}{flame(150, 172, 46, P["flame"])}</svg>')


def mark_thread(width, P, sw=2.2, n=9):
    """C: one thread, eight beads and the flame as the ninth"""
    W, H = 300, 44; y = 34; xs = [150 + (k - 4) * 26 for k in range(9)]
    beads = ''.join(f'<circle class="bd" data-x="{x}" data-y="{y}" cx="{x}" cy="{y}" r="5.4" fill="{P["bead"]}" stroke="{P["orn"]}" stroke-width="{sw}"/>' for k, x in enumerate(xs) if k != 4)
    return (f'<svg class="mk thread" viewBox="0 0 {W} {H}" width="{width}" height="{width * H / W:.1f}" style="overflow:visible">'
            f'<line class="ln" x1="6" y1="{y}" x2="{W - 6}" y2="{y}" stroke="{P["orn"]}" stroke-width="{sw}" stroke-linecap="round"/>{beads}{flame(150, y + 1, 31, P["flame"])}</svg>')


def footer(P, kind='word', url='ASKSUTRAM.COM'):
    w = f'<div class="s">Sutram</div><div class="u">{url}</div>'
    if kind == 'seal': return f'<div class="foot"><div style="display:flex;align-items:center;gap:18px">{mark_seal(78, P)}<div style="text-align:left"><div class="s" style="font-size:44px">Sutram</div><div class="u" style="margin-top:9px">{url}</div></div></div></div>'
    if kind == 'kolam': return f'<div class="foot"><div style="display:flex;align-items:center;gap:20px">{mark_kolam(78, P, sw=9)}<div style="text-align:left"><div class="s" style="font-size:44px">Sutram</div><div class="u" style="margin-top:9px">{url}</div></div></div></div>'
    if kind == 'thread': return f'<div class="foot"><div style="line-height:0;margin-bottom:9px">{mark_thread(330, P)}</div><div class="s" style="font-size:40px">Sutram</div><div class="u">{url}</div></div>'
    return f'<div class="foot">{w}</div>'


# ------------------------------------------------------------------ borders
def _arc(p0, c, p1, beads, P):
    o = [f'<path d="M{p0[0]},{p0[1]} Q{c[0]},{c[1]} {p1[0]},{p1[1]}" fill="none" stroke="{P["orn"]}" stroke-opacity=".38" stroke-width="1.6"/>']
    for t, col, rr in beads:
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0]; y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]
        o.append(f'<circle class="ab" data-arc="{p0[0]},{p0[1]},{c[0]},{c[1]},{p1[0]},{p1[1]},{t}" cx="{x:.1f}" cy="{y:.1f}" r="{rr}" fill="{col}" stroke="{P["orn"]}" stroke-opacity=".6" stroke-width="1.2"/>')
    return ''.join(o)


def _dust(seed, P, n=26):
    r = random.Random(seed)
    return ''.join(f'<circle class="dst" cx="{r.uniform(20, 1060):.0f}" cy="{r.uniform(20, 1330):.0f}" r="{r.choice([1.2, 1.6, 2])}" fill="{P["orn"]}" opacity="{r.uniform(.12, .3):.2f}"/>' for _ in range(n))


def _ring_petals(cx, cy, a, b, n, P, a0=0, sw=1.5, op=None, fill='none'):
    """a ring of n pointed petals between radius a and b"""
    op = P['orn_op'] if op is None else op; o = []
    for k in range(n):
        th = math.radians(a0 + k * 360 / n); dl = math.pi / n
        p = lambda r, t: (cx + r * math.cos(t), cy + r * math.sin(t))
        x0, y0 = p(a, th - dl); x1, y1 = p(b, th); x2, y2 = p(a, th + dl)
        c0 = p(a + (b - a) * .62, th - dl * .86); c1 = p(a + (b - a) * .62, th + dl * .86)
        o.append(f'<path d="M{x0:.1f},{y0:.1f} Q{c0[0]:.1f},{c0[1]:.1f} {x1:.1f},{y1:.1f} Q{c1[0]:.1f},{c1[1]:.1f} {x2:.1f},{y2:.1f}" fill="{fill}" stroke="{P["orn"]}" stroke-opacity="{op}" stroke-width="{sw}" stroke-linejoin="round"/>')
    return ''.join(o)


def _quarter_mandala(cx, cy, P, scale=1.0, bead_at=None, rot=0):
    """a mandala whose centre sits on the corner of the slide, so a quarter of it shows; its outer ring is the thread with beads"""
    c = P['orn']; op = P['orn_op']; S = scale; o = []
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{34 * S:.0f}" fill="none" stroke="{c}" stroke-opacity="{op}" stroke-width="1.5"/>')
    o.append(_ring_petals(cx, cy, 34 * S, 92 * S, 16, P, a0=rot + 11.25))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{100 * S:.0f}" fill="none" stroke="{c}" stroke-opacity="{op * .8:.2f}" stroke-width="1.2"/>')
    o.append(_ring_petals(cx, cy, 100 * S, 168 * S, 24, P, a0=rot + 7.5))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{178 * S:.0f}" fill="none" stroke="{c}" stroke-opacity="{op * .8:.2f}" stroke-width="1.2"/>')
    for k in range(72):
        th = math.radians(k * 5 + rot); x = cx + 192 * S * math.cos(th); y = cy + 192 * S * math.sin(th)
        if -4 < x < 1084 and -4 < y < 1354: o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.1" fill="{c}" opacity="{op + .1:.2f}"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{236 * S:.0f}" fill="none" stroke="{c}" stroke-opacity=".38" stroke-width="1.6"/>')
    for ang, col, rr in (bead_at or []):
        th = math.radians(ang); x = cx + 236 * S * math.cos(th); y = cy + 236 * S * math.sin(th)
        o.append(f'<circle class="mb" data-ring="{cx},{cy},{236 * S:.1f},{ang}" cx="{x:.1f}" cy="{y:.1f}" r="{rr}" fill="{col}" stroke="{c}" stroke-opacity=".6" stroke-width="1.2"/>')
    return ''.join(o)


def _buti(x, y, s, P, op=None):
    """a small four-petal flower"""
    op = P['orn_op'] + .12 if op is None else op
    pt = lambda a: f'<path d="M0,0 C{.3 * s:.1f},{-.34 * s:.1f} {.72 * s:.1f},{-.3 * s:.1f} {s},0 C{.72 * s:.1f},{.3 * s:.1f} {.3 * s:.1f},{.34 * s:.1f} 0,0 Z" transform="rotate({a})"/>'
    return f'<g transform="translate({x} {y})" fill="none" stroke="{P["orn"]}" stroke-opacity="{op:.2f}" stroke-width="1.4">{pt(45)}{pt(135)}{pt(225)}{pt(315)}<circle r="2" fill="{P["orn"]}" stroke="none" opacity=".8"/></g>'


def _frame(P, m=30, r=30):
    """a fine double rule with scooped corners and a small flower in each, like the border of a manuscript page"""
    c = P['orn']; op = P['orn_op']; W, H = 1080, 1350
    def rule(m, r, sw, o):
        return (f'<path d="M{m + r},{m} L{W - m - r},{m} A{r},{r} 0 0 0 {W - m},{m + r} L{W - m},{H - m - r} A{r},{r} 0 0 0 {W - m - r},{H - m} L{m + r},{H - m} A{r},{r} 0 0 0 {m},{H - m - r} L{m},{m + r} A{r},{r} 0 0 0 {m + r},{m} Z" '
                f'fill="none" stroke="{c}" stroke-opacity="{o:.2f}" stroke-width="{sw}"/>')
    o = [rule(m, r, 1.6, op), rule(m + 9, r - 2, 1, op * .7)]
    for x, y in ((m + 4, m + 4), (W - m - 4, m + 4), (m + 4, H - m - 4), (W - m - 4, H - m - 4)): o.append(_buti(x, y, 15, P))
    return ''.join(o)


def _braid(y, P, u=30, amp=8.5, flip=1):
    """a row of dots with one thread weaving round them: beads on a thread, as a border"""
    c = P['orn']; op = P['orn_op']; W = 1080; pts1, pts2 = [], []
    n = int(W / u) + 2; x0 = (W - (n - 1) * u) / 2
    for k in range(0, (n - 1) * 8 + 1):
        x = x0 + k * u / 8; ph = math.pi * (x - x0) / u
        pts1.append(f'{x:.1f},{y + amp * math.cos(ph):.1f}'); pts2.append(f'{x:.1f},{y - amp * math.cos(ph):.1f}')
    dots = ''.join(f'<circle cx="{x0 + k * u:.1f}" cy="{y}" r="2.4" fill="{c}" opacity="{op + .2:.2f}"/>' for k in range(n))
    return (f'<polyline points="{" ".join(pts1)}" fill="none" stroke="{c}" stroke-opacity="{op:.2f}" stroke-width="1.4"/>'
            f'<polyline points="{" ".join(pts2)}" fill="none" stroke="{c}" stroke-opacity="{op:.2f}" stroke-width="1.4"/>{dots}')


def decor(P, seed=1, border='arcs'):
    o = [_dust(seed, P)]
    if border == 'arcs':
        o += [_arc((700, -20), (960, 70), (1110, 230), [(.35, P['bead'], 5), (.6, P['bead'], 5), (.84, P['terra'], 8)], P),
              _arc((-30, 1150), (300, 1110), (560, 1380), [(.16, P['bead'], 5), (.36, P['bead'], 5), (.56, P['bead'], 5)], P)]
    elif border == 'mandala':
        o += [_quarter_mandala(1080, 0, P, 1.0, [(118, P['bead'], 5), (141, P['bead'], 5), (160, P['terra'], 8)]),
              _quarter_mandala(0, 1350, P, 1.0, [(-66, P['bead'], 5), (-44, P['bead'], 5), (-22, P['bead'], 5)])]
    elif border == 'frame':
        o += [_frame(P)]
    elif border == 'braid':
        o += [_braid(30, P), _braid(1320, P)]
    return f'<svg width="1080" height="1350" style="position:absolute;inset:0">{"".join(o)}</svg>'


def page(P, kick, inner, seed=1, border='arcs', foot='word', js=''):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{css(P)}</style></head><body><div class="slide">{decor(P, seed, border)}'
            f'<div class="kick">{kick}</div><div class="body">{inner}</div>{footer(P, foot)}</div>' + (f'<script>{js}</script>' if js else '') + '</body></html>')
