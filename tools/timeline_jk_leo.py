#!/usr/bin/env python3
"""Every meeting of Jupiter and Ketu (within 3 degrees) in Leo, 1600 to now, on one line.
Dates come from the engine scan (Swiss Ephemeris, Lahiri, mean node), run 31 Oct 2026:
1635, 1672, 1766, 1802, 1896, 1932, 2026. Writes svg/jk-leo-timeline.svg at slide size (912 wide).
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
CREAM = '#F2E6CC'; AMBER = '#E09460'; GOLD = '#D9A57A'; BG = '#0B0806'
W, H = 912, 330
X0, X1, Y = 40, 872, 170
Y0, Y1 = 1600, 2030
X = lambda yr: X0 + (yr - Y0) / (Y1 - Y0) * (X1 - X0)
YEARS = [1635, 1672, 1766, 1802, 1896, 1932, 2026]
TAG = {1635: 'a preacher banished', 1672: 'the disaster year', 1896: 'a 38-minute war', 1932: 'the fast and the famine', 2026: 'now'}


def t(x, y, s, size, col, op=1, anchor='middle', italic=False, fam='EB Garamond', ls=0, weight=None):
    st = ' font-style="italic"' if italic else ''
    wt = f' font-weight="{weight}"' if weight else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{fam}"{st}{wt} font-size="{size}" letter-spacing="{ls}" fill="{col}" fill-opacity="{op}">{s}</text>'


o = [f'<line x1="{X0}" y1="{Y}" x2="{X1}" y2="{Y}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="2"/>']
for c in range(1600, 2001, 100):
    o.append(f'<line x1="{X(c):.1f}" y1="{Y - 8}" x2="{X(c):.1f}" y2="{Y + 8}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.5"/>')
for k, yr in enumerate(YEARS):
    x = X(yr); up = (k % 2 == 0)
    now = yr == 2026
    col = AMBER if now else CREAM
    o.append(f'<circle cx="{x:.1f}" cy="{Y}" r="{13 if now else 10}" fill="{BG}" stroke="{col}" stroke-width="3"/>')
    if now: o.append(f'<circle cx="{x:.1f}" cy="{Y}" r="5" fill="{AMBER}"/>')
    yy = Y - 34 if up else Y + 58
    o.append(t(x, yy, str(yr), 40, col, 1, fam='Cormorant Garamond', weight=500))
    if yr in TAG:
        o.append(t(x, Y - 76 if up else Y + 96, TAG[yr], 24, AMBER if now else GOLD, .95, italic=True))
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(o) + '</svg>'
open(os.path.join(REPO, 'svg', 'jk-leo-timeline.svg'), 'w').write(svg)
print('svg/jk-leo-timeline.svg')
