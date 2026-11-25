"""Sutram Reel model: "How does a transit turn into an event?" (Ketu in Cancer facing Saturn, Parashari and Nadi).
Posted as posts/ketu-facing-saturn (Fri 27 Nov 2026). Sumant on 25 Nov: "Great u can post it", and he picked one video a
week (rules_25nov in plan/state.json). This file is the model for that weekly video: copy it to tools/reel/<post-id>.py,
change ID, the scene list S, the wheel geometry and scene_text, then:
    python3 tools/reel/<post-id>.py stills 2.6 9 15.6 ...   look at every still at full size first
    python3 tools/reel/<post-id>.py build                    scenes, concat, tanpura drone, mux; writes posts/<id>/
Needs: pip install skia-python numpy (fonts are in assets/fonts). Vertical 1080x1920, 30 fps, one file per scene,
joined with -c copy, sound added with -c:v copy. Look: the cream "day" colours, Fraunces headlines, Inter body.
Every fact on screen comes from the engine or a source opened before use; the example chart is labelled as an example."""
import math, os, shutil, subprocess, sys
import numpy as np
import skia

W, H, FPS = 1080, 1920, 30
CX, CY = 540, 1120
R_RING, R_LAB, R_G = 290, 352, 205
MX, TW = 96, 888

BG = (246, 240, 228)
NAVY, SLATE, WARM, RING = '#1E2A44', '#4E586C', '#756E61', '#D8CCB6'
LAV_FILL, LAV = '#ECE6F6', '#7E72B8'
APR_FILL, TERRA, TERRA_DK = '#FBE6D5', '#C2603E', '#8E3F22'
SAGE, SAGE_DK = '#5E8A6A', '#3F6A4C'
CARD1, CARD1_B = '#EFEAF7', '#D9D0EE'
CARD2, CARD2_B = '#FBEBDD', '#F0D3BB'
CHIP, CHIP_B = '#FBF7EF', '#E3D8C4'
ORANGE_DK = '#C8552A'

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ID = 'ketu-facing-saturn'
FD = os.path.join(REPO, 'assets', 'fonts') + '/'
IN = FD
WORK = f'/tmp/reel/{ID}'
TF = {
    'fr600': skia.Typeface.MakeFromFile(FD + 'fraunces-latin-600-normal.ttf'),
    'fr500i': skia.Typeface.MakeFromFile(FD + 'fraunces-latin-500-italic.ttf'),
    'fr400i': skia.Typeface.MakeFromFile(FD + 'fraunces-latin-400-italic.ttf'),
    'in400': skia.Typeface.MakeFromFile(IN + 'Inter-Regular.otf'),
    'in500': skia.Typeface.MakeFromFile(IN + 'Inter-Medium.otf'),
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
S = [(0, 5), (5, 11.5), (11.5, 18), (18, 26), (26, 32), (32, 40), (40, 46.5), (46.5, 54.5), (54.5, 63.5), (63.5, 70), (70, 75)]
TOTAL = 75.0


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


# ---------------- wheel geometry ----------------
SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']


def pos(r, deg):
    a = math.radians(deg)
    return CX + r * math.cos(a), CY - r * math.sin(a)


KETU = pos(R_G, 90)
KETU0 = pos(R_G, 120)
SATURN = (465, CY + R_G)
RAHU = (615, CY + R_G)
RAHU0 = pos(R_G, 300)
MARS = pos(200, 0)
MOON = pos(200, 180)
SUVE = pos(190, 30)
SKYMARS = (668, KETU[1] + 1)
A1 = ((515, 948), (420, 1130), (448, 1290))
A2 = ((482, 1292), (560, 1120), (560, 950))
A3 = ((700, 1088), (700, 950), (600, 925))
A4 = ((482, 930), (360, 960), (345, 1086))
N1 = ((528, 948), (499, 1120), (470, 1292))
N3 = ((650, 1292), (600, 1140), (712, 1056))


def pill(c, cx, cy, label, kind, a=1.0, fs=32, minw=104):
    if a <= 0.003:
        return
    f = font('in500', fs)
    w = max(minw, f.measureText(label) + 44)
    h = 62 if fs >= 30 else 58
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), h / 2, h / 2)
    if kind == 'birth':
        fill, st, tx, dash = LAV_FILL, LAV, NAVY, None
    else:
        fill, st, tx, dash = APR_FILL, TERRA, TERRA_DK, [11, 7]
    c.drawRRect(rr, paint(fill, a))
    c.drawRRect(rr, paint(st, a, True, 3, dash))
    text(c, label, cx, cy + fs * 0.36, f, tx, a, 'center')


def arrow(c, p0, ctrl, p1, hexc, width, prog, a, dash=None, head=True):
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
    if head:
        pt, tg = pm.getPosTan(L * clamp(prog))
        ang = math.atan2(tg.y(), tg.x())
        for s_ in (0.5, -0.5):
            hx = pt.x() - 24 * math.cos(ang + s_)
            hy = pt.y() - 24 * math.sin(ang + s_)
            c.drawLine(hx, hy, pt.x(), pt.y(), paint(hexc, a, True, width))


def pulse_ring(c, cx, cy, r0, r1, phase, hexc, a):
    if a <= 0.003:
        return
    for k in (0.0, 0.5):
        u = (phase + k) % 1.0
        c.drawCircle(cx, cy, lerp(r0, r1, u), paint(hexc, a * (1 - u) * 0.9, True, 4))


def wheel_state(t):
    st = {}
    st['wheel'] = ramp(t, 1.4, 2.8) * (1 - ramp(t, 18.0, 18.6) + ramp(t, 26.0, 26.7)) * (1 - ramp(t, 70.0, 70.8))
    st['house'] = 1 - ramp(t, 55.4, 56.4)
    st['ketu_a'] = ramp(t, 5.6, 6.2)
    st['ketu_p'] = ramp(t, 6.2, 8.2)
    st['rahu_a'] = ramp(t, 5.6, 6.2)
    st['rahu_p'] = ramp(t, 6.4, 8.2)
    fade_old = 1 - 0.6 * ramp(t, 32.0, 32.6)
    st['A1'] = (ramp(t, 12.4, 14.2), fade_old * (1 - ramp(t, 54.6, 55.4)))
    st['A2'] = (ramp(t, 32.8, 34.6), (1 - 0.6 * ramp(t, 40.0, 40.6)) * (1 - ramp(t, 54.6, 55.4)))
    st['A3'] = (ramp(t, 35.8, 37.6), (1 - 0.6 * ramp(t, 40.0, 40.6)) * (1 - ramp(t, 49.0, 49.5)))
    st['A4'] = (ramp(t, 41.0, 42.8), (1 - 0.6 * ramp(t, 46.5, 47.1)) * (1 - ramp(t, 54.6, 55.4)))
    st['skymars'] = ramp(t, 49.5, 50.4) * (1 - ramp(t, 54.6, 55.2))
    st['skymars_dy'] = -40 * (1 - ramp(t, 49.5, 50.6))
    st['pulse'] = ramp(t, 50.6, 51.0) * (1 - ramp(t, 54.0, 54.5))
    st['caplabel'] = ramp(t, 50.6, 51.2) * (1 - ramp(t, 54.6, 55.2))
    st['rahu_pulse'] = ramp(t, 27.0, 27.4) * (1 - ramp(t, 31.4, 31.9))
    st['mm'] = 1 - 0.68 * ramp(t, 56.0, 56.8)
    st['N1'] = (ramp(t, 57.0, 58.4), 1.0)
    st['N2'] = ramp(t, 58.6, 59.4)
    st['suve'] = ramp(t, 59.6, 60.2)
    st['N3'] = (ramp(t, 60.2, 61.6), 1.0)
    return st


def draw_wheel(c, t):
    st = wheel_state(t)
    wa = st['wheel']
    if wa <= 0.003:
        return
    c.saveLayerAlpha(None, int(255 * wa))
    c.drawCircle(CX, CY, R_RING, paint(RING, 1, True, 2.5))
    fl = font('in500', 30)
    for i, s in enumerate(SIGNS):
        x, y = pos(R_LAB, i * 30)
        house = (i - 8) % 12 + 1
        yb = y + 10
        if s == 'Capricorn' and st['caplabel'] > 0:
            text(c, 'Capricorn · 2', x, yb, fl, WARM, 1 - st['caplabel'], 'center')
            text(c, 'Exact on 17 Mar 2027', x, yb, font('in500', 30), ORANGE_DK, st['caplabel'], 'center')
            continue
        text(c, f'{s} · {house}', x, yb, fl, WARM, st['house'], 'center')
        text(c, s, x, yb, fl, WARM, 1 - st['house'], 'center')
    # Nadi box behind Saturn and Rahu
    if st['N2'] > 0:
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(380, CY + R_G - 43, 310, 86), 43, 43)
        c.drawRRect(rr, paint('#E4EEE4', st['N2'] * 0.9))
        c.drawRRect(rr, paint(SAGE, st['N2'], True, 4.5))
    # Parashari arrows
    p, a = st['A1']; arrow(c, *A1, TERRA, 5, p, a)
    p, a = st['A2']; arrow(c, *A2, LAV, 5, p, a)
    p, a = st['A3']; arrow(c, *A3, LAV, 5, p, a)
    p, a = st['A4']; arrow(c, *A4, TERRA, 5, p, a, dash=[14, 10])
    # Nadi ties
    p, a = st['N1']; arrow(c, *N1, SAGE, 6, p, a, dash=[16, 12], head=False)
    p, a = st['N3']; arrow(c, *N3, SAGE, 6, p, a, head=False)
    # pulses
    if st['pulse'] > 0:
        pulse_ring(c, 540, CY + R_G, 92, 125, (t - 50.6) / 1.6, ORANGE_DK, st['pulse'])
    if st['rahu_pulse'] > 0:
        pulse_ring(c, RAHU[0], RAHU[1], 60, 120, (t - 27.0) / 1.6, TERRA, st['rahu_pulse'])
    # birth grahas
    pill(c, *SATURN, 'Saturn', 'birth')
    pill(c, *MARS, 'Mars', 'birth', st['mm'])
    pill(c, *MOON, 'Moon', 'birth', st['mm'])
    pill(c, *SUVE, 'Sun, Venus', 'birth', st['suve'], fs=26)
    # sky grahas
    kx, ky = lerp(KETU0[0], KETU[0], st['ketu_p']), lerp(KETU0[1], KETU[1], st['ketu_p'])
    pill(c, kx, ky, 'Ketu', 'sky', st['ketu_a'])
    rx, ry = lerp(RAHU0[0], RAHU[0], st['rahu_p']), lerp(RAHU0[1], RAHU[1], st['rahu_p'])
    pill(c, rx, ry, 'Rahu', 'sky', st['rahu_a'])
    pill(c, SKYMARS[0], SKYMARS[1] + st['skymars_dy'], 'Mars', 'sky', st['skymars'])
    c.restore()


# ---------------- text scenes ----------------
def head(c, t, i, s, y=330, delay=0.0):
    a = sa(t, i, delay)
    return block(c, s, MX, y + slide(t, i, delay), font('fr500i', 70), NAVY, a, 82)


def body(c, t, i, s, y, delay=0.0, hexc=SLATE):
    a = sa(t, i, delay)
    return block(c, s, MX, y + slide(t, i, delay), font('in400', 42), hexc, a, 58)


def accent(c, t, i, s, y, delay=0.0, size=50):
    a = sa(t, i, delay)
    return block(c, s, MX, y + slide(t, i, delay), font('fr500i', size), TERRA, a, size + 12)


def chip(c, x, y, w, h, title, sub, a, fill=CHIP, border=CHIP_B):
    if a <= 0.003:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 22, 22)
    c.drawRRect(rr, paint(fill, a))
    c.drawRRect(rr, paint(border, a, True, 2.5))
    if sub:
        text(c, title, x + 26, y + 52, font('fr500i', 40), NAVY, a)
        text(c, sub, x + 26, y + 96, font('in400', 30), SLATE, a)
    else:
        text(c, title, x + 26, y + h / 2 + 12, font('in500', 34), NAVY, a)


def scene_text(c, t):
    # 1 title
    i = 0
    a = sa(t, i, 0.25)
    text(c, 'Parashari and Bhrigu Nandi Nadi', MX, 300 + slide(t, i, 0.25), font('in500', 32), TERRA, a)
    a = sa(t, i, 0.55)
    for k, ln in enumerate(['How a transit', 'becomes an event']):
        text(c, ln, MX, 430 + k * 108 + slide(t, i, 0.55), font('fr600', 100), NAVY, a)
    a = sa(t, i, 1.0)
    text(c, 'Ketu in Cancer, facing Saturn', MX, 655 + slide(t, i, 1.0), font('fr400i', 54), SLATE, a)
    # 2 setup
    i = 1
    yh = head(c, t, i, 'Late 2026 to mid 2028')
    yl = body(c, t, i, 'Ketu moves into Cancer and Rahu into Capricorn. In this example chart, Saturn sits in Capricorn, the 2nd house.', yh + 120, 0.3)
    a = sa(t, i, 1.2)
    if a > 0:
        yy = yl + 82 + slide(t, i, 1.2)
        pill(c, MX + 110, yy - 10, 'birth chart', 'birth', a, fs=28, minw=200)
        pill(c, MX + 350, yy - 10, 'in the sky', 'sky', a, fs=28, minw=190)
    # 3 Ketu's 7th
    i = 2
    yh = head(c, t, i, 'Ketu looks across at Saturn')
    yl = body(c, t, i, 'Its 7th aspect links the 8th house of sudden, hidden and shared money to the 2nd house of savings.', yh + 120, 0.3)
    accent(c, t, i, 'Hidden matters reach your savings.', yl + 92, 2.6)
    # 4 on vs facing
    i = 3
    head(c, t, i, 'On Saturn, or facing it?')
    for k, (y0, fill, border, title, sub, dl) in enumerate([
            (430, CARD1, CARD1_B, 'Ketu on Saturn', 'Works from inside, at full strength. Saturn\'s own karma pauses.', 0.6),
            (790, CARD2, CARD2_B, 'Ketu facing Saturn', 'Starts outside and lands inside, at about half strength.', 1.6)]):
        a = sa(t, i, dl)
        if a <= 0.003:
            continue
        dy = slide(t, i, dl)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(MX, y0 + dy, TW, 330), 28, 28)
        c.drawRRect(rr, paint(fill, a))
        c.drawRRect(rr, paint(border, a, True, 2.5))
        text(c, title, MX + 40, y0 + dy + 86, font('fr500i', 54), NAVY, a)
        block(c, sub, MX + 40, y0 + dy + 156, font('in400', 40), SLATE, a, 54, maxw=470)
        mx, my = 800, y0 + dy + 165
        if k == 0:
            box = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(mx - 125, my - 120, 250, 240), 24, 24)
            c.drawRRect(box, paint('#FFFFFF', a * 0.55))
            c.drawRRect(box, paint(CARD1_B, a, True, 2.5))
            text(c, 'Capricorn', mx, my - 76, font('in500', 26), WARM, a, 'center')
            pill(c, mx, my - 12, 'Ketu', 'sky', a)
            pill(c, mx, my + 62, 'Saturn', 'birth', a)
        else:
            pill(c, mx, my - 92, 'Ketu', 'sky', a)
            arrow(c, (mx, my - 52), (mx + 2, my), (mx, my + 50), TERRA, 5, 1.0, a, dash=[12, 9])
            pill(c, mx, my + 90, 'Saturn', 'birth', a)
    # 5 Rahu
    i = 4
    yh = head(c, t, i, 'Ketu never faces Saturn alone')
    yl = body(c, t, i, 'Rahu sits on Saturn at the same time.', yh + 120, 0.3)
    accent(c, t, i, 'Rahu pushes from inside. Ketu cuts from across.', yl + 92, 1.6)
    # 6 Saturn and Mars
    i = 5
    yh = head(c, t, i, 'Two aspects land on Ketu')
    yl = body(c, t, i, 'Saturn looks back: quick to arrive, slow to settle.', yh + 120, 0.4, NAVY)
    body(c, t, i, 'Mars adds its 4th: sharper, and costly, since here Mars rules the 12th house.', yl + 82, 3.4)
    # 7 Moon
    i = 6
    yl = head(c, t, i, 'Ketu pays out through its sign lord')
    yl = body(c, t, i, 'Cancer\'s lord, the Moon, sits in the 11th house of gains.', yl + 110, 0.4)
    accent(c, t, i, 'What goes out can come back the same way.', yl + 88, 2.4, 46)
    # 8 event
    i = 7
    head(c, t, i, 'How it becomes an event')
    items = [('1  Promise', 'the birth chart'), ('2  Links', 'the aspects'), ('3  Switch', 'the running dasha'), ('4  Spark', 'the exact degree')]
    for k, (ti, su) in enumerate(items):
        a = sa(t, i, 0.5 + 0.7 * k)
        dy = slide(t, i, 0.5 + 0.7 * k)
        x = MX + (k % 2) * 456
        y = 410 + (k // 2) * 136 + dy
        chip(c, x, y, 432, 120, ti, su, a)
    # 9 Nadi way
    i = 8
    yh = head(c, t, i, 'The Nadi way')
    yl = body(c, t, i, 'No houses, no special aspects. Grahas link only by direction, so Mars and the Moon drop out.', yh + 120, 0.4)
    a = sa(t, i, 4.0)
    if a > 0:
        yy = yl + 84 + slide(t, i, 4.0)
        c.drawLine(MX, yy - 12, MX + 70, yy - 12, paint(SAGE, a, True, 6))
        text(c, 'same sign: full', MX + 90, yy, font('in500', 32), SAGE_DK, a)
        c.drawLine(MX + 430, yy - 12, MX + 500, yy - 12, paint(SAGE, a, True, 6, [16, 12]))
        text(c, '7th: about half', MX + 520, yy, font('in500', 32), SAGE_DK, a)
    # 10 Nadi story
    i = 9
    head(c, t, i, 'Each graha is a matter')
    for k, lab in enumerate(['Saturn · work', 'Venus · money', 'Ketu · endings', 'Rahu · growth']):
        a = sa(t, i, 0.4 + 0.35 * k)
        dy = slide(t, i, 0.4 + 0.35 * k)
        chip(c, MX + (k % 2) * 456, 400 + (k // 2) * 100 + dy, 432, 84, lab, None, a)
    accent(c, t, i, 'One form of work ends. A bigger one grows. Money moves both ways.', 652, 2.6, 46)
    # 11 end
    i = 10
    a = sa(t, i, 0.6)
    if a > 0:
        dy = slide(t, i, 0.6)
        f = font('fr500i', 64)
        for k, ln in enumerate(['Your dates depend on', 'your own degrees.']):
            text(c, ln, W / 2, 800 + k * 80 + dy, f, NAVY, a, 'center')
    a = sa(t, i, 1.4)
    if a > 0:
        dy = slide(t, i, 1.4)
        text(c, 'Sutram', W / 2, 1120 + dy, font('fr600', 128), NAVY, a, 'center')
        text(c, 'sutram.ca', W / 2, 1200 + dy, font('in500', 46), ORANGE_DK, a, 'center')
        text(c, 'Know yourself · Know your time', W / 2, 1268 + dy, font('in400', 36), SLATE, a, 'center')


SURF = skia.Surface(W, H)


def render(t):
    c = SURF.getCanvas()
    c.clear(skia.Color(*BG))
    draw_wheel(c, t)
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
