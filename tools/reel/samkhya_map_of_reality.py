"""Sutram Reel: "What is reality made of?" Samkhya's map in 25 layers (The Thread, Maps of reality, part 1).

Asked by Sumant, Thu 26 Nov 2026 (Mexico, by voice): "as per Samkhya philosophy ... the universe is a superimposition ...
the subtler being the self or the observer, and then there comes intellect ... and then comes mind ... make a post and
then dynamic visual, really clearly in visual terms explaining the reality as per Samkhya ... and different models of
reality, different philosophies, visually explaining very beautifully." Posted as the Friday Thread of 4 Dec 2026 and the
week's video (rules_25nov). Built from the Ketu Reel model (tools/reel/ketu_facing_saturn.py): same look, kit and build.

Sources, every one opened on 26 Nov 2026 before use:
- Samkhya Karika of Ishvarakrishna (about 350 CE; Wikipedia, Samkhyakarika), verse meanings as in Raghavan Iyer's
  translation (Hermes, Sept 1987, theosophytrust.org/922-the-sankhya-karika-ishvarakrishna):
  3 root nature is not produced; the seven from intellect on are produced and producing; the sixteen are only produced;
    the Self is neither.  11 the manifest has the three gunas and is not conscious; the Self is the reverse.
  12, 13 the gunas: sattva buoyant and luminous, rajas exciting and moving, tamas heavy and enveloping; they work
    together, like a lamp.  18 there are many selves.  19 the Self is witness, solitary, neutral, spectator, non-agent.
  20 through contact with the Self the non-conscious seems conscious; agency belongs to the gunas, while the neutral Self
    seems to act.  21 the union, like a lame man and a blind man; from it creation proceeds.
  22 from nature comes intellect (mahat), from it the I-maker (ahamkara), from it the set of sixteen, and from five of
    those sixteen the five elements.  23 intellect is ascertainment.  24 the I-maker is self-assertion ("me, mine").
  25 the sattva side of the I-maker gives the eleven (mind and the ten organs); its tamas side (bhutadi) gives the five
    subtle elements; rajas drives both.  26 the five senses: eyes, ears, nose, tongue, skin; the five organs of action:
    voice, hands, feet, excretion, generation.  27 the mind is both, and it deliberates.  28 five organs only observe
    sound and the rest.  35 intellect, I-maker and mind are the guardians, the rest are the gates.
  38 the subtle elements are non-specific; from them come the five gross elements.  59 like a dancer who stops after
    showing herself to the audience, nature stops once she has shown herself to the Self.  66 one has seen, the other
    has been seen; nature desists.  68 the Self reaches kaivalya, aloneness.
- The mirror: the reflection theory of Vachaspati Mishra and Vijnana Bhikshu ("the mirror remains unchanged, but the
  image can be seen"), Ferenc Ruzsa, "Sankhya", Internet Encyclopedia of Philosophy (iep.utm.edu/Sankhya).
- Each element and its subtle element: space with sound, air with touch, fire with form, water with taste, earth with
  smell; ear hears, skin feels, eye sees, tongue tastes, nose smells (hinduwebsite.com/samkhya-tattvas.asp, after
  Vijnana Bhikshu).
- Brihat Parashara Hora Shastra 3.20: "agni-bhumi-nabhas-toya-vayavah ... bhaumadinam grahanam tattvani": fire, earth,
  ether (space), water and air are the tattvas of the grahas from Mars on: Mars, Mercury, Jupiter, Venus, Saturn
  (enjoylearningsanskrit.com/scriptures/parashara/chapter-3/verse-20).
No chart and no engine value in this post. The Samkhya order on screen is the Karika's (22): the seer, nature,
intellect, the I-maker, then mind; Sumant had said intellect, consciousness, mind; told to him with the post.

    python3 tools/reel/samkhya_map_of_reality.py stills 3 8.5 16.5 ...   look at every still at full size first
    python3 tools/reel/samkhya_map_of_reality.py build                   scenes, concat, drone, mux into posts/<ID>/
"""
import math, os, shutil, subprocess, sys
import numpy as np
import skia

W, H, FPS = 1080, 1920, 30
MX, TW = 96, 888

BG = (246, 240, 228)
NAVY, SLATE, WARM, RING = '#1E2A44', '#4E586C', '#756E61', '#D8CCB6'
LAV_FILL, LAV = '#ECE6F6', '#7E72B8'
APR_FILL, TERRA, TERRA_DK = '#FBE6D5', '#C2603E', '#8E3F22'
SAGE, SAGE_DK, SAGE_FILL = '#5E8A6A', '#3F6A4C', '#E3EADF'
POW_FILL, POW = '#E2EAF1', '#6F8FB0'
CHIP, CHIP_B = '#FBF7EF', '#E3D8C4'
ORANGE_DK = '#C8552A'
GOLD, GOLD_LT, GOLD_DK = '#D9A441', '#F6E3B0', '#9A6E1E'
SATTVA, RAJAS, TAMAS = '#D9A441', '#C2603E', '#4A5482'
GRAHA = {'Mars': '#C2643A', 'Mercury': '#6C8F6A', 'Jupiter': '#D8B25A', 'Venus': '#C79AB4', 'Saturn': '#4B5C8C'}
ELEM_FILL = {'space': '#ECE6F6', 'air': '#E2EAF1', 'fire': '#FBE6D5', 'water': '#DDEBEE', 'earth': '#EDE3D0'}

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ID = 'samkhya-map-of-reality'
FD = os.path.join(REPO, 'assets', 'fonts') + '/'
WORK = f'/tmp/reel/{ID}'
TF = {
    'fr600': skia.Typeface.MakeFromFile(FD + 'fraunces-latin-600-normal.ttf'),
    'fr500i': skia.Typeface.MakeFromFile(FD + 'fraunces-latin-500-italic.ttf'),
    'fr400i': skia.Typeface.MakeFromFile(FD + 'fraunces-latin-400-italic.ttf'),
    'in400': skia.Typeface.MakeFromFile(FD + 'Inter-Regular.otf'),
    'in500': skia.Typeface.MakeFromFile(FD + 'Inter-Medium.otf'),
}
assert all(TF.values())
_fonts = {}


def font(key, size):
    k = (key, size)
    if k not in _fonts:
        f = skia.Font(TF[key], size)
        f.setEdging(skia.Font.Edging.kAntiAlias)
        f.setSubpixel(True)
        _fonts[k] = f
    return _fonts[k]


def col(hexc, a=1.0):
    h = hexc.lstrip('#')
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(round(255 * max(0.0, min(1.0, a)))))


def mixhex(h1, h2, u):
    a = [int(h1.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(h2.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    return '#' + ''.join(f'{int(round(x + (y - x) * u)):02X}' for x, y in zip(a, b))


def paint(hexc, a=1.0, stroke=False, width=0.0, dash=None):
    p = skia.Paint(AntiAlias=True)
    p.setColor(col(hexc, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(width)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if dash:
        p.setPathEffect(skia.DashPathEffect.Make(dash, 0))
    return p


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ramp(t, t0, t1):
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return ease((t - t0) / (t1 - t0))


def lerp(a, b, u):
    return a + (b - a) * u


def text(c, s, x, y, f, hexc, a=1.0, align='left'):
    if a <= 0.003:
        return
    w = f.measureText(s)
    if align == 'center':
        x -= w / 2
    elif align == 'right':
        x -= w
    c.drawString(s, x, y, f, paint(hexc, a))


def wrap(s, f, maxw):
    lines, cur = [], ''
    for w_ in s.split():
        t_ = (cur + ' ' + w_).strip()
        if not cur or f.measureText(t_) <= maxw:
            cur = t_
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(c, s, x, y, f, hexc, a, lh, maxw=TW, align='left'):
    """wrapped text, first baseline at y; returns baseline of last line"""
    ls = wrap(s, f, maxw)
    for i, ln in enumerate(ls):
        text(c, ln, x, y + i * lh, f, hexc, a, align)
    return y + (len(ls) - 1) * lh


# ---------------- scene timing ----------------
S = [(0, 5), (5, 12), (12, 19), (19, 27), (27, 36), (36, 43), (43, 50), (50, 59), (59, 66), (66, 73), (73, 79)]
TOTAL = 79.0


def sa(t, i, delay=0.0, out=True):
    """alpha of text belonging to scene i (fade in after delay, fade out at scene end)"""
    s0, s1 = S[i]
    if t < s0 or t >= s1 + 0.001 and out:
        return 0.0
    a = ramp(t, s0 + 0.08 + delay, s0 + 0.65 + delay)
    if out and i < len(S) - 1:
        a *= 1 - ramp(t, s1 - 0.45, s1)
    return a


def slide(t, i, delay=0.0):
    s0, _ = S[i]
    return 22 * (1 - ramp(t, s0 + 0.08 + delay, s0 + 0.75 + delay))


def head(c, t, i, s, y=330, delay=0.0):
    a = sa(t, i, delay)
    return block(c, s, MX, y + slide(t, i, delay), font('fr500i', 70), NAVY, a, 82)


def body(c, t, i, s, y, delay=0.0, hexc=SLATE):
    a = sa(t, i, delay)
    return block(c, s, MX, y + slide(t, i, delay), font('in400', 42), hexc, a, 58)


def source(c, t, i, s, delay=1.2):
    """the source line, small, at the foot of the safe area"""
    a = sa(t, i, delay) * 0.95
    block(c, s, MX, 1468, font('in400', 28), WARM, a, 38)


# ---------------- drawing pieces ----------------
def rrect(c, x0, y0, x1, y1, r, fill, border, a, bw=2.5, dash=None):
    if a <= 0.003:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x0, y0, x1, y1), r, r)
    if fill:
        c.drawRRect(rr, paint(fill, a))
    if border:
        c.drawRRect(rr, paint(border, a, True, bw, dash))


def light(c, x, y, r, a, t, strength=1.0):
    """the seer: a steady light with a soft breathing halo"""
    if a <= 0.003:
        return
    br = 1 + 0.06 * math.sin(t * 2.1)
    R = r * (2.9 + 0.6 * strength) * br
    sh = skia.GradientShader.MakeRadial((x, y), R, [col(GOLD_LT, 0.95 * a), col(GOLD_LT, 0.45 * a), col(GOLD_LT, 0.0)], [0.0, 0.45, 1.0])
    p = skia.Paint(AntiAlias=True)
    p.setShader(sh)
    c.drawCircle(x, y, R, p)
    c.drawCircle(x, y, r * 1.28, paint(GOLD, 0.35 * a, True, 2))
    core = skia.GradientShader.MakeRadial((x - r * 0.25, y - r * 0.25), r * 1.2, [col('#FFF6DC', a), col(GOLD, a)], [0.0, 1.0])
    p2 = skia.Paint(AntiAlias=True)
    p2.setShader(core)
    c.drawCircle(x, y, r, p2)


def strand_path(x0, x1, yc, amp, wl, ph):
    p = skia.Path()
    first = True
    x = x0
    while x <= x1 + 0.1:
        # taper the ends so the braid starts and ends calmly
        env = min(1.0, (x - x0) / 60.0, (x1 - x) / 60.0)
        y = yc + amp * env * math.sin(2 * math.pi * (x - x0) / wl + ph)
        if first:
            p.moveTo(x, y)
            first = False
        else:
            p.lineTo(x, y)
        x += 4
    return p


def braid(c, x0, x1, yc, amp, wl, phase, a, width=7):
    if a <= 0.003:
        return
    for k, hexc in enumerate((TAMAS, RAJAS, SATTVA)):
        c.drawPath(strand_path(x0, x1, yc, amp, wl, phase + k * 2 * math.pi / 3), paint(hexc, a, True, width))


def swirl(c, x, y, R, t, a):
    """nature in scene 2: three strands looping round, never still"""
    if a <= 0.003:
        return
    for k, (hexc, n, sp) in enumerate(((SATTVA, 3, 0.9), (RAJAS, 4, -1.3), (TAMAS, 5, 0.7))):
        p = skia.Path()
        for j in range(0, 361, 3):
            th = math.radians(j)
            rr = R * (0.72 + 0.1 * k) + 18 * math.sin(n * th + sp * t + k)
            px, py = x + rr * math.cos(th), y + rr * math.sin(th)
            if j == 0:
                p.moveTo(px, py)
            else:
                p.lineTo(px, py)
        p.close()
        c.drawPath(p, paint(hexc, a, True, 6))


def arrow(c, p0, ctrl, p1, hexc, width, prog, a, dash=None, head=True, hs=18):
    if prog <= 0.001 or a <= 0.003:
        return
    path = skia.Path()
    path.moveTo(*p0)
    path.quadTo(ctrl[0], ctrl[1], p1[0], p1[1])
    pm = skia.PathMeasure(path, False)
    L = pm.getLength()
    seg = skia.Path()
    pm.getSegment(0, L * clamp(prog), seg, True)
    c.drawPath(seg, paint(hexc, a, True, width, dash))
    if head and prog > 0.6:
        pt, tg = pm.getPosTan(L * clamp(prog))
        ang = math.atan2(tg.y(), tg.x())
        for s_ in (0.5, -0.5):
            hx = pt.x() - hs * math.cos(ang + s_)
            hy = pt.y() - hs * math.sin(ang + s_)
            c.drawLine(hx, hy, pt.x(), pt.y(), paint(hexc, a, True, width))


def chip(c, cx, cy, label, a, fill, border, f, tx=NAVY, minw=0, h=58):
    if a <= 0.003:
        return
    w = max(minw, f.measureText(label) + 40)
    rrect(c, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2, fill, border, a)
    text(c, label, cx, cy + f.getSize() * 0.36, f, tx, a, 'center')


# ---------------- the map ----------------
SEER = (540, 620)
ROOT = (150, 718, 930, 790)
INT = (150, 808, 930, 872)
IMK = (150, 890, 930, 954)
MIND = (150, 972, 560, 1036)
X_ORG, X_QUAL, X_ELEM = 235, 590, 880
ROWS = [1135, 1190, 1245, 1300, 1355]
ORG = ['ear', 'skin', 'eye', 'tongue', 'nose']
QUAL = ['sound', 'touch', 'form', 'taste', 'smell']
ELEM = ['space', 'air', 'fire', 'water', 'earth']


def band(c, box, title, sub, right, a, fill, border, glow=0.0):
    if a <= 0.003:
        return
    x0, y0, x1, y1 = box
    f = mixhex(fill, GOLD_LT, glow) if glow > 0 else fill
    b = mixhex(border, GOLD, glow) if glow > 0 else border
    rrect(c, x0, y0, x1, y1, (y1 - y0) / 2, f, b, a)
    yb = (y0 + y1) / 2 + 13
    ft, fs = font('fr500i', 38), font('in400', 27)
    text(c, title, x0 + 30, yb, ft, NAVY, a)
    text(c, sub, x0 + 30 + ft.measureText(title) + 14, yb - 1, fs, WARM, a)
    if right:
        text(c, right, x1 - 30, yb - 1, font('in400', 30), SLATE, a, 'right')


def map_state(t):
    st = {}
    out = 1 - ramp(t, 65.4, 66.1)
    dimc = 1 - 0.75 * ramp(t, 50.2, 50.9)                 # dim everything but the seer and the intellect in scene 8
    back = ramp(t, 59.2, 59.8)                             # the dance scene: keep it dim, root lit
    st['seer'] = ramp(t, 19.2, 19.9) * out
    st['div'] = ramp(t, 19.6, 20.2) * out * dimc
    st['root'] = ramp(t, 20.0, 20.6) * out * lerp(dimc, 1.0, back)
    st['int'] = ramp(t, 21.0, 21.6) * out * (1 - (1 - dimc) * back)
    st['imk'] = ramp(t, 22.6, 23.2) * out * lerp(dimc, 1.0, ramp(t, 54.2, 54.8) * (1 - back))
    st['mind'] = ramp(t, 24.2, 24.8) * out * dimc
    st['table'] = out * (1 - ramp(t, 50.2, 50.9))
    st['glow'] = ramp(t, 51.8, 52.6) * (1 - ramp(t, 59.0, 59.6))
    st['beam'] = ramp(t, 50.9, 52.0) * (1 - ramp(t, 59.0, 59.6))
    st['refl'] = ramp(t, 52.4, 53.0) * (1 - ramp(t, 59.0, 59.6))
    st['bubble'] = ramp(t, 54.6, 55.2) * (1 - ramp(t, 59.0, 59.6))
    st['badges'] = ramp(t, 43.6, 44.4) * (1 - ramp(t, 49.4, 50.0))
    st['strong'] = ramp(t, 64.0, 65.0)
    return st


def draw_map(c, t):
    st = map_state(t)
    if st['seer'] <= 0.003:
        return
    # the seer, outside nature
    light(c, SEER[0], SEER[1], 26, st['seer'], t, 1 + 0.8 * st['strong'])
    a = st['seer'] * (1 - st['badges'])
    text(c, 'the seer', SEER[0] + 66, SEER[1] + 4, font('fr500i', 40), NAVY, st['seer'])
    text(c, 'Purusha', SEER[0] + 66 + font('fr500i', 40).measureText('the seer') + 14, SEER[1] + 3, font('in400', 27), WARM, st['seer'])
    if st['div'] > 0.003:
        c.drawLine(ROOT[0] + 40, 690, ROOT[2] - 40, 690, paint(WARM, 0.55 * st['div'], True, 2, [10, 10]))
    # beam from the seer into the intellect (scene 8)
    if st['beam'] > 0.003:
        y1 = lerp(SEER[1] + 30, INT[1] + 4, st['beam'])
        path = skia.Path()
        path.moveTo(SEER[0] - 22, SEER[1] + 26)
        path.lineTo(SEER[0] + 22, SEER[1] + 26)
        path.lineTo(SEER[0] + 150, y1)
        path.lineTo(SEER[0] - 150, y1)
        path.close()
        sh = skia.GradientShader.MakeLinear([(0, SEER[1]), (0, INT[1])], [col(GOLD_LT, 0.9 * st['beam']), col(GOLD_LT, 0.35 * st['beam'])])
        p = skia.Paint(AntiAlias=True)
        p.setShader(sh)
        c.drawPath(path, p)
    # nature, the root, with its three strands
    ra = st['root']
    if ra > 0.003:
        rrect(c, *ROOT, 36, CHIP, CHIP_B, ra)
        text(c, 'Nature', ROOT[0] + 30, 767, font('fr500i', 38), NAVY, ra)
        text(c, 'Prakriti', ROOT[0] + 30 + font('fr500i', 38).measureText('Nature') + 14, 766, font('in400', 27), WARM, ra)
        braid(c, 470, 900, 754, 11, 140, 0.7 * t, ra, 5)
    band(c, INT, 'Intellect', 'buddhi', 'decides: this is so', st['int'], LAV_FILL, LAV, st['glow'])
    if st['refl'] > 0.003:
        rx, ry = 590, (INT[1] + INT[3]) / 2
        c.drawCircle(rx, ry, 13, paint(GOLD, st['refl']))
        c.drawCircle(rx, ry, 20, paint(GOLD, 0.45 * st['refl'], True, 2))
    band(c, IMK, 'I-maker', 'ahamkara', 'claims: me, mine', st['imk'], APR_FILL, TERRA)
    band(c, MIND, 'Mind', 'manas', 'gathers', st['mind'], POW_FILL, POW)
    # the bubble on the I-maker (scene 8)
    if st['bubble'] > 0.003:
        ba = st['bubble']
        bx0, by0, bx1, by1 = 600, 978, 930, 1044
        rrect(c, bx0, by0, bx1, by1, 30, '#FFFFFF', TERRA, ba, 3)
        tri = skia.Path()
        tri.moveTo(700, by0 + 1)
        tri.lineTo(722, by0 - 22)
        tri.lineTo(744, by0 + 1)
        tri.close()
        c.drawPath(tri, paint('#FFFFFF', ba))
        c.drawLine(700, by0, 722, by0 - 22, paint(TERRA, ba, True, 3))
        c.drawLine(722, by0 - 22, 744, by0, paint(TERRA, ba, True, 3))
        text(c, '“I am angry”', (bx0 + bx1) / 2, by0 + 45, font('fr500i', 38), TERRA_DK, ba, 'center')
    draw_table(c, t, st['table'])
    # counting badges (scene 7)
    if st['badges'] > 0.003:
        ba = st['badges']
        for k, (y, n) in enumerate(((SEER[1], '1'), (754, '1'), (840, '1'), (922, '1'), (1004, '1'))):
            u = ramp(t, 43.6 + 0.35 * k, 44.1 + 0.35 * k) * ba
            if u <= 0.003:
                continue
            x = 958
            c.drawCircle(x, y, 22, paint(TERRA, u))
            text(c, n, x, y + 10, font('in500', 28), '#FFFFFF', u, 'center')


def draw_table(c, t, ta):
    if ta <= 0.003:
        return
    fh = font('in500', 28)
    fw = font('in500', 36)
    # streams from the I-maker (Karika 25): mind and senses on one side, the subtle elements on the other
    pa = ramp(t, 27.3, 28.3)
    arrow(c, (330, MIND[3] + 2), (290, 1052), (X_ORG, 1064), SAGE, 4, pa, ta, head=False)
    arrow(c, (760, IMK[3] + 2), (700, 1030), (X_QUAL + 20, 1064), TERRA, 4, pa, ta, head=False)
    text(c, '5 senses', X_ORG, 1093, fh, SAGE_DK, ta * ramp(t, 28.0, 28.6), 'center')
    text(c, '5 subtle elements', X_QUAL, 1093, fh, TERRA_DK, ta * ramp(t, 28.0, 28.6), 'center')
    text(c, '5 elements', X_ELEM, 1093, fh, NAVY, ta * ramp(t, 36.4, 37.0), 'center')
    for k in range(5):
        y = ROWS[k]
        ao = ramp(t, 28.8 + 0.32 * k, 29.3 + 0.32 * k) * ta
        aq = ramp(t, 29.0 + 0.32 * k, 29.5 + 0.32 * k) * ta
        text(c, ORG[k], X_ORG, y + 13, fw, NAVY, ao, 'center')
        text(c, QUAL[k], X_QUAL, y + 13, fw, TERRA_DK, aq, 'center')
        pl = ramp(t, 31.2 + 0.35 * k, 31.9 + 0.35 * k)
        arrow(c, (X_ORG + 82, y), (lerp(X_ORG + 82, X_QUAL - 80, 0.5), y), (X_QUAL - 80, y), SAGE, 3, pl, ta, dash=[9, 8], head=False)
        pe = ramp(t, 36.8 + 0.5 * k, 37.5 + 0.5 * k)
        arrow(c, (X_QUAL + 70, y), (lerp(X_QUAL + 70, X_ELEM - 84, 0.5), y), (X_ELEM - 84, y), TERRA, 3.5, pe, ta, hs=14)
        ae = ramp(t, 37.3 + 0.5 * k, 37.8 + 0.5 * k) * ta
        if ae > 0.003:
            chip(c, X_ELEM, y, ELEM[k], ae, ELEM_FILL[ELEM[k]], CHIP_B, fw, NAVY, minw=150, h=50)
    text(c, 'Plus 5 ways to act: speak, hold, walk, release, create.', MX, 1416, font('in400', 31), SLATE, ramp(t, 33.6, 34.3) * ta)


# ---------------- the dancer (scene 9) ----------------
def dancer(c, t):
    """nature as a dancer: big loops over the map, then she settles back into the three strands of the nature band"""
    a = ramp(t, 59.5, 60.2) * (1 - ramp(t, 64.8, 65.4))
    if a <= 0.003:
        return
    u = ramp(t, 62.4, 64.6)
    xa, xb = lerp(140, 470, u), lerp(940, 900, u)
    yc, amp, wl = lerp(1120, 754, u), lerp(150, 11, u), lerp(300, 140, u)
    taper, width = lerp(220, 60, u), lerp(14, 5, u)
    for k, hexc in enumerate((TAMAS, RAJAS, SATTVA)):
        ph = lerp(2.6 * t + 0.9 * k, 0.7 * t + k * 2 * math.pi / 3, u)
        p = skia.Path()
        x = xa
        first = True
        while x <= xb + 0.1:
            env = min(1.0, (x - xa) / taper, (xb - x) / taper)
            y = yc + amp * env * math.sin(2 * math.pi * (x - xa) / wl + ph) + (k - 1) * lerp(26, 0, u)
            if first:
                p.moveTo(x, y)
                first = False
            else:
                p.lineTo(x, y)
            x += 4
        c.drawPath(p, paint(hexc, a * 0.92, True, width))


# ---------------- other scene drawings ----------------
def draw_cover(c, t):
    a = ramp(t, 0.9, 1.8) * (1 - ramp(t, 4.5, 5.0))
    if a <= 0.003:
        return
    light(c, 540, 1010, 34, a, t)
    for k in range(5):
        u = ramp(t, 1.4 + 0.28 * k, 2.0 + 0.28 * k) * a
        w = 300 + 110 * k
        y0 = 1110 + 72 * k
        tint = [LAV_FILL, APR_FILL, POW_FILL, SAGE_FILL, ELEM_FILL['earth']][k]
        shimmer = 0.75 + 0.25 * math.sin(2.4 * t - 0.8 * k)
        rrect(c, 540 - w / 2, y0, 540 + w / 2, y0 + 52, 26, tint, CHIP_B, u * shimmer, 2)


def draw_two(c, t):
    a = ramp(t, 5.4, 6.2) * (1 - ramp(t, 11.4, 12.0))
    if a <= 0.003:
        return
    c.drawLine(540, 720, 540, 1190, paint(WARM, 0.45 * a, True, 2, [10, 10]))
    al = ramp(t, 5.8, 6.6) * a
    light(c, 300, 870, 48, al, t)
    text(c, 'Purusha', 300, 1080, font('fr500i', 54), NAVY, al, 'center')
    text(c, 'the seer', 300, 1132, font('in500', 36), SLATE, al, 'center')
    text(c, 'pure awareness', 300, 1180, font('in400', 31), WARM, al, 'center')
    ar = ramp(t, 7.0, 7.8) * a
    swirl(c, 780, 870, 130, t, ar)
    text(c, 'Prakriti', 780, 1080, font('fr500i', 54), NAVY, ar, 'center')
    text(c, 'nature', 780, 1132, font('in500', 36), SLATE, ar, 'center')
    text(c, 'everything seen', 780, 1180, font('in400', 31), WARM, ar, 'center')


def draw_strands(c, t):
    a = ramp(t, 12.3, 13.0) * (1 - ramp(t, 18.4, 19.0))
    if a <= 0.003:
        return
    tip = ramp(t, 14.8, 16.6)
    amp = lerp(10, 40, tip)
    ph = 0.2 + 2.4 * max(0.0, t - 14.8) * tip
    braid(c, 120, 960, 960, amp, lerp(260, 220, tip), ph, a, 9)
    sl = ramp(t, 14.2, 15.0) * a
    light(c, 540, 760, 26, sl, t)
    fl = font('in500', 31)
    for k, (lab, hexc, x) in enumerate((('clear · sattva', SATTVA, 225), ('moving · rajas', RAJAS, 540), ('heavy · tamas', TAMAS, 855))):
        u = ramp(t, 12.8 + 0.4 * k, 13.4 + 0.4 * k) * a
        if u <= 0.003:
            continue
        w = 262
        rrect(c, x - w / 2, 1110, x + w / 2, 1172, 31, CHIP, hexc, u, 3)
        text(c, lab, x, 1152, fl, NAVY, u, 'center')
    u = ramp(t, 16.8, 17.5) * a
    block(c, 'They pull different ways, yet work together, like the parts of one lamp.', MX, 1262, font('fr500i', 44), TERRA_DK, u, 56)


def draw_chart(c, t):
    a = ramp(t, 66.2, 66.9) * (1 - ramp(t, 72.5, 73.0))
    if a <= 0.003:
        return
    rows = [('fire', 'Mars'), ('earth', 'Mercury'), ('space', 'Jupiter'), ('water', 'Venus'), ('air', 'Saturn')]
    fe, fg = font('fr500i', 46), font('in500', 38)
    for k, (el, g) in enumerate(rows):
        y = 700 + 120 * k
        u = ramp(t, 66.8 + 0.55 * k, 67.4 + 0.55 * k) * a
        if u <= 0.003:
            continue
        rrect(c, 150, y, 470, y + 90, 45, ELEM_FILL[el], CHIP_B, u)
        text(c, el, 310, y + 61, fe, NAVY, u, 'center')
        arrow(c, (492, y + 45), (546, y + 45), (600, y + 45), WARM, 3, ramp(t, 67.2 + 0.55 * k, 67.7 + 0.55 * k), u, hs=14)
        rrect(c, 620, y, 930, y + 90, 45, CHIP, GRAHA[g], u, 3.5)
        c.drawCircle(668, y + 45, 13, paint(GRAHA[g], u))
        text(c, g, 700, y + 58, fg, NAVY, u)
    u = ramp(t, 69.8, 70.5) * a
    block(c, 'Which element leads in your chart?', MX, 1380, font('fr500i', 50), TERRA, u, 62)


def scene_text(c, t):
    # 1 cover
    i = 0
    a = sa(t, i, 0.2)
    text(c, 'The Thread · Maps of reality, part 1', MX, 300 + slide(t, i, 0.2), font('in500', 32), TERRA, a)
    a = sa(t, i, 0.45)
    ft = font('fr600', 100)
    for k, ln in enumerate(['What is reality', 'made of?']):
        text(c, ln, MX, 430 + k * 108 + slide(t, i, 0.45), ft, NAVY, a)
    a = sa(t, i, 0.9)
    for k, ln in enumerate(["Samkhya's map in 25 layers,", 'from the seer down to earth']):
        text(c, ln, MX, 660 + k * 66 + slide(t, i, 0.9), font('fr400i', 52), SLATE, a)
    # 2 two
    i = 1
    yh = head(c, t, i, 'Samkhya counts two')
    body(c, t, i, 'Awareness that never acts, and nature that never rests.', yh + 100, 0.3)
    source(c, t, i, 'Samkhya Karika, verses 3, 11 and 19')
    # 3 three strands
    i = 2
    yh = head(c, t, i, 'Nature is three strands')
    body(c, t, i, 'At rest they balance. Near the seer, the balance tips and nature starts to unfold.', yh + 100, 0.3)
    source(c, t, i, 'Samkhya Karika, verses 12, 13 and 21')
    # 4 the inner three
    i = 3
    yh = head(c, t, i, 'It unfolds, subtle first')
    body(c, t, i, 'Closest to the seer come three inner powers. They decide, claim and gather.', yh + 100, 0.3)
    source(c, t, i, 'Samkhya Karika, verses 22 to 24, 27 and 35', 2.0)
    # 5 senses and subtle elements
    i = 4
    yh = head(c, t, i, 'Five doors, five qualities')
    body(c, t, i, 'From the I-maker run two streams: senses that know, and the qualities they meet.', yh + 100, 0.3)
    source(c, t, i, 'Samkhya Karika, verses 25, 26 and 28', 2.0)
    # 6 gross elements
    i = 5
    yh = head(c, t, i, 'Subtle turns solid')
    body(c, t, i, 'Each quality condenses into an element. This last layer is your body and the world.', yh + 100, 0.3)
    source(c, t, i, 'Samkhya Karika, verse 38', 2.0)
    # 7 count
    i = 6
    yh = head(c, t, i, '25 layers in all')
    body(c, t, i, 'One seer and 24 layers of nature. Your body is the last layer. The one who knows it stands outside.', yh + 100, 0.3)
    a = sa(t, i, 2.6)
    text(c, '5 single layers + 4 rows of 5 = 25', MX, 1478 + slide(t, i, 2.6), font('in500', 34), TERRA_DK, a)
    # 8 mix-up
    i = 7
    yh = head(c, t, i, 'The mix-up')
    body(c, t, i, "The seer's light shows in the intellect, like a face in a mirror. Thinking seems aware, and the seer seems to act.", yh + 100, 0.3)
    a = sa(t, i, 4.4)
    if a > 0:
        dy = slide(t, i, 4.4)
        rrect(c, MX, 1130 + dy, MX + TW, 1300 + dy, 28, '#FFFFFF', CHIP_B, a)
        block(c, 'Anger rises in the layers. The I-maker calls it mine. The seer only sees it.', MX + 36, 1200 + dy, font('in400', 40), NAVY, a, 54, maxw=TW - 72)
    source(c, t, i, 'Samkhya Karika 20 and 24 · the mirror: Vachaspati Mishra', 2.2)
    # 9 dancer
    i = 8
    yh = head(c, t, i, 'Seen, the dance stops')
    body(c, t, i, 'Nature dances for the seer. Once fully seen, she stops, like a dancer after the show.', yh + 100, 0.3)
    a = sa(t, i, 5.2)
    block(c, 'Samkhya calls this freedom kaivalya: the seer, standing free.', MX, 1290 + slide(t, i, 5.2), font('fr500i', 48), TERRA, a, 60)
    source(c, t, i, 'Samkhya Karika, verses 59, 66 and 68', 2.0)
    # 10 chart
    i = 9
    yh = head(c, t, i, 'Jyotish uses the same word')
    body(c, t, i, 'Parashara calls the five elements the tattvas of five grahas.', yh + 100, 0.3)
    source(c, t, i, 'Brihat Parashara Hora Shastra, chapter 3, verse 20', 2.0)
    # 11 end
    i = 10
    a = sa(t, i, 0.5)
    if a > 0:
        dy = slide(t, i, 0.5)
        f = font('fr500i', 64)
        for k, ln in enumerate(['Which layer is loudest', 'in you today?']):
            text(c, ln, W / 2, 780 + k * 80 + dy, f, NAVY, a, 'center')
    a = sa(t, i, 1.3)
    if a > 0:
        dy = slide(t, i, 1.3)
        text(c, 'Sutram', W / 2, 1120 + dy, font('fr600', 128), NAVY, a, 'center')
        text(c, 'sutram.ca', W / 2, 1200 + dy, font('in500', 46), ORANGE_DK, a, 'center')
        text(c, 'Know yourself · Know your time', W / 2, 1268 + dy, font('in400', 36), SLATE, a, 'center')


SURF = skia.Surface(W, H)


def render(t):
    c = SURF.getCanvas()
    c.clear(skia.Color(*BG))
    draw_cover(c, t)
    draw_two(c, t)
    draw_strands(c, t)
    draw_map(c, t)
    dancer(c, t)
    draw_chart(c, t)
    scene_text(c, t)
    return SURF.makeImageSnapshot()


def stills(times, outdir=WORK + '/stills'):
    os.makedirs(outdir, exist_ok=True)
    for t in times:
        img = render(float(t))
        p = f'{outdir}/t{float(t):05.1f}.png'
        img.save(p, skia.kPNG)
        print(p)


def scenes(outdir=WORK + '/scenes'):
    os.makedirs(outdir, exist_ok=True)
    names = []
    for n, (s0, s1) in enumerate(S):
        f0, f1 = round(s0 * FPS), round(s1 * FPS)
        final = f'{outdir}/scene{n + 1:02d}.mp4'
        tmp = f'{outdir}/scene{n + 1:02d}.tmp.mp4'
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
               '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp]
        pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for k in range(f0, f1):
            arr = render(k / FPS).toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType)
            pr.stdin.write(arr.tobytes())
        pr.stdin.close()
        if pr.wait() == 0:
            os.replace(tmp, final)
            names.append(final)
            print('scene', n + 1, f1 - f0, 'frames', flush=True)
        else:
            sys.exit(f'scene {n + 1} failed')
    with open(f'{outdir}/list.txt', 'w') as fh:
        for p in names:
            fh.write(f"file '{p}'\n")


def build():
    """scenes, then join, drone and mux into posts/<ID>/<ID>-1.mp4, an X copy at 720x1280 and the cover still"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from tanpura import drone
    scenes()
    out = os.path.join(REPO, 'posts', ID)
    os.makedirs(out, exist_ok=True)
    run = lambda *a: subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)
    run('-f', 'concat', '-safe', '0', '-i', WORK + '/scenes/list.txt', '-c', 'copy', WORK + '/video.tmp.mp4')
    os.replace(WORK + '/video.tmp.mp4', WORK + '/video.mp4')
    drone(TOTAL, WORK + '/drone.wav')
    run('-i', WORK + '/video.mp4', '-i', WORK + '/drone.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        '-shortest', '-movflags', '+faststart', WORK + '/final.tmp.mp4')
    shutil.move(WORK + '/final.tmp.mp4', f'{out}/{ID}-1.mp4')
    run('-i', f'{out}/{ID}-1.mp4', '-vf', 'scale=720:1280:flags=lanczos', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', WORK + '/x.tmp.mp4')
    shutil.move(WORK + '/x.tmp.mp4', f'{out}/{ID}-x.mp4')
    run('-ss', '3.0', '-i', f'{out}/{ID}-1.mp4', '-frames:v', '1', '-q:v', '2', f'{out}/{ID}-1.jpg')
    print('built', out)


if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        stills(sys.argv[2:])
    elif sys.argv[1] == 'build':
        build()
    else:
        scenes()
