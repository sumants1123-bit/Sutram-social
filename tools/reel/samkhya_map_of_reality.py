"""Sutram Reel: "What is reality made of?" Samkhya's map, layer by layer (The Thread, Maps of reality, part 1).

Asked by Sumant, Thu 26 Nov 2026 (Mexico, by voice): "as per Samkhya philosophy ... the universe is a superimposition ...
the subtler being the self or the observer, and then there comes intellect ... and then comes mind ... make a post and
then dynamic visual, really clearly in visual terms explaining the reality as per Samkhya." Version 2, same evening,
after he watched version 1 (25 layers, subtle elements, a five-column table): "It's quite confusing and long. You don't
need to go to the subtle senses, then [tan]matras ... Slow it down and just overall share from bliss to mahat, from
mahat to intellect to ahamkara or I, and then the mind, etc. Just high level and make it a little slower. If you can
improve the visual, do that." Asked which words go on top, he picked Samkhya's own: the seer (pure awareness) at the
centre, and mahat as the intellect itself (one layer, two names); bliss (ananda) is Vedanta's word, left out.

The picture: a yantra of nested squares around one light. The light is the seer. Nature unfolds around it one layer at
a time, subtlest first: mahat the intellect, ahamkara the I, manas the mind, the senses, the body and the world. Each
layer covers the light a little more. Then the light shows through every layer (the mix-up), and the layers fall away
from the outside in (the way out). Ten scenes, 87 seconds, one idea a scene.

Sources, every one opened on 26 Nov 2026 before use:
- Samkhya Karika of Ishvarakrishna (about 350 CE; Wikipedia, Samkhyakarika), verse meanings as in Raghavan Iyer's
  translation (Hermes, Sept 1987, theosophytrust.org/922-the-sankhya-karika-ishvarakrishna):
  3, 11 nature unfolds, the seer does not; the seer is the reverse of the manifest.  19 the seer is witness, neutral,
  spectator, non-agent.  20 through contact with the seer the non-conscious seems conscious, and the seer seems to act.
  22 from nature comes mahat (the great one), from it the I-maker (ahamkara), from it the sixteen, and from five of those
  the five elements.  23 intellect (buddhi) is ascertainment: mahat and buddhi are one layer.  24 the I-maker is
  self-assertion ("me, mine").  25, 27 the mind (manas) comes with the ten organs and deliberates.  26 five senses (eye,
  ear, nose, tongue, skin) and five organs of action.  38 the five gross elements.  59 like a dancer who stops once
  seen, nature stops.  66 one has seen, the other has been seen.  68 kaivalya, the seer alone and free.
- Brihat Parashara Hora Shastra 3.20 gives the five elements, its tattvas, to Mars (fire), Mercury (earth), Jupiter
  (space), Venus (water) and Saturn (air) (enjoylearningsanskrit.com/scriptures/parashara/chapter-3/verse-20); caption only.
No chart and no engine value in this post.

    python3 tools/reel/samkhya_map_of_reality.py stills 3 11 21 ...   look at every still at full size first
    python3 tools/reel/samkhya_map_of_reality.py build                 scenes, concat, drone, mux into posts/<ID>/
"""
import math, os, shutil, subprocess, sys
import numpy as np
import skia

W, H, FPS = 1080, 1920, 30
MX, TW = 96, 888

BG = (246, 240, 228)
NAVY, SLATE, WARM = '#1E2A44', '#4E586C', '#756E61'
TERRA, TERRA_DK, ORANGE_DK = '#C2603E', '#8E3F22', '#C8552A'
GOLD, GOLD_LT = '#D9A441', '#F6E3B0'
BRASS = '#A9813A'
SATTVA, RAJAS, TAMAS = '#D9A441', '#C2603E', '#4A5482'

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


def paint(hexc, a=1.0, stroke=False, width=0.0, dash=None, phase=0.0):
    p = skia.Paint(AntiAlias=True)
    p.setColor(col(hexc, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(width)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if dash:
        p.setPathEffect(skia.DashPathEffect.Make(dash, phase))
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


# ---------------- scene timing: slower, one idea a scene ----------------
S = [(0, 6), (6, 16), (16, 25), (25, 34), (34, 43), (43, 52), (52, 61), (61, 71), (71, 80), (80, 87)]
TOTAL = 87.0


def sa(t, i, delay=0.0):
    """alpha of text belonging to scene i (slow fade in after delay, fade out at scene end)"""
    s0, s1 = S[i]
    if t < s0 or t >= s1:
        return 0.0
    a = ramp(t, s0 + 0.15 + delay, s0 + 1.0 + delay)
    if i < len(S) - 1:
        a *= 1 - ramp(t, s1 - 0.6, s1)
    return a


def slide(t, i, delay=0.0):
    s0, _ = S[i]
    return 24 * (1 - ramp(t, s0 + 0.15 + delay, s0 + 1.1 + delay))


def head(c, t, i, s, y=330, delay=0.0):
    return block(c, s, MX, y + slide(t, i, delay), font('fr500i', 76), NAVY, sa(t, i, delay), 88)


def body(c, t, i, s, y, delay=0.0, hexc=SLATE):
    return block(c, s, MX, y + slide(t, i, delay), font('in400', 44), hexc, sa(t, i, delay), 60)


def source(c, t, i, s, delay=2.0):
    text(c, s, MX, 1508, font('in400', 28), WARM, sa(t, i, delay) * 0.95)


# ---------------- the yantra of layers ----------------
CX, CY = 540, 1040
CORE = 96                                      # the seer's square: only the light, nature starts outside it
STEP = 62
LAYERS = [  # name, Sanskrit, fill, border, scene that unfolds it
    ('Intellect', 'mahat', '#ECE6F6', '#7E72B8', 2),
    ('The I', 'ahamkara', '#FBE6D5', '#C2603E', 3),
    ('Mind', 'manas', '#E2EAF1', '#6F8FB0', 4),
    ('Senses', 'indriya', '#E3EADF', '#5E8A6A', 5),
    ('Body and world', 'five elements', '#EDE3D0', '#A08A64', 6),
]
HALF = [CORE + STEP * (k + 1) for k in range(5)]   # 158, 220, 282, 344, 406


def corner(s):
    return 16 + 0.1 * s


def sq(s):
    return skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(CX - s, CY - s, CX + s, CY + s), corner(s), corner(s))


def light(c, x, y, r, a, t, glow=1.0):
    """the seer: a steady light with a soft, slow breathing halo"""
    if a <= 0.003:
        return
    br = 1 + 0.05 * math.sin(t * 1.6)
    R = r * 3.6 * glow * br
    sh = skia.GradientShader.MakeRadial((x, y), R, [col(GOLD_LT, 0.95 * a), col(GOLD_LT, 0.42 * a), col(GOLD_LT, 0.0)], [0.0, 0.45, 1.0])
    p = skia.Paint(AntiAlias=True)
    p.setShader(sh)
    c.drawCircle(x, y, R, p)
    c.drawCircle(x, y, r * 1.3, paint(GOLD, 0.35 * a, True, 2))
    core = skia.GradientShader.MakeRadial((x - r * 0.25, y - r * 0.25), r * 1.2, [col('#FFF6DC', a), col(GOLD, a)], [0.0, 1.0])
    p2 = skia.Paint(AntiAlias=True)
    p2.setShader(core)
    c.drawCircle(x, y, r, p2)


def swirl(c, x, y, R, t, a):
    """nature: three strands looping round, never still"""
    if a <= 0.003:
        return
    for k, (hexc, n, sp) in enumerate(((SATTVA, 3, 0.7), (RAJAS, 4, -1.0), (TAMAS, 5, 0.55))):
        p = skia.Path()
        for j in range(0, 361, 3):
            th = math.radians(j)
            rr = R * (0.86 + 0.07 * k) + 20 * math.sin(n * th + sp * t + k)
            px, py = x + rr * math.cos(th), y + rr * math.sin(th)
            if j == 0:
                p.moveTo(px, py)
            else:
                p.lineTo(px, py)
        p.close()
        c.drawPath(p, paint(hexc, a, True, 6))


def gates(c, s, a):
    """four T-shaped gates on the outer wall, as on Sutram's yantra"""
    if a <= 0.003:
        return
    pp = paint(BRASS, a, True, 3)
    g, d = 46, 22
    for ang in (0, 90, 180, 270):
        c.save()
        c.rotate(ang, CX, CY)
        y0 = CY - s
        c.drawLine(CX - g, y0, CX - g, y0 - d, pp)
        c.drawLine(CX + g, y0, CX + g, y0 - d, pp)
        c.drawLine(CX - g - 18, y0 - d, CX + g + 18, y0 - d, pp)
        c.restore()


def layer_state(t):
    """per layer: how far it has unfolded (0..1), its alpha, focus and glow"""
    st = []
    for k, (_, _, _, _, sc) in enumerate(LAYERS):
        s0 = S[sc][0]
        grow = ramp(t, s0 + 0.5, s0 + 2.3)
        fade = 1 - ramp(t, 72.4 + 0.8 * (4 - k), 73.4 + 0.8 * (4 - k))         # the way out: outside in
        fade *= 1 - ramp(t, 79.4, 80.2)
        cover = ramp(t, 0.8 + 0.25 * k, 2.0 + 0.25 * k) * (1 - ramp(t, 5.2, 6.0)) * 0.8   # the cover shows the whole yantra
        a = max(grow * fade, cover if t < 6 else 0.0)
        g = grow if t >= 6 else 1.0
        focus = 1.0
        if 16 <= t < 61:
            cur = next((kk for kk, L in enumerate(LAYERS) if S[L[4]][0] <= t < S[L[4]][1]), None)
            if cur is not None and k < cur:
                focus = 0.72
        glow = 0.4 * ramp(t, 62.0, 63.5) * (1 - ramp(t, 71.0, 72.4))
        st.append((g, a, focus, glow))
    return st


def draw_layers(c, t):
    """on the cover the yantra sits smaller and lower under the title, then eases into place"""
    u = ramp(t, 5.0, 6.6)
    c.save()
    c.translate(CX, CY + lerp(90, 0, u))
    c.scale(lerp(0.84, 1.0, u), lerp(0.84, 1.0, u))
    c.translate(-CX, -CY)
    _draw_layers(c, t)
    c.restore()


def _draw_layers(c, t):
    st = layer_state(t)
    # the seer's light sits under every layer: each one veils it a little more
    shown = sum(1 for g, a, f, gl in st if a > 0.5)
    seer_a = 1.0 if t >= 0.6 else ramp(t, 0.2, 0.6)
    seer_a *= 1 - ramp(t, 79.6, 80.4)
    glow = 1.0 - 0.06 * shown + 0.5 * ramp(t, 73.0, 76.5)
    light(c, CX, CY, 52, seer_a, t, glow)
    for k in range(5):
        g, a, focus, gl = st[k]
        if a <= 0.003:
            continue
        name, skt, fill, border, _ = LAYERS[k]
        s_in = CORE + STEP * k
        s_out = lerp(s_in + 6, HALF[k], g)
        band = skia.Path()
        band.addRRect(sq(s_out))
        band.addRRect(sq(s_in))
        band.setFillType(skia.PathFillType.kEvenOdd)
        aa = a * focus
        c.drawPath(band, paint(mixhex(fill, GOLD_LT, gl), 0.86 * aa))
        c.drawRRect(sq(s_out), paint(border, aa, True, 2.6))
        # a slow line of light walking round each wall, alternate ways
        ph = (t * 22 * (1 if k % 2 == 0 else -1)) % 40
        c.drawRRect(sq(s_out - 7), paint(border, 0.45 * aa, True, 1.6, [10, 30], ph))
        la = a * ramp(t, S[LAYERS[k][4]][0] + 1.6, S[LAYERS[k][4]][0] + 2.4) if t >= 6 else 0.0
        la = max(la, a * (1 if t >= S[LAYERS[k][4]][1] else 0))
        if la > 0.003:
            y = CY - (s_in + HALF[k]) / 2 + 11
            f1, f2 = font('fr500i', 34), font('in400', 25)
            w1, w2 = f1.measureText(name), f2.measureText(skt)
            x0 = CX - (w1 + 12 + w2) / 2
            text(c, name, x0, y, f1, NAVY, la * focus)
            text(c, skt, x0 + w1 + 12, y - 1, f2, WARM, la * focus)
    gates(c, HALF[4], st[4][1] * ramp(t, S[6][0] + 1.8, S[6][0] + 2.6) if t >= 6 else st[4][1])
    # the seer's name in its own square
    la = (ramp(t, 16.8, 17.6) if t >= 16 else 0.0) * (1 - ramp(t, 79.4, 80.2))
    text(c, 'the seer', CX, CY + 86, font('fr500i', 30), NAVY, la * 0.9, 'center')
    # the mix-up: the light shows through every layer
    ra = ramp(t, 62.0, 63.2) * (1 - ramp(t, 70.4, 71.2))
    if ra > 0.003:
        for j in range(8):
            ang = math.radians(22.5 + 45 * j)
            r1 = 60
            r2 = HALF[4] / max(abs(math.cos(ang)), abs(math.sin(ang)))
            c.drawLine(CX + r1 * math.cos(ang), CY + r1 * math.sin(ang), CX + r2 * math.cos(ang), CY + r2 * math.sin(ang),
                       paint(GOLD, 0.55 * ra, True, 3))
        c.save()
        c.clipRRect(sq(HALF[4] + 24))
        for w in range(3):
            u = ((t - 62.0) / 2.6 + w / 3.0) % 1.0
            rr = lerp(60, 560, u)
            c.drawCircle(CX, CY, rr, paint(GOLD, ra * 0.5 * (1 - u), True, 4))
        c.restore()


def draw_two(c, t):
    """scene 2: the seer and nature"""
    a = ramp(t, 6.3, 7.3) * (1 - ramp(t, 15.4, 16.4))
    if a <= 0.003:
        return
    al = ramp(t, 6.6, 7.6) * a
    f1, f2 = font('fr500i', 46), font('in400', 30)
    w1, w2 = f1.measureText('the seer'), f2.measureText('Purusha')
    x0 = CX - (w1 + 14 + w2) / 2
    text(c, 'the seer', x0, CY + 138, f1, NAVY, al)
    text(c, 'Purusha', x0 + w1 + 14, CY + 137, f2, WARM, al)
    ar = ramp(t, 9.0, 10.2) * a
    shrink = ramp(t, 15.0, 16.4)
    swirl(c, CX, CY, lerp(320, 150, shrink), t, ar)
    w1, w2 = f1.measureText('nature'), f2.measureText('Prakriti')
    x0 = CX - (w1 + 14 + w2) / 2
    text(c, 'nature', x0, CY + 412, f1, NAVY, ar * (1 - shrink))
    text(c, 'Prakriti', x0 + w1 + 14, CY + 411, f2, WARM, ar * (1 - shrink))


def scene_text(c, t):
    # 1 cover
    i = 0
    a = sa(t, i, 0.0)
    text(c, 'The Thread · Maps of reality, part 1', MX, 300 + slide(t, i, 0.0), font('in500', 32), TERRA, a)
    a = sa(t, i, 0.25)
    for k, ln in enumerate(['What is reality', 'made of?']):
        text(c, ln, MX, 430 + k * 108 + slide(t, i, 0.25), font('fr600', 100), NAVY, a)
    # (the cover's subtitle sits under the title; the yantra below is faint)
    # 2 two
    i = 1
    yh = head(c, t, i, 'Samkhya sees two')
    body(c, t, i, 'The seer: pure awareness, only watching. Nature: all that moves and can be seen.', yh + 100, 0.4)
    source(c, t, i, 'Samkhya Karika, verses 3, 11 and 19')
    # 3 mahat
    i = 2
    yh = head(c, t, i, 'Mahat, the intellect')
    body(c, t, i, 'The first and clearest layer, also called buddhi. It knows and decides.', yh + 100, 0.4)
    source(c, t, i, 'Samkhya Karika, verses 22 and 23')
    # 4 I
    i = 3
    yh = head(c, t, i, 'Then the I')
    body(c, t, i, 'Ahamkara, the I-maker. It says me and mine.', yh + 100, 0.4)
    source(c, t, i, 'Samkhya Karika, verses 22 and 24')
    # 5 mind
    i = 4
    yh = head(c, t, i, 'Then the mind')
    body(c, t, i, 'Manas thinks, wishes and gathers what the senses bring.', yh + 100, 0.4)
    source(c, t, i, 'Samkhya Karika, verses 25 and 27')
    # 6 senses
    i = 5
    yh = head(c, t, i, 'Then the senses')
    body(c, t, i, 'Five ways to know: see, hear, smell, taste, touch. And five ways to act.', yh + 100, 0.4)
    source(c, t, i, 'Samkhya Karika, verse 26')
    # 7 body and world
    i = 6
    yh = head(c, t, i, 'Last, body and world')
    body(c, t, i, 'All made of five elements: space, air, fire, water and earth.', yh + 100, 0.4)
    source(c, t, i, 'Samkhya Karika, verses 22 and 38')
    # 8 the mix-up
    i = 7
    yh = head(c, t, i, 'The mix-up')
    yb = body(c, t, i, "The light is the seer's. The layers only carry it, yet they seem awake.", yh + 100, 0.4)
    text(c, 'So we say “I am angry.”', MX, yb + 72 + slide(t, i, 3.6), font('fr500i', 46), TERRA_DK, sa(t, i, 3.6))
    source(c, t, i, 'Samkhya Karika, verse 20')
    # 9 the way out
    i = 8
    yh = head(c, t, i, 'The way out')
    yb = body(c, t, i, 'See each layer as a layer. Then nature rests, and the seer stands free.', yh + 100, 0.4)
    text(c, 'Samkhya calls it kaivalya.', MX, yb + 72 + slide(t, i, 4.2), font('fr500i', 46), TERRA_DK, sa(t, i, 4.2))
    source(c, t, i, 'Samkhya Karika, verses 59, 66 and 68')
    # 10 end
    i = 9
    a = sa(t, i, 0.5)
    if a > 0:
        dy = slide(t, i, 0.5)
        f = font('fr500i', 66)
        for k, ln in enumerate(['Which layer is loudest', 'in you today?']):
            text(c, ln, W / 2, 780 + k * 84 + dy, f, NAVY, a, 'center')
    a = sa(t, i, 1.4)
    if a > 0:
        dy = slide(t, i, 1.4)
        text(c, 'Sutram', W / 2, 1120 + dy, font('fr600', 128), NAVY, a, 'center')
        text(c, 'sutram.ca', W / 2, 1200 + dy, font('in500', 46), ORANGE_DK, a, 'center')
        text(c, 'Know yourself · Know your time', W / 2, 1268 + dy, font('in400', 36), SLATE, a, 'center')


def cover_sub(c, t):
    a = sa(t, 0, 0.6)
    text(c, "Samkhya's answer, layer by layer", MX, 660 + slide(t, 0, 0.6), font('fr400i', 54), SLATE, a)


SURF = skia.Surface(W, H)


def render(t):
    c = SURF.getCanvas()
    c.clear(skia.Color(*BG))
    draw_layers(c, t)
    draw_two(c, t)
    scene_text(c, t)
    cover_sub(c, t)
    return SURF.makeImageSnapshot()


def stills(times, outdir=WORK + '/stills'):
    os.makedirs(outdir, exist_ok=True)
    for t in times:
        img = render(float(t))
        p = f'{outdir}/t{float(t):05.1f}.png'
        img.save(p, skia.kPNG)
        print(p)


def scenes(outdir=WORK + '/scenes'):
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
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
