#!/usr/bin/env python3
"""The philosophy library (15 Nov): posts that make people stop and look. Each one: a PHILOSOPHY pill and a plain
title, a drawn picture that moves, something the reader does right now, the question that turns back on them,
the Jyotish link, one classical line with its verse, and Try it today.
    python3 tools/philosophy.py            writes specs/, captions/ and x-drafts/ for every post below
    python3 tools/philosophy.py <id> ...   only those posts
Then: tools/render.py specs/<id>.json, tools/anim_motion.py specs/<id>.json --slide 1."""
import json, os, sys, math
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- drawing helpers (coordinates in a 600 x 520 box) ----------
def bird(cx, cy, face=1, k=None, o=None, fill='BG', stroke='CREAM', sw=4.5):
    """A small line-drawn bird standing at (cx, cy) = its feet, facing right (face=1) or left (-1). k: shared keyframes."""
    X = lambda x: cx + face * x; Y = lambda y: cy + y
    P = lambda pts: ' '.join(f'{X(a):.1f},{Y(b):.1f}' if isinstance(a, (int, float)) else a for a, b in pts)
    body = (f"M{X(-34):.1f},{Y(-26):.1f} C{X(-30):.1f},{Y(-54):.1f} {X(10):.1f},{Y(-62):.1f} {X(30):.1f},{Y(-44):.1f} "
            f"C{X(38):.1f},{Y(-36):.1f} {X(36):.1f},{Y(-22):.1f} {X(22):.1f},{Y(-16):.1f} C{X(4):.1f},{Y(-6):.1f} {X(-20):.1f},{Y(-8):.1f} {X(-34):.1f},{Y(-26):.1f} Z")
    tail = f"M{X(-32):.1f},{Y(-28):.1f} L{X(-60):.1f},{Y(-40):.1f} L{X(-54):.1f},{Y(-20):.1f} Z"
    beak = f"M{X(38):.1f},{Y(-52):.1f} L{X(54):.1f},{Y(-48):.1f} L{X(38):.1f},{Y(-43):.1f} Z"
    legs = f"M{X(-2):.1f},{Y(-10):.1f} L{X(-4):.1f},{Y(0):.1f} M{X(8):.1f},{Y(-10):.1f} L{X(8):.1f},{Y(0):.1f}"
    org = o or [cx, cy]
    els = [dict(t='path', a=dict(d=tail, fill=fill, stroke=stroke, **{'stroke-width': sw, 'stroke-linejoin': 'round'})),
           dict(t='path', a=dict(d=body, fill=fill, stroke=stroke, **{'stroke-width': sw, 'stroke-linejoin': 'round'})),
           dict(t='circle', a=dict(cx=round(X(26), 1), cy=Y(-48), r=15, fill=fill, stroke=stroke, **{'stroke-width': sw})),
           dict(t='path', a=dict(d=beak, fill='AMBER', stroke='AMBER', **{'stroke-width': 2, 'stroke-linejoin': 'round'})),
           dict(t='circle', a=dict(cx=round(X(30), 1), cy=Y(-51), r=2.6, fill=stroke)),
           dict(t='path', a=dict(d=legs, fill='none', stroke='GOLD', **{'stroke-width': 3, 'stroke-linecap': 'round'}))]
    if k:
        for e in els: e['k'] = k; e['o'] = org
    return els

def glow(cx, cy, r, k, grad='anG'):
    return dict(t='circle', a=dict(cx=cx, cy=cy, r=r, fill=f'url(#{grad})'), k=k)

def ring(cx, cy, r, k, color='AMBER', sw=2.4):
    return dict(t='circle', a=dict(cx=cx, cy=cy, r=r, fill='none', stroke=color, **{'stroke-width': sw}), k=k)

# ---------- the posts ----------
POSTS = []
def post(**p): POSTS.append(p); return p

# 1. The observer: two birds on one tree (Mundaka Upanishad 3.1.1-2)
def birds_visual():
    els = []
    tree = 'M300,520 C302,460 296,400 300,330 M300,352 C262,330 206,318 150,300 M300,318 C346,292 400,262 462,236 M300,330 C300,290 304,250 300,200'
    els.append(dict(t='path', a=dict(d=tree, fill='none', stroke='GOLD', **{'stroke-width': 7, 'stroke-linecap': 'round', 'stroke-opacity': .75})))
    for cx, cy, r in [(300, 170, 70), (210, 230, 54), (395, 196, 58), (250, 150, 44), (350, 140, 46), (160, 270, 34), (470, 214, 34)]:
        els.append(dict(t='circle', a=dict(cx=cx, cy=cy, r=r, fill='LEAF', **{'fill-opacity': .12, 'stroke': 'LEAF', 'stroke-opacity': .25, 'stroke-width': 1.5})))
    # fruit the first bird eats
    F = lambda cx, cy, t_gone: dict(t='circle', a=dict(cx=cx, cy=cy, r=10, fill='ROSE'),
                                   k=[[0, {'r': 10, 'opacity': 1}], [t_gone - .2, {'r': 10}], [t_gone, {'r': 0, 'opacity': 0}], [7.2, {'r': 0, 'opacity': 0}], [7.9, {'r': 10, 'opacity': 1}]])
    els += [F(150, 316, 3.1), F(132, 306, 4.3), dict(t='circle', a=dict(cx=172, cy=322, r=9, fill='ROSE', opacity=.8))]
    # the watcher's light
    els.append(glow(420, 214, 150, [[0, {'opacity': 0}], [4.4, {'opacity': 0}], [6.0, {'opacity': 1}], [7.2, {'opacity': 1}], [7.9, {'opacity': 0}]], 'anW'))
    els.append(ring(420, 214, 70, [[0, {'opacity': 0, 'r': 60}], [4.6, {'opacity': 0, 'r': 60}], [6.0, {'opacity': .7, 'r': 84}], [7.2, {'opacity': .6, 'r': 88}], [7.9, {'opacity': 0, 'r': 60}]]))
    # the eating bird pecks twice, the watching bird stays still
    peck = [[0, {'rot': 0}], [2.4, {'rot': 0}], [2.9, {'rot': -32}], [3.2, {'rot': -32}], [3.5, {'rot': 0}], [3.7, {'rot': 0}], [4.1, {'rot': -32}], [4.4, {'rot': -32}], [4.7, {'rot': 0}]]
    els += bird(208, 318, face=-1, k=peck, o=[200, 312])
    els += bird(420, 248, face=-1)
    return dict(w=600, h=520, vb='60 90 480 430', k=1.12, els=els)

post(id='phil-observer', title='Who is the\nobserver?', sub='Two birds sit on one tree', visual=birds_visual, cover_at=6.2,
     slides=[
        dict(at=1.0, title='Two birds,\none tree', closing='The oldest picture of you'),
        dict(at=3.0, title='One eats\nthe fruit', closing='Sweet, bitter, sweet again'),
        dict(at=6.2, title='The other\nonly watches', closing='It never eats. It never leaves'),
        dict(title='Right now you are\ntasting life', body=['Plans, worries, this post', '*Who is watching you taste it?*']),
        dict(title='Look for\nthe watcher', closing='No shape. No colour. No name'),
        dict(jyotish=True, title='The Moon tastes.\nThe Sun watches', closing='The Moon is the mind; the Sun is the soul',
             orbs=[{'kind': 'moon', 'r': 50, 'illum': .5, 'waxing': True}, {'kind': 'sun', 'r': 54, 'rings': False}]),
        dict(quote='Dvā suparṇā sayujā sakhāyā', source='Mundaka Upanishad 3.1.1', label='The Upanishads', closing='Two birds, close friends, on one tree'),
        dict(tryit=True, body=['At your next meal, notice the tasting', '*Then notice who notices*'], closing='Which bird are you?'),
     ],
     caption='''Who is the observer?

The Upanishads give the oldest picture of you. Two birds, close friends, sit on the same tree. One eats the fruit, sweet and bitter. The other eats nothing. It only watches (Mundaka Upanishad 3.1.1; the same verse is in the Rig Veda, 1.164.20).

Right now you are tasting life: plans, worries, this post. Who is watching you taste it?

Look for the watcher. You will not find a shape, a colour or a name. You find only the watching.

The next verse says the bird that eats grows sad, lost in the fruit. When it turns and sees the other bird, its sadness falls away (Mundaka Upanishad 3.1.2).

In Jyotish the Moon is the mind and the Sun is the soul (Brihat Parashara Hora Shastra, chapter 3). The mind tastes, the soul watches.

Try it today. At your next meal, notice the tasting. Then notice who notices. Which bird are you?''',
     x_text='''Who is the observer?

Two birds sit on one tree. One eats the fruit, sweet and bitter. The other only watches (Mundaka Upanishad 3.1.1)

Right now you are tasting life. Who is watching you taste it?''',
     x_slides=[1, 3, 4, 6], tags='#awareness #upanishads #vedanta #jyotish #sutram')


# ---------- more drawing helpers ----------
def C(cx, cy, r, **a): return dict(t='circle', a=dict(cx=cx, cy=cy, r=r, **a))
def Pth(d, **a): return dict(t='path', a=dict(d=d, **a))
def T(x, y, text, size=22, color='GOLD', anchor='middle', **a):
    return dict(t='text', a=dict(x=x, y=y, text=text, fill=color, **{'font-family': 'EB Garamond', 'font-size': size, 'text-anchor': anchor, 'letter-spacing': 3}, **a))
LINE = {'fill': 'none', 'stroke': 'CREAM', 'stroke-width': 5, 'stroke-linecap': 'round', 'stroke-linejoin': 'round'}
def lit(on, off=None, k=None): return k
def fade(times, vals): return [[t, {'opacity': v}] for t, v in zip(times, vals)]

def breath_visual():
    rk = [[0, {'r': 70}], [.6, {'r': 112}], [1.2, {'r': 70}], [1.8, {'r': 112}], [2.4, {'r': 70}], [5.2, {'r': 150}], [8, {'r': 70}]]
    rk2 = [[0, {'r': 90}], [.7, {'r': 130}], [1.3, {'r': 90}], [1.9, {'r': 130}], [2.5, {'r': 90}], [5.4, {'r': 176}], [8, {'r': 90}]]
    return dict(w=600, h=520, k=1.12, els=[
        glow(300, 260, 230, fade([0, 2.2, 3.2, 7.2, 8], [0, 0, 1, 1, 0]), 'anW'),
        dict(t='circle', a=dict(cx=300, cy=260, r=90, fill='none', stroke='GOLD', **{'stroke-width': 2, 'stroke-opacity': .45}), k=rk2, e='sine'),
        dict(t='circle', a=dict(cx=300, cy=260, r=70, fill='none', stroke='CREAM', **{'stroke-width': 6}), k=rk, e='sine'),
        C(300, 260, 9, fill='AMBER')])

def flame_paths(big=1.0):
    def f(s, dx=0):
        P = lambda x, y: f"{300 + (x - 300) * s + dx:.1f},{420 - (420 - y) * s:.1f}"
        return (f"M{P(300,420)} C{P(230,400)} {P(220,330)} {P(250,280)} C{P(262,320)} {P(280,330)} {P(284,300)} C{P(270,250)} {P(290,190)} {P(330,150)} "
                f"C{P(326,210)} {P(360,240)} {P(368,270)} C{P(372,250)} {P(380,240)} {P(392,228)} C{P(410,300)} {P(400,390)} {P(300,420)} Z")
    return f
def anger_visual():
    f = flame_paths()
    big1, big2, small = f(1.0), f(1.0, 0)[:], f(.48)
    big2 = flame_paths()(1.05, -8)
    fk = [[0, {'d': big1}], [.5, {'d': big2}], [1.0, {'d': big1}], [1.5, {'d': big2}], [2.0, {'d': big1}], [2.5, {'d': big2}], [3.2, {'d': big1}], [5.0, {'d': small}], [7.0, {'d': small}], [8, {'d': big1}]]
    return dict(w=600, h=520, k=1.1, els=[
        glow(300, 330, 200, [[0, {'opacity': .9}], [3.2, {'opacity': .9}], [5, {'opacity': .35}], [7, {'opacity': .35}], [8, {'opacity': .9}]]),
        dict(t='path', a=dict(d=big1, fill='RED', **{'fill-opacity': .85, 'stroke': 'AMBER', 'stroke-width': 3}), k=fk, e='sine'),
        Pth('M220,430 H380', stroke='GOLD', **{'stroke-width': 4, 'stroke-linecap': 'round'}),
        glow(300, 110, 90, fade([0, 2.4, 3.2, 7, 8], [0, 0, 1, 1, 0]), 'anW'),
        dict(t='path', a=dict(d='M262,110 C282,92 318,92 338,110 C318,128 282,128 262,110 Z', fill='none', stroke='CREAM', **{'stroke-width': 4}), k=fade([0, 2.4, 3.2, 7, 8], [0, 0, 1, 1, 0])),
        dict(t='circle', a=dict(cx=300, cy=110, r=8, fill='CREAM'), k=fade([0, 2.4, 3.2, 7, 8], [0, 0, 1, 1, 0]))])

def eye(cx, cy, iris, k_open):
    op = f"M{cx-88},{cy} C{cx-48},{cy-52} {cx+48},{cy-52} {cx+88},{cy} C{cx+48},{cy+52} {cx-48},{cy+52} {cx-88},{cy} Z"
    cl = f"M{cx-88},{cy} C{cx-48},{cy-3} {cx+48},{cy-3} {cx+88},{cy} C{cx+48},{cy+3} {cx-48},{cy+3} {cx-88},{cy} Z"
    dk = [[t, {'d': op if v else cl}] for t, v in k_open]
    ik = [[t, {'opacity': 1 if v else 0}] for t, v in k_open]
    look = [[0, {'tx': 0}], [1.0, {'tx': -16}], [2.0, {'tx': 16}], [2.4, {'tx': 0}], [8, {'tx': 0}]]
    return [dict(t='path', a=dict(d=op, fill='BG', stroke='CREAM', **{'stroke-width': 4.5}), k=dk),
            dict(t='circle', a=dict(cx=cx, cy=cy, r=27, fill=iris), k=[a + b for a, b in zip([[x[0], dict(x[1])] for x in ik], [[]] * len(ik))]),
            dict(t='circle', a=dict(cx=cx, cy=cy, r=10, fill='BG'), k=ik)]
def reading_visual():
    ko = [(0, 1), (2.45, 1), (2.6, 0), (2.75, 1), (8, 1)]
    els = [glow(300, 120, 170, fade([0, 3.0, 4.6, 7.2, 8], [0, 0, 1, 1, 0]), 'anW')]
    els += eye(190, 300, 'MOON', ko) + eye(410, 300, 'SUN', ko)
    els += [T(190, 400, 'MOON', 20), T(410, 400, 'SUN', 20)]
    return dict(w=600, h=520, k=1.1, els=els)

def chart_visual():
    cx, cy, R = 300, 290, 190
    els = [C(cx, cy, R, fill='none', stroke='GOLD', **{'stroke-width': 3, 'stroke-opacity': .7}), C(cx, cy, R * .55, fill='none', stroke='GOLD', **{'stroke-width': 2, 'stroke-opacity': .5})]
    d = ' '.join(f"M{cx + R*.55*math.cos(math.radians(a)):.1f},{cy + R*.55*math.sin(math.radians(a)):.1f} L{cx + R*math.cos(math.radians(a)):.1f},{cy + R*math.sin(math.radians(a)):.1f}" for a in range(0, 360, 30))
    els.append(Pth(d, stroke='GOLD', **{'stroke-width': 2, 'stroke-opacity': .5}))
    for col, rr, a0, turns, sz in [('SUN', .78, 20, 1, 13), ('MOON', .7, 140, 2, 11), ('RED', .86, 250, 1, 10), ('LEAF', .66, 300, -1, 10), ('AMBER', .9, 80, 1, 9)]:
        x = cx + R * rr * math.cos(math.radians(a0)); y = cy + R * rr * math.sin(math.radians(a0))
        els.append(dict(t='circle', a=dict(cx=round(x, 1), cy=round(y, 1), r=sz, fill=col), k=[[0, {'rot': 0}], [8, {'rot': 360 * turns}]], e='lin', o=[cx, cy]))
    els += [glow(500, 70, 110, [[0, {'opacity': .75}], [4, {'opacity': 1}], [8, {'opacity': .75}]], 'anW'), C(500, 70, 10, fill='CREAM'),
            Pth('M488,84 L436,150', stroke='CREAM', **{'stroke-width': 2, 'stroke-dasharray': '4 8', 'stroke-opacity': .7})]
    return dict(w=600, h=520, k=1.08, els=els)

def gap_visual():
    els = [glow(300, 270, 200, fade([0, 3.4, 4.6, 6.0, 6.8, 8], [.15, .15, 1, 1, .15, .15]), 'anW'), C(300, 270, 10, fill='CREAM')]
    spots = [(170, 200, 0.0), (420, 170, .5), (230, 360, 1.0), (400, 330, 1.5), (300, 150, 2.0), (180, 300, 5.9), (420, 260, 6.3)]
    for x, y, t0 in spots:
        k = [[0, {'opacity': 0, 'r': 6, 'cy': y}], [t0, {'opacity': 0, 'r': 6, 'cy': y}], [t0 + .3, {'opacity': .9, 'r': 26, 'cy': y}], [t0 + 1.6, {'opacity': .6, 'r': 30, 'cy': y - 24}], [t0 + 2.2, {'opacity': 0, 'r': 34, 'cy': y - 40}], [8, {'opacity': 0, 'r': 34, 'cy': y - 40}]]
        els.append(dict(t='circle', a=dict(cx=x, cy=y, r=6, fill='none', stroke='CREAM', **{'stroke-width': 3}), k=k))
    return dict(w=600, h=520, k=1.1, els=els)

def wave(y, amp):
    pts = ' '.join(f"{x},{y + amp * math.sin(x / 26):.1f}" for x in range(80, 521, 20))
    return 'M' + pts.replace(' ', ' L')
def lake_visual():
    els = [C(300, 120, 46, fill='url(#anM)'), glow(300, 120, 120, [[0, {'opacity': .5}], [8, {'opacity': .5}]], 'anW')]
    for i, y in enumerate((330, 370, 410)):
        k = [[0, {'d': wave(y, 9)}], [1.0, {'d': wave(y, -9)}], [2.0, {'d': wave(y, 9)}], [4.5, {'d': wave(y, 0)}], [7.0, {'d': wave(y, 0)}], [8, {'d': wave(y, 9)}]]
        els.append(dict(t='path', a=dict(d=wave(y, 9), fill='none', stroke='WATER', **{'stroke-width': 3.5, 'stroke-opacity': .9}), k=k, e='sine'))
    els.append(dict(t='ellipse', a=dict(cx=300, cy=372, rx=46, ry=40, fill='none', stroke='MOON', **{'stroke-width': 8, 'stroke-dasharray': '6 22'}),
                    k=[[0, {'stroke-dasharray': '6 22', 'opacity': .55}], [2.5, {'stroke-dasharray': '6 22', 'opacity': .55}], [4.5, {'stroke-dasharray': '300 0', 'opacity': .95}], [7.0, {'stroke-dasharray': '300 0', 'opacity': .95}], [8, {'stroke-dasharray': '6 22', 'opacity': .55}]]))
    els.append(dict(t='ellipse', a=dict(cx=300, cy=372, rx=40, ry=34, fill='MOON', opacity=0), k=fade([0, 3.0, 4.5, 7.0, 8], [0, 0, .55, .55, 0])))
    return dict(w=600, h=520, k=1.1, els=els)

def eclipse_visual():
    k = [[0, {'cx': 80}], [3.6, {'cx': 300}], [4.4, {'cx': 300}], [8, {'cx': 520}]]
    return dict(w=600, h=520, k=1.1, els=[
        glow(300, 260, 240, [[0, {'opacity': 1}], [3.4, {'opacity': .55}], [4.6, {'opacity': .55}], [8, {'opacity': 1}]], 'anW'),
        C(300, 260, 92, fill='url(#anS)'),
        ring(300, 260, 100, fade([0, 3.2, 3.6, 4.4, 4.8, 8], [0, 0, .9, .9, 0, 0]), 'MOON', 5),
        dict(t='circle', a=dict(cx=80, cy=260, r=94, fill='BG', stroke='GOLD', **{'stroke-width': 1.5, 'stroke-opacity': .5}), k=k, e='lin'),
        T(300, 430, 'THE SUN NEVER STOPS SHINING', 20)])

def moonfull_visual():
    defs = "<clipPath id='mclip'><circle cx='300' cy='250' r='110'/></clipPath>"
    k = [[0, {'cx': 300}], [4.0, {'cx': 540}], [4.001, {'cx': 60}], [8, {'cx': 300}]]
    return dict(w=600, h=520, k=1.1, defs=defs, els=[
        C(300, 250, 110, fill='url(#anM)'),
        dict(t='circle', a=dict(cx=300, cy=250, r=112, fill='BG', opacity=.94, **{'clip-path': 'url(#mclip)'}), k=k, e='lin'),
        C(300, 250, 122, fill='none', stroke='MOON', **{'stroke-width': 2, 'stroke-dasharray': '3 9', 'stroke-opacity': .7}),
        T(300, 430, 'ALWAYS WHOLE', 20)])

def sleep_visual():
    rows = [('WAKING', 150, 0.0), ('DREAM', 240, 2.6), ('DEEP SLEEP', 330, 5.2)]
    els = []
    for name, y, t0 in rows:
        k = fade([0, t0, t0 + .4, t0 + 2.4, t0 + 2.8, 8], [.25, .25, 1, 1, .25, .25]) if t0 else fade([0, 2.4, 2.8, 7.6, 8], [1, 1, .25, .25, 1])
        els.append(dict(t='rect', a=dict(x=120, y=y - 34, width=360, height=68, rx=34, fill='CREAM', **{'fill-opacity': .08, 'stroke': 'CREAM', 'stroke-width': 3}), k=k))
        els.append(dict(t='text', a=dict(x=300, y=y + 8, text=name, fill='CREAM', **{'font-family': 'EB Garamond', 'font-size': 24, 'text-anchor': 'middle', 'letter-spacing': 4}), k=k))
    els += [glow(300, 430, 160, [[0, {'opacity': .9}], [4, {'opacity': 1}], [8, {'opacity': .9}]], 'anW'),
            Pth('M110,430 H490', stroke='AMBER', **{'stroke-width': 5, 'stroke-linecap': 'round'}), T(300, 476, 'THE ONE WHO KNOWS', 20, 'AMBER')]
    return dict(w=600, h=520, k=1.08, els=els)

def neti_visual():
    names = [('BODY', 200, 1.0), ('NAME', 160, 2.0), ('THOUGHTS', 120, 3.0), ('FEELINGS', 80, 4.0)]
    els = [glow(300, 270, 190, fade([0, 4.0, 5.2, 7.2, 8], [.2, .2, 1, 1, .2]), 'anW'), C(300, 270, 12, fill='CREAM')]
    for nm, r, t0 in names:
        k = fade([0, t0, t0 + .6, 7.2, 8], [1, 1, 0, 0, 1])
        els.append(dict(t='circle', a=dict(cx=300, cy=270, r=r, fill='none', stroke='GOLD', **{'stroke-width': 3}), k=k))
        els.append(dict(t='text', a=dict(x=300, y=270 - r + 28, text=nm, fill='GOLD', **{'font-family': 'EB Garamond', 'font-size': 20, 'text-anchor': 'middle', 'letter-spacing': 4}), k=k))
    return dict(w=600, h=520, k=1.08, els=els)

def rope_visual():
    curve = 'M140,380 C200,300 260,420 320,340 C370,270 420,380 470,300'
    return dict(w=600, h=520, k=1.1, els=[
        glow(110, 220, 260, fade([0, 2.4, 4.0, 7.2, 8], [.08, .08, 1, 1, .08]), 'anW'),
        Pth('M96,236 Q110,206 124,236 Z', fill='AMBER', k=None), Pth('M92,240 H128 L120,256 H100 Z', fill='GOLD'),
        dict(t='path', a=dict(d=curve, fill='none', stroke='LEAF', **{'stroke-width': 18, 'stroke-linecap': 'round', 'stroke-opacity': .9}), k=fade([0, 4.0, 5.0, 7.2, 8], [.9, .9, 0, 0, .9])),
        dict(t='ellipse', a=dict(cx=478, cy=294, rx=22, ry=14, fill='LEAF'), k=fade([0, 4.0, 5.0, 7.2, 8], [1, 1, 0, 0, 1])),
        dict(t='circle', a=dict(cx=484, cy=290, r=3, fill='BG'), k=fade([0, 4.0, 5.0, 7.2, 8], [1, 1, 0, 0, 1])),
        dict(t='path', a=dict(d=curve, fill='none', stroke='GOLD', **{'stroke-width': 16, 'stroke-linecap': 'round', 'stroke-dasharray': '10 6'}), k=fade([0, 4.0, 5.0, 7.2, 8], [0, 0, 1, 1, 0]))])

def pot_visual():
    pot = 'M220,180 C200,200 170,250 175,320 C180,390 240,430 300,430 C360,430 420,390 425,320 C430,250 400,200 380,180 Z'
    els = []
    for x in range(90, 520, 40):
        for y in range(90, 470, 40):
            els.append(C(x, y, 2.4, fill='CREAM', opacity=.35))
    els += [glow(300, 300, 200, [[0, {'opacity': .35}], [8, {'opacity': .35}]], 'anW'),
            dict(t='path', a=dict(d=pot, fill='none', stroke='AMBER', **{'stroke-width': 7, 'stroke-linejoin': 'round'}), k=fade([0, 3.0, 4.6, 7.0, 8], [1, 1, 0, 0, 1])),
            dict(t='path', a=dict(d='M210,180 H390', fill='none', stroke='AMBER', **{'stroke-width': 7, 'stroke-linecap': 'round'}), k=fade([0, 3.0, 4.6, 7.0, 8], [1, 1, 0, 0, 1]))]
    return dict(w=600, h=520, k=1.08, els=els)

def onelight_visual():
    els = [glow(110, 260, 200, [[0, {'opacity': .8}], [4, {'opacity': 1}], [8, {'opacity': .8}]], 'anW'), C(110, 260, 60, fill='url(#anS)')]
    for x, y, r in [(290, 160, 26), (330, 330, 20), (430, 230, 32), (500, 380, 18), (520, 120, 16)]:
        els.append(C(x, y, r, fill='#2A2622'))
        els.append(dict(t='path', a=dict(d=f"M{x},{y-r} A{r},{r} 0 0 0 {x},{y+r} A{r*.4:.1f},{r} 0 0 1 {x},{y-r} Z", fill='MOON'), k=fade([0, 4, 8], [.75, 1, .75])))
    els.append(dict(t='path', a=dict(d='M180,200 L260,170 M180,260 L280,260 M180,320 L300,340', stroke='AMBER', **{'stroke-width': 2.5, 'stroke-dasharray': '6 10', 'stroke-dashoffset': 0}), k=[[0, {'stroke-dashoffset': 0}], [8, {'stroke-dashoffset': -64}]], e='lin'))
    return dict(w=600, h=520, k=1.08, els=els)

def screen_visual():
    fire = flame_paths()(.42)
    fire = fire.replace('M300.0', 'M300.0')
    rain = ' '.join(f"M{x},{150 + (x * 7) % 60} L{x - 12},{200 + (x * 7) % 60}" for x in range(170, 440, 26))
    return dict(w=600, h=520, k=1.08, els=[
        dict(t='rect', a=dict(x=120, y=110, width=360, height=250, rx=8, fill='CREAM', **{'fill-opacity': .06, 'stroke': 'GOLD', 'stroke-width': 5})),
        dict(t='path', a=dict(d=fire, fill='RED', **{'fill-opacity': .9}, transform='translate(0 -110)'), k=fade([0, 2.4, 2.8, 7.6, 8], [1, 1, 0, 0, 1])),
        dict(t='path', a=dict(d=rain, fill='none', stroke='SKY', **{'stroke-width': 3, 'stroke-linecap': 'round'}), k=fade([0, 2.6, 3.0, 5.0, 5.4, 8], [0, 0, 1, 1, 0, 0])),
        dict(t='circle', a=dict(cx=300, cy=235, r=46, fill='url(#anS)'), k=fade([0, 5.2, 5.6, 7.6, 8], [0, 0, 1, 1, 0])),
        Pth('M260,360 L230,430 M340,360 L370,430 M210,430 H390', fill='none', stroke='GOLD', **{'stroke-width': 4, 'stroke-linecap': 'round'}),
        T(300, 470, 'THE SCREEN STAYS THE SAME', 19)])

def mirror_visual():
    els = [glow(300, 260, 170, [[0, {'opacity': .9}], [8, {'opacity': .9}]], 'anW'),
           dict(t='ellipse', a=dict(cx=300, cy=260, rx=150, ry=190, fill='none', stroke='GOLD', **{'stroke-width': 8}))]
    for i, x in enumerate(range(190, 431, 60)):
        t0 = 2.4 + i * .45
        els.append(dict(t='ellipse', a=dict(cx=x, cy=260, rx=70, ry=190, fill='MOON', opacity=.62, filter='url(#anB)', **{'clip-path': 'url(#mrr)'}), k=fade([0, t0, t0 + .5, 7.2, 8], [.62, .62, 0, 0, .62])))
    return dict(w=600, h=520, k=1.08, defs="<clipPath id='mrr'><ellipse cx='300' cy='260' rx='146' ry='186'/></clipPath>", els=els)

def ocean_visual():
    return dict(w=600, h=520, k=1.08, els=[
        C(470, 110, 36, fill='url(#anM)'),
        dict(t='rect', a=dict(x=70, y=330, width=460, height=150, fill='WATER', **{'fill-opacity': .35})),
        Pth('M70,330 H530', stroke='MOON', **{'stroke-width': 4}),
        dict(t='path', a=dict(d='M100,120 C150,190 120,250 170,330 M250,90 C290,170 240,240 290,330 M380,150 C350,220 420,270 390,330', fill='none', stroke='SKY',
             **{'stroke-width': 6, 'stroke-linecap': 'round', 'stroke-dasharray': '18 14', 'stroke-dashoffset': 0}), k=[[0, {'stroke-dashoffset': 0}], [8, {'stroke-dashoffset': -128}]], e='lin'),
        T(300, 420, 'STILL FULL', 20, 'MOON')])

def cloud(x, y, s=1.0):
    return f"M{x-60*s:.1f},{y:.1f} C{x-60*s:.1f},{y-30*s:.1f} {x-20*s:.1f},{y-40*s:.1f} {x-6*s:.1f},{y-26*s:.1f} C{x+6*s:.1f},{y-56*s:.1f} {x+56*s:.1f},{y-52*s:.1f} {x+58*s:.1f},{y-20*s:.1f} C{x+86*s:.1f},{y-20*s:.1f} {x+86*s:.1f},{y+10*s:.1f} {x+60*s:.1f},{y+10*s:.1f} L{x-50*s:.1f},{y+10*s:.1f} C{x-70*s:.1f},{y+10*s:.1f} {x-72*s:.1f},{y:.1f} {x-60*s:.1f},{y:.1f} Z"
def sky_visual():
    els = [dict(t='rect', a=dict(x=70, y=90, width=460, height=360, rx=24, fill='SKY', **{'fill-opacity': .12, 'stroke': 'GOLD', 'stroke-width': 2, 'stroke-opacity': .4})),
           glow(430, 160, 70, [[0, {'opacity': .9}], [4, {'opacity': 1}], [8, {'opacity': .9}]], 'anW'), C(430, 160, 7, fill='CREAM')]
    for y, s, dark, sh in [(210, 1.0, False, 0), (320, 1.2, True, 3.0), (390, .8, False, 5.5)]:
        x0 = -60 + sh * 90; x1 = x0 + 720
        k = [[0, {'d': cloud(x0, y, s)}], [8, {'d': cloud(x1, y, s)}]] if sh < 4 else [[0, {'d': cloud(x0 - 720, y, s)}], [8, {'d': cloud(x0, y, s)}]]
        els.append(dict(t='path', a=dict(d=cloud(x0, y, s), fill='#4A4A50' if dark else 'MOON', **{'fill-opacity': .85 if dark else .55, 'clip-path': 'url(#skc)'}), k=k, e='lin'))
    return dict(w=600, h=520, k=1.08, defs="<clipPath id='skc'><rect x='70' y='90' width='460' height='360' rx='24'/></clipPath>", els=els)

def bell_visual():
    bell = 'M260,150 C260,110 340,110 340,150 L350,230 C352,250 368,256 368,266 H232 C232,256 248,250 250,230 Z'
    els = [dict(t='path', a=dict(d=bell, fill='none', stroke='GOLD', **{'stroke-width': 6, 'stroke-linejoin': 'round'}),
                k=[[0, {'rot': 0}], [.15, {'rot': 8}], [.35, {'rot': -6}], [.6, {'rot': 3}], [.9, {'rot': 0}], [8, {'rot': 0}]], o=[300, 112]),
           C(300, 278, 9, fill='GOLD')]
    for i in range(4):
        t0 = .3 + i * .45
        els.append(dict(t='circle', a=dict(cx=300, cy=210, r=60, fill='none', stroke='CREAM', **{'stroke-width': 3}),
                        k=[[0, {'r': 60, 'opacity': 0}], [t0, {'r': 60, 'opacity': .9}], [t0 + 2.4, {'r': 250, 'opacity': 0}], [8, {'r': 250, 'opacity': 0}]], e='out'))
    els += [glow(300, 400, 120, fade([0, 3.6, 5.0, 7.4, 8], [0, 0, 1, 1, 0]), 'anW'), dict(t='circle', a=dict(cx=300, cy=400, r=8, fill='CREAM'), k=fade([0, 3.6, 5.0, 7.4, 8], [0, 0, 1, 1, 0]))]
    return dict(w=600, h=520, k=1.08, els=els)

def lamp_visual():
    f = flame_paths()
    tall = f(.4, 0); lean1 = f(.36, -14); lean2 = f(.38, 12)
    tall = tall.replace('420.0', '420.0')
    fk = [[0, {'d': lean1}], [.4, {'d': lean2}], [.8, {'d': lean1}], [1.2, {'d': lean2}], [1.6, {'d': lean1}], [2.0, {'d': lean2}], [2.4, {'d': lean1}], [2.8, {'d': lean2}], [3.6, {'d': tall}], [7.4, {'d': tall}], [8, {'d': lean1}]]
    wind = 'M70,170 C140,150 180,190 250,170 M60,230 C130,210 170,250 240,230 M80,290 C150,270 190,310 260,290'
    return dict(w=600, h=520, k=1.1, els=[
        glow(300, 330, 180, [[0, {'opacity': .45}], [2.8, {'opacity': .45}], [3.8, {'opacity': 1}], [7.4, {'opacity': 1}], [8, {'opacity': .45}]], 'anG'),
        dict(t='path', a=dict(d=lean1, fill='SUN', transform='translate(0 0)'), k=fk, e='sine'),
        Pth('M220,420 C230,460 370,460 380,420 Z', fill='GOLD', **{'fill-opacity': .9}),
        dict(t='path', a=dict(d=wind, fill='none', stroke='SKY', **{'stroke-width': 3, 'stroke-linecap': 'round', 'stroke-dasharray': '30 18', 'stroke-dashoffset': 0}),
             k=[[0, {'stroke-dashoffset': 0, 'opacity': .9}], [2.8, {'stroke-dashoffset': -140, 'opacity': .9}], [3.4, {'stroke-dashoffset': -170, 'opacity': 0}], [7.4, {'stroke-dashoffset': -170, 'opacity': 0}], [8, {'stroke-dashoffset': -200, 'opacity': .9}]], e='lin')])


# ---------- the rest of the library, in posting order ----------
S = lambda **k: dict(**k)
SUN = {'kind': 'sun', 'r': 54, 'rings': False}; MOONR = {'kind': 'moon', 'r': 50, 'illum': .5, 'waxing': True}
MOONL = {'kind': 'moon', 'r': 50, 'illum': .5, 'waxing': False}

post(id='phil-not-your-chart', title='You are not\nyour chart', sub='Who is it that reads the chart?', visual=chart_visual, cover_at=4.0,
     slides=[S(at=2.0, title='The chart\nmoves', closing='Grahas, signs, houses, dashas'),
             S(at=5.0, title='Something\nwatches it move', closing='It has no house of its own'),
             S(title='The chart is\nthe field', body=['Body, mind, timing, karma', '*You are the one who knows the field*']),
             S(title='Read your chart\nlike a map', closing='It shows the road ahead'),
             S(jyotish=True, title='The 1st house\nis the body', closing='The knower has no house', orbs=[SUN]),
             S(quote='Kṣetra, kṣetrajña', source='Bhagavad Gita, chapter 13', label='Bhagavad Gita', closing='The field, and the knower of the field'),
             S(tryit=True, body=['When a reading scares you', '*Ask: who is reading this?*'], closing='The chart shows the weather')],
     caption="""You are not your chart

Your birth chart moves: grahas walk through signs, houses light up, dashas (the periods each graha runs) begin and end. It describes a body, a mind and their timing.

Something watches all of it move. That watcher has no house of its own.

The Gita calls the body and mind the field (kshetra), and you the knower of the field (kshetrajna) (Bhagavad Gita, chapter 13). In Jyotish the 1st house is the body (Brihat Parashara Hora Shastra, chapter 11). The knower is in no house.

So read your chart like a map. It shows the weather you walk through. It does not say who you are.

Try it today. When a reading scares you, ask yourself who is reading it.""",
     x_text="""You are not your chart

The chart is the field: body, mind, timing. You are the one who knows the field (Bhagavad Gita, chapter 13)

Read your chart like a map. It shows the road ahead""",
     x_slides=[1, 3, 4, 7], tags='#jyotish #vedicastrology #bhagavadgita #awareness #sutram')

post(id='phil-breath', title='Who is\nbreathing?', sub='Notice your breath, right now', visual=breath_visual, cover_at=4.6,
     slides=[S(at=1.0, title='Notice\nyour breath', closing="Don't control it. Just watch"),
             S(at=4.6, title='It slows\nby itself', closing='Nobody slowed it'),
             S(title='Are you\nbreathing?', body=['Or is breathing happening', '*and you are the one who knows?*']),
             S(title='Breath and mind\nmove together', closing='Still breath, still mind'),
             S(jyotish=True, title='The Moon\nis the mind', closing='Moods rise and fall like its tides', orbs=[MOONL]),
             S(quote='Cale vāte calaṃ cittam', source='Hatha Yoga Pradipika 2.2', label='Hatha Yoga Pradipika', closing='When the breath moves, the mind moves'),
             S(tryit=True, body=['Three slow breaths before you reply', '*Watch who is watching*'], closing='The breath knows the way')],
     caption="""Who is breathing?

Notice your breath, right now. Don't control it. Just watch.

It slows by itself. Nobody slowed it.

So are you breathing? Or is breathing happening, and you are the one who knows it?

The yoga texts say breath and mind move together: when the breath moves, the mind moves; when the breath is still, the mind is still (Hatha Yoga Pradipika 2.2). In Jyotish the Moon is the mind (Brihat Parashara Hora Shastra, chapter 3), and moods rise and fall like its tides.

Try it today. Take three slow breaths before you reply to anyone. Watch who is watching.""",
     x_text="""Who is breathing?

Notice your breath. It slows by itself. Nobody slowed it

When the breath moves, the mind moves (Hatha Yoga Pradipika 2.2)""",
     x_slides=[1, 3, 4, 7], tags='#breath #awareness #yoga #jyotish #sutram')

post(id='phil-eclipse', title='The Sun is\nnever eclipsed', sub='Only the view is blocked', visual=eclipse_visual, cover_at=2.6,
     slides=[S(at=3.0, title='A shadow\ncrosses', closing='From here, the Sun seems to go dark'),
             S(at=6.4, title='The Sun keeps\nshining', closing='Nothing touched the Sun'),
             S(title='Bad days are\nlike this', body=['Fear, grief, confusion pass over', '*The light behind them never stops*']),
             S(title='You are\nthe light', closing='Shadows pass'),
             S(jyotish=True, title='Rahu and Ketu\nare shadows', closing='Shadow grahas, with no light of their own', orbs=[SUN, {'kind': 'rahu', 'r': 46}]),
             S(quote='Ādityavaj jñānam', source='Bhagavad Gita 5.16', label='Bhagavad Gita', closing='Knowledge shines like the Sun'),
             S(tryit=True, body=['On a dark day, remember', '*A shadow is passing*'], closing='The Sun was never gone')],
     caption="""The Sun is never eclipsed

In an eclipse a shadow crosses, and from here the Sun seems to go dark. The Sun keeps shining. Nothing touched it. Only the view was blocked.

Bad days are like this. Fear, grief and confusion pass over. The light behind them never stops.

In Jyotish, Rahu and Ketu are the shadow grahas: points of shadow with no light of their own. They block the view for a while, then move on.

The Gita says that when ignorance is cleared, knowledge shines like the Sun (Bhagavad Gita 5.16).

Try it today. On a dark day, remember that a shadow is passing. The Sun was never gone.""",
     x_text="""The Sun is never eclipsed. Only the view is blocked

Bad days are like this. The light behind them never stops

Knowledge shines like the Sun (Bhagavad Gita 5.16)""",
     x_slides=[1, 3, 5, 6], tags='#eclipse #rahu #ketu #jyotish #sutram')

post(id='phil-screen', title='The screen\nand the film', sub='Fire on screen never burns it', visual=screen_visual, cover_at=1.3,
     slides=[S(at=1.3, title='A fire\non the screen', closing="The screen doesn't burn"),
             S(at=4.0, title='A flood\non the screen', closing='The screen stays dry'),
             S(title='Your life\nis the film', body=['Good scenes, hard scenes', '*You are the screen they play on*']),
             S(title='Enjoy the film', closing='Remember the screen'),
             S(jyotish=True, title='Every dasha\nis a new film', closing='The screen is the same', orbs=[{'kind': 'saturn', 'r': 46}, {'kind': 'jupiter', 'r': 50}]),
             S(quote='Nainaṃ dahati pāvakaḥ', source='Bhagavad Gita 2.23', label='Bhagavad Gita', closing='Fire does not burn it'),
             S(tryit=True, body=['In a hard scene today', '*Remember the screen*'], closing='Then keep watching')],
     caption="""The screen and the film

A fire on the screen does not burn the screen. A flood on the screen does not wet it.

Your life is the film, with good scenes and hard scenes. You are the screen they play on.

In Jyotish a dasha is the period one graha runs in your life, and each dasha is a new film: a Saturn film, a Jupiter film. The screen is the same through all of them.

The Gita says weapons do not cut the self and fire does not burn it (Bhagavad Gita 2.23).

Try it today. In a hard scene, remember the screen. Then keep watching.""",
     x_text="""The screen and the film

Fire on the screen never burns the screen. Your life is the film. You are the screen

Fire does not burn it (Bhagavad Gita 2.23)""",
     x_slides=[1, 3, 4, 6], tags='#awareness #bhagavadgita #dasha #jyotish #sutram')

post(id='phil-reading', title='Who is\nreading this?', sub='The eyes see the words. Who sees?', visual=reading_visual, cover_at=5.5,
     slides=[S(at=1.0, title='The eyes\nsee the words', closing='Black shapes on a screen'),
             S(at=5.5, title='Something knows\nwhat they see', closing='That knowing has no eyes'),
             S(title='Can you see\nyour seeing?', body=['You can see your hand', '*Can you see the one who sees?*']),
             S(title='That is what\nyou are', closing='The light behind the eyes'),
             S(jyotish=True, title='The Sun rules the right eye\nThe Moon, the left', closing='Who looks through both?', orbs=[SUN, MOONL]),
             S(quote='Yena cakṣūṃṣi paśyati', source='Kena Upanishad 1.6', label='Kena Upanishad', closing='That by which the eyes see'),
             S(tryit=True, body=['Look at something you love', '*Then notice the looking*'], closing='You are what notices')],
     caption="""Who is reading this?

Your eyes see the words, black shapes on a screen. Something knows what they see. That knowing has no eyes.

You can see your hand. Can you see the one who sees?

The Kena Upanishad calls it that by which the eyes see (Kena Upanishad 1.6).

In Jyotish the Sun rules the right eye and the Moon the left (Nadi texts, table of significations). Who looks through both?

Try it today. Look at something you love. Then notice the looking.""",
     x_text="""Who is reading this?

The eyes see the words. Something knows what they see

That by which the eyes see (Kena Upanishad 1.6)""",
     x_slides=[1, 3, 4, 6], tags='#awareness #upanishads #jyotish #nondual #sutram')

post(id='phil-anger', title='Anger,\nseen', sub='Name it, and watch the heat drop', visual=anger_visual, cover_at=5.5,
     slides=[S(at=1.0, title='Anger is here', closing='Say it, quietly, in your head'),
             S(at=5.5, title='The heat drops', closing="You didn't fight it. You saw it"),
             S(title='Who saw\nthe anger?', body=["The anger can't see itself", '*Something else was watching*']),
             S(title='Seen anger\nloses its grip', closing='Unseen anger runs the show'),
             S(jyotish=True, title='Mars is the ego', closing='Fire is useful. Fire in charge burns', orbs=[{'kind': 'mars', 'r': 50}]),
             S(quote='Krodhād bhavati sammohaḥ', source='Bhagavad Gita 2.63', label='Bhagavad Gita', closing='From anger comes confusion'),
             S(tryit=True, body=['Next time you feel it rise', '*Say: anger is here*'], closing='Then watch who is listening')],
     caption="""Anger, seen

Next time anger comes, say it quietly in your head: anger is here. Watch what happens. The heat drops. You didn't fight it. You saw it.

Who saw the anger? Anger can't see itself. Something else was watching.

Seen anger loses its grip. Unseen anger runs the show. The Gita traces the chain: from anger comes confusion, from confusion the memory goes (Bhagavad Gita 2.63).

In the Nadi texts Mars stands for ego, fire and energy. Fire is useful. Fire in charge burns.

Try it today. When you feel it rise, say: anger is here. Then watch who is listening.""",
     x_text="""Anger, seen

Say it quietly: anger is here. The heat drops. You didn't fight it. You saw it

From anger comes confusion (Bhagavad Gita 2.63)""",
     x_slides=[1, 2, 3, 6], tags='#anger #awareness #bhagavadgita #mars #sutram')

post(id='phil-lake', title='The still lake', sub='A calm mind shows the Moon', visual=lake_visual, cover_at=5.5,
     slides=[S(at=1.0, title='Waves break\nthe Moon', closing='A busy mind sees in pieces'),
             S(at=5.5, title='Still water\nholds it whole', closing='Nothing was added. Waves stopped'),
             S(title="You can't\nflatten water", body=['Hitting it makes more waves', '*Just stop stirring*']),
             S(title='Clarity is\nalready there', closing='Under the waves'),
             S(jyotish=True, title='The Moon\nis the mind', closing='And the Moon moves the tides', orbs=[MOONL]),
             S(quote="Tadā draṣṭuḥ svarūpe 'vasthānam", source='Yoga Sutra 1.3', label='Yoga Sutras', quotesize=78, closing='Then the seer rests in itself'),
             S(tryit=True, body=['When you are stirred up today', '*Stop stirring for ten breaths*'], closing='Let the lake settle')],
     caption="""The still lake

On choppy water the Moon breaks into pieces. On still water it shows whole. Nothing was added to the lake. The waves stopped.

You can't flatten water by hitting it. That makes more waves. You just stop stirring. Clarity is already there, under the waves.

Patanjali says that when the mind's waves settle, the seer rests in itself (Yoga Sutra 1.3). In Jyotish the Moon is the mind (Brihat Parashara Hora Shastra, chapter 3), and the Moon moves the tides.

Try it today. When you are stirred up, stop stirring for ten breaths. Let the lake settle.""",
     x_text="""The still lake

On choppy water the Moon breaks into pieces. On still water it shows whole

Then the seer rests in itself (Yoga Sutra 1.3)""",
     x_slides=[1, 2, 3, 6], tags='#mind #yogasutras #moon #jyotish #sutram')

post(id='phil-moon-full', title='The Moon is\nalways full', sub='Only the lit part changes', visual=moonfull_visual, cover_at=2.4,
     slides=[S(at=2.4, title='From here\nit waxes', closing='Crescent, half, full'),
             S(at=6.0, title='And wanes', closing='But the Moon never shrank'),
             S(title='Your moods\nwax and wane', body=['Happy, low, restless, calm', '*You were whole the whole time*']),
             S(title='Watch the phase,\nknow the whole', closing='Both are true'),
             S(jyotish=True, title='The Moon\nis the mind', closing='Its phases are moods', orbs=[MOONL]),
             S(quote='Pūrṇam adaḥ pūrṇam idam', source='Isha Upanishad, opening verse', label='Isha Upanishad', closing='That is whole. This is whole'),
             S(tryit=True, body=['Tonight, look at the Moon', '*The dark part is still Moon*'], closing='Whole, always')],
     caption="""The Moon is always full

From here the Moon waxes and wanes: crescent, half, full, and back. The Moon itself never shrank. Only the lit part we see changed.

Your moods wax and wane too. Happy, low, restless, calm. You were whole the whole time.

In Jyotish the Moon is the mind (Brihat Parashara Hora Shastra, chapter 3). Its phases are moods. Nothing is damaged.

The Isha Upanishad opens with it. That is whole, this is whole (purnam adah purnam idam).

Try it tonight. Look at the Moon. The dark part is still Moon.""",
     x_text="""The Moon is always full. Only the lit part changes

Your moods wax and wane. You were whole the whole time

That is whole. This is whole (Isha Upanishad)""",
     x_slides=[1, 2, 3, 5], tags='#moon #mind #upanishads #jyotish #sutram')

post(id='phil-rope', title='Rope or snake?', sub='Fear lives in the dark', visual=rope_visual, cover_at=1.0,
     slides=[S(at=1.0, title='At dusk,\na snake', closing='Your heart jumps'),
             S(at=6.0, title='A lamp:\nit was a rope', closing='Nothing moved. You saw'),
             S(title='Most fear\nis like this', body=['It is just unlit', '*Bring a lamp*']),
             S(title='Seeing clearly\nis the cure', closing='Bring the lamp, and look'),
             S(jyotish=True, title="Rahu is drawn\nas a serpent's head", closing='Shadows look bigger than they are', orbs=[{'kind': 'rahu', 'r': 50}]),
             S(quote='Rajju-sarpa', source='Gaudapada, Mandukya Karika 2.17', label='Mandukya Karika', closing='A rope mistaken for a snake'),
             S(tryit=True, body=['Pick one fear today', '*Look at it in good light*'], closing='Rope or snake?')],
     caption="""Rope or snake?

At dusk you see a snake on the path, and your heart jumps. Someone brings a lamp. It was a rope. Nothing moved. You saw.

Most fear is like this. It is just unlit. Seeing clearly is the cure. Bring the lamp.

The old teachers used this picture: a rope, not clearly seen in the dark, is taken for a snake (Gaudapada, Mandukya Karika 2.17).

In Jyotish, Rahu is drawn as a serpent's head, a shadow graha. Shadows look bigger than they are.

Try it today. Pick one fear and look at it in good light. Rope or snake?""",
     x_text="""Rope or snake?

At dusk, a snake. A lamp: it was a rope. Nothing moved. You saw

Most fear is like this. It is just unlit""",
     x_slides=[1, 2, 3, 4], tags='#fear #vedanta #rahu #jyotish #sutram')

post(id='phil-sky', title='Clouds and\nthe sky', sub='Thoughts pass. The sky stays', visual=sky_visual, cover_at=2.0,
     slides=[S(at=2.0, title='Clouds pass', closing='Dark ones, light ones'),
             S(at=6.0, title='The sky\nwas never touched', closing='Not one mark'),
             S(title='Thoughts are\nthe clouds', body=['Some dark, some light', '*You are the sky they move in*']),
             S(title="Don't fight\nthe clouds", closing='Be the sky'),
             S(jyotish=True, title='Jupiter rules space', closing='The teacher is wide like the sky', orbs=[{'kind': 'jupiter', 'r': 52}]),
             S(quote='Yathākāśa-sthito nityam', source='Bhagavad Gita 9.6', label='Bhagavad Gita', closing='As the wind rests in space'),
             S(tryit=True, body=['When a dark thought comes', '*Say: a cloud*'], closing='Then look at the sky')],
     caption="""Clouds and the sky

Clouds pass, dark ones and light ones. The sky was never touched. Not one mark.

Thoughts are the clouds. Some dark, some light. You are the sky they move in. Don't fight the clouds. Be the sky.

The Gita says: as the great wind moves everywhere and still rests in space, so all beings rest in me (Bhagavad Gita 9.6). In Jyotish, Jupiter, the teacher, rules space, akasha in Sanskrit (Brihat Parashara Hora Shastra, chapter 3).

Try it today. When a dark thought comes, say: a cloud. Then look at the sky.""",
     x_text="""Clouds and the sky

Thoughts are the clouds. You are the sky they move in

Don't fight the clouds. Be the sky""",
     x_slides=[1, 2, 3, 4], tags='#mind #bhagavadgita #jupiter #jyotish #sutram')

post(id='phil-gap', title='The gap\nbetween thoughts', sub='Wait for your next thought', visual=gap_visual, cover_at=5.0,
     slides=[S(at=2.5, title='Thoughts come', closing='And thoughts go'),
             S(at=5.0, title='Then a gap', closing='Nothing is happening. You are still here'),
             S(title='Who was\nwaiting?', body=['Before the next thought came', '*something was already awake*']),
             S(title='Thoughts move\nin the stillness', closing='Like clouds in the sky'),
             S(jyotish=True, title='The Moon changes.\nThe sky does not', closing='The Moon is the mind', orbs=[MOONL]),
             S(quote='Yogaś citta-vṛtti-nirodhaḥ', source='Yoga Sutra 1.2', label='Yoga Sutras', quotesize=80, closing="Yoga is the stilling of the mind's waves"),
             S(tryit=True, body=['Close your eyes for one minute', '*Watch for the next thought*'], closing='Rest in the gap')],
     caption="""The gap between thoughts

Close your eyes and wait for your next thought. Thoughts come and thoughts go. Then, a gap. Nothing is happening, and you are still here.

Who was waiting? Before the next thought came, something was already awake.

Patanjali defines yoga in four words: the stilling of the mind's waves (Yoga Sutra 1.2). In Jyotish the Moon is the mind (Brihat Parashara Hora Shastra, chapter 3). The Moon changes. The sky does not.

Try it today. Close your eyes for one minute and watch for the next thought. Rest in the gap.""",
     x_text="""The gap between thoughts

Wait for your next thought. Then a gap. Who was waiting?

Yoga is the stilling of the mind's waves (Yoga Sutra 1.2)""",
     x_slides=[1, 2, 3, 4], tags='#meditation #yogasutras #mind #jyotish #sutram')

post(id='phil-pot', title='Space in a pot', sub='Break the pot. Where did the space go?', visual=pot_visual, cover_at=1.0,
     slides=[S(at=1.0, title='Space inside\nthe pot', closing='Seems to be its own'),
             S(at=6.0, title='The pot breaks', closing='The space was never inside'),
             S(title='Your body\nis the pot', body=['Awareness seems to be inside', '*It was never inside*']),
             S(title='One space,\nmany pots', closing='One awareness, many people'),
             S(jyotish=True, title='One sky,\ntwelve houses', closing='A chart draws rooms in one sky', orbs=[SUN]),
             S(quote='Ghaṭākāśa', source='Gaudapada, Mandukya Karika 3.3', label='Mandukya Karika', closing='The self is like space in pots'),
             S(tryit=True, body=['Feel the space in the room', '*Feel the space where you are*'], closing='Same space')],
     caption="""Space in a pot

The space inside a pot seems to be its own. Break the pot. The space was never inside. It was the same space all along.

Your body is the pot. Awareness seems to be inside it. It was never inside. One space, many pots. One awareness, many people.

Gaudapada uses this picture. The self is like space, appearing as many, like the space in pots (Mandukya Karika 3.3).

In Jyotish a chart draws twelve houses in one sky. The rooms are many. The sky is one.

Try it today. Feel the space in the room. Feel the space where you are. Same space.""",
     x_text="""Space in a pot

Break the pot. The space was never inside

One space, many pots. One awareness, many people""",
     x_slides=[1, 2, 3, 4], tags='#vedanta #advaita #awareness #jyotish #sutram')

post(id='phil-one-light', title='One light,\nmany forms', sub='Everything you see shines with one light', visual=onelight_visual, cover_at=4.0,
     slides=[S(at=2.0, title='Moon, Mars,\nJupiter, Venus', closing='Each one shines'),
             S(at=5.0, title='None has its\nown light', closing="Each shines with the Sun's"),
             S(title='Your thoughts,\nfeelings, memories', body=['Each one is lit', '*by the same awareness*']),
             S(title='Find the light', closing='It was there in each one'),
             S(jyotish=True, title='The Sun is\nthe soul', closing='The other grahas shine by its light', orbs=[SUN]),
             S(quote='Tasya bhāsā sarvam idaṃ vibhāti', source='Katha Upanishad 2.2.15', label='Katha Upanishad', quotesize=76, closing='By its light all this shines'),
             S(tryit=True, body=['Look at anything near you', '*Notice what lets you see it*'], closing='That is the light')],
     caption="""One light, many forms

The Moon, Mars, Jupiter and Venus each shine in the night sky. None has its own light. Each shines with the Sun's.

Your thoughts, feelings and memories are the same. Each one is lit by the same awareness. Find the light. It was there in each one.

In Jyotish the Sun is the soul (Brihat Parashara Hora Shastra, chapter 3), and the other grahas you can see shine by its light.

The Katha Upanishad says that by its light, all this shines (2.2.15).

Try it today. Look at anything near you, and notice what lets you see it. That is the light.""",
     x_text="""One light, many forms

The Moon, Mars, Jupiter, Venus: none has its own light. Each shines with the Sun's

By its light all this shines (Katha Upanishad 2.2.15)""",
     x_slides=[1, 2, 3, 6], tags='#awareness #upanishads #sun #jyotish #sutram')

post(id='phil-sleep', title='Who knows\nyou slept well?', sub='Waking, dreaming, deep sleep', visual=sleep_visual, cover_at=6.5,
     slides=[S(at=1.2, title='Awake, you\nsee the world', closing='Dreaming, you see a dream world'),
             S(at=6.5, title='In deep sleep\nthere is nothing', closing='Yet you wake up and say: I slept well'),
             S(title='Who was there\nto know it?', body=['Not the body. Not the mind', '*Something stayed awake*']),
             S(title='It is here now', closing='Under waking, dreaming and sleep'),
             S(jyotish=True, title='The Sun is\nthe soul', closing='Its light never sleeps', orbs=[SUN]),
             S(quote='Turīya', source='Mandukya Upanishad 7', label='Mandukya Upanishad', closing='The fourth: awake under all three'),
             S(tryit=True, body=['Tonight, as you fall asleep', '*Notice the last moment you notice*'], closing='Who was noticing?')],
     caption="""Who knows you slept well?

Awake, you see the world. Dreaming, you see a dream world. In deep sleep there is nothing at all. Yet you wake up and say: I slept well.

Who was there to know it? Not the body. Not the mind. Something stayed awake. It is here now, under waking, dreaming and sleep.

The Mandukya Upanishad calls it turiya, the fourth: the awareness under all three states (Mandukya Upanishad 7). In Jyotish the Sun is the soul (Brihat Parashara Hora Shastra, chapter 3). Its light never sleeps.

Try it tonight. As you fall asleep, notice the last moment you notice. Who was noticing?""",
     x_text="""Who knows you slept well?

In deep sleep there is nothing. Yet you wake up and say: I slept well

Who was there to know it?""",
     x_slides=[1, 2, 3, 4], tags='#sleep #upanishads #awareness #jyotish #sutram')

post(id='phil-neti', title='Not this,\nnot this', sub='What is left when you take everything away?', visual=neti_visual, cover_at=6.0,
     slides=[S(at=0.5, title='Body, name,\nthoughts, feelings', closing='You can watch each one'),
             S(at=6.0, title='Take each away', closing='Something is left. The watching'),
             S(title='If you can\nsee it', body=['it is not you', '*You are the seeing*']),
             S(title="Even the thought\n'I am this'", closing='is something you notice'),
             S(jyotish=True, title='Your chart shows\nbody and mind', closing='Not the one who knows them', orbs=[SUN]),
             S(quote='Neti neti', source='Brihadaranyaka Upanishad 2.3.6', label='The Upanishads', closing='Not this, not this'),
             S(tryit=True, body=['Name three things you are not', '*Notice who is naming*'], closing='Rest there')],
     caption="""Not this, not this

Body, name, thoughts, feelings. You can watch each one. Take each away, and something is left: the watching.

If you can see it, it is not you. You are the seeing. Even the thought "I am this" is something you notice.

The Brihadaranyaka Upanishad describes the self in two words: neti neti, not this, not this (2.3.6).

In Jyotish your chart shows a body and a mind and their timing. It does not show the one who knows them.

Try it today. Name three things you are not. Notice who is naming. Rest there.""",
     x_text="""Not this, not this (Brihadaranyaka Upanishad 2.3.6)

Body, name, thoughts, feelings. If you can see it, it is not you

You are the seeing""",
     x_slides=[1, 2, 3, 4], tags='#netineti #upanishads #advaita #jyotish #sutram')

post(id='phil-mirror', title='The dusty mirror', sub='The face was never dusty', visual=mirror_visual, cover_at=6.0,
     slides=[S(at=1.0, title='Dust on\nthe mirror', closing='The reflection looks dull'),
             S(at=6.0, title='Wipe it', closing='Nothing was added to the face'),
             S(title='Desire is dust', body=['Wanting clouds the seeing', '*The one who sees stays clean*']),
             S(title='Clean the mirror', closing="Don't chase the face"),
             S(jyotish=True, title='Venus is\ndesire', closing='Lovely, and it can cover the light', orbs=[{'kind': 'venus', 'r': 50}]),
             S(quote='Yathādarśo malena ca', source='Bhagavad Gita 3.38', label='Bhagavad Gita', closing='As a mirror is covered by dust'),
             S(tryit=True, body=['Notice one wanting today', '*Watch it like dust*'], closing='It settles if you let it')],
     caption="""The dusty mirror

Dust on a mirror makes the reflection look dull. Wipe it, and nothing is added to the face. The face was never dusty.

The Gita says knowledge is covered by desire as fire is covered by smoke and a mirror by dust (Bhagavad Gita 3.38). Wanting clouds the seeing. The one who sees stays clean. So clean the mirror. Don't chase the face.

In Jyotish, Venus is desire and pleasure. Lovely, and it can cover the light.

Try it today. Notice one wanting. Watch it like dust. It settles if you let it.""",
     x_text="""The dusty mirror

Wipe the mirror and nothing is added to the face. The face was never dusty

As a mirror is covered by dust (Bhagavad Gita 3.38)""",
     x_slides=[1, 2, 3, 6], tags='#desire #bhagavadgita #venus #jyotish #sutram')

post(id='phil-ocean', title='Rivers into\nthe ocean', sub="The ocean doesn't rise or fall", visual=ocean_visual, cover_at=3.0,
     slides=[S(at=2.0, title='Rivers pour in', closing="Desires, news, other people's moods"),
             S(at=6.0, title='The ocean\nstays itself', closing='Full, and still'),
             S(title='Be the ocean', body=['Let things flow in', "*You don't have to rise*"]),
             S(title="A full ocean\ndoesn't chase rivers", closing='Peace is that'),
             S(jyotish=True, title='The Moon pulls\nthe tides', closing='The depths stay still', orbs=[MOONL]),
             S(quote='Samudram āpaḥ praviśanti', source='Bhagavad Gita 2.70', label='Bhagavad Gita', closing='Waters enter the ocean; it stays still'),
             S(tryit=True, body=['When news pours in today', '*Let it flow in*'], closing='Stay the ocean')],
     caption="""Rivers into the ocean

Rivers pour into the ocean all day long. Desires, news, other people's moods. The ocean stays itself, full and still.

Be the ocean. Let things flow in. You don't have to rise. A full ocean doesn't chase rivers. Peace is that.

The Gita: as waters enter the ocean, which is filled yet stays still, so the one whom desires enter finds peace (Bhagavad Gita 2.70).

In Jyotish the Moon is the mind (Brihat Parashara Hora Shastra, chapter 3). The Moon pulls the tides. The depths stay still.

Try it today. When news pours in, let it flow in. Stay the ocean.""",
     x_text="""Rivers into the ocean

Desires, news, other people's moods pour in. The ocean stays itself

Be the ocean (Bhagavad Gita 2.70)""",
     x_slides=[1, 2, 3, 4], tags='#peace #bhagavadgita #moon #jyotish #sutram')

post(id='phil-bell', title='Listen to\nthe silence', sub='Ring a bell. Wait', visual=bell_visual, cover_at=1.5,
     slides=[S(at=1.5, title='The sound\nspreads', closing='Then fades'),
             S(at=6.0, title='What is left?', closing='Silence. And the one who hears it'),
             S(title='The silence was\nthere first', body=['Sound appears in it', '*and goes back into it*']),
             S(title='Your mind\nworks the same', closing='Words rise from silence'),
             S(jyotish=True, title='Mercury is\nspeech', closing='Silence is the space it speaks in', orbs=[{'kind': 'mercury', 'r': 46}]),
             S(quote='Amātraś caturthaḥ', source='Mandukya Upanishad 12', label='Mandukya Upanishad', closing='The fourth part of Om is silence'),
             S(tryit=True, body=['Ring a bell, or tap a glass', '*Listen until it is gone*'], closing='Keep listening')],
     caption="""Listen to the silence

Ring a bell. The sound spreads, then fades. What is left? Silence, and the one who hears it.

The silence was there first. Sound appears in it and goes back into it. Your mind works the same way. Words rise from silence.

The Mandukya Upanishad says the fourth part of Om has no sound at all: the silence after it (Mandukya Upanishad 12). In Jyotish, Mercury is speech. Silence is the space it speaks in.

Try it today. Ring a bell, or tap a glass. Listen until it is gone. Keep listening.""",
     x_text="""Listen to the silence

Ring a bell. The sound fades. What is left? Silence, and the one who hears it

The fourth part of Om is silence (Mandukya Upanishad 12)""",
     x_slides=[1, 2, 3, 4], tags='#silence #om #upanishads #jyotish #sutram')

post(id='phil-lamp', title='A lamp where\nno wind blows', sub='That is a still mind', visual=lamp_visual, cover_at=5.5,
     slides=[S(at=1.5, title='Wind makes\nthe flame dance', closing='Worry, hurry, noise'),
             S(at=5.5, title='No wind,\nsteady flame', closing='It lights the whole room'),
             S(title="You can't hold\na flame still", body=['You can only', '*shut the window*']),
             S(title='Fewer gusts,\nmore light', closing='Less news, less rush'),
             S(jyotish=True, title='The Moon flickers.\nThe Sun burns steady', closing='Mind and soul', orbs=[MOONR, SUN]),
             S(quote='Yathā dīpo nivāta-sthaḥ', source='Bhagavad Gita 6.19', label='Bhagavad Gita', closing='As a lamp in a windless place'),
             S(tryit=True, body=['Close one window today', '*Phone, news, or noise*'], closing='Watch the flame steady')],
     caption="""A lamp where no wind blows

Worry, hurry and noise make a flame dance like wind. When the wind stops, the flame stands steady and lights the whole room.

You can't hold a flame still with your hands. You can only shut the window. Fewer gusts, more light.

The Gita's picture of a still mind: like a lamp in a windless place, it does not flicker (Bhagavad Gita 6.19). In Jyotish the Moon is the mind and the Sun is the soul (Brihat Parashara Hora Shastra, chapter 3). The Moon flickers. The Sun burns steady.

Try it today. Close one window, whether phone, news or noise. Watch the flame steady.""",
     x_text="""A lamp where no wind blows

You can't hold a flame still. You can only shut the window

Like a lamp in a windless place (Bhagavad Gita 6.19)""",
     x_slides=[1, 2, 3, 4], tags='#stillness #bhagavadgita #mind #jyotish #sutram')

# ---------- build ----------
def build(p):
    vis = p['visual']()
    sl = []
    sl.append({'type': 'cover', 'kicker': 'Sutram', 'stars': True, 'swipe': True, 'tag': 'Philosophy', 'title': p['title'], 'titleclass': 'h1',
               'titlesize': p.get('titlesize', 116), 'subtitle': p['sub'], 'subsize': 56, 'anim': dict(vis, at=p.get('cover_at', 0), mt=34)})
    for s in p['slides']:
        if 'at' in s:
            sl.append({'type': 'text', 'anim': dict(vis, at=s['at'], mt=0, mb=16, k=vis.get('k', 1.12) * .96), 'title': s['title'], 'titleclass': 'h2',
                       'closing': s.get('closing'), 'closingsize': 56})
        elif s.get('jyotish'):
            sl.append({'type': 'text', 'label': 'In Jyotish', 'labelsize': 34, 'orbs': s.get('orbs'), 'orbgap': 70, 'title': s['title'], 'titleclass': 'h2',
                       'titlesize': 88, 'closing': s.get('closing'), 'closingsize': 54})
        elif s.get('quote'):
            sl.append({'type': 'quote', 'label': s.get('label', 'The Upanishads'), 'labelsize': 34, 'quote': s['quote'], 'quotesize': s.get('quotesize', 92),
                       'source': s['source'], 'closing': s.get('closing'), 'closingsize': 56})
        elif s.get('tryit'):
            sl.append({'type': 'text', 'title': 'Try it today', 'titleclass': 'h1', 'titlesize': 120, 'body': s['body'], 'bodysize': 42, 'bodygap': 10,
                       'closing': s.get('closing'), 'closingsize': 62})
        else:
            x = {'type': 'text', 'title': s['title'], 'titleclass': 'h1', 'titlesize': s.get('titlesize', 112)}
            if s.get('body'): x.update(body=s['body'], bodysize=48, bodygap=10)
            if s.get('closing'): x.update(closing=s['closing'], closingsize=62)
            if s.get('orbs'): x['orbs'] = s['orbs']
            sl.append(x)
    spec = {'id': p['id'], 'kicker': 'Philosophy', 'decor_theme': 'thread', 'slides': sl}
    json.dump(spec, open(os.path.join(REPO, 'specs', p['id'] + '.json'), 'w'), ensure_ascii=False, indent=1)
    cap = p['caption'].strip() + '\n\nAsk your chart a question at asksutram.com\nWeekly newsletter: sutram.ca/newsletter\n\n' + p['tags'] + '\n'
    open(os.path.join(REPO, 'captions', p['id'] + '.txt'), 'w').write(cap)
    open(os.path.join(REPO, 'x-drafts', p['id'] + '-x.txt'), 'w').write(p['x_text'].strip() + '\n\nasksutram.com\nsutram.ca/newsletter\n')

if __name__ == '__main__':
    want = set(sys.argv[1:])
    for p in POSTS:
        if not want or p['id'] in want: build(p); print('wrote', p['id'])
