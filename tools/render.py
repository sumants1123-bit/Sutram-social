"""Render a Sutram Instagram post from a JSON spec into 1080x1350 JPEGs.

Usage: python3 tools/render.py specs/<post-id>.json
Writes posts/<post-id>/<post-id>-<n>.jpg and posts/<post-id>/<post-id>-overview.jpg.
Design: matched to the @sutramthread feed (centred, all serif, warm glow, thin gold orbit,
pearl Moon and orange Sun from asksutram.com). Slide text never ends with a period.
"""
import json, os, sys, math, random, re
from playwright.sync_api import sync_playwright
from PIL import Image

HERE=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.dirname(HERE)
NM='file://'+os.path.join(HERE,'node_modules','@fontsource')+'/'
FONTS=''.join(f'<link rel="stylesheet" href="{NM}{f}">' for f in [
 'cormorant-garamond/500.css','cormorant-garamond/600.css','cormorant-garamond/500-italic.css',
 'eb-garamond/400.css','eb-garamond/500.css','eb-garamond/400-italic.css'])
CREAM='#F2E6CC'; AMBER='#E09460'; GOLD='#D9A57A'; BG='#0B0806'
# one colour per part (13 Nov): amber, powder blue, sage, lavender. Used on the tabs, the section label and step numbers
PART_COLORS=['#E09460','#8FB8D8','#A9C79B','#C6A9DB']

TXT=1.4   # v5 (2 Nov): Sumant, again: text too small. Body and labels about 22% larger; never smaller than this

def css(s):
    f=lambda px: f'{px*s:.1f}px'
    return f'''*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;background:{BG}}}
.slide{{position:relative;width:1080px;height:1350px;overflow:hidden;color:{CREAM};text-align:center;
background:radial-gradient(52% 34% at 50% 44%,rgba(150,88,44,.20) 0%,rgba(150,88,44,0) 100%),
radial-gradient(70% 14% at 50% 100%,rgba(224,148,96,.10) 0%,rgba(224,148,96,0) 100%),
radial-gradient(125% 95% at 50% 38%,#17110C 0%,#0B0806 55%,#050403 100%);}}
.decor{{position:absolute;inset:0;pointer-events:none}}
.grain{{position:absolute;inset:0;pointer-events:none;opacity:.055;mix-blend-mode:screen}}
.kick{{position:absolute;top:84px;left:0;right:0;display:flex;align-items:center;justify-content:center;gap:24px;font:500 27px/1 'EB Garamond';letter-spacing:.30em;text-transform:uppercase;color:{GOLD}}}
.kick span{{padding-left:.30em}}
.kick i{{position:relative;display:block;height:1px;width:92px;background:linear-gradient(90deg,rgba(217,165,122,0),rgba(217,165,122,.75))}}
.kick i::after{{content:"";position:absolute;right:-3px;top:-3px;width:6px;height:6px;background:{AMBER};transform:rotate(45deg)}}
.kick i.r{{transform:scaleX(-1)}}
.frame{{position:absolute;inset:0;pointer-events:none}}
.foot{{position:absolute;bottom:66px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:10px}}
.foot .w{{font:500 38px/1 'Cormorant Garamond';color:rgba(242,230,204,.66)}}
.foot .u{{font:500 19px/1 'EB Garamond';letter-spacing:.32em;text-transform:uppercase;color:rgba(242,230,204,.48)}}
.body{{position:absolute;left:84px;right:84px;top:160px;bottom:196px;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.t{{font-family:'Cormorant Garamond';font-weight:500;color:{CREAM};letter-spacing:-.01em;text-shadow:0 0 42px rgba(224,148,96,.22)}}
.p .ti{{font-size:1.16em;line-height:1}}
.scene{{display:flex;flex-direction:column;align-items:center;margin-bottom:{f(46)}}}
.rooms{{display:flex;justify-content:center;gap:{f(14)}}}
.room{{display:flex;flex-direction:column;align-items:center}}
.room.dim{{opacity:.30}}
.arch{{position:relative;display:flex;align-items:center;justify-content:center;border:1.7px solid rgba(217,165,122,.46);background:linear-gradient(180deg,rgba(217,165,122,.085),rgba(217,165,122,0) 72%)}}
.room.focus .arch{{border-color:rgba(232,160,108,.98);background:radial-gradient(82% 72% at 50% 58%,rgba(224,148,96,.26),rgba(224,148,96,0) 76%),linear-gradient(180deg,rgba(217,165,122,.12),rgba(217,165,122,0) 72%);box-shadow:0 0 54px rgba(224,148,96,.20),inset 0 0 34px rgba(224,148,96,.10)}}
.sg{{font:500 {f(26)}/1 'EB Garamond';letter-spacing:.26em;text-transform:uppercase;color:{GOLD};padding-left:.26em}}
.room.focus .sg{{color:{CREAM}}}
.tag{{font:italic 500 {f(31)}/1 'Cormorant Garamond';color:{AMBER};height:{f(31)};white-space:nowrap}}
.conn{{display:flex;align-items:center;gap:{f(14)};margin:{f(10)} 0;font:italic 500 {f(29)}/1 'Cormorant Garamond';color:{AMBER}}}
.conn i{{display:block;width:{f(70)};height:0;border-top:1.6px dashed rgba(224,148,96,.6)}}
.ti{{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;color:{AMBER}}}
.p{{font:400 {f(46)}/1.4 'EB Garamond';color:rgba(242,230,204,.88)}}
.pi{{font:400 italic {f(44)}/1.38 'EB Garamond';color:rgba(242,230,204,.86)}}
.src{{font:500 {f(30)}/1.3 'EB Garamond';letter-spacing:.16em;text-transform:uppercase;color:rgba(242,230,204,.64)}}
.lab{{font:500 {f(30)}/1 'EB Garamond';letter-spacing:.26em;text-transform:uppercase;color:{GOLD}}}
.rule{{position:relative;height:1px;width:180px;background:linear-gradient(90deg,rgba(217,165,122,0),rgba(217,165,122,.8),rgba(217,165,122,0));margin:{f(32)} auto}}
.rule::after{{content:"";position:absolute;left:50%;top:50%;width:7px;height:7px;background:{AMBER};transform:translate(-50%,-50%) rotate(45deg)}}
.h1{{font-size:{f(132)};line-height:.98}} .h2{{font-size:{f(106)};line-height:1}} .h3{{font-size:{f(80)};line-height:1.05}}
.sub{{font-size:{f(62)};line-height:1.22}}
.row{{display:flex;justify-content:space-between;align-items:baseline;padding:{f(12)} 0;border-bottom:1px solid rgba(217,165,122,.2);text-align:left;gap:16px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;column-gap:56px;width:100%}}
.ro svg{{margin:0!important}}
.tabs{{position:absolute;top:134px;left:30px;right:30px;display:flex;justify-content:center;gap:9px}}
.tab{{display:flex;align-items:center;gap:9px;padding:10px 18px 10px 11px;border:1.3px solid rgba(217,165,122,.34);border-radius:999px;font:500 25px/1 'EB Garamond';letter-spacing:.11em;text-transform:uppercase;color:rgba(242,230,204,.56);white-space:nowrap}}
.tab b{{display:flex;align-items:center;justify-content:center;width:29px;height:29px;border-radius:50%;border:1.2px solid rgba(217,165,122,.5);font:600 20px/1 'Cormorant Garamond';letter-spacing:0;color:rgba(242,230,204,.7)}}
.tab.done{{color:rgba(242,230,204,.70);border-color:rgba(217,165,122,.46)}}
.tab.done b{{background:rgba(217,165,122,.22)}}
.tab.on{{background:var(--pc,{AMBER});border-color:var(--pc,{AMBER});color:#1B0F07;font-weight:600;box-shadow:0 0 34px color-mix(in srgb,var(--pc,{AMBER}) 38%,transparent)}}
.tab.on b{{border-color:#1B0F07;color:#1B0F07}}
.slide.tabbed .body{{top:210px}}
.slide.tabbed .lab,.slide.tabbed .nstep .tg{{color:var(--pc,{GOLD})}}
.slide.tabbed .nstep>b{{border-color:var(--pc,{AMBER});color:var(--pc,{AMBER})}}
.who{{font:italic 500 {f(33)}/1.1 'Cormorant Garamond';color:rgba(242,230,204,.9);margin-top:{f(8)};white-space:nowrap}}
.rnote{{font:italic 500 {f(31)}/1.1 'Cormorant Garamond';color:{AMBER};margin-top:{f(5)};white-space:nowrap}}
.reach{{position:absolute;left:0;pointer-events:none;overflow:visible}}
.swipe{{position:absolute;left:0;right:0;bottom:152px;display:flex;justify-content:center;align-items:center;gap:20px;font:500 33px/1 'EB Garamond';letter-spacing:.26em;text-transform:uppercase;color:{CREAM}}}
.swipe svg{{display:block}}
.contents{{display:grid;grid-template-columns:auto auto;justify-content:center;column-gap:{f(54)};row-gap:{f(12)};margin-top:{f(34)};text-align:left}}
.contents div{{display:flex;align-items:center;gap:{f(16)};font:500 {f(46)}/1.1 'EB Garamond';color:rgba(242,230,204,.92)}}
.contents b{{display:flex;align-items:center;justify-content:center;flex:0 0 auto;width:{f(52)};height:{f(52)};border-radius:50%;border:1.4px solid {AMBER};font:600 {f(34)}/1 'Cormorant Garamond';color:{AMBER}}}
.nstep{{display:flex;align-items:flex-start;gap:{f(26)};text-align:left;width:100%;padding:{f(17)} 0}}
.nstep+.nstep{{border-top:1px solid rgba(217,165,122,.22)}}
.nstep>b{{flex:0 0 auto;display:flex;align-items:center;justify-content:center;width:{f(74)};height:{f(74)};border-radius:50%;border:1.6px solid {AMBER};font:600 {f(46)}/1 'Cormorant Garamond';color:{AMBER};margin-top:{f(2)}}}
.nstep .hd{{font:500 {f(60)}/1.08 'Cormorant Garamond';color:{CREAM}}}
.nstep .ln{{font:400 {f(46)}/1.28 'EB Garamond';color:rgba(242,230,204,.88);margin-top:{f(7)}}}
.nstep .tg{{font:500 {f(27)}/1 'EB Garamond';letter-spacing:.18em;text-transform:uppercase;color:{GOLD};margin-bottom:{f(8)}}}
.narrow{{width:100%;margin-top:{f(26)}}}
.narrow .it{{padding:{f(13)} 0}}
.narrow .bar{{height:{f(10)};border-radius:{f(5)};background:linear-gradient(90deg,rgba(224,148,96,.95),rgba(224,148,96,.45));margin:0 auto {f(13)}}}
.narrow .hd{{font:500 {f(70)}/1 'Cormorant Garamond';color:{CREAM}}}
.narrow .ln{{font:400 {f(44)}/1.26 'EB Garamond';color:rgba(242,230,204,.88);margin-top:{f(6)}}}
'''
GRAIN='<svg class="grain" width="1080" height="1350"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1350" filter="url(#g)"/></svg>'

def clean(t):
    """No period at the end of slide text; keep ellipses, decimals and abbreviations inside."""
    if not isinstance(t,str): return t
    t=t.strip()
    while t.endswith('.') and not t.endswith('..'): t=t[:-1].rstrip()
    return t
def esc(t): return clean(t).replace("'",'’').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br>')
def rich(t):
    """*word* makes amber italic."""
    return re.sub(r'\*(.+?)\*', r'<span class="ti">\1</span>', esc(t))

def stars(seed=7,n=120,ymax=900,tt=0.0):
    r=random.Random(seed); out=[]
    for _ in range(n):
        x=r.uniform(0,1080); y=r.uniform(0,ymax); rad=r.choice([.6,.8,1,1.2,1.5])
        op=r.uniform(.12,.6)*(1-y/ymax*.55); op=max(.03,op*(1+.55*math.sin(2*math.pi*(r.choice([1,2,3])*tt+r.random()))))
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="#FFF1D6" opacity="{op:.3f}"/>')
    return f'<svg class="sf" style="position:absolute;inset:0" width="1080" height="1350">{"".join(out)}</svg>'
_n=[0]
def uid(p): _n[0]+=1; return f'{p}{_n[0]}'
def moon(R=140, illum=1.0, waxing=True):
    g,b,h=uid('mg'),uid('mb'),uid('mh'); s=2*R+160; c=s/2; k=1-2*illum; rx=abs(k)*R; sh=''
    if illum<0.999:
        if waxing: d=f'M{c},{c-R} A{R},{R} 0 0 0 {c},{c+R} A{rx},{R} 0 0 {1 if illum>0.5 else 0} {c},{c-R} Z'
        else:      d=f'M{c},{c-R} A{R},{R} 0 0 1 {c},{c+R} A{rx},{R} 0 0 {0 if illum>0.5 else 1} {c},{c-R} Z'
        sh=f'<path d="{d}" fill="#0B0806" opacity=".93" filter="url(#{b})"/>'
    cr=''.join(f'<circle cx="{c+dx*R}" cy="{c+dy*R}" r="{rr*R}" fill="#8F888D" opacity="{op}" filter="url(#{b})"/>' for dx,dy,rr,op in [(-.18,-.12,.16,.16),(.22,.05,.12,.14),(.05,.32,.10,.12),(-.32,.22,.08,.12),(.30,-.30,.07,.10)])
    return f'''<svg class="orbsvg" data-kind="moon" data-r="{R}" data-c="{c}" width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:-60px auto -40px"><defs><radialGradient id="{g}" cx="40%" cy="36%" r="72%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".3" stop-color="#F3EFEB"/><stop offset=".66" stop-color="#D6D0CF"/><stop offset="1" stop-color="#A39DA2"/></radialGradient><filter id="{b}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{max(2,R/40)}"/></filter><filter id="{h}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{R/5}"/></filter></defs><circle class="oglow" cx="{c}" cy="{c}" r="{R*1.04}" fill="#FFF4E6" opacity=".28" filter="url(#{h})"/><circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/>{cr}{sh}</svg>'''
def sun(R=100, rings=True):
    g,h=uid('sg'),uid('sh'); s=int(R*5.2) if rings else 2*R+160; c=s/2
    rg=''.join(f'<circle class="sring" data-f="{f}" cx="{c}" cy="{c}" r="{R*f}" fill="none" stroke="#E09460" stroke-opacity="{o}" stroke-width="1.2"/>' for f,o in [(1.55,.16),(2.05,.11),(2.55,.07)]) if rings else ''
    return f'''<svg class="orbsvg" data-kind="sun" data-r="{R}" data-c="{c}" width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:{-R*0.9:.0f}px auto {-R*0.9:.0f}px"><defs><radialGradient id="{g}" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#FFE8CF"/><stop offset=".22" stop-color="#FBB37C"/><stop offset=".58" stop-color="#EE7838"/><stop offset=".88" stop-color="#C9521F"/><stop offset="1" stop-color="#A8401A"/></radialGradient><filter id="{h}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{R/3.2}"/></filter></defs>{rg}<circle class="oglow" cx="{c}" cy="{c}" r="{R*1.08}" fill="#EF7A3C" opacity=".45" filter="url(#{h})"/><circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/></svg>'''
def orbit(w=720,h=160,beads=5,tilt=-7,lit=None):
    pad=40; W=w+2*pad; H=h+2*pad+40; cx,cy=W/2,H/2; bs=''
    for i in range(beads):
        a=math.pi*(0.15+0.7*i/max(1,beads-1)); x=cx-(w/2)*math.cos(a); y=cy+(h/2)*math.sin(a)
        bs+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{11 if lit==i else 9}" fill="{AMBER if lit==i else CREAM}" opacity="{1 if lit==i else .85}"/>'
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="display:block;margin:0 auto"><g transform="rotate({tilt} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{h/2}" fill="none" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.6"/>{bs}</g></svg>'
def north(s=320, nums=False, hi=1):
    """North Indian chart. Houses stay put (the 1st is the top diamond, then they run anticlockwise); hi lights one house or a list."""
    h=s/2;q=s/4;x0=y0=4; g=uid('nh')
    P={1:[(h,0),(3*q,q),(h,h),(q,q)],2:[(0,0),(h,0),(q,q)],3:[(0,0),(q,q),(0,h)],4:[(0,h),(q,q),(h,h),(q,3*q)],5:[(0,h),(q,3*q),(0,s)],6:[(0,s),(q,3*q),(h,s)],
       7:[(h,s),(q,3*q),(h,h),(3*q,3*q)],8:[(h,s),(3*q,3*q),(s,s)],9:[(s,s),(3*q,3*q),(s,h)],10:[(s,h),(3*q,3*q),(h,h),(3*q,q)],11:[(s,h),(3*q,q),(s,0)],12:[(s,0),(3*q,q),(h,0)]}
    his=[k for k in (hi if isinstance(hi,(list,tuple)) else [hi]) if k in P]
    pts=lambda k: ' '.join(f'{x0+x:.1f},{y0+y:.1f}' for x,y in P[k])
    lit=''.join(f'<polygon class="pulse" points="{pts(k)}" fill="{AMBER}" fill-opacity=".30" filter="url(#{g})"/><polygon points="{pts(k)}" fill="{AMBER}" fill-opacity=".20" stroke="{AMBER}" stroke-width="2.4"/>' for k in his)
    lab=''
    if nums:
        pos={1:(h,q*.9),2:(q,q*.45),3:(q*.45,q),4:(q,h),5:(q*.45,3*q),6:(q,3.55*q),7:(h,3.1*q),8:(3*q,3.55*q),9:(3.55*q,3*q),10:(3*q,h),11:(3.55*q,q),12:(3*q,q*.45)}
        lab=''.join(f'<text x="{x0+x}" y="{y0+y+(s/26 if n in his else 9)}" text-anchor="middle" font-family="Cormorant Garamond" font-style="italic" font-weight="{600 if n in his else 500}" font-size="{s/(7.2 if n in his else 11):.0f}" fill="{CREAM if n in his else AMBER}" fill-opacity="{1 if n in his else .8}">{n}</text>' for n,(x,y) in pos.items())
    return f'''<svg width="{s+8}" height="{s+8}" style="display:block;margin:0 auto;overflow:visible"><defs><filter id="{g}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{s/22:.1f}"/></filter></defs>{lit}<g stroke="{GOLD}" stroke-opacity=".85" stroke-width="2" fill="none"><rect x="{x0}" y="{y0}" width="{s}" height="{s}"/><line x1="{x0}" y1="{y0}" x2="{x0+s}" y2="{y0+s}"/><line x1="{x0+s}" y1="{y0}" x2="{x0}" y2="{y0+s}"/><polygon points="{x0+h},{y0} {x0+s},{y0+h} {x0+h},{y0+s} {x0},{y0+h}"/></g>{lab}</svg>'''
SIGNS=['Pisces','Aries','Taurus','Gemini','Aquarius',None,None,'Cancer','Capricorn',None,None,'Leo','Sagittarius','Scorpio','Libra','Virgo']
def south(s=320, labels=True, asc=None):
    c=s/4;x0=y0=4;out=''
    for i in range(16):
        r,k=divmod(i,4)
        if SIGNS[i] is None: continue
        x=x0+k*c;y=y0+r*c
        fill=f' fill="{AMBER}" fill-opacity=".18"' if asc==SIGNS[i] else ' fill="none"'
        out+=f'<rect x="{x}" y="{y}" width="{c}" height="{c}"{fill} stroke="{GOLD}" stroke-opacity=".85" stroke-width="2"/>'
        if labels: out+=f'<text x="{x+c/2}" y="{y+c/2+6}" text-anchor="middle" font-family="EB Garamond" font-size="{s/17:.0f}" fill="{CREAM}" fill-opacity=".75">{SIGNS[i][:3]}</text>'
    return f'<svg width="{s+8}" height="{s+8}" style="display:block;margin:0 auto">{out}</svg>'
def icon(kind, s=64):
    c=s/2
    if kind=='moon':
        g=uid('im'); return f'<svg width="{s}" height="{s}"><defs><radialGradient id="{g}" cx="40%" cy="36%" r="72%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".6" stop-color="#D6D0CF"/><stop offset="1" stop-color="#A39DA2"/></radialGradient></defs><circle cx="{c}" cy="{c}" r="{s*0.36}" fill="url(#{g})"/></svg>'
    if kind=='sun':
        g=uid('is'); return f'<svg width="{s}" height="{s}"><defs><radialGradient id="{g}" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#FFE8CF"/><stop offset=".3" stop-color="#FBB37C"/><stop offset=".7" stop-color="#EE7838"/><stop offset="1" stop-color="#A8401A"/></radialGradient></defs><circle cx="{c}" cy="{c}" r="{s*0.36}" fill="url(#{g})"/></svg>'
    # asc: the Sun's disc rising on the horizon line
    return f'<svg width="{s}" height="{s}"><path d="M{s*0.2},{s*0.62} A{s*0.3},{s*0.3} 0 0 1 {s*0.8},{s*0.62}" fill="none" stroke="{GOLD}" stroke-width="2.4"/><line x1="{s*0.06}" y1="{s*0.62}" x2="{s*0.94}" y2="{s*0.62}" stroke="{GOLD}" stroke-width="2.4"/></svg>'
def venus_orb(R=80):
    """Venus, the lover: pale gold under soft cloud, with a shaded limb and a thin bright rim (v6)."""
    g,h,cl,sh,bl=uid('vg'),uid('vh'),uid('vc'),uid('vs'),uid('vb'); s=2*R+160; c=s/2
    clouds=''.join(f'<ellipse cx="{c+dx*R:.1f}" cy="{c+dy*R:.1f}" rx="{rx*R:.1f}" ry="{ry*R:.1f}" fill="{col}" opacity="{op}" transform="rotate({rot} {c} {c})" filter="url(#{bl})"/>'
                   for dx,dy,rx,ry,col,op,rot in [(-.1,-.42,.95,.11,'#FFFFFF',.34,-14),(.1,-.08,1.0,.10,'#C9A56B',.30,-12),(-.05,.26,1.0,.12,'#FFFFFF',.26,-10),(.1,.58,.9,.10,'#B8925A',.30,-8)])
    return (f'<svg class="orbsvg" data-kind="venus" data-r="{R}" data-c="{c}" width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:-60px auto -50px"><defs>'
            f'<radialGradient id="{g}" cx="38%" cy="34%" r="74%"><stop offset="0" stop-color="#FFFBF2"/><stop offset=".35" stop-color="#F6E7C8"/><stop offset=".75" stop-color="#E2C48F"/><stop offset="1" stop-color="#B8925A"/></radialGradient>'
            f'<radialGradient id="{sh}" cx="36%" cy="30%" r="82%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#3A2410" stop-opacity=".55"/></radialGradient>'
            f'<clipPath id="{cl}"><circle cx="{c}" cy="{c}" r="{R}"/></clipPath>'
            f'<filter id="{h}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{R/3.2:.1f}"/></filter>'
            f'<filter id="{bl}" filterUnits="userSpaceOnUse" x="0" y="0" width="{s}" height="{s}"><feGaussianBlur stdDeviation="{R*.09:.1f}"/></filter></defs>'
            f'<circle class="oglow" cx="{c}" cy="{c}" r="{R*1.12:.1f}" fill="#F3DDB0" opacity=".42" filter="url(#{h})"/><circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/>'
            f'<g clip-path="url(#{cl})"><g class="drift">{clouds}</g><circle cx="{c}" cy="{c}" r="{R}" fill="url(#{sh})"/></g>'
            f'<circle cx="{c}" cy="{c}" r="{R-.8:.1f}" fill="none" stroke="#FFF6E0" stroke-opacity=".30" stroke-width="1.5"/></svg>')
def jupiter_orb(R=95):
    """Jupiter, the teacher: cream and tan bands that waver like weather, the red spot, a shaded limb and a thin bright rim (v6)."""
    g,h,cl,sh,wv=uid('jg'),uid('jh'),uid('jc'),uid('js'),uid('jw'); s=2*R+160; c=s/2
    bands=''.join(f'<rect x="{c-R*1.2:.1f}" y="{c+R*y:.1f}" width="{2.4*R:.1f}" height="{R*hh:.1f}" fill="{col}" opacity="{op}"/>' for y,hh,col,op in [(-.80,.09,'#C9A27A',.30),(-.62,.10,'#B9875A',.40),(-.38,.14,'#A86F45',.48),(-.12,.08,'#F1DDBB',.40),(.06,.16,'#9C6440',.50),(.30,.08,'#C99A6B',.40),(.48,.12,'#A87450',.42),(.70,.08,'#C9A27A',.34)])
    return (f'<svg class="orbsvg" data-kind="jupiter" data-r="{R}" data-c="{c}" width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:-60px auto -50px"><defs>'
            f'<radialGradient id="{g}" cx="38%" cy="32%" r="78%"><stop offset="0" stop-color="#F9ECD6"/><stop offset=".45" stop-color="#E4C79F"/><stop offset=".85" stop-color="#A57850"/><stop offset="1" stop-color="#6E4A2E"/></radialGradient>'
            f'<radialGradient id="{sh}" cx="36%" cy="30%" r="82%"><stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#1E0E05" stop-opacity=".62"/></radialGradient>'
            f'<clipPath id="{cl}"><circle cx="{c}" cy="{c}" r="{R}"/></clipPath>'
            f'<filter id="{h}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{R/3.2:.1f}"/></filter>'
            f'<filter id="{wv}" filterUnits="userSpaceOnUse" x="0" y="0" width="{s}" height="{s}"><feTurbulence type="fractalNoise" baseFrequency="{1.1/R:.4f} {5.5/R:.4f}" numOctaves="2" seed="4" result="n"/><feOffset class="jdrift" in="n" dx="0" dy="0" result="n2"/><feDisplacementMap in="SourceGraphic" in2="n2" scale="{R*.16:.1f}" xChannelSelector="R" yChannelSelector="G"/><feGaussianBlur stdDeviation="{max(.6,R*.012):.2f}"/></filter></defs>'
            f'<circle class="oglow" cx="{c}" cy="{c}" r="{R*1.1:.1f}" fill="#E0B98A" opacity=".34" filter="url(#{h})"/><circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/>'
            f'<g clip-path="url(#{cl})"><g filter="url(#{wv})">{bands}<ellipse class="jspot" cx="{c+R*.30:.1f}" cy="{c+R*.17:.1f}" rx="{R*.15:.1f}" ry="{R*.08:.1f}" fill="#A0492E" opacity=".72"/></g><circle cx="{c}" cy="{c}" r="{R}" fill="url(#{sh})"/></g>'
            f'<circle cx="{c}" cy="{c}" r="{R-.8:.1f}" fill="none" stroke="#FFE9C9" stroke-opacity=".28" stroke-width="1.5"/></svg>')
def asc_orb(s=230):
    h=uid('ah'); w=int(s*1.8); ht=int(s*1.0); cy=int(ht*0.66); cx=w/2; R=s*0.36
    return f'<svg width="{w}" height="{ht}" viewBox="0 0 {w} {ht}" style="display:block;margin:-46px auto -40px"><defs><filter id="{h}" filterUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{ht}"><feGaussianBlur stdDeviation="{s*0.08:.1f}"/></filter></defs><ellipse cx="{cx}" cy="{cy-R*0.3:.1f}" rx="{R*1.1:.1f}" ry="{R*0.7:.1f}" fill="#E09460" opacity=".40" filter="url(#{h})"/><circle cx="{cx-R:.1f}" cy="{cy}" r="18" fill="#E09460" opacity=".55" filter="url(#{h})"/><path d="M{cx-R:.1f},{cy} A{R:.1f},{R:.1f} 0 0 1 {cx+R:.1f},{cy}" fill="none" stroke="#D9A57A" stroke-width="3"/><line x1="{cx-s*0.62:.1f}" y1="{cy}" x2="{cx+s*0.62:.1f}" y2="{cy}" stroke="#D9A57A" stroke-width="3"/><circle cx="{cx-R:.1f}" cy="{cy}" r="9" fill="#E09460"/></svg>'
def _blob(c, R, pts, rot=0):
    """A smooth closed shape through points given on the unit disc (Catmull-Rom curve), placed at centre c, radius R."""
    a=math.radians(rot); P=[(c+R*(x*math.cos(a)-y*math.sin(a)), c+R*(x*math.sin(a)+y*math.cos(a))) for x,y in pts]; n=len(P)
    d=f'M{P[0][0]:.1f},{P[0][1]:.1f}'
    for k in range(n):
        p0,p1,p2,p3=P[k-1],P[k],P[(k+1)%n],P[(k+2)%n]
        d+=f' C{p1[0]+(p2[0]-p0[0])/6:.1f},{p1[1]+(p2[1]-p0[1])/6:.1f} {p2[0]-(p3[0]-p1[0])/6:.1f},{p2[1]-(p3[1]-p1[1])/6:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d+' Z'
def mars_orb(R=80, dim=False):
    """Mars as a small world: rust body, soft dark lands across it, a white polar cap and a shaded limb."""
    g,h,cl,sh,bl,cb=uid('mg'),uid('mh'),uid('mc'),uid('ms'),uid('mb'),uid('mp'); s=2*R+120; c=s/2
    stops=('#F6B58C','#D8703F','#A9451F','#5E2210') if not dim else ('#B8826A','#8A5440','#5E3324','#2E170E')
    glow='' if dim else f'<circle class="oglow" cx="{c}" cy="{c}" r="{R*1.1}" fill="#E0703C" opacity=".32" filter="url(#{h})"/>'
    band=_blob(c,R,[(-1.1,.02),(-.7,-.12),(-.38,-.02),(-.08,-.16),(.25,-.06),(.6,.05),(1.1,.02),(1.1,.3),(.62,.26),(.3,.34),(.02,.24),(-.3,.38),(-.7,.3),(-1.1,.36)],rot=-16)
    spot=_blob(c,R,[(.22,.58),(.46,.5),(.62,.6),(.5,.74),(.28,.72)],rot=0)
    patch=_blob(c,R,[(-.62,-.5),(-.38,-.58),(-.2,-.46),(-.42,-.38)],rot=0)
    lands=f'<path d="{band}" fill="#5A220F" opacity=".38" filter="url(#{bl})"/><path d="{spot}" fill="#5A220F" opacity=".26" filter="url(#{bl})"/><path d="{patch}" fill="#5A220F" opacity=".2" filter="url(#{bl})"/>'
    cap=f'<ellipse cx="{c-R*.08:.1f}" cy="{c-R*.9:.1f}" rx="{R*.36:.1f}" ry="{R*.15:.1f}" fill="#FFF3EA" opacity="{.55 if dim else .8}" filter="url(#{cb})"/>'
    return (f'<svg class="orbsvg" data-kind="mars" data-r="{R}" data-c="{c}" width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:-40px auto -40px"><defs>'
            f'<radialGradient id="{g}" cx="38%" cy="32%" r="76%"><stop offset="0" stop-color="{stops[0]}"/><stop offset=".45" stop-color="{stops[1]}"/><stop offset=".85" stop-color="{stops[2]}"/><stop offset="1" stop-color="{stops[3]}"/></radialGradient>'
            f'<radialGradient id="{sh}" cx="36%" cy="30%" r="82%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>'
            f'<clipPath id="{cl}"><circle cx="{c}" cy="{c}" r="{R}"/></clipPath>'
            f'<filter id="{h}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{R/3.2:.1f}"/></filter>'
            f'<filter id="{bl}" filterUnits="userSpaceOnUse" x="0" y="0" width="{s}" height="{s}"><feGaussianBlur stdDeviation="{R*.07:.1f}"/></filter>'
            f'<filter id="{cb}" filterUnits="userSpaceOnUse" x="0" y="0" width="{s}" height="{s}"><feGaussianBlur stdDeviation="{R*.035:.1f}"/></filter></defs>'
            f'{glow}<circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/><g clip-path="url(#{cl})"><g class="drift">{lands}</g>{cap}<circle cx="{c}" cy="{c}" r="{R}" fill="url(#{sh})"/></g>'
            f'<circle cx="{c}" cy="{c}" r="{R-.8:.1f}" fill="none" stroke="#FFD9BE" stroke-opacity="{.10 if dim else .18}" stroke-width="1.6"/></svg>')
def mercury_orb(R=70, dim=False):
    """Mercury: small, quick and cratered, in the grey-green of durva grass that Parashara gives it."""
    g,h,cl,sh,bl=uid('qg'),uid('qh'),uid('qc'),uid('qs'),uid('qb'); s=2*R+120; c=s/2
    stops=('#E4F0D6','#A3C08C','#5E8456','#24361F') if not dim else ('#B4BBA8','#87927C','#59644F','#272D22')
    glow='' if dim else f'<circle class="oglow" cx="{c}" cy="{c}" r="{R*1.1}" fill="#9CC283" opacity=".30" filter="url(#{h})"/>'
    craters=''.join(f'<circle cx="{c+dx*R:.1f}" cy="{c+dy*R:.1f}" r="{rr*R:.1f}" fill="#3E4D3E" opacity="{op}" filter="url(#{bl})"/><circle cx="{c+dx*R-rr*R*.25:.1f}" cy="{c+dy*R-rr*R*.25:.1f}" r="{rr*R*.7:.1f}" fill="#FFFFFF" opacity="{op*.22:.2f}" filter="url(#{bl})"/>'
                    for dx,dy,rr,op in [(-.30,-.18,.15,.30),(.24,.10,.11,.26),(.02,.42,.09,.24),(-.42,.30,.07,.22),(.38,-.36,.08,.22),(-.05,-.48,.06,.2),(.55,.32,.06,.2)])
    return (f'<svg class="orbsvg" data-kind="mercury" data-r="{R}" data-c="{c}" width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:-40px auto -40px"><defs>'
            f'<radialGradient id="{g}" cx="38%" cy="32%" r="76%"><stop offset="0" stop-color="{stops[0]}"/><stop offset=".45" stop-color="{stops[1]}"/><stop offset=".85" stop-color="{stops[2]}"/><stop offset="1" stop-color="{stops[3]}"/></radialGradient>'
            f'<radialGradient id="{sh}" cx="36%" cy="30%" r="82%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>'
            f'<clipPath id="{cl}"><circle cx="{c}" cy="{c}" r="{R}"/></clipPath>'
            f'<filter id="{h}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{R/3.2:.1f}"/></filter>'
            f'<filter id="{bl}" filterUnits="userSpaceOnUse" x="0" y="0" width="{s}" height="{s}"><feGaussianBlur stdDeviation="{max(1.2,R*.025):.1f}"/></filter></defs>'
            f'{glow}<circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/><g clip-path="url(#{cl})">{craters}<circle cx="{c}" cy="{c}" r="{R}" fill="url(#{sh})"/></g>'
            f'<circle cx="{c}" cy="{c}" r="{R-.8:.1f}" fill="none" stroke="#E8F0DE" stroke-opacity="{.08 if dim else .16}" stroke-width="1.4"/></svg>')
def node_orb(R=80, kind='ketu'):
    """Rahu and Ketu are shadow points: a dark disc in eclipse, with a streaming corona and one bright bead on the rim (v6)."""
    g,h,cr=uid('ng'),uid('nh'),uid('nc'); s=int(2*R+160); c=s/2
    rim='#E09460' if kind=='ketu' else '#A9B9D6'; hot='#FFE3C4' if kind=='ketu' else '#EEF4FF'
    bx,by=(c+R*.72,c-R*.70) if kind=='ketu' else (c-R*.72,c-R*.70)
    return (f'<svg class="orbsvg" data-kind="{kind}" data-r="{R}" data-c="{c}" width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:-60px auto -50px"><defs>'
            f'<radialGradient id="{g}" cx="50%" cy="50%" r="50%"><stop offset=".55" stop-color="{rim}" stop-opacity="0"/><stop offset=".74" stop-color="{rim}" stop-opacity=".62"/><stop offset="1" stop-color="{rim}" stop-opacity="0"/></radialGradient>'
            f'<filter id="{h}" filterUnits="userSpaceOnUse" x="0" y="0" width="{s}" height="{s}"><feGaussianBlur stdDeviation="{R/6:.1f}"/></filter>'
            f'<filter id="{cr}" filterUnits="userSpaceOnUse" x="0" y="0" width="{s}" height="{s}"><feGaussianBlur stdDeviation="{max(.8,R*.03):.1f}"/></filter></defs>'
            f'<circle cx="{c}" cy="{c}" r="{R*1.42:.1f}" fill="url(#{g})" filter="url(#{h})"/>'
            f'<circle class="ncor" cx="{c}" cy="{c}" r="{R*1.20:.1f}" fill="none" stroke="{rim}" stroke-opacity=".42" stroke-width="{R*.36:.1f}" stroke-dasharray="{R*.035:.2f} {R*.105:.2f}" filter="url(#{cr})"/>'
            f'<circle cx="{c}" cy="{c}" r="{R}" fill="#070504"/>'
            f'<circle cx="{c}" cy="{c}" r="{R}" fill="none" stroke="{rim}" stroke-opacity=".95" stroke-width="{max(2.2,R*.045):.1f}"/>'
            f'<circle cx="{c}" cy="{c}" r="{R-max(6,R*.12):.1f}" fill="none" stroke="{rim}" stroke-opacity=".16" stroke-width="1"/>'
            f'<g class="nbead"><circle cx="{bx:.1f}" cy="{by:.1f}" r="{R*.20:.1f}" fill="{hot}" opacity=".30" filter="url(#{h})"/><circle cx="{bx:.1f}" cy="{by:.1f}" r="{max(1.8,R*.055):.1f}" fill="{hot}"/></g></svg>')
def saturn_orb(R=70):
    """Saturn, the auditor: pale gold with soft bands and a tilted ring; the back of the ring passes behind the disc."""
    g,h,cl,sh,bk,fr=uid('tg'),uid('th'),uid('tc'),uid('ts'),uid('tb'),uid('tf'); s=int(2*R+160); c=s/2
    tilt=-18; rx=R*1.62; ry=R*0.40; sw=R*0.13
    bands=''.join(f'<rect x="{c-R:.1f}" y="{c+R*y:.1f}" width="{2*R:.1f}" height="{R*hh:.1f}" fill="{col}" opacity="{op}"/>' for y,hh,col,op in [(-.55,.12,'#B89B68',.30),(-.25,.10,'#CDB487',.30),(.05,.14,'#A88A5A',.34),(.38,.10,'#BFA374',.28)])
    ring=lambda clip,op: (f'<g transform="rotate({tilt} {c} {c})"><g clip-path="url(#{clip})">'
                          f'<ellipse cx="{c}" cy="{c}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="#E6D3A8" stroke-opacity="{op}" stroke-width="{sw:.1f}"/>'
                          f'<ellipse cx="{c}" cy="{c}" rx="{rx*0.83:.1f}" ry="{ry*0.83:.1f}" fill="none" stroke="#C9B080" stroke-opacity="{op*0.7:.2f}" stroke-width="{sw*0.55:.1f}"/></g></g>')
    return (f'<svg class="orbsvg" data-kind="saturn" data-r="{R}" data-c="{c}" width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:-60px auto -50px"><defs>'
            f'<radialGradient id="{g}" cx="38%" cy="32%" r="78%"><stop offset="0" stop-color="#F8EDD3"/><stop offset=".45" stop-color="#E3CD9C"/><stop offset=".85" stop-color="#A88A58"/><stop offset="1" stop-color="#6B5434"/></radialGradient>'
            f'<radialGradient id="{sh}" cx="36%" cy="30%" r="82%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient>'
            f'<clipPath id="{cl}"><circle cx="{c}" cy="{c}" r="{R}"/></clipPath>'
            f'<clipPath id="{bk}"><rect x="0" y="0" width="{s}" height="{c}"/></clipPath>'
            f'<clipPath id="{fr}"><rect x="0" y="{c}" width="{s}" height="{c}"/></clipPath>'
            f'<filter id="{h}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{R/3.4:.1f}"/></filter></defs>'
            f'<circle class="oglow" cx="{c}" cy="{c}" r="{R*1.1:.1f}" fill="#E8D09A" opacity=".28" filter="url(#{h})"/>'
            f'{ring(bk,.55)}<circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/><g clip-path="url(#{cl})">{bands}<circle cx="{c}" cy="{c}" r="{R}" fill="url(#{sh})"/></g>{ring(fr,.9)}</svg>')
def top_orb(s=300):
    """The spinning top, a dreamer's test of what is real, inside thin orbits with grahas riding them (Inception post, 6 Nov)."""
    g=uid('tp'); W=s*1.7; H=s*1.12; cx=W/2; cy=H*0.47
    o=[f'<defs><linearGradient id="{g}m" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5A4129"/><stop offset=".32" stop-color="#F1DDB2"/><stop offset=".55" stop-color="#C39A62"/><stop offset="1" stop-color="#3E2D1C"/></linearGradient>'
       f'<radialGradient id="{g}f" cx="45%" cy="40%" r="70%"><stop offset="0" stop-color="#FFF6E4"/><stop offset="1" stop-color="#D9B983"/></radialGradient>'
       f'<radialGradient id="{g}g" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{AMBER}" stop-opacity=".30"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient></defs>']
    o.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{s*.62:.1f}" ry="{s*.5:.1f}" fill="url(#{g}g)"/>')
    rings=[(s*.80,s*.17,-10),(s*.66,s*.14,7),(s*.52,s*.11,-3)]
    for rx,ry,rot in rings:
        o.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{GOLD}" stroke-opacity=".34" stroke-width="1.6" transform="rotate({rot} {cx:.1f} {cy:.1f})"/>')
    tx,ty=cx,cy+s*.36
    body=(f'M{cx-s*.30:.1f},{cy-s*.20:.1f} C{cx-s*.30:.1f},{cy+s*.02:.1f} {cx-s*.09:.1f},{cy+s*.18:.1f} {tx:.1f},{ty:.1f} '
          f'C{cx+s*.09:.1f},{cy+s*.18:.1f} {cx+s*.30:.1f},{cy+s*.02:.1f} {cx+s*.30:.1f},{cy-s*.20:.1f} Z')
    o.append(f'<ellipse cx="{cx:.1f}" cy="{cy+s*.385:.1f}" rx="{s*.17:.1f}" ry="{s*.026:.1f}" fill="#000" opacity=".55"/>')
    o.append(f'<g transform="rotate(8 {tx:.1f} {ty:.1f})"><path d="{body}" fill="url(#{g}m)"/>'
             f'<path d="M{cx-s*.27:.1f},{cy-s*.08:.1f} Q{cx:.1f},{cy:.1f} {cx+s*.27:.1f},{cy-s*.08:.1f}" fill="none" stroke="{AMBER}" stroke-opacity=".8" stroke-width="2.2"/>'
             f'<path d="M{cx-s*.19:.1f},{cy+s*.09:.1f} Q{cx:.1f},{cy+s*.15:.1f} {cx+s*.19:.1f},{cy+s*.09:.1f}" fill="none" stroke="{AMBER}" stroke-opacity=".55" stroke-width="1.8"/>'
             f'<ellipse cx="{cx:.1f}" cy="{cy-s*.20:.1f}" rx="{s*.30:.1f}" ry="{s*.065:.1f}" fill="url(#{g}f)"/>'
             f'<rect x="{cx-s*.03:.1f}" y="{cy-s*.42:.1f}" width="{s*.06:.1f}" height="{s*.22:.1f}" rx="{s*.02:.1f}" fill="url(#{g}m)"/>'
             f'<ellipse cx="{cx:.1f}" cy="{cy-s*.42:.1f}" rx="{s*.03:.1f}" ry="{s*.012:.1f}" fill="#FFF6E4"/></g>')
    o.append(f'<path d="M{cx-s*.42:.1f},{cy-s*.13:.1f} A{s*.42:.1f},{s*.10:.1f} 0 0 0 {cx+s*.20:.1f},{cy-s*.04:.1f}" fill="none" stroke="{CREAM}" stroke-opacity=".5" stroke-width="2" stroke-linecap="round"/>')
    for rx,ry,rot in rings:   # the front half of each orbit passes in front of the top
        o.append(f'<path d="M{cx-rx:.1f},{cy:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {cx+rx:.1f},{cy:.1f}" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.6" transform="rotate({rot} {cx:.1f} {cy:.1f})"/>')
    for (rx,ry,rot),kind,a0 in zip(rings+[rings[0]],['sun','moon','mars','venus'],[198,342,64,128]):
        a=math.radians(a0); x=cx+rx*math.cos(a); y=cy+ry*math.sin(a); c=math.cos(math.radians(rot)); s_=math.sin(math.radians(rot))
        X=cx+(x-cx)*c-(y-cy)*s_; Y=cy+(x-cx)*s_+(y-cy)*c
        col,rad={'sun':('#F08A4C',s*.055),'moon':('#F5EEDF',s*.045),'mars':('#B9573C',s*.036),'venus':('#EBD9A8',s*.04)}[kind]
        o.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{rad*2.4:.1f}" fill="{col}" opacity=".16"/><circle cx="{X:.1f}" cy="{Y:.1f}" r="{rad:.1f}" fill="{col}"/>')
    return f'<svg width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">{"".join(o)}</svg>'
BODY_Y=[30,82,150,205,262,310,355,405,480,585,665,780]   # Aries (head) to Pisces (feet) on a figure 800 tall, Parashara's order
_FIG=[(0,6),(24,12),(36,34),(38,58),(32,84),(22,100),(16,108),(17,126),(40,136),(74,146),(90,160),(96,190),(100,250),(104,300),(110,360),(116,410),(120,440),(114,462),(102,452),
      (98,420),(88,360),(80,300),(72,240),(66,200),(62,230),(56,290),(58,330),(66,380),(70,420),(66,500),(58,570),(56,600),(60,650),(50,720),(44,762),(58,786),(40,794),(18,790),
      (20,760),(22,700),(24,640),(20,600),(18,570),(14,500),(8,430),(0,420)]
def _figure(cx, top, H, pearls=True, lit=None):
    """A standing figure in thin gold line with the thread running crown to feet and twelve pearls on it, one for each sign."""
    k=H/800; g=uid('kf'); P=[(cx+x*k, top+y*k) for x,y in _FIG]+[(cx-x*k, top+y*k) for x,y in reversed(_FIG[1:-1])]; n=len(P)
    d=f'M{P[0][0]:.1f},{P[0][1]:.1f}'
    for i in range(n):
        p0,p1,p2,p3=P[i-1],P[i],P[(i+1)%n],P[(i+2)%n]
        d+=f' C{p1[0]+(p2[0]-p0[0])/6:.1f},{p1[1]+(p2[1]-p0[1])/6:.1f} {p2[0]-(p3[0]-p1[0])/6:.1f},{p2[1]-(p3[1]-p1[1])/6:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    o=(f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AMBER}" stop-opacity=".20"/><stop offset=".55" stop-color="{AMBER}" stop-opacity=".07"/><stop offset="1" stop-color="{AMBER}" stop-opacity=".02"/></linearGradient>'
       f'<filter id="{g}b" x="-40%" y="-10%" width="180%" height="120%"><feGaussianBlur stdDeviation="{9*k:.1f}"/></filter></defs>'
       f'<path d="{d} Z" fill="{AMBER}" opacity=".10" filter="url(#{g}b)"/><path d="{d} Z" fill="url(#{g})" stroke="{GOLD}" stroke-opacity=".78" stroke-width="{max(1.4,2.0*k):.2f}" stroke-linejoin="round"/>'
       f'<line x1="{cx}" y1="{top-14*k:.1f}" x2="{cx}" y2="{top+H+8*k:.1f}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="{max(1,1.3*k):.2f}"/>')
    if pearls:
        for j,y in enumerate(BODY_Y):
            on=(lit is None or j in lit); yy=top+y*k
            o+=(f'<g class="seq"><circle cx="{cx}" cy="{yy:.1f}" r="{15*k:.1f}" fill="{AMBER}" opacity="{.20 if on else .08}"/><circle cx="{cx}" cy="{yy:.1f}" r="{max(3.2,6.4*k):.1f}" fill="{AMBER if on else CREAM}"/></g>')
    return o
def figure_orb(h=430):
    w=h*.42
    return f'<svg width="{w:.0f}" height="{h+28:.0f}" viewBox="0 0 {w:.0f} {h+28:.0f}" style="display:block;margin:0 auto;overflow:visible">{_figure(w/2,14,h)}</svg>'
def bodymap(items, s=1.0, rowh=62):
    """The figure on the left, the twelve signs on the right, a fine line from each pearl to its name."""
    n=len(items); Hh=n*rowh; W=912; cx=142; top=10; H=Hh-20; k=H/800; o=_figure(cx,top,H); xl=452
    for j,(a,b) in enumerate(items):
        y=top+BODY_Y[j]*k; yr=(j+.5)*rowh
        o+=(f'<path d="M{cx+10*k:.1f},{y:.1f} H{cx+150:.1f} L{xl-26},{yr:.1f} H{xl-8}" fill="none" stroke="{GOLD}" stroke-opacity=".42" stroke-width="1.2"/>'
            f'<text x="{xl}" y="{yr+15:.1f}" font-family="Cormorant Garamond" font-weight="500" font-size="50" fill="{CREAM}">{esc(a)}</text>'
            f'<text x="{W-2}" y="{yr+13:.1f}" text-anchor="end" font-family="EB Garamond" font-style="italic" font-size="43" fill="{AMBER}">{esc(b)}</text>')
        if j<n-1: o+=f'<line x1="{xl}" y1="{(j+1)*rowh:.1f}" x2="{W}" y2="{(j+1)*rowh:.1f}" stroke="{GOLD}" stroke-opacity=".16" stroke-width="1"/>'
    return f'<svg width="{W*s:.0f}" height="{Hh*s:.0f}" viewBox="0 0 {W} {Hh}" style="display:block;margin:{18*s:.0f}px auto 0;overflow:visible">{o}</svg>'

def orb_size(o):
    """Width of an orb's drawing canvas (the glow needs room), so a row can space grahas by their centres."""
    k=o.get('kind'); r=o.get('r',80)
    if k=='top': return o.get('s',300)*1.7
    if k=='figure': return o.get('h',430)*.42
    if k in ('mars','mercury'): return 2*r+120
    if k=='sun': return r*5.2 if o.get('rings',True) else 2*r+160
    return 2*r+160
def orbrow(orbs, spacing=None, gap=18):
    """Grahas side by side. spacing = distance between centres (an orb's own dx overrides it); otherwise a plain gap."""
    out=''; prev=None
    for o in orbs:
        w=orb_size(o); d=o.get('dx',spacing)
        ml=0 if prev is None else ((d-(prev+w)/2) if d is not None else gap)
        out+=f'<div style="flex:0 0 auto;margin-left:{ml:.1f}px">{orb(o)}</div>'
        prev=w
    return f'<div style="display:flex;align-items:center;justify-content:center">{out}</div>'
def orb(o):
    if not o: return ''
    if o.get('kind')=='saturn': return saturn_orb(o.get('r',70))
    if o.get('kind') in ('ketu','rahu'): return node_orb(o.get('r',80), o['kind'])
    k=o.get('kind');
    if k=='mercury': return mercury_orb(o.get('r',70),o.get('dim',False))
    if k=='moon': return moon(o.get('r',140),o.get('illum',1.0),o.get('waxing',True))
    if k=='sun': return sun(o.get('r',95),o.get('rings',True))
    if k=='orbit': return orbit(o.get('w',720),o.get('h',160),o.get('beads',5),o.get('tilt',-7),o.get('lit'))
    if k=='mars': return mars_orb(o.get('r',80),o.get('dim',False))
    if k=='asc': return asc_orb(o.get('s',230))
    if k=='venus': return venus_orb(o.get('r',80))
    if k=='jupiter': return jupiter_orb(o.get('r',95))
    if k=='north': return north(o.get('s',320),o.get('nums',False),o.get('hi',1))
    if k=='figure': return figure_orb(o.get('h',430))
    if k=='south': return south(o.get('s',320),o.get('labels',True),o.get('asc'))
    if k=='top': return top_orb(o.get('s',300))
    return ''

def scene_html(sc, s=1.0):
    """v6: the signs as rooms in a row, grahas inside them. Rooms run in sign order, left to right, so 'ahead' is to the right;
    inside a room the graha with more degrees stands further right. 'across' rooms hang from above, facing the row."""
    F=lambda px: f'{px*s:.1f}px'
    W=sc.get('w',262); Hh=sc.get('h',208)
    def room(r, flip=False, k=1.0):
        w=W*k*r.get('wide',1); h=Hh*k; rad=F(150*k)
        if r.get('spacer'): return f'<div class="spacer" style="width:{F(w)};height:1px;visibility:hidden"></div>'
        who=(f'<div class="who">{esc(r["names"])}</div>' if r.get('names') else '')+(f'<div class="rnote">{esc(r["note"])}</div>' if r.get('note') else '')
        ob=f'<div style="transform:scale({s*k*r.get("zoom",1):.3f})">{orbrow(r["orbs"], r.get("spacing"))}</div>' if r.get('orbs') else ''
        fr=(f'<div style="position:absolute;{"top" if flip else "bottom"}:{F(9)};right:{F(16)};font:italic 500 {F(25)}/1 \'Cormorant Garamond\';color:{AMBER}">in front ▸</div>' if r.get('front') else '')
        arch=f'<div class="arch" style="width:{F(w)};height:{F(h)};border-radius:{("0 0 "+rad+" "+rad) if flip else (rad+" "+rad+" 0 0")}">{ob}{fr}</div>'
        sg=f'<div class="sg" style="margin:{("0 0 "+F(12)) if flip else (F(13)+" 0 0")}">{esc(r["sign"])}</div>'
        tag=f'<div class="tag" style="margin:{(F(9)+" 0 0") if flip else ("0 0 "+F(10))}">{esc(r.get("tag",""))}</div>'
        inner=(sg+who+arch+(tag if r.get('tag') else '')) if flip else (tag+arch+sg+who)
        return f'<div class="room {r.get("state","")}">{inner}</div>'
    def reach(rooms, links, k=1.0):
        # an arc over the row, from the room a graha stands in to the room it also works from; the arrow lands on that room
        ws=[W*k*r.get('wide',1)*s for r in rooms]; xs=[]; x=0.0
        for w_ in ws: xs.append(x+w_/2); x+=w_+14*s
        tot=x-14*s; H=120*s; y0=H-5*s; o=''
        for a,b,text in links:
            x1,x2=xs[a],xs[b]; mid=(x1+x2)/2; d=-1 if x2<x1 else 1
            o+=(f'<path class="rarc" pathLength="1" d="M{x1:.1f},{y0:.1f} C{x1:.1f},{26*s:.1f} {x2:.1f},{26*s:.1f} {x2:.1f},{y0-13*s:.1f}" fill="none" stroke="{AMBER}" stroke-width="{max(2.2,2.6*s):.1f}" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="0"/>'
                f'<path class="rhead" d="M{x2-10*s:.1f},{y0-15*s:.1f} L{x2:.1f},{y0:.1f} L{x2+10*s:.1f},{y0-15*s:.1f} Z" fill="{AMBER}"/>'
                f'<circle cx="{x1:.1f}" cy="{y0:.1f}" r="{4.5*s:.1f}" fill="{AMBER}"/>'
                f'<text class="rlab" x="{mid:.1f}" y="{31*s:.1f}" text-anchor="middle" font-family="Cormorant Garamond" font-style="italic" font-weight="500" font-size="{31*s:.1f}" fill="{AMBER}">{esc(text)}</text>')
        return f'<svg class="reach" width="{tot:.0f}" height="{H:.0f}" viewBox="0 0 {tot:.0f} {H:.0f}" style="top:{41*s-H:.1f}px">{o}</svg>'
    out=''
    if sc.get('across'):
        out+=f'<div class="rooms" style="align-items:flex-start">{"".join(room(r,True,sc.get("acrossk",.82)) for r in sc["across"])}</div>'
        out+=f'<div class="conn" style="{"transform:translateX("+F(sc["connx"])+");" if sc.get("connx") else ""}"><i></i>{esc(sc.get("conn","face to face"))}<i></i></div>'
    rc=reach(sc['rooms'], sc['reach']) if sc.get('reach') else ''
    named=any(r.get('names') or r.get('note') for r in sc['rooms'])
    out+=f'<div class="rooms" style="position:relative;align-items:{"flex-start" if named else "flex-end"};{"margin-top:"+F(sc.get("reachpad",74))+";" if rc else ""}">{"".join(room(r) for r in sc["rooms"])}{rc}</div>'
    if sc.get('caption'): out+=f'<div class="who" style="margin-top:{F(14)};opacity:.72">{esc(sc["caption"])}</div>'
    return f'<div class="scene">{out}</div>'

def path_html(pt, s=1.0):
    """A graha's backward walk drawn to scale on a ruler of degrees (v7, 13 Nov).
    pt: left {sign, from}, right {sign, to} set the ruler; 'start' and 'turn' are [sign, degrees];
    labels: start, cross_back, turn, cross_fwd as [date, words]; 'kind' is the graha; 'behind' names the sign off the left edge."""
    Wd=912; Ht=470; m=34; L=pt['left']; Rg=pt['right']; span=(30-L['from'])+Rg['to']; k=(Wd-2*m)/span
    X=lambda sign,deg: m+((deg-L['from']) if sign==L['sign'] else (30-L['from']+deg))*k
    xd=X(Rg['sign'],0); xs=X(*pt['start']); xt=X(*pt['turn']); yu,yl,ym=150,262,206; yr=388
    o=[]; fam="font-family='EB Garamond'"
    # the two signs and the door between them
    o.append(f"<text x='{(m+xd)/2:.0f}' y='44' text-anchor='middle' {fam} font-weight='500' font-size='36' letter-spacing='9' fill='{GOLD}'>{esc(L['sign']).upper()}</text>")
    o.append(f"<text x='{(xd+Wd-m)/2:.0f}' y='44' text-anchor='middle' {fam} font-weight='500' font-size='36' letter-spacing='9' fill='{GOLD}'>{esc(Rg['sign']).upper()}</text>")
    o.append(f"<line x1='{xd:.1f}' y1='62' x2='{xd:.1f}' y2='{yr}' stroke='{GOLD}' stroke-opacity='.6' stroke-width='1.6' stroke-dasharray='7 7'/>")
    # ruler: a tick for every degree, a number every five
    o.append(f"<line x1='{m}' y1='{yr}' x2='{Wd-m}' y2='{yr}' stroke='{GOLD}' stroke-opacity='.7' stroke-width='1.6'/>")
    for j in range(int(span)+1):
        deg=L['from']+j; sign=L['sign'] if deg<30 else Rg['sign']; dd=deg if deg<30 else deg-30; x=m+j*k; big=(dd%5==0)
        o.append(f"<line x1='{x:.1f}' y1='{yr}' x2='{x:.1f}' y2='{yr+(18 if big else 9)}' stroke='{GOLD}' stroke-opacity='{.9 if big else .5}' stroke-width='{1.6 if big else 1.1}'/>")
        if big: o.append(f"<text x='{x:.1f}' y='{yr+50}' text-anchor='middle' {fam} font-size='29' fill='{CREAM}' fill-opacity='.8'>{dd:.0f}°</text>")
    # the walk: back along the upper line, the turn exactly at its degree, forward along the lower line
    r_=ym-yu
    o.append(f"<path class='pback' pathLength='1' d='M{xs:.1f},{yu} L{xt+r_:.1f},{yu} Q{xt:.1f},{yu} {xt:.1f},{ym}' fill='none' stroke='{AMBER}' stroke-width='3.4' stroke-linecap='round'/>")
    o.append(f"<path class='pfwd' pathLength='1' d='M{xt:.1f},{ym} Q{xt:.1f},{yl} {xt+r_:.1f},{yl} L{Wd-m-22:.1f},{yl}' fill='none' stroke='{CREAM}' stroke-opacity='.9' stroke-width='3.4' stroke-linecap='round'/>")
    o.append(f"<path class='pfm' d='M{Wd-m-24:.1f},{yl-11} L{Wd-m-4:.1f},{yl} L{Wd-m-24:.1f},{yl+11} Z' fill='{CREAM}' fill-opacity='.9'/>")
    for xa in [xs-(xs-xt-r_)*f for f in (.3,.62)]: o.append(f"<path class='pbm' data-x='{xa:.0f}' d='M{xa+9:.1f},{yu-10} L{xa-9:.1f},{yu} L{xa+9:.1f},{yu+10}' fill='none' stroke='{AMBER}' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/>")
    xf=xt+r_+(Wd-m-xt-r_)*.55; o.append(f"<path class='pfm' d='M{xf-9:.1f},{yl-10} L{xf+9:.1f},{yl} L{xf-9:.1f},{yl+10}' fill='none' stroke='{CREAM}' stroke-opacity='.9' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/>")
    dot=lambda x,y,c: f"<circle cx='{x:.1f}' cy='{y}' r='13' fill='{c}' opacity='.22'/><circle cx='{x:.1f}' cy='{y}' r='6.5' fill='{c}'/>"
    o.append(dot(xs,yu,AMBER)+dot(xd,yu,AMBER)+dot(xd,yl,CREAM))
    def lab(x,y,anchor,date,words,cls):
        return (f"<g class='plab {cls}'><text x='{x:.1f}' y='{y}' text-anchor='{anchor}' font-family='Cormorant Garamond' font-weight='600' font-size='40' fill='{CREAM}'>{esc(date)}</text>"
                f"<text x='{x:.1f}' y='{y+33}' text-anchor='{anchor}' font-family='Cormorant Garamond' font-style='italic' font-weight='500' font-size='31' fill='{AMBER}'>{esc(words)}</text></g>")
    lb=pt['labels']
    o.append(lab(min(xs,Wd-m-96),yu-58,'middle',*lb['start'],'l1'))
    o.append(lab(xd+4,yu-58,'middle',*lb['cross_back'],'l2'))
    o.append(lab(xt-52,ym-10,'end',*lb['turn'],'l3'))
    o.append(lab(xd+26,yl+50,'start',*lb['cross_fwd'],'l4'))
    if pt.get('behind'): o.append(f"<text x='{m}' y='{yl+62}' text-anchor='start' font-family='Cormorant Garamond' font-style='italic' font-weight='500' font-size='29' fill='{CREAM}' fill-opacity='.72'>◂ {esc(pt['behind'])}</text>")
    R_=pt.get('r',34)
    ob=f'<div class="porb" data-x0="{xs:.1f}" data-xt="{xt:.1f}" data-xd="{xd:.1f}" data-yu="{yu}" data-ym="{ym}" data-yl="{yl}" data-r="{r_}" style="position:absolute;left:{xt:.1f}px;top:{ym}px;width:0;height:0"><div style="position:absolute;left:0;top:0;transform:translate(-50%,-50%)">{orb({"kind":pt["kind"],"r":R_})}</div></div>'
    return (f'<div class="pathd" style="position:relative;width:{Wd}px;height:{Ht}px;zoom:{s:.3f};margin:{pt.get("mt",6)}px auto {pt.get("mb",0)}px;text-align:left">'
            f'<svg width="{Wd}" height="{Ht}" viewBox="0 0 {Wd} {Ht}" style="position:absolute;inset:0;overflow:visible">{"".join(o)}</svg>{ob}</div>')

def timeline_html(tl, s=1.0):
    """Who walks backward, and when: one bar per graha on a calendar drawn to scale, with a line for today (v8, 13 Nov).
    tl: from, to (ISO dates set the calendar); today [ISO date, label]; rows [{kind, who, name, from, to, dates}].
    The part of a bar after today is lighter (still to come); a cream dot marks where a graha turns forward."""
    import datetime as _dt
    D=lambda d: _dt.date.fromisoformat(d)
    rows=tl['rows']; n_=len(rows); Wd=912; gut=tl.get('gutter',338); x0=gut; x1=Wd-22
    a=D(tl['from']); b=D(tl['to']); k=(x1-x0)/(b-a).days; X=lambda d: x0+(D(d)-a).days*k
    RH=tl.get('rowh',140); top=96; yb_=top+RH*n_; Ht=yb_+70
    fam="font-family='EB Garamond'"; o=[]; H=[]
    o.append(f"<line x1='{x0}' y1='{yb_+4}' x2='{x1}' y2='{yb_+4}' stroke='{GOLD}' stroke-opacity='.55' stroke-width='1.4'/>")
    d=_dt.date(a.year,a.month,1)
    while d<=b:
        nd=(d.replace(day=28)+_dt.timedelta(days=4)).replace(day=1)
        xs=max(x0,x0+(d-a).days*k); xe=min(x1,x0+(nd-a).days*k)
        if d>=a: o.append(f"<line x1='{xs:.1f}' y1='{top-18}' x2='{xs:.1f}' y2='{yb_+14}' stroke='{GOLD}' stroke-opacity='.16' stroke-width='1.2'/>")
        if xe-xs>62: o.append(f"<text x='{(xs+xe)/2:.1f}' y='{yb_+50}' text-anchor='middle' {fam} font-weight='500' font-size='30' letter-spacing='3' fill='{CREAM}' fill-opacity='.72'>{d.strftime('%b').upper()}</text>")
        d=nd
    for i in range(1,n_): o.append(f"<line x1='0' y1='{top+i*RH}' x2='{Wd}' y2='{top+i*RH}' stroke='{GOLD}' stroke-opacity='.14' stroke-width='1'/>")
    td,tlab=tl['today']; xt=X(td)
    o.append(f"<line x1='{xt:.1f}' y1='{top-26}' x2='{xt:.1f}' y2='{yb_+14}' stroke='{CREAM}' stroke-opacity='.85' stroke-width='2' stroke-dasharray='6 7'/>")
    o.append(f"<text class='tlt' x='{xt:.1f}' y='{top-40}' text-anchor='middle' font-family='Cormorant Garamond' font-weight='600' font-size='40' fill='{CREAM}'>{esc(tlab)}</text>")
    for i,r in enumerate(rows):
        y=top+i*RH+RH*.38; xa=X(r['from']); xb=X(r['to']); xn=min(xb,xt)
        o.append(f"<rect class='tbar' x='{xa:.1f}' y='{y-10:.1f}' width='{max(0,xn-xa):.1f}' height='20' rx='10' fill='{AMBER}'/>")
        if xb>xt: o.append(f"<rect x='{xt:.1f}' y='{y-10:.1f}' width='{xb-xt:.1f}' height='20' rx='10' fill='{AMBER}' fill-opacity='.38'/><rect x='{xt:.1f}' y='{y-10:.1f}' width='{min(10,xb-xt):.1f}' height='20' fill='{AMBER}'/>")
        o.append(f"<circle cx='{xa:.1f}' cy='{y:.1f}' r='7' fill='{AMBER}'/><circle cx='{xb:.1f}' cy='{y:.1f}' r='8.5' fill='{CREAM}'/>")
        txt=r.get('dates',''); w=len(txt)*15.2
        # the dates sit under the bar and never cross today's line: a bar that ends by today has them end just before it
        if xb<=xt+1: o.append(f"<text x='{xt-14:.1f}' y='{y+56:.1f}' text-anchor='end' {fam} font-size='34' fill='{CREAM}' fill-opacity='.88'>{esc(txt)}</text>")
        elif xa+w<=Wd: o.append(f"<text x='{xa:.1f}' y='{y+56:.1f}' text-anchor='start' {fam} font-size='34' fill='{CREAM}' fill-opacity='.88'>{esc(txt)}</text>")
        else: o.append(f"<text x='{xb:.1f}' y='{y+56:.1f}' text-anchor='end' {fam} font-size='34' fill='{CREAM}' fill-opacity='.88'>{esc(txt)}</text>")
        o.append(f"<text x='86' y='{y-2:.1f}' text-anchor='start' font-family='Cormorant Garamond' font-weight='500' font-size='45' fill='{CREAM}'>{esc(r['who'])}</text>")
        o.append(f"<text x='86' y='{y+34:.1f}' text-anchor='start' font-family='Cormorant Garamond' font-style='italic' font-weight='500' font-size='33' fill='{GOLD}'>{esc(r['name'])}</text>")
        H.append(f'<div style="position:absolute;left:36px;top:{y:.1f}px;transform:translate(-50%,-50%)">{orb({"kind":r["kind"],"r":r.get("r",28)})}</div>')
    return (f'<div class="tline" style="position:relative;width:{Wd}px;height:{Ht}px;zoom:{s:.3f};margin:{tl.get("mt",14)}px auto {tl.get("mb",6)}px;text-align:left">'
            f'<svg width="{Wd}" height="{Ht}" viewBox="0 0 {Wd} {Ht}" style="position:absolute;inset:0;overflow:visible">{"".join(o)}</svg>{"".join(H)}</div>')

def ruler_html(ru, s=1.0):
    """Grahas inside one sign, placed to scale on its degrees, with the fast one's road ahead (v8, 13 Nov).
    ru: sign; from, to (degrees shown); ticks [[deg, label]]; items [{kind, who, deg, d}];
    road {from_deg, stops [[deg, when, words]], words} draws the fast graha's dashed road with dated stops."""
    Wd=912; m=40; x0,x1=m,Wd-m; a,b=ru['from'],ru['to']; k=(x1-x0)/(b-a); X=lambda d: x0+(d-a)*k
    yo=170; yr=ru.get('yr',430); Ht=yr+60; o=[]; H=[]; fam="font-family='EB Garamond'"
    o.append(f"<text x='{x0}' y='40' text-anchor='start' {fam} font-weight='500' font-size='34' letter-spacing='9' fill='{GOLD}'>{esc(ru['sign']).upper()}</text>")
    o.append(f"<line x1='{x0}' y1='{yr}' x2='{x1}' y2='{yr}' stroke='{GOLD}' stroke-opacity='.7' stroke-width='1.6'/>")
    st=ru.get('minor',1/6); j=0
    while a+j*st<=b+1e-9:
        x=X(a+j*st); o.append(f"<line x1='{x:.1f}' y1='{yr}' x2='{x:.1f}' y2='{yr+9}' stroke='{GOLD}' stroke-opacity='.5' stroke-width='1.1'/>"); j+=1
    for d_,lab in ru.get('ticks',[]):
        x=X(d_); o.append(f"<line x1='{x:.1f}' y1='{yr}' x2='{x:.1f}' y2='{yr+18}' stroke='{GOLD}' stroke-opacity='.9' stroke-width='1.6'/>")
        o.append(f"<text x='{x:.1f}' y='{yr+52}' text-anchor='middle' {fam} font-size='30' fill='{CREAM}' fill-opacity='.8'>{esc(lab)}</text>")
    for it in ru['items']:
        x=X(it['deg']); r=it.get('r',34)
        o.append(f"<line x1='{x:.1f}' y1='{yo+r+40}' x2='{x:.1f}' y2='{yr-4}' stroke='{GOLD}' stroke-opacity='.3' stroke-width='1.2' stroke-dasharray='3 6'/>")
        o.append(f"<text x='{x:.1f}' y='{yo-r-22}' text-anchor='middle' font-family='Cormorant Garamond' font-weight='500' font-size='38' fill='{CREAM}'>{esc(it['who'])}</text>")
        o.append(f"<text x='{x:.1f}' y='{yo+r+34}' text-anchor='middle' font-family='Cormorant Garamond' font-style='italic' font-weight='500' font-size='31' fill='{GOLD}'>{esc(it['d'])}</text>")
        H.append(f'<div class="rorb" data-x="{x:.1f}" style="position:absolute;left:{x:.1f}px;top:{yo}px;transform:translate(-50%,-50%)">{orb({"kind":it["kind"],"r":r})}</div>')
    rd=ru.get('road')
    if rd:
        yp=yo+r+90; xs=X(rd['from_deg'])+8; xe=min(x1+6,X(max(st_[0] for st_ in rd['stops']))+60)
        o.append(f"<path class='rroad' d='M{xs:.1f},{yp} L{xe-14:.1f},{yp}' fill='none' stroke='{AMBER}' stroke-width='3' stroke-dasharray='10 9' stroke-linecap='round'/>")
        o.append(f"<path d='M{xe-22:.1f},{yp-10} L{xe:.1f},{yp} L{xe-22:.1f},{yp+10} Z' fill='{AMBER}'/>")
        for d_,when,words in rd['stops']:
            x=X(d_); o.append(f"<circle cx='{x:.1f}' cy='{yp}' r='12' fill='{AMBER}' opacity='.25'/><circle cx='{x:.1f}' cy='{yp}' r='6.5' fill='{AMBER}'/>")
            o.append(f"<text x='{x:.1f}' y='{yp+44}' text-anchor='middle' font-family='Cormorant Garamond' font-weight='600' font-size='36' fill='{CREAM}'>{esc(when)}</text>")
            o.append(f"<text x='{x:.1f}' y='{yp+76}' text-anchor='middle' font-family='Cormorant Garamond' font-style='italic' font-weight='500' font-size='29' fill='{AMBER}'>{esc(words)}</text>")
        if rd.get('words'): o.append(f"<text x='{xs-6:.1f}' y='{yp+44}' text-anchor='start' font-family='Cormorant Garamond' font-style='italic' font-weight='500' font-size='29' fill='{AMBER}'>{esc(rd['words'])}</text>")
    return (f'<div class="rulerd" style="position:relative;width:{Wd}px;height:{Ht}px;zoom:{s:.3f};margin:{ru.get("mt",10)}px auto {ru.get("mb",4)}px;text-align:left">'
            f'<svg width="{Wd}" height="{Ht}" viewBox="0 0 {Wd} {Ht}" style="position:absolute;inset:0;overflow:visible">{"".join(o)}</svg>{"".join(H)}</div>')

def slide_html(sp, s=1.0):
    F=lambda px: f'{px*s:.1f}px'
    T=lambda px: F(px*TXT)
    t=sp['type']; H=[]
    if sp.get('orb'): H.append(f'<div style="margin-bottom:24px">{orb(sp["orb"])}</div>')
    # a row of grahas on one slide (the characters on stage); a negative orbgap lets them crowd together
    if sp.get('scene'): H.append(scene_html(sp['scene'],s))
    if sp.get('path') and sp.get('pathpos','top')=='top': H.append(path_html(sp['path'],s))
    if sp.get('orbs'):
        row=orbrow(sp["orbs"], sp.get("orbspacing"), sp.get("orbgap",18))
        if sp.get('mirror'):
            # as above, so below: the grahas over a thin horizon, with a faint reflection fading downward
            H.append(f'<div style="margin-bottom:0">{row}</div><div style="width:{F(560)};height:1px;background:rgba(217,165,122,.55);margin:{F(4)} auto {F(2)}"></div>'
                     f'<div style="transform:scaleY(-1);opacity:.30;filter:blur(1.2px);-webkit-mask-image:linear-gradient(to top,#000 0%,rgba(0,0,0,0) 80%);mask-image:linear-gradient(to top,#000 0%,rgba(0,0,0,0) 80%);margin-bottom:{F(22)}">{row}</div>')
        else:
            H.append(f'<div style="margin-bottom:22px">{row}</div>')
    bs=f'font-size:{T(sp["bodysize"])};' if sp.get('bodysize') else ''
    if sp.get('label'): H.append(f'<div class="lab" style="margin-bottom:22px;{"font-size:"+T(sp["labelsize"]) if sp.get("labelsize") else ""}">{esc(sp["label"])}</div>')
    if t in ('cover','cta','text','list','grid','quote','quotes','steps','sentence','sky','rows','stack','icons','svg','compare','cast','bodymap','nsteps','narrow'):
        if sp.get('title'):
            cls=sp.get('titleclass') or {'cover':'h1','cta':'h1'}.get(t,'h2' if len(clean(sp['title']))<26 else 'h3')
            ts=f' style="font-size:{F(sp["titlesize"])}"' if sp.get('titlesize') else ''
            H.append(f'<div class="t {cls}"{ts}>{rich(sp["title"])}</div>')
        if sp.get('subtitle'): H.append(f'<div class="ti sub" style="margin-top:22px;{"font-size:"+F(sp["subsize"])+";" if sp.get("subsize") else ""}">{rich(sp["subtitle"]).replace(chr(60)+"span class="+chr(34)+"ti"+chr(34)+">",chr(60)+"span style="+chr(34)+"color:"+CREAM+chr(34)+">")}</div>')
    if sp.get('lead'): H.append(f'<div class="p" style="margin-top:{F(20)};font-size:{T(sp.get("leadsize",36))};line-height:1.3">{rich(sp["lead"])}</div>')
    if sp.get('contents'):
        H.append('<div class="contents">'+''.join(f'<div><b style="border-color:{PART_COLORS[k%len(PART_COLORS)]};color:{PART_COLORS[k%len(PART_COLORS)]}">{k+1}</b>{esc(c)}</div>' for k,c in enumerate(sp['contents']))+'</div>')
    if sp.get('path') and sp.get('pathpos')=='mid': H.append(path_html(sp['path'],s))
    if sp.get('timeline'): H.append(timeline_html(sp['timeline'],s))
    if sp.get('ruler'): H.append(ruler_html(sp['ruler'],s))
    if t=='nsteps':
        # numbered steps, left aligned: a small tag line, a head and a line under it; "n" overrides the number (e.g. the rule's own number)
        H.append(f'<div style="width:100%;margin-top:{F(sp.get("stepsmt",22))}">'+''.join(
            f'<div class="nstep"><b>{esc(str(st.get("n",k+1)))}</b><div style="flex:1;min-width:0">'
            +(f'<div class="tg">{esc(st["tag"])}</div>' if st.get('tag') else '')
            +f'<div class="hd" style="{"font-size:"+F(sp["headsize"])+";" if sp.get("headsize") else ""}">{rich(st["head"])}</div>'
            +(f'<div class="ln" style="{bs}">{rich(st["line"])}</div>' if st.get('line') else '')+'</div></div>' for k,st in enumerate(sp['steps']))+'</div>')
    if t=='narrow':
        # how the timing narrows: each line shorter than the one above
        n_=len(sp['items'])
        H.append('<div class="narrow">'+''.join(f'<div class="it"><div class="bar" style="width:{(86-k*(66/max(1,n_-1))):.0f}%"></div><div class="hd">{rich(a)}</div><div class="ln" style="{bs}">{rich(b)}</div></div>' for k,(a,b) in enumerate(sp['items']))+'</div>')
    if t=='quote':
        H.append('<div class="rule"></div>')
        qs=f'font-size:{F(sp["quotesize"])};line-height:1.12;' if sp.get('quotesize') else ''
        H.append(f'<div class="ti h3" style="color:{CREAM};{qs}">“{esc(sp["quote"])}”</div>')
        if sp.get('source'): H.append(f'<div class="src" style="margin-top:24px;font-size:{F(27)}">{esc(sp["source"])}</div>')
    if t=='quotes':
        for i,(lab,qt,src) in enumerate(sp['items']):
            if i: H.append('<div class="rule" style="margin:8px auto"></div>')
            H.append(f'<div style="padding:24px 0"><div class="lab">{esc(lab)}</div><div class="ti" style="font-size:{F(58)};line-height:1.15;margin-top:16px;color:{CREAM}">“{esc(qt)}”</div><div class="src" style="margin-top:14px">{esc(src)}</div></div>')
    if t=='list':
        items=sp['items']; half=(len(items)+1)//2 if sp.get('columns',2)==2 else len(items)
        cols=[items[:half],items[half:]] if sp.get('columns',2)==2 else [items]
        body=''.join('<div>'+''.join(f'<div class="row"><span class="t" style="font-size:{F(52)}">{esc(a)}</span><span class="pi" style="text-align:right;font-size:{F(38)}">{esc(b)}</span></div>' for a,b in col)+'</div>' for col in cols)
        H.append(f'<div class="{"grid2" if len(cols)==2 else ""}" style="margin-top:34px;width:100%">{body}</div>')
    if t=='bodymap': H.append(bodymap(sp['items'], s, sp.get('rowh',62)))
    if t=='rows':
        # a third value set to true lights that row in amber; roworbs puts a small graha in front of each name
        ro=sp.get('roworbs') or []
        def _ro(k):
            if k>=len(ro) or not ro[k]: return ''
            return f'<span class="ro" style="position:relative;flex:0 0 {F(74)};width:{F(74)};height:{F(60)};margin-right:{F(20)}"><span style="position:absolute;left:50%;top:50%;display:block;transform:translate(-50%,-50%) scale({s:.3f})">{orb(ro[k])}</span></span>'
        H.append('<div style="margin-top:30px;width:100%">'+''.join(f'<div class="row" style="align-items:center"><span style="display:flex;align-items:center">{_ro(k)}<span class="t" style="font-size:{F(sp.get("namesize",52))};white-space:nowrap">{esc(it[0])}</span></span><span class="p" style="text-align:right;font-size:{T(sp.get("bodysize",34))};{"color:"+AMBER+";" if len(it)>2 and it[2] else ""}">{esc(it[1])}</span></div>' for k,it in enumerate(sp['items']))+'</div>')
    if t=='grid':
        # a 4th value set to true lights that cell's middle line in amber (e.g. Jupiter's best houses)
        H.append('<div class="grid2" style="margin-top:22px">'+''.join(f'<div style="padding:{F(sp.get("cellpad",20))} 0"><div class="lab">{esc(cell[0])}</div><div class="t" style="font-size:{F(sp.get("cellsize",50))};line-height:1.1;margin-top:12px;{"color:"+AMBER+";" if len(cell)>3 and cell[3] else ""}">{esc(cell[1])}</div><div class="pi" style="margin-top:4px;{bs}">{esc(cell[2])}</div></div>' for cell in sp['cells'])+'</div>')
    if t=='steps':
        roman=['i','ii','iii','iv','v','vi']
        for i,(a,b) in enumerate(sp['steps']):
            H.append(f'<div style="padding:20px 0"><div class="ti" style="font-size:{F(60)};line-height:1">{roman[i]}</div><div class="t" style="font-size:{F(62)};line-height:1.05;margin-top:4px">{esc(a)}</div><div class="p" style="margin-top:6px">{esc(b)}</div></div>')
    if t=='stack':
        H.append('<div class="rule"></div>')
        for a,b in sp['items']:
            H.append(f'<div style="padding:18px 0"><div class="t" style="font-size:{F(64)};line-height:1.05">{esc(a)}</div><div class="p" style="margin-top:8px;{bs}">{esc(b)}</div></div>')
    if t=='icons':
        H.append('<div style="margin-top:34px;display:inline-block;text-align:left">'+''.join(f'<div style="display:flex;align-items:center;gap:30px;padding:16px 0">{icon(k,80)}<div><div class="t" style="font-size:{F(64)};line-height:1">{esc(a)}</div><div class="p" style="margin-top:6px;{bs}">{esc(b)}</div></div></div>' for k,a,b in sp['items'])+'</div>')
    if t=='svg':
        svg=open(os.path.join(REPO,sp['svgfile'])).read(); w=sp.get('svgwidth',760)
        vb=re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"',svg); hgt=round(w*float(vb.group(4))/float(vb.group(3))) if vb else w
        svg=re.sub(r'width="\d+" height="\d+"',f'width="{w}" height="{hgt}"',svg,count=1)
        H.append(f'<div style="margin:{sp.get("svgmargin","8px auto 0")};line-height:0">{svg}</div>')
        if sp.get('footnote'): H.append(f'<div class="ti" style="font-size:{F(sp.get("footsize",44))};line-height:1.2;margin-top:4px">{esc(sp["footnote"])}</div>')
    if t=='compare':
        cells=''
        for k,col in enumerate(sp['columns']):
            ic=scene_html(col['scene'],s*col.get('scenek',.92)).replace('class="scene"','class="scene" style="margin-bottom:0"') if col.get('scene') else (orb(col['orb']) if col.get('orb') else '')
            lines=''.join(f'<div class="p" style="margin-top:6px;{bs}">{esc(l)}</div>' for l in col['lines'])
            cl=(f'font-size:{T(sp["collabsize"])};' if sp.get('collabsize') else '')+(f'letter-spacing:{sp["collabls"]};' if sp.get('collabls') else '')
            cells+=f'<div style="padding:10px 8px;{"border-left:1px solid rgba(217,165,122,.3);" if k else ""}"><div style="{"margin-bottom:"+F(30)+";" if col.get("scene") else "height:"+F(sp.get("orbbox",150))+";"}display:flex;align-items:center;justify-content:center">{ic}</div><div class="lab" style="margin-top:8px;{cl}">{esc(col.get("label",""))}</div><div class="t" style="font-size:{F(sp.get("headsize",54))};line-height:1.05;margin-top:10px">{esc(col["head"])}</div><div style="margin-top:12px">{lines}</div></div>'
        n_=len(sp['columns'])
        H.append(f'<div style="display:grid;grid-template-columns:repeat({n_},1fr);column-gap:0;width:100%;margin-top:30px">{cells}</div>')
    if t=='cast':
        # the characters on stage: grahas on the left, who they are and what they're doing on the right
        rows=''
        for it in sp['items']:
            ob=orbrow(it.get('orbs',[]), it.get('spacing',sp.get('castspacing',70)))
            ls=f'font-size:{T(sp["castlabsize"])};' if sp.get('castlabsize') else ''
            rows+=(f'<div style="display:flex;align-items:center;gap:{F(26)};width:100%;text-align:left;padding:{F(16)} 0;{"border-top:1px solid rgba(217,165,122,.2);" if rows else ""}">'
                   f'<div style="flex:0 0 {F(sp.get("castorbw",210))};min-width:0;height:{F(sp.get("castorbh",118))};display:flex;align-items:center;justify-content:center">{ob}</div>'
                   f'<div style="flex:1;min-width:0"><div class="lab" style="{ls}">{esc(it.get("label",""))}</div>'
                   f'<div class="t" style="font-size:{F(sp.get("headsize",50))};line-height:1.05;margin-top:{F(8)}">{esc(it["head"])}</div>'
                   f'<div class="p" style="margin-top:{F(6)};line-height:1.3;{bs}">{esc(it["line"])}</div></div></div>')
        H.append(f'<div style="width:100%;margin-top:{F(24)}">{rows}</div>')
    if t=='sentence':
        H.append('<div class="rule"></div>')
        H.append(f'<div class="t h3">{esc(sp["example"])}</div>')
        H.append('<div style="margin-top:28px">'+''.join(f'<div class="p" style="margin-top:10px;{bs}"><span class="lab" style="margin-right:20px">{esc(a)}</span>{esc(b)}</div>' for a,b in sp['rows'])+'</div>')
        if sp.get('conclusion'): H.append(f'<div class="ti sub" style="margin-top:36px">{esc(sp["conclusion"])}</div>')
    if t=='sky':
        H.append('<div class="grid2" style="margin-top:26px;border-top:1px solid rgba(217,165,122,.28);border-bottom:1px solid rgba(217,165,122,.28);padding:6px 0">'+''.join(f'<div style="padding:12px 0"><div class="lab">{esc(a)}</div><div class="p" style="margin-top:10px;font-size:{F(44)};line-height:1.15">{esc(b)}</div></div>' for a,b in sp['cells'])+'</div>')
        H.append(f'<div class="grid2" style="grid-template-columns:1fr 1fr;margin-top:22px"><div><span class="lab">Good for</span><div class="p" style="margin-top:8px;font-size:{F(40)};line-height:1.2">{esc(sp["good"])}</div></div><div><span class="lab">Go slow on</span><div class="p" style="margin-top:8px;font-size:{F(40)};line-height:1.2">{esc(sp["slow"])}</div></div></div>')
    if sp.get('body'):
        bg=sp.get('bodygap',0)
        H.append('<div style="margin-top:30px">'+''.join(f'<div class="p" style="{bs}{"margin-top:"+F(bg)+";" if (k and bg) else ""}">{rich(l)}</div>' for k,l in enumerate(sp['body']))+'</div>')
    if sp.get('note'): H.append(f'<div class="src" style="margin-top:28px;letter-spacing:.1em">{esc(sp["note"])}</div>')
    if t=='cta':
        H.append('<div class="rule"></div>'+''.join(f'<div class="p" style="margin-top:6px;{bs}">{esc(l)}</div>' for l in sp.get('lines',[])))
        if sp.get('next'): H.append(f'<div class="src" style="margin-top:28px">{esc(sp["next"])}</div>')
    if sp.get('closing'): H.append(f'<div class="ti sub" style="margin-top:34px;{"font-size:"+F(sp["closingsize"])+";" if sp.get("closingsize") else ""}">{esc(sp["closing"])}</div>')
    # a small second link under the closing line (the newsletter, after asksutram.com)
    if sp.get('after'): H.append(f'<div class="src" style="margin-top:22px;letter-spacing:.12em">{esc(sp["after"])}</div>')
    return ''.join(H)

def _bead(x,y,kind,uidp):
    """A background planet. Wrapped as a glint so it is hidden when it would sit on text (same check as the stars)."""
    return f'<g class="gl" data-x="{x:.0f}" data-y="{y:.0f}">{_bead_raw(x,y,kind,uidp)}</g>'
def _bead_raw(x,y,kind,uidp):
    """Small background planets: pearl moon, banded Jupiter, pale Venus, red Mars."""
    g=uid(uidp)
    if kind=='moon':
        return f'<defs><radialGradient id="{g}" cx="38%" cy="34%" r="75%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".6" stop-color="#D8D2D0"/><stop offset="1" stop-color="#8E888C"/></radialGradient></defs><circle cx="{x:.1f}" cy="{y:.1f}" r="22" fill="#FFF4E6" opacity=".10"/><circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="url(#{g})"/>'
    if kind=='jupiter':
        return (f'<defs><radialGradient id="{g}" cx="38%" cy="32%" r="78%"><stop offset="0" stop-color="#F4E3C6"/><stop offset=".55" stop-color="#D5B285"/><stop offset="1" stop-color="#7A5536"/></radialGradient>'
                f'<clipPath id="{g}c"><circle cx="{x:.1f}" cy="{y:.1f}" r="15"/></clipPath></defs><circle cx="{x:.1f}" cy="{y:.1f}" r="30" fill="#E0B98A" opacity=".08"/>'
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="url(#{g})"/><g clip-path="url(#{g}c)" opacity=".45"><rect x="{x-15:.1f}" y="{y-6:.1f}" width="30" height="3" fill="#9C6440"/><rect x="{x-15:.1f}" y="{y+2:.1f}" width="30" height="4" fill="#A8744F"/></g>')
    if kind=='mars':
        return f'<defs><radialGradient id="{g}" cx="38%" cy="34%" r="75%"><stop offset="0" stop-color="#F3B08A"/><stop offset=".6" stop-color="#C2643A"/><stop offset="1" stop-color="#6E2E17"/></radialGradient></defs><circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="url(#{g})"/>'
    if kind=='mercury':
        return f'<defs><radialGradient id="{g}" cx="38%" cy="34%" r="75%"><stop offset="0" stop-color="#EEF2E6"/><stop offset=".6" stop-color="#A9BA9E"/><stop offset="1" stop-color="#4E5E4C"/></radialGradient></defs><circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#DCE8D0" opacity=".08"/><circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="url(#{g})"/>'
    return f'<defs><radialGradient id="{g}" cx="38%" cy="34%" r="75%"><stop offset="0" stop-color="#FFFBF2"/><stop offset=".6" stop-color="#EBD3A4"/><stop offset="1" stop-color="#A88152"/></radialGradient></defs><circle cx="{x:.1f}" cy="{y:.1f}" r="16" fill="#F3DDB0" opacity=".10"/><circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="url(#{g})"/>'

def _stars(rr, n=46, tt=0.0):
    """v6: three depths of stars. Fine dust, small stars, and a few bright ones with a thin cross of light.
    tt (0..1) is the place in the motion loop: stars twinkle and come back to where they started."""
    o=[]; tw=lambda base,amp,k,ph: max(0.02, base*(1+amp*math.sin(2*math.pi*(k*tt+ph))))
    for _ in range(n*2):
        x=rr.uniform(0,1080); y=rr.uniform(0,1350)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr.choice([.45,.55,.7])}" fill="#FFF1D6" opacity="{tw(rr.uniform(.05,.20),.5,rr.choice([1,2]),rr.random()):.3f}"/>')
    for _ in range(n):
        x=rr.uniform(0,1080); y=rr.uniform(0,1350); rad=rr.choice([.7,.9,1.1,1.3])
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="#FFF1D6" opacity="{tw(rr.uniform(.10,.36),.6,rr.choice([1,2,3]),rr.random()):.3f}"/>')
    for _ in range(5 if n else 0):
        x=rr.choice([rr.uniform(70,330),rr.uniform(750,1010)]); y=rr.choice([rr.uniform(150,340),rr.uniform(960,1120)]); L=rr.uniform(9,17)
        k=tw(1,.45,rr.choice([1,2]),rr.random()); L*=.75+.25*k
        o.append(f'<g class="gl" data-x="{x:.0f}" data-y="{y:.0f}" opacity="{min(1,k):.3f}"><circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#FFF1D6" opacity=".07"/>'
                 f'<path d="M{x-L:.1f},{y:.1f} H{x+L:.1f} M{x:.1f},{y-L:.1f} V{y+L:.1f}" stroke="#FFF1D6" stroke-opacity=".34" stroke-width=".8" stroke-linecap="round"/>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="#FFF7E6" opacity=".8"/></g>')
    return o

def _phase(x,y,R,illum,waxing=True,op=.9):
    """A small Moon in a given phase (illum 0..1)."""
    k=1-2*illum; rx=abs(k)*R; g=uid('ph')
    base=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R}" fill="#D8D2D0" opacity="{op}"/>'
    if illum>0.98: return base
    if waxing: d=f'M{x:.1f},{y-R:.1f} A{R},{R} 0 0 0 {x:.1f},{y+R:.1f} A{rx:.1f},{R} 0 0 {1 if illum>0.5 else 0} {x:.1f},{y-R:.1f} Z'
    else:      d=f'M{x:.1f},{y-R:.1f} A{R},{R} 0 0 1 {x:.1f},{y+R:.1f} A{rx:.1f},{R} 0 0 {0 if illum>0.5 else 1} {x:.1f},{y-R:.1f} Z'
    return base+f'<path d="{d}" fill="#0B0806" opacity=".92"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{R}" fill="none" stroke="#D8D2D0" stroke-opacity=".35" stroke-width="1"/>'

def _crescent(x,y,R,op=.5):
    m=uid('cm'); g=uid('cg')
    return (f'<defs><mask id="{m}"><circle cx="{x}" cy="{y}" r="{R}" fill="#fff"/><circle cx="{x+R*0.42:.1f}" cy="{y-R*0.12:.1f}" r="{R*0.96:.1f}" fill="#000"/></mask>'
            f'<radialGradient id="{g}" cx="30%" cy="45%" r="80%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".7" stop-color="#DCD6D3"/><stop offset="1" stop-color="#9C969A"/></radialGradient></defs>'
            f'<circle cx="{x}" cy="{y}" r="{R*1.5:.1f}" fill="#FFF4E6" opacity=".05"/><circle cx="{x}" cy="{y}" r="{R}" fill="url(#{g})" mask="url(#{m})" opacity="{op}"/>')

THEMES=['solar','lunar','zodiac','jupiter','thread']
PHASES=[(.15,True),(.4,True),(.7,True),(1.0,True),(.7,False),(.4,False),(.15,False)]
def phase_index(illum, waxing):
    """Which of the seven phases on the lunar strip is nearest to the real Moon."""
    return min(range(7), key=lambda k: abs(PHASES[k][0]-illum)+(0 if (PHASES[k][1]==waxing or k==3) else 9))
def decor(i, seed, dense=False, theme='solar', hi_phase=None, tt=0.0):
    """Quiet moving sky behind every slide. Five themes rotate across posts:
    solar (Sun at the top right, Venus and Mars, Jupiter and the Moon at the bottom left),
    lunar (the Moon's phases down the left edge, a crescent at the top right),
    zodiac (a slowly turning zodiac wheel at the top left, Saturn at the bottom right),
    jupiter (Jupiter and its four moons at the bottom left, a crescent at the top right),
    thread (Sutram's thread with five pearls sweeping through two corners).
    Planets and pearls move a few degrees on each slide, so they seem to turn as you swipe."""
    r=random.Random(seed*131+7); rr=random.Random(seed*977+i*31)
    o=_stars(rr, 0 if dense else 46, tt)
    sw=math.sin(2*math.pi*tt); br=(1-math.cos(4*math.pi*tt))/2   # sway (-1..1) and breath (0..1, twice a loop); both 0 at the start
    if theme=='solar':
        sx,sy=1110,-34
        o.append(f'<circle cx="{sx}" cy="{sy}" r="{120+16*br:.1f}" fill="#EF7A3C" opacity="{.07+.04*br:.3f}"/><circle cx="{sx}" cy="{sy}" r="{74+8*br:.1f}" fill="#EF7A3C" opacity="{.10+.05*br:.3f}"/><circle cx="{sx}" cy="{sy}" r="44" fill="#F08A4C" opacity="{.30+.10*br:.3f}"/>')
        for R,kind,a0,step in [(112,'mercury',124,4),(190,'venus',152,-3.5),(318,'mars',108,-1.6)]:
            o.append(f'<circle cx="{sx}" cy="{sy}" r="{R}" fill="none" stroke="{GOLD}" stroke-opacity=".15" stroke-width="1.2"/>')
            a=math.radians(a0+r.uniform(-3,3)+(i-1)*step+sw*step*.8); o.append(_bead(sx+R*math.cos(a), sy+R*math.sin(a), kind, 'db'))
        cx,cy=-90,1460
        for R,kind,a0,step in [(330,'moon',-60,4.5),(520,'jupiter',-40,3.2)]:
            o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{R}" ry="{R*0.86:.0f}" fill="none" stroke="{GOLD}" stroke-opacity=".14" stroke-width="1.2"/>')
            a=math.radians(a0+r.uniform(0,4)+(i-1)*step+sw*step*.5); o.append(_bead(cx+R*math.cos(a), cy+R*0.86*math.sin(a), kind, 'db'))
    elif theme=='lunar':
        # phases down the left edge; the brightest one moves down as you swipe
        n=7
        for k in range(n):
            y=360+k*92; ill,wax=PHASES[k]
            hi=(k==hi_phase) if hi_phase is not None else (k==((i-1)%n))
            if hi: o.append(f'<circle cx="46" cy="{y}" r="{22+7*br:.1f}" fill="#FFF4E6" opacity="{.10+.08*br:.3f}"/>')
            o.append(_phase(46,y,10 if hi else 8,ill,wax,.95 if hi else .55))
        o.append(f'<line x1="46" y1="330" x2="46" y2="{360+6*92+30}" stroke="{GOLD}" stroke-opacity=".12" stroke-width="1"/>')
        # a large faint crescent peeking in at the top right
        o.append(_crescent(1000,92,70,.55))
    elif theme=='zodiac':
        cx,cy,R=-110,-110,430; rot=(i-1)*4+r.uniform(0,30)+1.6*sw
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{GOLD}" stroke-opacity=".26" stroke-width="1.3"/><circle cx="{cx}" cy="{cy}" r="{R-46}" fill="none" stroke="{GOLD}" stroke-opacity=".16" stroke-width="1"/>')
        ab=['ARI','TAU','GEM','CAN','LEO','VIR','LIB','SCO','SAG','CAP','AQU','PIS']
        for k in range(12):
            a=math.radians(k*30+rot); x1,y1=cx+R*math.cos(a),cy+R*math.sin(a); x2,y2=cx+(R-46)*math.cos(a),cy+(R-46)*math.sin(a)
            o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" stroke-opacity=".28" stroke-width="1.2"/>')
            am=math.radians(k*30+15+rot); lx,ly=cx+(R-23)*math.cos(am),cy+(R-23)*math.sin(am)
            if 0<lx<1080 and 0<ly<1350: o.append(f'<text x="{lx:.1f}" y="{ly+5:.1f}" text-anchor="middle" font-family="EB Garamond" font-size="15" letter-spacing="2" fill="{GOLD}" fill-opacity=".55" transform="rotate({k*30+15+rot+90:.1f} {lx:.1f} {ly:.1f})">{ab[k]}</text>')
        # Saturn with its ring at the bottom right
        sx,sy=1000+(i-1)*-6,1236
        g=uid('sat')
        o.append(f'<defs><radialGradient id="{g}" cx="38%" cy="34%" r="75%"><stop offset="0" stop-color="#F3E3C0"/><stop offset=".6" stop-color="#CDB07E"/><stop offset="1" stop-color="#7E6640"/></radialGradient></defs><circle cx="{sx}" cy="{sy}" r="34" fill="#E8D3A8" opacity=".07"/><ellipse cx="{sx}" cy="{sy}" rx="30" ry="8" fill="none" stroke="#D9C49A" stroke-opacity=".55" stroke-width="2" transform="rotate(-18 {sx} {sy})"/><circle cx="{sx}" cy="{sy}" r="13" fill="url(#{g})"/><path d="M{sx-29},{sy+9} A30,8 0 0 0 {sx+29},{sy-9}" fill="none" stroke="#D9C49A" stroke-opacity=".75" stroke-width="2" transform="rotate(-18 {sx} {sy})"/>')
    elif theme=='jupiter':
        jx,jy=118,1236
        o.append(f'<line x1="20" y1="{jy}" x2="380" y2="{jy}" stroke="{GOLD}" stroke-opacity=".12" stroke-width="1"/>')
        g=uid('jj')
        o.append(f'<defs><radialGradient id="{g}" cx="38%" cy="32%" r="78%"><stop offset="0" stop-color="#F4E3C6"/><stop offset=".55" stop-color="#D5B285"/><stop offset="1" stop-color="#7A5536"/></radialGradient><clipPath id="{g}c"><circle cx="{jx}" cy="{jy}" r="24"/></clipPath></defs>'
                 f'<circle cx="{jx}" cy="{jy}" r="46" fill="#E0B98A" opacity=".08"/><circle cx="{jx}" cy="{jy}" r="24" fill="url(#{g})"/><g clip-path="url(#{g}c)" opacity=".5"><rect x="{jx-24}" y="{jy-10}" width="48" height="4" fill="#9C6440"/><rect x="{jx-24}" y="{jy+3}" width="48" height="6" fill="#A8744F"/><ellipse cx="{jx+8}" cy="{jy+7}" rx="5" ry="3" fill="#A0563A"/></g>')
        # the four moons shift along their line on each slide, as they really do
        for k,(base,amp,per) in enumerate([(52,40,1.0),(96,60,1.8),(150,70,3.4),(230,80,6.9)]):
            ph=(i-1)/per*math.pi*0.9+k+(2*math.pi*tt if k<2 else .22*sw)
            mx=jx+(base*math.sin(ph) if k%2 else -base*math.sin(ph)) ; mx=jx+base*math.cos(ph)
            o.append(f'<circle cx="{mx:.1f}" cy="{jy}" r="{3.6 if k<3 else 4.2}" fill="#F2E6CC" opacity=".8"/>')
        o.append(_crescent(1000,92,60,.5))
    elif theme=='thread':
        # v6: two sweeps of the thread, tucked into the top right and bottom left corners, each the rim of a sky instrument:
        # a second inner line and a degree scale between them. The scale turns and the five pearls slide along as you swipe; one pearl is lit.
        # The sweeps stay clear of the kicker and of the thread at the foot.
        arcs=[(1160,-80,360,210,24,[.30,.66]),(-90,1440,420,240,-14,[.22,.50,.78])]
        lit=(i-1)%5; kidx=0
        for cx,cy,rx,ry,rot,fr in arcs:
            c=math.cos(math.radians(rot)); s_=math.sin(math.radians(rot))
            def pt(a,k=1.0):
                px,py=cx+rx*k*math.cos(a),cy+ry*k*math.sin(a)
                return cx+(px-cx)*c-(py-cy)*s_, cy+(px-cx)*s_+(py-cy)*c
            vis=[d for d in range(0,720) if 14<pt(math.radians(d/2))[0]<1066 and 14<pt(math.radians(d/2))[1]<1336]
            # the visible stretch is one run of half-degrees; if it wraps past 360, shift it
            if vis and vis[0]==0 and vis[-1]==719:
                gap=next(k for k in range(len(vis)-1) if vis[k+1]-vis[k]>1); vis=vis[gap+1:]+[v+720 for v in vis[:gap+1]]
            o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{GOLD}" stroke-opacity=".32" stroke-width="1.5" transform="rotate({rot} {cx} {cy})"/>')
            o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*.9:.1f}" ry="{ry*.9:.1f}" fill="none" stroke="{GOLD}" stroke-opacity=".14" stroke-width="1" transform="rotate({rot} {cx} {cy})"/>')
            ph=(i-1)*2.5+15*tt; tk=[]
            for d in range(0,360,3):
                a=math.radians(d+ph); big=(d%15==0)
                x1,y1=pt(a); x2,y2=pt(a,.955 if big else .978)
                if -20<x1<1100 and -20<y1<1370: tk.append(f'M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}')
            o.append(f'<path d="{" ".join(tk)}" fill="none" stroke="{GOLD}" stroke-opacity=".32" stroke-width="1"/>')
            for f0 in fr:
                on=(kidx==lit); kidx+=1
                if not vis: continue
                f=.08+((f0-.08+(i-1)*.045)%.84)+.014*sw
                fi=min(max(f,0),1)*(len(vis)-1); k0=int(fi); k1=min(k0+1,len(vis)-1); xa,ya=pt(math.radians(vis[k0]/2)); xb,yb=pt(math.radians(vis[k1]/2)); x,y=xa+(xb-xa)*(fi-k0),ya+(yb-ya)*(fi-k0)
                if on: o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{24+9*br:.1f}" fill="{AMBER}" opacity="{.16+.12*br:.3f}"/>')
                o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{8.5 if on else 6.5}" fill="{AMBER if on else CREAM}" opacity="{.98 if on else .72}"/>')
    elif theme=='dream':
        # Inception's folding city in Sutram's colours (6 Nov): a cool dream haze above, the city hanging upside down
        # from the top edge and curling a little more on each slide, the same city upright along the bottom,
        # and two faint frames, dream inside dream, turning as you swipe
        gid=uid('dh')
        o.insert(0,f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7C9BB2" stop-opacity=".22"/><stop offset=".5" stop-color="#7C9BB2" stop-opacity="0"/></linearGradient></defs><rect width="1080" height="1350" fill="url(#{gid})"/>')
        for k,(w,h,a0,st) in enumerate([(1250,1580,-3,1.5),(960,1230,2.5,-1.1)]):
            o.append(f'<rect x="{540-w/2}" y="{675-h/2}" width="{w}" height="{h}" rx="22" fill="none" stroke="{GOLD}" stroke-opacity="{.11 if k==0 else .075}" stroke-width="1.2" transform="rotate({a0+(i-1)*st:.2f} 540 675)"/>')
        rb=random.Random(seed*53+1); blds=[]; x=-760.0
        while x<760:
            w=rb.uniform(28,74); h=rb.uniform(60,190); blds.append((x+w/2,w,h,rb.randrange(10**6))); x+=w+rb.uniform(3,12)
        R=1700-(i-1)*120; cx,cy=540,R
        for sx,w,h,ws in blds:
            if abs(sx)<250: continue   # an open street in the middle keeps the kicker clear
            a=sx/R; bx=cx+R*math.sin(a); by=cy-R*math.cos(a)
            if not (-120<bx<1200): continue
            wr=random.Random(ws)
            win=''.join(f'<rect x="{-w/2+6+c*10:.1f}" y="{10+q*16:.1f}" width="3.4" height="6" fill="#BFD3E0" opacity="{wr.uniform(.25,.6):.2f}"/>' for c in range(int((w-10)//10)) for q in range(int((h-18)//16)) if wr.random()<.2)
            o.append(f'<g transform="translate({bx:.1f} {by:.1f}) rotate({math.degrees(a):.2f})"><rect x="{-w/2:.1f}" y="-8" width="{w:.1f}" height="{h+8:.1f}" fill="#0C0A0B" stroke="#9FB8C9" stroke-opacity=".26" stroke-width="1.1"/>{win}</g>')
        for sx,w,h,ws in blds:
            x0=540+sx-w/2
            if x0>1080 or x0+w<0: continue
            hh=h*.75*(0.4 if abs(sx)<260 else 1)   # lower in the middle so the footer stays clear
            wr=random.Random(ws+1)
            win=''.join(f'<rect x="{x0+6+c*10:.1f}" y="{1350-hh+10+q*16:.1f}" width="3.4" height="6" fill="{AMBER}" opacity="{wr.uniform(.25,.6):.2f}"/>' for c in range(int((w-10)//10)) for q in range(int((hh-18)//16)) if wr.random()<.2)
            o.append(f'<rect x="{x0:.1f}" y="{1350-hh:.1f}" width="{w:.1f}" height="{hh+4:.1f}" fill="#0E0A08" stroke="{GOLD}" stroke-opacity=".32" stroke-width="1.1"/>{win}')
    return f'<svg class="decor" width="1080" height="1350">{"".join(o)}</svg>'

def theme_for(spec):
    """Pick the background theme: the spec's own choice, or one that suits the post type, so the feed keeps changing."""
    if spec.get('decor_theme') in THEMES+['dream']: return spec['decor_theme']
    k=(spec.get('kicker') or '').lower(); pid=spec['id']
    if k.startswith("today's sky"): return 'lunar'
    if 'thread' in k or 'scripture' in k: return 'thread'
    if 'sky patterns' in k: return 'solar'
    return THEMES[sum(map(ord,pid))%len(THEMES)]

def real_phase(spec):
    """On a Today's Sky post the lunar strip lights the Moon's real phase; elsewhere the lit phase moves as you swipe."""
    if isinstance(spec.get('decor_phase'),int): return spec['decor_phase']
    o=(spec['slides'][0].get('orb') or {})
    if (spec.get('kicker') or '').lower().startswith("today's sky") and o.get('kind')=='moon':
        return phase_index(o.get('illum',1.0), o.get('waxing',True))
    return None

# Sumant, 29 Oct: every post promotes asksutram.com first, then sutram.ca/newsletter, and nothing else
FOOT_URL='asksutram.com'
def frame(i=None,n=None):
    """v6 (10 Nov): corner marks like an almanac plate, and the thread at the foot with one bead per slide.
    The lit bead walks along the thread as you swipe."""
    m,L=50,44; o=[]
    for x,y,dx,dy in [(m,m,1,1),(1080-m,m,-1,1),(m,1350-m,1,-1),(1080-m,1350-m,-1,-1)]:
        o.append(f'<path d="M{x},{y+dy*L} V{y} H{x+dx*L}" fill="none" stroke="{GOLD}" stroke-opacity=".42" stroke-width="1.4"/><circle cx="{x}" cy="{y}" r="2.4" fill="{AMBER}" opacity=".85"/>')
    if n and n>1 and i:
        gap=30 if n<=12 else (24 if n<=16 else 20); W=(n-1)*gap; x0=540-W/2; y=1350-170
        o.append(f'<line x1="{x0-54}" y1="{y}" x2="{x0+W+54}" y2="{y}" stroke="{GOLD}" stroke-opacity=".34" stroke-width="1.1"/>')
        for k in range(n):
            x=x0+k*gap
            if k+1==i: o.append(f'<circle class="bd-glow" cx="{x}" cy="{y}" r="15" fill="{AMBER}" opacity=".20"/><circle class="bd-lit" cx="{x}" cy="{y}" r="6.2" fill="{AMBER}"/>')
            elif k+1<i: o.append(f'<circle cx="{x}" cy="{y}" r="3.6" fill="{CREAM}" opacity=".8"/>')
            else: o.append(f'<circle class="bd-next" cx="{x}" cy="{y}" r="3.4" fill="{BG}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.1"/>')
    return f'<svg class="frame" width="1080" height="1350">{"".join(o)}</svg>'
SWIPE=f'<div class="swipe"><span>Swipe to read</span><svg width="78" height="30" viewBox="0 0 78 30"><path d="M2,15 H72 M58,4 L73,15 L58,26" fill="none" stroke="{AMBER}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
def tabs_html(parts, cur):
    if not parts: return ''
    pc=lambda k: PART_COLORS[k%len(PART_COLORS)]
    return '<div class="tabs">'+''.join(f'<span class="tab{" on" if k+1==cur else (" done" if (cur and k+1<cur) else "")}"><b style="{"" if k+1==cur else "border-color:"+pc(k)+";color:"+pc(k)}">{k+1}</b>{esc(p_)}</span>' for k,p_ in enumerate(parts))+'</div>'
def page(inner,kicker,s,starfield=None,url=FOOT_URL,dec='',i=None,n=None,parts=None,part=None,swipe=False):
    tb=tabs_html(parts,part) if (parts and part is not None) else ''
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{css(s)}</style></head><body><div class="slide{" tabbed" if tb else ""}" style="{"--pc:"+PART_COLORS[(part-1)%len(PART_COLORS)] if (tb and part and parts and part<=len(parts)) else ""}">{dec}{starfield or ''}{GRAIN}{frame() if swipe else frame(i,n)}<div class="kick"><i></i><span>{esc(kicker)}</span><i class="r"></i></div>{tb}<div class="body">{inner}</div>{SWIPE if swipe else ''}<div class="foot"><div class="w">Sutram</div><div class="u">{url}</div></div></div></body></html>'''

HIDE_GLINTS="""()=>{const R=[];const add=(r,p)=>{if(r.width>0&&r.height>0)R.push([r.left-p,r.top-p,r.right+p,r.bottom+p])};
const w=document.createTreeWalker(document.querySelector('.slide'),NodeFilter.SHOW_TEXT);let n;const rg=document.createRange();
while(n=w.nextNode()){if(!n.nodeValue.trim()||n.parentElement.closest('svg.decor,svg.sf,svg.grain,svg.frame'))continue;rg.selectNodeContents(n);for(const r of rg.getClientRects())add(r,46)}
document.querySelectorAll('.body svg,.arch').forEach(e=>add(e.getBoundingClientRect(),4));
const hid=[];document.querySelectorAll('.gl').forEach((g,k)=>{const x=+g.dataset.x,y=+g.dataset.y;if(R.some(r=>x>r[0]&&x<r[2]&&y>r[1]&&y<r[3])){g.style.display='none';hid.push(k)}});window.__hid=hid;return hid}"""
def dec_for(spec,i,tt=0.0):
    sp=spec['slides'][i-1]; pid=spec['id']
    return '' if spec.get('decor') is False else decor(i, sum(map(ord,pid)), dense=bool(sp.get('stars')), theme=theme_for(spec), hi_phase=real_phase(spec), tt=tt)
def sf_for(spec,i,tt=0.0):
    sp=spec['slides'][i-1]
    return stars(seed=i*7+len(spec['id']),tt=tt) if sp.get('stars') else ''
def build_slide(pg, spec, i, out):
    """Lay slide i out at the largest text scale that fits and leave it loaded in the page. Returns (scale, overflow)."""
    pid=spec['id']; sp=spec['slides'][i-1]; kicker=sp.get('kicker',spec.get('kicker','Sutram'))
    for s in (1,.96,.92,.88,.84,.8,.76,.72,.68):
        html=page(slide_html(sp,s),kicker,s,sf_for(spec,i),dec=dec_for(spec,i),i=i,n=len(spec['slides']),parts=spec.get('parts'),part=sp.get('part'),swipe=bool(sp.get('swipe'))); fn=os.path.join(out,f'_s{i}.html'); open(fn,'w').write(html)
        pg.goto('file://'+fn); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
        ov=pg.evaluate("()=>{const b=document.querySelector('.body');return b.scrollHeight-b.clientHeight}")
        if ov<=0: break
    os.remove(fn); pg.evaluate(HIDE_GLINTS)
    return s,ov
def render(spec_path):
    spec=json.load(open(spec_path)); pid=spec['id']; out=os.path.join(REPO,'posts',pid); os.makedirs(out,exist_ok=True)
    outs=[]; scales=[]
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
        for i,sp in enumerate(spec['slides'],1):
            s,ov=build_slide(pg,spec,i,out); scales.append(s)
            if ov>0: print(f'  ! {pid} slide {i} still overflows by {ov}px at scale {s}')
            raw=os.path.join(out,f'_raw{i}.png'); pg.screenshot(path=raw)
            im=Image.open(raw).convert('RGB').resize((1080,1350),Image.LANCZOS)
            o=os.path.join(out,f'{pid}-{i}.jpg'); im.save(o,quality=93,optimize=True,progressive=True); outs.append(o)
            os.remove(raw)
        b.close()
    n=len(outs); cols=min(4,n); rows=(n+cols-1)//cols
    sheet=Image.new('RGB',(24+cols*384,24+rows*474),(5,4,3))
    for k,o in enumerate(outs):
        r,c=divmod(k,cols); sheet.paste(Image.open(o).resize((360,450),Image.LANCZOS),(24+c*384,24+r*474))
    sheet.save(os.path.join(out,f'{pid}-overview.jpg'),quality=88)
    small=[f'{k+1}:{v}' for k,v in enumerate(scales) if v<1]
    print(pid,'->',n,'slides'+(('  text shrunk on '+' '.join(small)) if small else ''))
    return outs

if __name__=='__main__':
    for a in sys.argv[1:]: render(a)
