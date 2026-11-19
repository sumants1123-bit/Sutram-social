"""Small drawings for the day and night look (tools/look.py): the wheel of the Moon's 27 stars.

The seven natures of the stars follow Brihat Samhita, chapter 98 (verses 6 to 11), as panchangs list them today:
steady (dhruva), sharp (tikshna), fierce (ugra), light (laghu), soft (mridu), soft-and-sharp (mridu-tikshna) and moving.
N. C. Iyer's 1884 translation prints Hasta in the moving group where the usual lists have Punarvasu; this follows the usual lists,
which place each of the 27 stars in exactly one group (checked 19 Nov 2026 against wisdomlib.org and drikpanchang.com)."""
import math
NAK = ['Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra',
       'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati']
NATURES = ['steady', 'moving', 'light', 'soft', 'fierce', 'sharp', 'mixed']
STARS = {'steady': ['Rohini', 'Uttara Phalguni', 'Uttara Ashadha', 'Uttara Bhadrapada'], 'moving': ['Punarvasu', 'Swati', 'Shravana', 'Dhanishta', 'Shatabhisha'], 'light': ['Ashwini', 'Pushya', 'Hasta'],
         'soft': ['Mrigashira', 'Chitra', 'Anuradha', 'Revati'], 'fierce': ['Bharani', 'Magha', 'Purva Phalguni', 'Purva Ashadha', 'Purva Bhadrapada'], 'sharp': ['Ardra', 'Ashlesha', 'Jyeshtha', 'Mula'], 'mixed': ['Krittika', 'Vishakha']}
NATURE_OF = {s: n for n, l in STARS.items() for s in l}
assert sorted(NATURE_OF) == sorted(NAK) and len(NATURE_OF) == 27
COL = {'day': {'steady': '#9DB59A', 'moving': '#A9C3DB', 'light': '#EBCB7A', 'soft': '#C8B8E0', 'fierce': '#CC7A58', 'sharp': '#3E4A68', 'mixed': '#9CCFC0'},
       'night': {'steady': '#9DB59A', 'moving': '#A9C3DB', 'light': '#EBCB7A', 'soft': '#C8B8E0', 'fierce': '#D98A66', 'sharp': '#7D90C4', 'mixed': '#9CCFC0'}}


def _wedge(r0, r1, a0, a1):
    p = lambda r, a: (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))
    x0, y0 = p(r1, a0); x1, y1 = p(r1, a1); x2, y2 = p(r0, a1); x3, y3 = p(r0, a0)
    return f'M{x0:.2f},{y0:.2f} A{r1:.2f},{r1:.2f} 0 0 1 {x1:.2f},{y1:.2f} L{x2:.2f},{y2:.2f} A{r0:.2f},{r0:.2f} 0 0 0 {x3:.2f},{y3:.2f} Z'


def wheel(P, size=520, lit=None, mode='', pick=None, quarters=False, dot=False, inner='', hole=.6):
    """27 slices round the Moon's road, Ashwini first at the top, going clockwise, each coloured by its nature.
    lit: None for all, a nature name, or a list of star names. pick: one star drawn in full with a brass edge.
    quarters: split the picked star in four. dot: a small Moon on the road, at the picked star. inner: HTML for the middle."""
    col = COL[P['name']]; R = 100.0; r0 = R * hole; step = 360 / 27; gap = 1.5; o = []
    names = STARS.get(lit) if isinstance(lit, str) else lit
    for i, s in enumerate(NAK):
        a0 = -90 + i * step + gap / 2; a1 = -90 + (i + 1) * step - gap / 2; n = NATURE_OF[s]
        on = names is None or s in names or s == pick
        o.append(f'<g class="wg{" pk" if s == pick else ""}" data-i="{i}" data-c="{NATURES.index(n)}" data-on="{1 if on else 0}" opacity="{1 if on else .26}"><path d="{_wedge(r0, R, a0, a1)}" fill="{col[n]}"/></g>')
    if pick:
        i = NAK.index(pick); a0 = -90 + i * step + gap / 2; a1 = -90 + (i + 1) * step - gap / 2
        o.append(f'<path class="pke" d="{_wedge(r0 - 3.5, R + 3.5, a0 - .9, a1 + .9)}" fill="none" stroke="{P["orn"]}" stroke-width="1.5" stroke-linejoin="round"/>')
        if quarters:
            for k in (1, 2, 3):
                a = math.radians(a0 + (a1 - a0) * k / 4)
                o.append(f'<line class="qt" x1="{r0 * math.cos(a):.2f}" y1="{r0 * math.sin(a):.2f}" x2="{R * math.cos(a):.2f}" y2="{R * math.sin(a):.2f}" stroke="{P["paper"]}" stroke-width="1.5"/>')
        if dot:
            am = -90 + (i + .5) * step; rm = (r0 + R) / 2 - 31
            o.append(f'<circle class="mv" data-a="{am:.3f}" data-r="{rm:.2f}" cx="{rm * math.cos(math.radians(am)):.2f}" cy="{rm * math.sin(math.radians(am)):.2f}" r="5.2" fill="{P["bead"]}" stroke="{P["orn"]}" stroke-width="1.4"/>')
    mid = f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);line-height:0">{inner}</div>' if inner else ''
    return (f'<div class="wheel" data-mode="{mode}" style="position:relative;flex:0 0 auto;width:{size:.1f}px;height:{size:.1f}px">'
            f'<svg viewBox="-106 -106 212 212" width="{size:.1f}" height="{size:.1f}" style="display:block;overflow:visible">{"".join(o)}</svg>{mid}</div>')
