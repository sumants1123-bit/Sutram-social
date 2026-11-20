#!/usr/bin/env python3
"""Your 2027, second promo (19 Nov 2026): the slides after the moving cover.

Sumant, 19 Nov 6:44 PM, after seeing the first Your 2027 post go out: "Can we elaborate more, add content, index, more
samples, make it more cool, visual, add more details, promote a section called expert vedic astrologer notes".
So: an index of what is inside, the expert's notes first, then seven real pages of the new sample (name removed),
each cut from the sample PDF itself and shown large enough to read. Then the same last slide as the first post.

    Y27_PUBLIC=1 python3 /home/claude/_private/y27v2/sample.py     # the name-free pages of the sample (private builder)
    python3 tools/y27_look/film.py --film                          # slide 1
    python3 tools/y27_look/slides.py                               # slides 2 to 10 and the overview

The code is here; the sample PDF and everything this writes stay outside the repo (Y27_WORK) until Sumant
approves the post. Only then do the finished slides go to posts/your-2027-look-inside.
"""
import os, sys, json, subprocess
from PIL import Image
sys.path.insert(0, '/home/claude/sutram-social/tools'); import look as L
from playwright.sync_api import sync_playwright
H = os.environ.get('Y27_WORK', '/home/claude/_private/y27v2/promo'); OUT = f'{H}/out'; PG = f'{H}/pages'; os.makedirs(PG, exist_ok=True)
PDF = f'{H}/../out_public/your-2027-sample-v2-public.pdf'; PID = 'your-2027-look-inside'
DAY, NIGHT = L.PAL['day'], L.PAL['night']; DPI = 340; K = DPI / 96            # the PDF page is 576 x 864 CSS px
KICK = 'Sutram · Your 2027'
AIM = ['#E8C56E', '#9DB59A', '#DDA088', '#A9C3DB']
PETAL = 'M-4.2,-23 C-8,-38 -17.6,-50 -17.6,-66 C-17.6,-79 -6.5,-88 0,-104 C6.5,-88 17.6,-79 17.6,-66 C17.6,-50 8,-38 4.2,-23 Q0,-20.5 -4.2,-23 Z'
INNERP = 'M-2.6,-20 C-5.2,-27 -8,-33 -8,-40 C-8,-46.5 -3.2,-50 0,-58 C3.2,-50 8,-46.5 8,-40 C8,-33 5.2,-27 2.6,-20 Z'

def crop(page, y0, y1, x0=28, x1=548):
    """a piece of one page of the sample PDF, in the page's own CSS px"""
    src = f'{PG}/p-{page:02d}.png'
    if not os.path.exists(src): subprocess.run(['pdftoppm', '-r', str(DPI), '-png', '-f', str(page), '-l', str(page), '-singlefile', PDF, src[:-4]], check=True)
    out = f'{PG}/c-{page:02d}-{y0}-{y1}.png'; Image.open(src).crop((round(x0 * K), round(y0 * K), round(x1 * K), round(y1 * K))).save(out); return out, (y1 - y0) / (x1 - x0)

EXTRA = f"""
.pcard{{position:relative;width:1000px;margin:0 -32px;border-radius:28px;overflow:hidden;background:#FBF7EF;border:1.5px solid {DAY['line']};box-shadow:0 38px 70px -30px rgba(30,42,68,.34),0 12px 26px -12px rgba(30,42,68,.16)}}
.pcard img{{display:block;width:100%}} .pcard .fade{{position:absolute;left:0;right:0;bottom:0;height:110px;background:linear-gradient(to bottom,rgba(251,247,239,0),rgba(251,247,239,.96))}}
.pcard .fadet{{position:absolute;left:0;right:0;top:0;height:54px;background:linear-gradient(to bottom,#FCF8F1 0,#FCF8F1 52%,rgba(252,248,241,0) 100%)}}
.tag{{position:absolute;right:26px;top:22px;font:600 15px/1 Inter;letter-spacing:.24em;text-transform:uppercase;color:{DAY['mute']};background:rgba(255,253,248,.9);border:1px solid {DAY['line']};border-radius:999px;padding:9px 14px 9px 16px}}
"""
def sample(head, page, y0, y1, fade=True, fadet=False, size=72, tag='top'):
    fn, _ = crop(page, y0, y1)
    return (f'<div class="t" style="font-size:{size}px">{head}</div><div style="height:36px"></div>'
            f'<div class="pcard"><img src="file://{fn}">' + ('<div class="fadet"></div>' if fadet else '') + ('<div class="fade"></div>' if fade else '') + f'<div class="tag" style="{"" if tag == "top" else tag}">Sample page</div></div>')

INDEX = [('Start here', [f'<b style="color:{DAY["terra"]}">Expert Vedic astrologer’s notes</b>', 'Your 2027 in one picture']),
         ('You', ['The house you were born with', 'Your lotus', 'The time you are in']),
         ('Your year', ['Dates to circle', 'Three stories', 'Your year by area of life']),
         ('Month by month', ['January to December', 'A calendar file for your phone']),
         ('Make it yours', ['Your question, answered', 'Check it against your past'])]
def index():
    rows = ''
    for k, (part, items) in enumerate(INDEX):
        bead = f'<span style="width:22px;height:22px;border-radius:50%;flex:none;margin-top:16px;border:2.4px solid {DAY["brass"]};background:{DAY["terra"] if k == 0 else "#FFFDF8"};{"border-color:" + DAY["terra"] if k == 0 else ""}"></span>'
        its = f'<span style="color:{DAY["brass"]};margin:0 12px">·</span>'.join(items)
        rows += (f'<div style="display:flex;gap:30px;align-items:flex-start;padding:{0 if k == 0 else 25}px 0 25px;{"" if k == 0 else "border-top:1.5px solid " + DAY["line"]}">{bead}'
                 f'<div style="text-align:left"><div style="font:600 50px/1.08 \'Cormorant Garamond\';color:{DAY["ink"]}">{part}</div><div style="font:400 29px/1.42 Inter;color:{DAY["ink2"]};margin-top:8px;text-wrap:pretty">{its}</div></div></div>')
    return (f'<div class="lab">A look inside</div><div class="t h2" style="margin-top:16px">What is in your report</div><div style="height:44px"></div>'
            f'<div style="position:relative;width:100%"><div style="position:absolute;left:10px;top:30px;bottom:96px;width:2px;background:{DAY["brass"]};opacity:.5"></div><div style="position:relative">{rows}</div></div>')

def lotus_mark(size):
    o = [f'<svg width="{size}" height="{size}" viewBox="-112 -112 224 224"><defs><filter id="gl" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3.4"/></filter></defs><circle r="107.5" fill="none" stroke="{NIGHT["brass"]}" stroke-width=".5" opacity=".4"/>']
    for h in range(1, 13):
        col = AIM[(h - 1) % 4]; on = h in (1, 4, 9); o.append(f'<g transform="rotate({h * 30})"><path d="{PETAL}" fill="{col}" fill-opacity=".11" stroke="{NIGHT["brass"]}" stroke-width=".7" stroke-opacity=".5"/>'
            + (f'<path d="{PETAL}" fill="{col}" opacity=".5" filter="url(#gl)"/><path d="{PETAL}" fill="{col}" fill-opacity=".94"/><path d="M0,-58 L0,-93" stroke="#FFFDF8" stroke-width=".7" stroke-opacity=".4" stroke-linecap="round"/>' if on else '') + '</g>')
    for h in range(12): o.append(f'<path d="{INNERP}" transform="rotate({h * 30 + 15})" fill="rgba(255,240,214,.09)" stroke="{NIGHT["brass"]}" stroke-width=".6" stroke-opacity=".6"/>')
    o.append(f'<circle r="17.5" fill="#17110D" stroke="{NIGHT["brass"]}" stroke-width=".9"/><g transform="translate(-7.4 -10.2) scale(.148)"><path d="{L.FLAME}" fill="{NIGHT["terra"]}"/></g></svg>')
    return ''.join(o)
def last():
    return (f'{lotus_mark(250)}<div style="height:26px"></div><div class="lab" style="color:{NIGHT["brass"]}">Your 2027 · year report</div>'
            f'<div class="t" style="font-size:236px;line-height:.94;margin-top:10px;letter-spacing:-.02em;font-feature-settings:\'lnum\' 1;font-variant-numeric:lining-nums">CA$39</div>'
            f'<div class="sub" style="margin-top:14px;color:{NIGHT["brass"]}">Delivered within 5 days</div>'
            f'<div style="margin-top:58px;padding:28px 54px 30px;border:2px solid {NIGHT["terra"]};border-radius:999px;font:600 50px/1 \'Cormorant Garamond\';color:{NIGHT["ink"]}">DM us the word <span style="font-style:italic;color:{NIGHT["terra"]}">2027</span></div>'
            f'<div style="margin-top:34px;font:400 27px/1.4 Inter;color:{NIGHT["mute"]}">Made from your birth date, time and place</div>')

SLIDES = [
    ('day', index(), 2),
    ('day', sample('Notes from an expert<br>Vedic astrologer', 4, 37, 487, fade=False), 3),
    ('day', sample('Your whole year on one wheel', 5, 35, 520, fade=False), 4),
    ('day', sample('Your chart, drawn as a lotus', 6, 35, 520, fade=False), 5),
    ('day', sample('Three stories carry your year', 8, 35, 458, fade=False), 6),
    ('day', sample('Every date shows its reason', 9, 388, 812, fade=False, fadet=True), 7),
    ('day', sample('Where it lands in your life', 11, 35, 447), 8),
    ('day', sample('Then month by month', 12, 35, 447, tag='top:88px'), 9),
    ('night', last(), 10),
]

def shoot(pg, html, out):
    fn = f'{H}/_slide.html'; open(fn, 'w').write(html); pg.goto('file://' + fn); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
    over = pg.evaluate("()=>{const b=document.querySelector('.body');return b.scrollHeight-b.clientHeight}")
    raw = f'{H}/_raw.png'; pg.screenshot(path=raw); Image.open(raw).convert('RGB').resize((1080, 1350), Image.LANCZOS).save(out, quality=93, optimize=True, progressive=True); return over

if __name__ == '__main__':
    outs = [f'{OUT}/{PID}-1.jpg']; Image.open(f'{OUT}/poster.png').convert('RGB').save(outs[0], quality=93, optimize=True, progressive=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=2)
        for theme, inner, n in SLIDES:
            P = L.PAL[theme]; html = L.page(P, KICK, inner, seed=40 + n, border='arcs', foot='word').replace('</style>', EXTRA + '</style>', 1)
            o = f'{OUT}/{PID}-{n}.jpg'; over = shoot(pg, html, o); outs.append(o); print(n, theme, 'px past the body:', over)
        b.close()
    cols = 5; rows = (len(outs) + cols - 1) // cols; w, h = 432, 540
    sheet = Image.new('RGB', (20 + cols * (w + 20), 20 + rows * (h + 20)), (232, 224, 208))
    for k, o in enumerate(outs):
        r, c = divmod(k, cols); sheet.paste(Image.open(o).resize((w, h), Image.LANCZOS), (20 + c * (w + 20), 20 + r * (h + 20)))
    sheet.save(f'{OUT}/{PID}-overview.jpg', quality=88); print(len(outs), 'slides', f'{OUT}/{PID}-overview.jpg')
