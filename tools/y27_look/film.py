#!/usr/bin/env python3
"""Your 2027, second promo (19 Nov 2026): the moving cover in the new colours.

Sumant, 19 Nov 7:02 PM: "I like the current 2027 intro post. The video that changes. But this one is also nice.
I like the colors of this one." So this keeps what the current cover does (the sky travels through the year, the date
changes in the middle, the room both slow grahas point at lights up) and draws it as the lotus of the new sample,
in its night colours. Every position and date comes from the engine's data.json. Nothing is worked out here except
where to draw it.

    python3 tools/y27_look/film.py            # frames at a few moments, to look at
    python3 tools/y27_look/film.py --film     # the whole film

The code is here; the engine's data for the sample person and everything this writes stay outside the repo
(Y27_WHO and Y27_WORK), because the pages are a real person's reading.
"""
import json, math, os, sys, datetime as dt, subprocess, shutil, colorsys
sys.path.insert(0, '/home/claude/sutram-social/tools'); import look as L
HERE = os.path.dirname(os.path.abspath(__file__)); H = os.environ.get('Y27_WORK', '/home/claude/_private/y27v2/promo'); WHO = os.environ.get('Y27_WHO', '/home/claude/_private/your2027/people/sumant')
D = json.load(open(f'{WHO}/data.json')); YEAR = D['year']; P = L.PAL['night']
OUT = f'{H}/out'; os.makedirs(OUT, exist_ok=True)
MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
Y0 = dt.date(YEAR, 1, 1); day = lambda iso: (dt.date.fromisoformat(iso) - Y0).days
SHORT = D['words']['area_short']; RIS = D['birth_chart']['rising_sign_index']
AIM = ['#E8C56E', '#9DB59A', '#DDA088', '#A9C3DB']
GC = {'Sun': '#E2A93B', 'Mars': '#C6553B', 'Mercury': '#7FAE8A', 'Jupiter': '#E4C766', 'Venus': '#E3B4C4', 'Saturn': '#7F8FB5', 'Rahu': '#9AA6B4', 'Ketu': '#B08D74'}
PETAL = 'M-4.2,-23 C-8,-38 -17.6,-50 -17.6,-66 C-17.6,-79 -6.5,-88 0,-104 C6.5,-88 17.6,-79 17.6,-66 C17.6,-50 8,-38 4.2,-23 Q0,-20.5 -4.2,-23 Z'
INNERP = 'M-2.6,-20 C-5.2,-27 -8,-33 -8,-40 C-8,-46.5 -3.2,-50 0,-58 C3.2,-50 8,-46.5 8,-40 C8,-33 5.2,-27 2.6,-20 Z'

# ---- the sky, day by day, as the engine gives it: where each graha stands on the lotus ----
order = D['clock']['order']; rows = D['clock']['rows']; assert D['clock']['start'] == f'{YEAR}-01-01' and len(rows) == 365
turn = lambda lon: round((lon - RIS * 30 + 15) % 360, 2)          # degrees clockwise from the top; room 12 sits at the top
ANG = {g: [turn(r[order.index(g)]) for r in rows] for g in ('Sun', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu')}
ANG['Ketu'] = [round((a + 180) % 360, 2) for a in ANG['Rahu']]
lit = [[0.0] * 13 for _ in range(365)]
for w in D['sky']['both_slow_grahas_on']:
    a, b = max(0, day(w['from']['date'])), min(364, day(w['to']['date']))
    for i in range(a, b + 1):
        for h in w['houses']: lit[i][h['house']] = 1.0
K = 5                                                                # a petal opens and closes over about ten days
LIT = [[round(sum(lit[min(364, max(0, i + k))][h] * (K + 1 - abs(k)) for k in range(-K, K + 1)) / (K + 1) ** 2, 3) for h in range(13)] for i in range(365)]
MEET = D['sky']['exact_meetings']; KEYS = []
for m in MEET:
    d = day(m['when']['date'])
    if KEYS and d - KEYS[-1]['day'] <= 2: KEYS[-1]['houses'].append(m['house']); KEYS[-1]['walkers'].append(m['walker']); continue
    KEYS.append(dict(day=d, label=f"{dt.date.fromisoformat(m['when']['date']).day} {MON[dt.date.fromisoformat(m['when']['date']).month - 1]}", houses=[m['house']], walkers=[m['walker']]))
ECL = [day(e['when']['date']) for e in D['sky']['eclipses']]
LAB = [f'{(Y0 + dt.timedelta(days=i)).day} {MON[(Y0 + dt.timedelta(days=i)).month - 1]}' for i in range(365)]
MSTART = [day(f'{YEAR}-{m:02d}-01') for m in range(1, 13)] + [365]

# ---- time: a short hold on 1 January, then the year, stopping on each exact meeting ----
KF = [[0, 0], [.5, 0]]; t = .5; prev = 0
for k in KEYS:
    t += max(.8, (k['day'] - prev) / 62); KF.append([round(t, 2), k['day']]); k['t0'] = round(t, 2); t += .62; KF.append([round(t, 2), k['day']]); k['t1'] = round(t, 2); prev = k['day']
t += (364 - prev) / 54; KF.append([round(t, 2), 364]); t += .75; KF.append([round(t, 2), 364]); LEN = round(t, 2)

def mix(c, w, a):
    c = [int(c[i:i + 2], 16) for i in (1, 3, 5)]; w = [int(w[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(x + (y - x) * a):02x}' for x, y in zip(c, w))
ORB = {'Mercury': (103, 9.5), 'Venus': (120, 10.5), 'Sun': (137, 12.5), 'Mars': (154, 11), 'Jupiter': (171, 14), 'Saturn': (188, 13.5), 'Rahu': (204, 10), 'Ketu': (204, 9)}
GRAD = ''.join(f'<radialGradient id="g{g}" cx="36%" cy="30%" r="78%"><stop offset="0" stop-color="{mix(c, "#ffffff", .62)}"/><stop offset=".5" stop-color="{c}"/><stop offset="1" stop-color="{mix(c, "#000000", .34)}"/></radialGradient>' for g, c in GC.items())
ARROW = f'<svg width="60" height="20" viewBox="0 0 64 22"><path d="M2,11 H58 M47,2 L60,11 L47,20" fill="none" stroke="{P["brass"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
JS = open(f'{HERE}/film.js').read()
PAGE = f'''<!doctype html><html><head><meta charset="utf-8"><style>{L.css(P)}
.slide::after{{content:"";position:absolute;left:0;right:0;top:330px;height:920px;background:radial-gradient(closest-side,rgba(217,165,122,.16),rgba(217,165,122,.05) 62%,transparent 100%);pointer-events:none}}
.ttl{{position:absolute;top:92px;left:0;right:0;text-align:center;font:600 176px/.92 'Cormorant Garamond';letter-spacing:-.02em;color:{P['ink']}}} .ttl i{{color:{P['terra']}}}
.line{{position:absolute;top:286px;left:0;right:0;text-align:center;font:italic 500 44px/1.1 'Cormorant Garamond';color:{P['brass']}}}
.swipe{{position:absolute;bottom:50px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:20px;font:600 20px/1 Inter;letter-spacing:.42em;text-transform:uppercase;color:{P['brass']};padding-left:.42em}}
#clock{{position:absolute;inset:0;z-index:2}} text{{font-kerning:normal}}
</style></head><body><div class="slide">{L.decor(P, 27, 'arcs')}
<div class="kick">Sutram · Year report</div>
<div class="ttl">Your <i>{YEAR}</i></div>
<div class="line">Your year, read from your own birth chart</div>
<svg id="clock" width="1080" height="1350" viewBox="0 0 1080 1350"><defs>{GRAD}
<filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.2"/></filter>
<filter id="soft" x="-120%" y="-120%" width="340%" height="340%"><feGaussianBlur stdDeviation="7"/></filter></defs><g id="root" transform="translate(540 796)"></g></svg>
<div class="swipe"><span>Swipe</span>{ARROW}</div></div>
<script>const DATA = {json.dumps(dict(ang=ANG, lit=LIT, keys=KEYS, ecl=ECL, lab=LAB, mstart=MSTART, kf=KF, len=LEN, short=SHORT, aim=AIM, orb=ORB, gc=GC, petal=PETAL, innerp=INNERP, flame=L.FLAME, year=YEAR,
    ink=P['ink'], brass=P['brass'], terra=P['terra'], mon=[m.upper() for m in MON]))};
{JS}</script></body></html>'''

if __name__ == '__main__':
    from playwright.sync_api import sync_playwright
    fn = f'{H}/film.html'; open(fn, 'w').write(PAGE); print('keys', [(k['label'], k['t0'], k['t1'], k['houses']) for k in KEYS], 'length', LEN, 's')
    film = '--film' in sys.argv
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
        pg.goto('file://' + fn); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        if not film:
            for t in [float(a) for a in sys.argv[1:]] or [0, 1.4, KEYS[0]['t0'] + .3, KEYS[1]['t0'] + .3, KEYS[2]['t0'] + .35, LEN - .1]:
                pg.evaluate('t => window.__fab(t)', t); pg.screenshot(path=f'{OUT}/f_{t:05.2f}.png'); print('frame', t)
        else:
            fr = f'{OUT}/frames'; shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr); n = round(LEN * 30)
            for i in range(n):
                pg.evaluate('t => window.__fab(t)', i / 30); pg.screenshot(path=f'{fr}/{i:04d}.jpg', type='jpeg', quality=92)
            part = f'{OUT}/your-2027-look-inside-1.part.mp4'; final = f'{OUT}/your-2027-look-inside-1.mp4'
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', f'{fr}/%04d.jpg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', part], check=True)
            os.replace(part, final); print(final, n, 'frames', round(os.path.getsize(final) / 1e6, 2), 'MB')
            pg.evaluate('t => window.__fab(t)', KEYS[-1]['t1'] - .05); pg.screenshot(path=f'{OUT}/poster.png')
        b.close()
