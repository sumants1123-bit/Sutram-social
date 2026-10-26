"""Sutram Instagram theme v3: matched to the @sutramthread feed (centered, all serif, warm glow,
thin gold orbits) with the Sun and Moon orbs from asksutram.com."""
import random, os, math
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT='/tmp/claude-0/-home-claude/7585c9d0-90d4-572f-bf7f-e3180b29fe46/scratchpad/'
NM='file://'+ROOT+'preview/node_modules/@fontsource/'
FONTS=''.join(f'<link rel="stylesheet" href="{NM}{f}">' for f in [
 'cormorant-garamond/500.css','cormorant-garamond/600.css','cormorant-garamond/500-italic.css','cormorant-garamond/600-italic.css',
 'eb-garamond/400.css','eb-garamond/500.css','eb-garamond/400-italic.css'])
CREAM='#F2E6CC'; AMBER='#E09460'; GOLD='#D9A57A'; BG='#0B0806'
CSS=f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;background:{BG}}}
.slide{{position:relative;width:1080px;height:1350px;overflow:hidden;color:{CREAM};text-align:center;
background:
 radial-gradient(52% 34% at 50% 44%,rgba(150,88,44,.20) 0%,rgba(150,88,44,0) 100%),
 radial-gradient(70% 14% at 50% 100%,rgba(224,148,96,.10) 0%,rgba(224,148,96,0) 100%),
 radial-gradient(125% 95% at 50% 38%,#17110C 0%,#0B0806 55%,#050403 100%);}}
.grain{{position:absolute;inset:0;pointer-events:none;opacity:.055;mix-blend-mode:screen}}
.kick{{position:absolute;top:92px;left:0;right:0;font:500 23px/1 'EB Garamond';letter-spacing:.34em;text-transform:uppercase;color:{GOLD}}}
.foot{{position:absolute;bottom:70px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:10px}}
.foot .w{{font:500 36px/1 'Cormorant Garamond';color:rgba(242,230,204,.62);letter-spacing:.02em}}
.foot .u{{font:500 17px/1 'EB Garamond';letter-spacing:.32em;text-transform:uppercase;color:rgba(242,230,204,.42)}}
.body{{position:absolute;left:100px;right:100px;top:170px;bottom:200px;display:flex;flex-direction:column;align-items:center}}
.t{{font-family:'Cormorant Garamond';font-weight:500;color:{CREAM};letter-spacing:-.01em}}
.ti{{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;color:{AMBER}}}
.p{{font:400 33px/1.45 'EB Garamond';color:rgba(242,230,204,.80)}}
.pi{{font:400 italic 33px/1.45 'EB Garamond';color:rgba(242,230,204,.80)}}
.src{{font:500 20px/1.3 'EB Garamond';letter-spacing:.24em;text-transform:uppercase;color:rgba(242,230,204,.46)}}
.lab{{font:500 21px/1 'EB Garamond';letter-spacing:.3em;text-transform:uppercase;color:{GOLD}}}
.rule{{height:1px;width:110px;background:rgba(217,165,122,.55)}}
.hair{{height:1px;width:100%;background:rgba(217,165,122,.22)}}
'''
GRAIN='''<svg class="grain" width="1080" height="1350"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1350" filter="url(#g)"/></svg>'''

def stars(n=120,seed=7,ymax=900):
    r=random.Random(seed); out=[]
    for _ in range(n):
        x=r.uniform(0,1080); y=r.uniform(0,ymax); rad=r.choice([.6,.8,1,1.2,1.5])
        op=r.uniform(.12,.6)*(1-y/ymax*.55)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="#FFF1D6" opacity="{op:.2f}"/>')
    return f'<svg style="position:absolute;inset:0" width="1080" height="1350">{"".join(out)}</svg>'

_uid=[0]
def _id(p): _uid[0]+=1; return f'{p}{_uid[0]}'

def moon(R=150, illum=1.0, waxing=True, halo=True):
    """Pearl Moon like asksutram.com, with the real phase as a soft shadow."""
    g=_id('mg'); b=_id('mb'); h=_id('mh'); s=2*R+160; c=s/2
    k=1-2*illum; rx=abs(k)*R
    shadow=''
    if illum<0.999:
        if waxing:   # dark on the left
            d=f'M{c},{c-R} A{R},{R} 0 0 0 {c},{c+R} A{rx},{R} 0 0 {1 if illum>0.5 else 0} {c},{c-R} Z'
        else:        # dark on the right
            d=f'M{c},{c-R} A{R},{R} 0 0 1 {c},{c+R} A{rx},{R} 0 0 {0 if illum>0.5 else 1} {c},{c-R} Z'
        shadow=f'<path d="{d}" fill="#0B0806" opacity=".93" filter="url(#{b})"/>'
    craters=''.join(f'<circle cx="{c+dx*R}" cy="{c+dy*R}" r="{rr*R}" fill="#8F888D" opacity="{op}" filter="url(#{b})"/>' for dx,dy,rr,op in
                    [(-.18,-.12,.16,.16),(.22,.05,.12,.14),(.05,.32,.10,.12),(-.32,.22,.08,.12),(.30,-.30,.07,.10)])
    halo_svg=f'<circle cx="{c}" cy="{c}" r="{R*1.04}" fill="#FFF4E6" opacity=".28" filter="url(#{h})"/>' if halo else ''
    return f'''<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block">
<defs><radialGradient id="{g}" cx="40%" cy="36%" r="72%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".3" stop-color="#F3EFEB"/><stop offset=".66" stop-color="#D6D0CF"/><stop offset="1" stop-color="#A39DA2"/></radialGradient>
<filter id="{b}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{max(2,R/40)}"/></filter>
<filter id="{h}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{R/5}"/></filter></defs>
{halo_svg}<circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/>{craters}{shadow}</svg>'''

def sun(R=150, rings=True, halo=True):
    """Orange Sun like asksutram.com, with faint concentric orbits."""
    g=_id('sg'); h=_id('sh'); s=2*R+160 if not rings else int(R*5.2); c=s/2
    ring_svg=''.join(f'<circle cx="{c}" cy="{c}" r="{R*f}" fill="none" stroke="#E09460" stroke-opacity="{o}" stroke-width="1.2"/>' for f,o in [(1.55,.16),(2.05,.11),(2.55,.07)]) if rings else ''
    halo_svg=f'<circle cx="{c}" cy="{c}" r="{R*1.08}" fill="#EF7A3C" opacity=".45" filter="url(#{h})"/>' if halo else ''
    return f'''<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block">
<defs><radialGradient id="{g}" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#FFE8CF"/><stop offset=".22" stop-color="#FBB37C"/><stop offset=".58" stop-color="#EE7838"/><stop offset=".88" stop-color="#C9521F"/><stop offset="1" stop-color="#A8401A"/></radialGradient>
<filter id="{h}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{R/3.2}"/></filter></defs>
{ring_svg}{halo_svg}<circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/></svg>'''

def orbit(w=760, h=170, beads=5, tilt=-8, lit=None, stroke=GOLD):
    """Thin gold orbit with beads: the thread with its pearls."""
    pad=40; W=w+2*pad; H=h+2*pad+60; cx=W/2; cy=H/2
    bs=''
    for i in range(beads):
        a=math.pi*(0.15+0.7*i/(beads-1)) if beads>1 else math.pi/2
        x=cx+ (w/2)*math.cos(a+math.pi); y=cy+ (h/2)*math.sin(a+math.pi)*-1
        if lit==i: bs+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{AMBER}"/>'
        else: bs+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#F2E6CC" opacity=".85"/>'
    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="display:block;overflow:visible">
<g transform="rotate({tilt} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{h/2}" fill="none" stroke="{stroke}" stroke-opacity=".55" stroke-width="1.6"/>{bs}</g></svg>'''

def chart(s=330, sw=2):
    h=s/2;q=s/4; x0=y0=4
    return f'''<svg width="{s+8}" height="{s+8}" style="display:block">
<polygon points="{x0+h},{y0} {x0+3*q},{y0+q} {x0+h},{y0+h} {x0+q},{y0+q}" fill="{AMBER}" fill-opacity=".20"/>
<g stroke="{GOLD}" stroke-opacity=".85" stroke-width="{sw}" fill="none"><rect x="{x0}" y="{y0}" width="{s}" height="{s}"/>
<line x1="{x0}" y1="{y0}" x2="{x0+s}" y2="{y0+s}"/><line x1="{x0+s}" y1="{y0}" x2="{x0}" y2="{y0+s}"/>
<polygon points="{x0+h},{y0} {x0+s},{y0+h} {x0+h},{y0+s} {x0},{y0+h}"/></g></svg>'''

def asc_icon(sz=70):
    return f'<svg width="{sz}" height="{sz}" viewBox="0 0 72 72"><line x1="6" y1="50" x2="66" y2="50" stroke="{GOLD}" stroke-width="2.4"/><path d="M16 50 A20 20 0 0 1 56 50" fill="none" stroke="{GOLD}" stroke-width="2.4"/><line x1="36" y1="22" x2="36" y2="12" stroke="{GOLD}" stroke-width="2.4"/></svg>'

def page(inner, kicker, extra='', url='sutram.ca'):
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body>
<div class="slide">{extra}{GRAIN}
<div class="kick">{kicker}</div>
<div class="body">{inner}</div>
<div class="foot"><div class="w">Sutram</div><div class="u">{url}</div></div></div></body></html>'''

def render(post_id, slides):
    out_dir=ROOT+f'posts3/{post_id}/'; os.makedirs(out_dir,exist_ok=True)
    outs=[]
    with sync_playwright() as p:
        b=p.chromium.launch()
        pg=b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
        for i,h in enumerate(slides,1):
            fn=out_dir+f'slide{i}.html'; open(fn,'w').write(h)
            pg.goto('file://'+fn); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(350)
            raw=out_dir+f'raw{i}.png'; pg.screenshot(path=raw)
            ov=pg.evaluate("()=>{const b=document.querySelector('.body');return b.scrollHeight-b.clientHeight}")
            im=Image.open(raw).convert('RGB').resize((1080,1350),Image.LANCZOS)
            out=out_dir+f'{post_id}-{i}.jpg'; im.save(out,quality=93,optimize=True,progressive=True); outs.append(out)
            os.remove(raw)
            if ov>0: print(f'  ! {post_id} slide {i} overflows by {ov}px')
        b.close()
    n=len(outs); cols=min(4,n); rows=(n+cols-1)//cols
    sheet=Image.new('RGB',(24+cols*384,24+rows*474),(5,4,3))
    for k,o in enumerate(outs):
        r,c=divmod(k,cols); sheet.paste(Image.open(o).resize((360,450),Image.LANCZOS),(24+c*384,24+r*474))
    sheet.save(out_dir+f'{post_id}-overview.jpg',quality=90)
    print(post_id,'->',n,'slides')
    return outs
