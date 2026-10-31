#!/usr/bin/env python3
"""Every meeting of Jupiter and Ketu (within 3 degrees) in Leo, 1600 to now.
Dates come from the engine scan (Swiss Ephemeris, Lahiri, mean node), run 31 Oct 2026:
1635, 1672, 1766, 1802, 1896, 1932, 2026.
v2 (31 Oct, Sumant: the first version's visual and text were too small): a vertical timeline
that fills the slide, big years and big labels. Writes svg/jk-leo-timeline-v2.svg (912 wide).
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
CREAM = '#F2E6CC'; AMBER = '#E09460'; GOLD = '#D9A57A'; BG = '#0B0806'
W, H = 912, 660
LX = 150                       # the line
ROWS = [('1635', 'a preacher banished', False),
        ('1672', 'the disaster year', False),
        ('1766 · 1802', 'no clear match', False),
        ('1896', 'a 38-minute war', False),
        ('1932', 'the fast and the famine', False),
        ('2026', 'now', True)]
TOP, STEP = 62, 107


def t(x, y, s, size, col, op=1, anchor='start', italic=False, fam='EB Garamond', weight=None):
    st = ' font-style="italic"' if italic else ''
    wt = f' font-weight="{weight}"' if weight else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{fam}"{st}{wt} font-size="{size}" fill="{col}" fill-opacity="{op}">{s}</text>'


o = [f'<defs><filter id="tg" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="7"/></filter></defs>']
o.append(f'<line x1="{LX}" y1="{TOP - 30}" x2="{LX}" y2="{TOP + STEP * (len(ROWS) - 1) + 30}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="2.4"/>')
for k, (yr, tag, now) in enumerate(ROWS):
    y = TOP + STEP * k
    col = AMBER if now else CREAM
    quiet = tag == 'no clear match'
    if now:
        o.append(f'<circle cx="{LX}" cy="{y}" r="20" fill="{AMBER}" opacity=".45" filter="url(#tg)"/>')
    o.append(f'<circle cx="{LX}" cy="{y}" r="{16 if now else 13}" fill="{BG}" stroke="{col}" stroke-width="3.4" stroke-opacity="{.55 if quiet else 1}"/>')
    if now: o.append(f'<circle cx="{LX}" cy="{y}" r="7" fill="{AMBER}"/>')
    o.append(t(LX + 52, y + 22, yr, 66, col, .55 if quiet else 1, fam='Cormorant Garamond', weight=500))
    tx = LX + 52 + (330 if quiet else 160)
    o.append(t(tx, y + 14, tag, 38, AMBER if now else GOLD, .6 if quiet else .97, italic=True))
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(o) + '</svg>'
open(os.path.join(REPO, 'svg', 'jk-leo-timeline-v2.svg'), 'w').write(svg)
print('svg/jk-leo-timeline-v2.svg')
