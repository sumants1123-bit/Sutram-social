#!/usr/bin/env python3
"""The meeting at the doorway: Jupiter (the teacher), Ketu (the monk) and Mars (the soldier)
crossing from Cancer into Leo, Oct to Dec 2026. A simple date-by-position chart from engine data
(Swiss Ephemeris, sidereal Lahiri, mean node), drawn at the size it shows on the slide (912 wide)
so every word stays readable on a phone.
Writes svg/knot-2026-v2.svg. Usage: .venv/bin/python tools/knot.py
v2 (30 Oct, Sumant): simpler for everyday readers, bigger words. No degree axis, no Gandanta band;
just the two signs, the doorway, three named lines, three crossing dates and the week they meet.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transit_story import Sky, sdiff, root, jd_of, local
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
CREAM = '#F2E6CC'; AMBER = '#E09460'; GOLD = '#D9A57A'; BG = '#0B0806'; SHADOW = '#BDB2A6'

sky = Sky('mean')
J0, J1 = jd_of('2026-10-28', 0), jd_of('2026-12-13', 0)
LO, HI = 110.0, 127.0                 # Cancer 20 to Leo 7
W, H = 912, 662
X0, X1, Y0, Y1 = 172, 728, 120, 600   # plot box; names sit to the right of X1
X = lambda jd: X0 + (jd - J0) / (J1 - J0) * (X1 - X0)
Y = lambda lon: Y1 - (lon - LO) / (HI - LO) * (Y1 - Y0)
YD = Y(120.0)                          # the doorway between Cancer and Leo


def path(name):
    pts, n = [], 460
    for i in range(n + 1):
        jd = J0 + (J1 - J0) * i / n
        l = sky.lon(jd, name)
        if LO <= l <= HI: pts.append(f"{X(jd):.1f},{Y(l):.1f}")
        elif pts: break
    return ' '.join(pts)


def cross(name, lo, hi, target=120.0):
    return root(lambda x: sdiff(sky.lon(x, name), target), jd_of(lo, 0), jd_of(hi, 0))


def t(x, y, s, size=26, col=GOLD, op=.9, anchor='middle', ls=0, italic=False, weight=None, fam='EB Garamond'):
    st = ' font-style="italic"' if italic else ''
    wt = f' font-weight="{weight}"' if weight else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{fam}"{st}{wt} font-size="{size}" letter-spacing="{ls}" fill="{col}" fill-opacity="{op}">{s}</text>'


o = [f'<defs><filter id="kg" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><feGaussianBlur stdDeviation="5"/></filter></defs>']

# the week they meet: all three within 1 degree
k0 = root(lambda x: abs(sdiff(sky.lon(x, 'Mars'), sky.lon(x, 'Jupiter'))) - 1, jd_of('2026-11-12', 0), jd_of('2026-11-14', 0))
k1 = root(lambda x: abs(sdiff(sky.lon(x, 'Mars'), sky.lon(x, 'Ketu'))) - 1, jd_of('2026-11-15', 0), jd_of('2026-11-18', 0))
o.append(f'<rect x="{X(k0):.1f}" y="{Y0 - 6}" width="{X(k1) - X(k0):.1f}" height="{Y1 - Y0 + 6}" rx="4" fill="{AMBER}" fill-opacity=".16"/>')
kx = (X(k0) + X(k1)) / 2
o.append(t(kx, Y0 - 58, 'all three together', 32, CREAM, .95, italic=True))
o.append(t(kx, Y0 - 20, '13–16 NOV', 32, AMBER, 1, ls=3))

# the two signs and the doorway between them
o.append(f'<line x1="{X0}" y1="{YD:.1f}" x2="{X1}" y2="{YD:.1f}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="2" stroke-dasharray="8 8"/>')
o.append(t(X0 - 22, Y(124.2) + 10, 'LEO', 30, GOLD, .9, 'end', 4))
o.append(t(X0 - 22, Y(114.6) + 10, 'CANCER', 30, GOLD, .9, 'end', 3))
o.append(f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{GOLD}" stroke-opacity=".3"/>')

# months along the bottom
d1, d2 = X(jd_of('2026-11-01', 0)), X(jd_of('2026-12-01', 0))
for x in (d1, d2):
    o.append(f'<line x1="{x:.1f}" y1="{Y1}" x2="{x:.1f}" y2="{Y1 + 12}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.5"/>')
o.append(t((d1 + d2) / 2, Y1 + 46, 'NOVEMBER', 26, GOLD, .85, ls=4))
o.append(t((d2 + X1) / 2, Y1 + 46, 'DECEMBER', 26, GOLD, .85, ls=4))

# the three grahas
for name, col, w, dash in (('Ketu', SHADOW, 3.6, '11 9'), ('Jupiter', CREAM, 4.4, ''), ('Mars', AMBER, 4.4, '')):
    p = path(name)
    if not dash: o.append(f'<polyline points="{p}" fill="none" stroke="{col}" stroke-opacity=".42" stroke-width="{w + 6}" filter="url(#kg)"/>')
    da = f' stroke-dasharray="{dash}"' if dash else ''
    o.append(f'<polyline points="{p}" fill="none" stroke="{col}" stroke-opacity=".97" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{da}/>')

# who walks through the doorway, and when
for name, lo, hi, lab, col in (('Jupiter', '2026-10-30', '2026-11-01', '31 OCT', CREAM),
                               ('Mars', '2026-11-11', '2026-11-13', '12 NOV', AMBER),
                               ('Ketu', '2026-12-03', '2026-12-07', '5 DEC', SHADOW)):
    tc = cross(name, lo, hi)
    o.append(f'<circle cx="{X(tc):.1f}" cy="{YD:.1f}" r="8" fill="{BG}" stroke="{col}" stroke-width="3"/>')
    # Mars climbs steeply through its dot, so its date sits to the right of the line
    if name == 'Mars': o.append(t(X(tc) + 16, YD + 44, lab, 28, col, .98, 'start', 2))
    else: o.append(t(X(tc), YD + 44, lab, 28, col, .98, ls=2))
o.append(t(X0 - 22, YD + 10, 'the doorway', 28, GOLD, .95, 'end', 0, italic=True))

# names at the ends of the lines
def name(x, y, nm, role, col):
    o.append(t(x, y, nm, 42, col, 1, 'start', 0, fam='Cormorant Garamond', weight=500))
    o.append(t(x, y + 32, role, 28, col, .9, 'start', 0, italic=True))

name(X1 + 14, Y(sky.lon(J1, 'Jupiter')) + 4, 'Jupiter', 'the teacher', CREAM)
name(X1 + 14, Y(sky.lon(J1, 'Ketu')) + 26, 'Ketu', 'the monk', SHADOW)
tm_top = root(lambda x: sky.lon(x, 'Mars') - HI, jd_of('2026-11-18', 0), jd_of('2026-12-05', 0))
name(X(tm_top) + 18, Y0 + 34, 'Mars', 'the soldier', AMBER)

svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(o) + '</svg>'
os.makedirs(os.path.join(REPO, 'svg'), exist_ok=True)
open(os.path.join(REPO, 'svg', 'knot-2026-v2.svg'), 'w').write(svg)
print('svg/knot-2026-v2.svg', f'together {local(k0):%d %b %H:%M} to {local(k1):%d %b %H:%M}',
      f'Ketu back into Cancer {local(cross("Ketu", "2026-12-03", "2026-12-07")):%d %b %H:%M}')
