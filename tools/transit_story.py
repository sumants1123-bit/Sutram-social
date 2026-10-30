#!/usr/bin/env python3
"""Transit fact sheet for Sutram's Nadi-style transit stories.

The engine computes; the story is written from these facts only.

Usage:
  .venv/bin/python tools/transit_story.py START END [--focus Jupiter] [--node mean|true]
                                           [--table 2026-10-31,2026-11-14] [--step 2]
  e.g. .venv/bin/python tools/transit_story.py 2026-10-25 2027-05-01 --focus Jupiter

Prints, in Toronto time (Swiss Ephemeris, sidereal Lahiri):
  1. Positions on chosen dates: sign, degree, nakshatra and pada (with its lord), speed, R
  2. Events, in order:
     - sign changes, stations (with the degree), nakshatra changes of the slow planets
     - Gandanta crossings (the water-to-fire junctions: Cancer/Leo, Scorpio/Sagittarius, Pisces/Aries)
     - meetings between planets: entering 3 degrees, entering 1 degree, exact, leaving 1, leaving 3
     - exact degree links that involve the focus group: 0 (together), 60 (3-11), 120 (5-9), 180 (7)
     - deep exaltation and deep debilitation points within 3 and 1 degrees
     - combustion windows, sign exchanges, the Moon passing over the focus group
  3. Nadi links for the focus planet on each date in the table: same sign, 2nd and 12th,
     3rd and 11th, 5th and 9th, 7th; a retrograde planet also acts from the sign before it;
     hemming (papakartari) by sign and by degree.
"""
import argparse, datetime as dt
from zoneinfo import ZoneInfo
import swisseph as swe

TZ = ZoneInfo('America/Toronto')
swe.set_sid_mode(swe.SIDM_LAHIRI)
F = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
LORD = dict(Aries='Mars', Taurus='Venus', Gemini='Mercury', Cancer='Moon', Leo='Sun', Virgo='Mercury', Libra='Venus',
            Scorpio='Mars', Sagittarius='Jupiter', Capricorn='Saturn', Aquarius='Saturn', Pisces='Jupiter')
NAK = ['Ashwini','Bharani','Krittika','Rohini','Mrigashira','Ardra','Punarvasu','Pushya','Ashlesha','Magha',
       'Purva Phalguni','Uttara Phalguni','Hasta','Chitra','Swati','Vishakha','Anuradha','Jyeshtha','Mula',
       'Purva Ashadha','Uttara Ashadha','Shravana','Dhanishta','Shatabhisha','Purva Bhadrapada','Uttara Bhadrapada','Revati']
NLORD = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']
IDS = dict(Sun=swe.SUN, Moon=swe.MOON, Mercury=swe.MERCURY, Venus=swe.VENUS, Mars=swe.MARS, Jupiter=swe.JUPITER, Saturn=swe.SATURN)
SLOW = ['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Rahu','Ketu']
MALEFIC = {'Sun','Mars','Saturn','Rahu','Ketu'}
EXALT = dict(Sun=10, Moon=33, Mars=298, Mercury=165, Jupiter=95, Venus=357, Saturn=200)   # deep exaltation, absolute degrees
COMBUST = dict(Mars=(17,17), Mercury=(14,12), Jupiter=(11,11), Venus=(10,8), Saturn=(15,15))  # (direct, retrograde)
GANDANTA = {0: 'Revati to Ashwini (Pisces/Aries)', 120: 'Ashlesha to Magha (Cancer/Leo)', 240: 'Jyeshtha to Mula (Scorpio/Sagittarius)'}
LINKS = {1:'same sign', 2:'2nd (ahead)', 12:'12th (behind)', 3:'3rd', 11:'11th', 5:'5th (trine)', 9:'9th (trine)', 7:'7th (facing)'}


def sdiff(a, b):
    """Signed a minus b, in -180..180."""
    return (a - b + 180) % 360 - 180


def deg(lon):
    s = int(lon // 30); d = lon - 30 * s; m = int(round((d % 1) * 60))
    di = int(d)
    if m == 60: di, m = di + 1, 0
    return f"{SIGNS[s]} {di}°{m:02d}'"


def nak(lon):
    i = int(lon // (40 / 3)); pada = int((lon % (40 / 3)) // (10 / 3)) + 1
    return NAK[i], pada, NLORD[i % 9]


def local(jd):
    y, m, d, h = swe.revjul(jd)
    t = dt.datetime(y, m, d, tzinfo=dt.timezone.utc) + dt.timedelta(hours=h)
    return t.astimezone(TZ)


def tstr(jd):
    t = local(jd)
    return f"{t:%a} {t.day} {t:%b %Y}, {t.hour % 12 or 12}:{t:%M} {'AM' if t.hour < 12 else 'PM'}"


def jd_of(date_str, hour=12):
    t = dt.datetime.fromisoformat(date_str).replace(hour=hour, tzinfo=TZ).astimezone(dt.timezone.utc)
    return swe.julday(t.year, t.month, t.day, t.hour + t.minute / 60)


def root(f, a, b, n=36):
    fa = f(a)
    for _ in range(n):
        m = (a + b) / 2; fm = f(m)
        if (fa < 0) == (fm < 0): a, fa = m, fm
        else: b = m
    return (a + b) / 2


class Sky:
    def __init__(self, node='mean'):
        self.node = swe.MEAN_NODE if node == 'mean' else swe.TRUE_NODE

    def p(self, jd, name):
        if name in IDS:
            r = swe.calc_ut(jd, IDS[name], F)[0]; return r[0] % 360, r[3]
        r = swe.calc_ut(jd, self.node, F)[0]; lon = r[0] % 360
        return ((lon + 180) % 360 if name == 'Ketu' else lon), r[3]

    def lon(self, jd, name): return self.p(jd, name)[0]
    def spd(self, jd, name): return self.p(jd, name)[1]


def retro(sky, jd, name):
    return name not in ('Rahu', 'Ketu', 'Sun', 'Moon') and sky.spd(jd, name) < 0


def nadi_links(sky, jd, focus):
    """Who the focus planet is linked to by sign, the Nadi way."""
    fs = int(sky.lon(jd, focus) // 30); out = []
    for name in SLOW + ['Moon']:
        if name == focus: continue
        s = int(sky.lon(jd, name) // 30)
        h = (s - fs) % 12 + 1
        if h in LINKS: out.append(f"{name} {LINKS[h]}")
        if retro(sky, jd, name):
            hp = ((s - 1) - fs) % 12 + 1
            if hp in LINKS and hp != h: out.append(f"{name} (retrograde, acting from {SIGNS[(s - 1) % 12]}) {LINKS[hp]}")
    # hemming by sign: malefics in both the 2nd and the 12th
    behind = [n for n in SLOW if n != focus and (int(sky.lon(jd, n) // 30) - fs) % 12 == 11 and n in MALEFIC]
    ahead = [n for n in SLOW if n != focus and (int(sky.lon(jd, n) // 30) - fs) % 12 == 1 and n in MALEFIC]
    hem = f"hemmed by sign: {', '.join(behind)} behind / {', '.join(ahead)} ahead" if behind and ahead else ''
    # hemming by degree: the nearest planet on each side within 10 degrees
    fl = sky.lon(jd, focus); near = []
    for n in SLOW:
        if n == focus: continue
        d = sdiff(sky.lon(jd, n), fl)
        if abs(d) <= 10: near.append((d, n))
    b = max([x for x in near if x[0] < 0], default=None); a = min([x for x in near if x[0] > 0], default=None)
    hemd = ''
    if b and a:
        hemd = f"by degree: {b[1]} {abs(b[0]):.2f}° behind, {a[1]} {a[0]:.2f}° ahead" + (' (both malefic: papakartari)' if b[1] in MALEFIC and a[1] in MALEFIC else '')
    return out, hem, hemd


def scan(sky, jd0, jd1, step_h, focus):
    ev = []
    step = step_h / 24
    n = int((jd1 - jd0) / step) + 1
    jds = [jd0 + i * step for i in range(n)]
    names = SLOW
    focus_group = {focus, 'Ketu', 'Mars'}
    prev = None
    for jd in jds:
        cur = {nm: sky.p(jd, nm) for nm in names + ['Moon']}
        if prev:
            pjd, pc = prev
            for nm in names:
                (l0, v0), (l1, v1) = pc[nm], cur[nm]
                s0, s1 = int(l0 // 30), int(l1 // 30)
                if s0 != s1:
                    b = 30 * s1 if (s1 - s0) % 12 == 1 else 30 * s0
                    t = root(lambda x: sdiff(sky.lon(x, nm), b), pjd, jd)
                    back = (s1 - s0) % 12 == 11
                    txt = f"{nm} enters {SIGNS[s1]}" + (' (moving backward)' if back else '')
                    if b in GANDANTA:
                        g = GANDANTA[b]
                        if back:
                            w, sg = g.split(' (')
                            x, y = w.split(' to '); u, v = sg.rstrip(')').split('/')
                            g = f"{y} to {x} ({v}/{u})"
                        txt += f"; crosses the Gandanta, {g}"
                    ev.append((t, txt))
                if nm not in ('Sun',) and (v0 < 0) != (v1 < 0) and nm not in ('Rahu', 'Ketu'):
                    t = root(lambda x: sky.spd(x, nm), pjd, jd)
                    ev.append((t, f"{nm} stations {'direct' if v1 > 0 else 'retrograde'} at {deg(sky.lon(t, nm))}"))
                if nm in ('Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu', 'Venus', 'Mercury'):
                    k0, k1 = int(l0 // (40 / 3)), int(l1 // (40 / 3))
                    if k0 != k1:
                        b = (40 / 3) * k1 if (k1 - k0) % 27 == 1 else (40 / 3) * k0
                        t = root(lambda x: sdiff(sky.lon(x, nm), b), pjd, jd)
                        ev.append((t, f"{nm} enters {NAK[k1]} (nakshatra of {NLORD[k1 % 9]})" + (' (moving backward)' if (k1 - k0) % 27 == 26 and nm not in ('Rahu', 'Ketu') else '')))
                # deep exaltation / debilitation
                if nm in EXALT:
                    for pt, label in ((EXALT[nm], 'deep exaltation'), ((EXALT[nm] + 180) % 360, 'deep debilitation')):
                        d0, d1 = sdiff(l0, pt), sdiff(l1, pt)
                        for th in (3, 1):
                            if (abs(d0) - th) * (abs(d1) - th) < 0:
                                t = root(lambda x: abs(sdiff(sky.lon(x, nm), pt)) - th, pjd, jd)
                                ev.append((t, f"{nm} {'within' if abs(d1) < th else 'leaves'} {th}° of its {label} point ({deg(pt)})"))
                        if d0 * d1 < 0 and abs(d0) < 5:
                            t = root(lambda x: sdiff(sky.lon(x, nm), pt), pjd, jd)
                            ev.append((t, f"{nm} exactly on its {label} point ({deg(pt)})"))
                # combustion
                if nm in COMBUST:
                    orb0 = COMBUST[nm][1 if v0 < 0 else 0]; orb1 = COMBUST[nm][1 if v1 < 0 else 0]
                    c0 = abs(sdiff(l0, pc['Sun'][0])) < orb0; c1 = abs(sdiff(l1, cur['Sun'][0])) < orb1
                    if c0 != c1: ev.append((jd, f"{nm} {'becomes combust (within ' + str(orb1) + '° of the Sun)' if c1 else 'leaves combustion'}"))
            # pairs
            for i, a in enumerate(names):
                for bn in names[i + 1:]:
                    if {a, bn} == {'Rahu', 'Ketu'}: continue
                    d0 = sdiff(pc[a][0], pc[bn][0]); d1 = sdiff(cur[a][0], cur[bn][0])
                    if d0 * d1 < 0 and abs(d0) < 10:
                        t = root(lambda x: sdiff(sky.lon(x, a), sky.lon(x, bn)), pjd, jd)
                        ev.append((t, f"{a} and {bn} exact at {deg(sky.lon(t, a))}"))
                    for th in (3, 1):
                        if (abs(d0) - th) * (abs(d1) - th) < 0:
                            t = root(lambda x: abs(sdiff(sky.lon(x, a), sky.lon(x, bn))) - th, pjd, jd)
                            ev.append((t, f"{a} and {bn} {'come within' if abs(d1) < th else 'move beyond'} {th}°"))
                    if a in focus_group or bn in focus_group:
                        for ang in (60, 120, 180):
                            for sgn in ((1, -1) if ang != 180 else (1,)):
                                e0 = sdiff(d0, sgn * ang); e1 = sdiff(d1, sgn * ang)
                                if e0 * e1 < 0 and abs(e0) < 10:
                                    t = root(lambda x: sdiff(sdiff(sky.lon(x, a), sky.lon(x, bn)), sgn * ang), pjd, jd)
                                    ev.append((t, f"{a} and {bn} exactly {ang}° apart ({deg(sky.lon(t, a))} / {deg(sky.lon(t, bn))})"))
            # sign exchanges
            def exch(c):
                out = set()
                for i, a in enumerate(['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn']):
                    for bn in ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn'][i + 1:]:
                        sa, sb = SIGNS[int(c[a][0] // 30)], SIGNS[int(c[bn][0] // 30)]
                        if a != 'Moon' and bn != 'Moon' and LORD[sa] == bn and LORD[sb] == a: out.add((a, bn))
                return out
            x0, x1 = exch(pc), exch(cur)
            for pair in x1 - x0: ev.append((jd, f"Sign exchange begins: {pair[0]} and {pair[1]}"))
            for pair in x0 - x1: ev.append((jd, f"Sign exchange ends: {pair[0]} and {pair[1]}"))
            # the Moon over the focus group
            for nm in focus_group:
                d0 = sdiff(pc['Moon'][0], pc[nm][0]); d1 = sdiff(cur['Moon'][0], cur[nm][0])
                if d0 * d1 < 0 and abs(d0) < 20:
                    t = root(lambda x: sdiff(sky.lon(x, 'Moon'), sky.lon(x, nm)), pjd, jd)
                    ev.append((t, f"Moon passes over {nm} ({deg(sky.lon(t, nm))})"))
        prev = (jd, cur)
    ev.sort()
    return ev


def table(sky, jd, focus):
    rows = []
    for nm in ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu','Ketu']:
        l, v = sky.p(jd, nm); nk, pada, lord = nak(l)
        r = ' R' if retro(sky, jd, nm) else ''
        rows.append(f"  {nm:8s} {deg(l):16s} {nk} {pada} ({lord}){r}  speed {v:+.3f}°/day")
    links, hem, hemd = nadi_links(sky, jd, focus)
    rows.append(f"  Nadi links for {focus}: " + '; '.join(links))
    if hem: rows.append('  ' + hem)
    if hemd: rows.append('  ' + hemd)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('start'); ap.add_argument('end')
    ap.add_argument('--focus', default='Jupiter')
    ap.add_argument('--node', default='mean', choices=['mean', 'true'])
    ap.add_argument('--table', default='')
    ap.add_argument('--step', type=float, default=2.0, help='scan step in hours')
    a = ap.parse_args()
    sky = Sky(a.node)
    jd0, jd1 = jd_of(a.start, 0), jd_of(a.end, 23)
    print(f"# Transit facts {a.start} to {a.end} (Toronto time, Lahiri, {a.node} node), focus {a.focus}\n")
    for d in [a.start] + [x for x in a.table.split(',') if x]:
        jd = jd_of(d, 12)
        print(f"## Positions, {tstr(jd)}")
        print('\n'.join(table(sky, jd, a.focus))); print()
    print("## Events")
    for t, txt in scan(sky, jd0, jd1, a.step, a.focus):
        print(f"- {tstr(t)}: {txt}")


if __name__ == '__main__':
    main()
