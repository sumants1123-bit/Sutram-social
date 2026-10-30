#!/usr/bin/env python3
"""The knot at the doorway: Mars, Jupiter and Ketu crossing the Cancer-Leo Gandanta, Oct to Dec 2026.
A date-by-degree chart drawn from engine data (Swiss Ephemeris, sidereal Lahiri, mean node).
Writes svg/knot-2026.svg. Usage: .venv/bin/python tools/knot.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transit_story import Sky, sdiff, root, jd_of, local
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
CREAM = '#F2E6CC'; AMBER = '#E09460'; GOLD = '#D9A57A'; BG = '#0B0806'; SHADOW = '#B9AEA2'

sky = Sky('mean')
J0, J1 = jd_of('2026-10-25', 0), jd_of('2026-12-20', 0)
LO, HI = 110.0, 128.0                  # Cancer 20 to Leo 8
W, H = 1030, 720
X0, X1, Y0, Y1 = 138, 890, 104, 600      # plot box
X = lambda jd: X0 + (jd - J0) / (J1 - J0) * (X1 - X0)
Y = lambda lon: Y1 - (lon - LO) / (HI - LO) * (Y1 - Y0)


def path(name):
    pts = []
    n = 400
    for i in range(n + 1):
        jd = J0 + (J1 - J0) * i / n
        l = sky.lon(jd, name)
        if LO <= l <= HI: pts.append(f"{X(jd):.1f},{Y(l):.1f}")
        elif pts: break
    return ' '.join(pts)


def meet(a, b, lo, hi):
    t = root(lambda x: sdiff(sky.lon(x, a), sky.lon(x, b)), jd_of(lo, 0), jd_of(hi, 0))
    return t, sky.lon(t, a)


def cross(name, lo, hi, target=120.0):
    t = root(lambda x: sdiff(sky.lon(x, name), target), jd_of(lo, 0), jd_of(hi, 0))
    return t


def t(x, y, s, size=20, col=GOLD, op=.85, anchor='middle', ls=2, italic=False, weight=None, fam='EB Garamond'):
    st = ' font-style="italic"' if italic else ''
    wt = f' font-weight="{weight}"' if weight else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{fam}"{st}{wt} font-size="{size}" letter-spacing="{ls}" fill="{col}" fill-opacity="{op}">{s}</text>'


o = []
o.append(f'<defs><filter id="kg" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><feGaussianBlur stdDeviation="5"/></filter></defs>')
# Gandanta band: Ashlesha pada 4 and Magha pada 1 (Cancer 26 40 to Leo 3 20)
o.append(f'<rect x="{X0}" y="{Y(123.333):.1f}" width="{X1 - X0}" height="{Y(116.667) - Y(123.333):.1f}" fill="{AMBER}" fill-opacity=".06"/>')
o.append(f'<line x1="{X0}" y1="{Y(120):.1f}" x2="{X1}" y2="{Y(120):.1f}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.4" stroke-dasharray="6 7"/>')
o.append(t(X(jd_of('2026-11-25', 0)), Y(120) + 30, 'CANCER  |  LEO', 20, GOLD, .8, 'middle', 3))
o.append(t(X1 - 6, Y(116.667) - 12, 'the doorway: Gandanta', 25, AMBER, .95, 'end', 1, italic=True))
# y ticks
for lon, lab in ((110, 'CAN 20°'), (115, 'CAN 25°'), (120, 'LEO 0°'), (125, 'LEO 5°')):
    o.append(f'<line x1="{X0 - 8}" y1="{Y(lon):.1f}" x2="{X0}" y2="{Y(lon):.1f}" stroke="{GOLD}" stroke-opacity=".45"/>')
    o.append(t(X0 - 14, Y(lon) + 7, lab, 20, GOLD, .8, 'end', 2))
o.append(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="{GOLD}" stroke-opacity=".25"/>')
o.append(f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{GOLD}" stroke-opacity=".25"/>')
# x ticks
for d, lab in (('2026-11-01', '1 NOV'), ('2026-11-15', '15 NOV'), ('2026-12-01', '1 DEC'), ('2026-12-15', '15 DEC')):
    x = X(jd_of(d, 0))
    o.append(f'<line x1="{x:.1f}" y1="{Y1}" x2="{x:.1f}" y2="{Y1 + 8}" stroke="{GOLD}" stroke-opacity=".45"/>')
    o.append(t(x, Y1 + 36, lab, 21, GOLD, .8, 'middle', 3))
# the knot window: all three within 1 degree
k0 = root(lambda x: abs(sdiff(sky.lon(x, 'Mars'), sky.lon(x, 'Jupiter'))) - 1, jd_of('2026-11-12', 0), jd_of('2026-11-14', 0))
k1 = root(lambda x: abs(sdiff(sky.lon(x, 'Mars'), sky.lon(x, 'Ketu'))) - 1, jd_of('2026-11-15', 0), jd_of('2026-11-18', 0))
o.append(f'<rect x="{X(k0):.1f}" y="{Y0 - 6}" width="{X(k1) - X(k0):.1f}" height="{Y1 - Y0 + 6}" fill="{AMBER}" fill-opacity=".13"/>')
o.append(t((X(k0) + X(k1)) / 2, Y0 - 20, '13–16 NOV', 24, AMBER, .98, 'middle', 3))
o.append(t((X(k0) + X(k1)) / 2, Y0 - 52, 'all three within 1°', 25, CREAM, .92, 'middle', 1, italic=True))
# planet lines
for name, col, w, dash in (('Ketu', SHADOW, 2.6, '9 7'), ('Jupiter', CREAM, 3.2, ''), ('Mars', AMBER, 3.2, '')):
    p = path(name)
    if not dash: o.append(f'<polyline points="{p}" fill="none" stroke="{col}" stroke-opacity=".45" stroke-width="{w + 5}" filter="url(#kg)"/>')
    o.append(f'<polyline points="{p}" fill="none" stroke="{col}" stroke-opacity=".95" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{f" stroke-dasharray={chr(34)}{dash}{chr(34)}" if dash else ""}/>')
# crossings of the doorway
for name, lo, hi, lab, dy, col in (('Jupiter', '2026-10-30', '2026-11-01', '31 OCT', 34, CREAM), ('Mars', '2026-11-11', '2026-11-13', '12 NOV', 34, AMBER), ('Ketu', '2026-12-04', '2026-12-06', '5 DEC', -22, SHADOW)):
    tc = cross(name, lo, hi)
    o.append(f'<circle cx="{X(tc):.1f}" cy="{Y(120):.1f}" r="6.5" fill="{BG}" stroke="{col}" stroke-width="2.4"/>')
    o.append(t(X(tc), Y(120) + dy, lab, 19, col, .95, 'middle', 2))
# the three exact meetings
for a, b, lo, hi in (('Jupiter', 'Ketu', '2026-11-10', '2026-11-13'), ('Mars', 'Ketu', '2026-11-13', '2026-11-16'), ('Mars', 'Jupiter', '2026-11-15', '2026-11-17')):
    tm, lm = meet(a, b, lo, hi)
    o.append(f'<circle cx="{X(tm):.1f}" cy="{Y(lm):.1f}" r="5" fill="{CREAM}"/>')
# Jupiter pauses
tj = root(lambda x: sky.spd(x, 'Jupiter'), jd_of('2026-12-10', 0), jd_of('2026-12-15', 0))
o.append(f'<circle cx="{X(tj):.1f}" cy="{Y(sky.lon(tj, "Jupiter")):.1f}" r="6.5" fill="{BG}" stroke="{CREAM}" stroke-width="2.4"/>')
o.append(t(X(tj) - 10, Y(sky.lon(tj, 'Jupiter')) - 20, '12 DEC, PAUSES', 19, CREAM, .9, 'middle', 2))
# line labels
tm_end = J1
o.append(t(X1 + 10, Y(sky.lon(tm_end, 'Jupiter')) + 9, 'Jupiter', 31, CREAM, .97, 'start', 0, fam='Cormorant Garamond', weight=500))
o.append(t(X1 + 10, Y(sky.lon(tm_end, 'Ketu')) + 12, 'Ketu', 31, SHADOW, .97, 'start', 0, fam='Cormorant Garamond', weight=500))
tm_top = root(lambda x: sky.lon(x, 'Mars') - HI, jd_of('2026-11-20', 0), jd_of('2026-12-05', 0))
o.append(t(X(tm_top) + 14, Y0 + 26, 'Mars', 31, AMBER, .97, 'start', 0, fam='Cormorant Garamond', weight=500))
# start-of-chart labels
o.append(t(X0 + 12, Y(sky.lon(J0, 'Mars')) - 14, 'Mars, at its weakest', 22, AMBER, .9, 'start', 1, italic=True))

svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(o) + '</svg>'
os.makedirs(os.path.join(REPO, 'svg'), exist_ok=True)
open(os.path.join(REPO, 'svg', 'knot-2026.svg'), 'w').write(svg)
print('svg/knot-2026.svg', f'knot window {local(k0):%d %b %H:%M} to {local(k1):%d %b %H:%M}', f'Jupiter pauses {local(tj):%d %b %H:%M}')
