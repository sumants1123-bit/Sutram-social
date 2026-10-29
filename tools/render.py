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

TXT=1.15   # v4 (29 Oct): text about 15% larger, Sumant found v3 hard to read on a phone

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
.kick{{position:absolute;top:86px;left:0;right:0;font:500 27px/1 'EB Garamond';letter-spacing:.30em;text-transform:uppercase;color:{GOLD}}}
.foot{{position:absolute;bottom:66px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:10px}}
.foot .w{{font:500 38px/1 'Cormorant Garamond';color:rgba(242,230,204,.66)}}
.foot .u{{font:500 19px/1 'EB Garamond';letter-spacing:.32em;text-transform:uppercase;color:rgba(242,230,204,.48)}}
.body{{position:absolute;left:84px;right:84px;top:160px;bottom:196px;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.t{{font-family:'Cormorant Garamond';font-weight:500;color:{CREAM};letter-spacing:-.01em}}
.ti{{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;color:{AMBER}}}
.p{{font:400 {f(38)}/1.4 'EB Garamond';color:rgba(242,230,204,.88)}}
.pi{{font:400 italic {f(36)}/1.38 'EB Garamond';color:rgba(242,230,204,.86)}}
.src{{font:500 {f(24)}/1.3 'EB Garamond';letter-spacing:.16em;text-transform:uppercase;color:rgba(242,230,204,.64)}}
.lab{{font:500 {f(25)}/1 'EB Garamond';letter-spacing:.26em;text-transform:uppercase;color:{GOLD}}}
.rule{{height:1px;width:110px;background:rgba(217,165,122,.55);margin:{f(32)} auto}}
.h1{{font-size:{f(132)};line-height:.98}} .h2{{font-size:{f(106)};line-height:1}} .h3{{font-size:{f(80)};line-height:1.05}}
.sub{{font-size:{f(54)};line-height:1.22}}
.row{{display:flex;justify-content:space-between;align-items:baseline;padding:{f(12)} 0;border-bottom:1px solid rgba(217,165,122,.2);text-align:left;gap:16px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;column-gap:56px;width:100%}}
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

def stars(seed=7,n=120,ymax=900):
    r=random.Random(seed); out=[]
    for _ in range(n):
        x=r.uniform(0,1080); y=r.uniform(0,ymax); rad=r.choice([.6,.8,1,1.2,1.5])
        op=r.uniform(.12,.6)*(1-y/ymax*.55)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="#FFF1D6" opacity="{op:.2f}"/>')
    return f'<svg style="position:absolute;inset:0" width="1080" height="1350">{"".join(out)}</svg>'
_n=[0]
def uid(p): _n[0]+=1; return f'{p}{_n[0]}'
def moon(R=140, illum=1.0, waxing=True):
    g,b,h=uid('mg'),uid('mb'),uid('mh'); s=2*R+160; c=s/2; k=1-2*illum; rx=abs(k)*R; sh=''
    if illum<0.999:
        if waxing: d=f'M{c},{c-R} A{R},{R} 0 0 0 {c},{c+R} A{rx},{R} 0 0 {1 if illum>0.5 else 0} {c},{c-R} Z'
        else:      d=f'M{c},{c-R} A{R},{R} 0 0 1 {c},{c+R} A{rx},{R} 0 0 {0 if illum>0.5 else 1} {c},{c-R} Z'
        sh=f'<path d="{d}" fill="#0B0806" opacity=".93" filter="url(#{b})"/>'
    cr=''.join(f'<circle cx="{c+dx*R}" cy="{c+dy*R}" r="{rr*R}" fill="#8F888D" opacity="{op}" filter="url(#{b})"/>' for dx,dy,rr,op in [(-.18,-.12,.16,.16),(.22,.05,.12,.14),(.05,.32,.10,.12),(-.32,.22,.08,.12),(.30,-.30,.07,.10)])
    return f'''<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:-60px auto -40px"><defs><radialGradient id="{g}" cx="40%" cy="36%" r="72%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".3" stop-color="#F3EFEB"/><stop offset=".66" stop-color="#D6D0CF"/><stop offset="1" stop-color="#A39DA2"/></radialGradient><filter id="{b}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{max(2,R/40)}"/></filter><filter id="{h}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{R/5}"/></filter></defs><circle cx="{c}" cy="{c}" r="{R*1.04}" fill="#FFF4E6" opacity=".28" filter="url(#{h})"/><circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/>{cr}{sh}</svg>'''
def sun(R=100, rings=True):
    g,h=uid('sg'),uid('sh'); s=int(R*5.2) if rings else 2*R+160; c=s/2
    rg=''.join(f'<circle cx="{c}" cy="{c}" r="{R*f}" fill="none" stroke="#E09460" stroke-opacity="{o}" stroke-width="1.2"/>' for f,o in [(1.55,.16),(2.05,.11),(2.55,.07)]) if rings else ''
    return f'''<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:{-R*0.9:.0f}px auto {-R*0.9:.0f}px"><defs><radialGradient id="{g}" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#FFE8CF"/><stop offset=".22" stop-color="#FBB37C"/><stop offset=".58" stop-color="#EE7838"/><stop offset=".88" stop-color="#C9521F"/><stop offset="1" stop-color="#A8401A"/></radialGradient><filter id="{h}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{R/3.2}"/></filter></defs>{rg}<circle cx="{c}" cy="{c}" r="{R*1.08}" fill="#EF7A3C" opacity=".45" filter="url(#{h})"/><circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/></svg>'''
def orbit(w=720,h=160,beads=5,tilt=-7,lit=None):
    pad=40; W=w+2*pad; H=h+2*pad+40; cx,cy=W/2,H/2; bs=''
    for i in range(beads):
        a=math.pi*(0.15+0.7*i/max(1,beads-1)); x=cx-(w/2)*math.cos(a); y=cy+(h/2)*math.sin(a)
        bs+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{11 if lit==i else 9}" fill="{AMBER if lit==i else CREAM}" opacity="{1 if lit==i else .85}"/>'
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="display:block;margin:0 auto"><g transform="rotate({tilt} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{h/2}" fill="none" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.6"/>{bs}</g></svg>'
def north(s=320, nums=False):
    h=s/2;q=s/4;x0=y0=4
    lab=''
    if nums:
        pos={1:(h,q*.9),2:(q,q*.45),3:(q*.45,q),4:(q,h),5:(q*.45,3*q),6:(q,3.55*q),7:(h,3.1*q),8:(3*q,3.55*q),9:(3.55*q,3*q),10:(3*q,h),11:(3.55*q,q),12:(3*q,q*.45)}
        lab=''.join(f'<text x="{x0+x}" y="{y0+y+9}" text-anchor="middle" font-family="Cormorant Garamond" font-style="italic" font-size="{s/11:.0f}" fill="{AMBER}">{n}</text>' for n,(x,y) in pos.items())
    return f'''<svg width="{s+8}" height="{s+8}" style="display:block;margin:0 auto"><polygon points="{x0+h},{y0} {x0+3*q},{y0+q} {x0+h},{y0+h} {x0+q},{y0+q}" fill="{AMBER}" fill-opacity=".18"/><g stroke="{GOLD}" stroke-opacity=".85" stroke-width="2" fill="none"><rect x="{x0}" y="{y0}" width="{s}" height="{s}"/><line x1="{x0}" y1="{y0}" x2="{x0+s}" y2="{y0+s}"/><line x1="{x0+s}" y1="{y0}" x2="{x0}" y2="{y0+s}"/><polygon points="{x0+h},{y0} {x0+s},{y0+h} {x0+h},{y0+s} {x0},{y0+h}"/></g>{lab}</svg>'''
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
    g,h=uid('vg'),uid('vh'); s=2*R+160; c=s/2
    return f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:-60px auto -50px"><defs><radialGradient id="{g}" cx="38%" cy="34%" r="74%"><stop offset="0" stop-color="#FFFBF2"/><stop offset=".35" stop-color="#F6E7C8"/><stop offset=".75" stop-color="#E2C48F"/><stop offset="1" stop-color="#B8925A"/></radialGradient><filter id="{h}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{R/3.4}"/></filter></defs><circle cx="{c}" cy="{c}" r="{R*1.1}" fill="#F3DDB0" opacity=".38" filter="url(#{h})"/><circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/></svg>'
def jupiter_orb(R=95):
    g,h,cl=uid('jg'),uid('jh'),uid('jc'); s=2*R+160; c=s/2
    bands=''.join(f'<rect x="{c-R}" y="{c+R*y:.1f}" width="{2*R}" height="{R*hh:.1f}" fill="{col}" opacity="{op}"/>' for y,hh,col,op in [(-.62,.10,'#B9875A',.35),(-.38,.14,'#A86F45',.42),(-.12,.08,'#E9D3B0',.35),(.06,.16,'#9C6440',.45),(.30,.08,'#C99A6B',.35),(.48,.12,'#A87450',.35),(.70,.08,'#C9A27A',.3)])
    return f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" style="display:block;margin:-60px auto -50px"><defs><radialGradient id="{g}" cx="38%" cy="32%" r="78%"><stop offset="0" stop-color="#F7E9D2"/><stop offset=".45" stop-color="#E2C49C"/><stop offset=".85" stop-color="#A57850"/><stop offset="1" stop-color="#6E4A2E"/></radialGradient><clipPath id="{cl}"><circle cx="{c}" cy="{c}" r="{R}"/></clipPath><filter id="{h}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{R/3.4}"/></filter></defs><circle cx="{c}" cy="{c}" r="{R*1.08}" fill="#E0B98A" opacity=".30" filter="url(#{h})"/><circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})"/><g clip-path="url(#{cl})">{bands}<circle cx="{c}" cy="{c}" r="{R}" fill="url(#{g})" opacity=".35"/><ellipse cx="{c+R*.28}" cy="{c+R*.16}" rx="{R*.13}" ry="{R*.07}" fill="#A0563A" opacity=".55"/></g><circle cx="{c}" cy="{c}" r="{R}" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="{R*.08}" style="filter:blur(4px)"/></svg>'
def asc_orb(s=230):
    h=uid('ah'); w=int(s*1.8); ht=int(s*1.0); cy=int(ht*0.66); cx=w/2; R=s*0.36
    return f'<svg width="{w}" height="{ht}" viewBox="0 0 {w} {ht}" style="display:block;margin:-46px auto -40px"><defs><filter id="{h}" filterUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{ht}"><feGaussianBlur stdDeviation="{s*0.08:.1f}"/></filter></defs><ellipse cx="{cx}" cy="{cy-R*0.3:.1f}" rx="{R*1.1:.1f}" ry="{R*0.7:.1f}" fill="#E09460" opacity=".40" filter="url(#{h})"/><circle cx="{cx-R:.1f}" cy="{cy}" r="18" fill="#E09460" opacity=".55" filter="url(#{h})"/><path d="M{cx-R:.1f},{cy} A{R:.1f},{R:.1f} 0 0 1 {cx+R:.1f},{cy}" fill="none" stroke="#D9A57A" stroke-width="3"/><line x1="{cx-s*0.62:.1f}" y1="{cy}" x2="{cx+s*0.62:.1f}" y2="{cy}" stroke="#D9A57A" stroke-width="3"/><circle cx="{cx-R:.1f}" cy="{cy}" r="9" fill="#E09460"/></svg>'
def orb(o):
    if not o: return ''
    k=o.get('kind'); 
    if k=='moon': return moon(o.get('r',140),o.get('illum',1.0),o.get('waxing',True))
    if k=='sun': return sun(o.get('r',95),o.get('rings',True))
    if k=='orbit': return orbit(o.get('w',720),o.get('h',160),o.get('beads',5),o.get('tilt',-7),o.get('lit'))
    if k=='asc': return asc_orb(o.get('s',230))
    if k=='venus': return venus_orb(o.get('r',80))
    if k=='jupiter': return jupiter_orb(o.get('r',95))
    if k=='north': return north(o.get('s',320),o.get('nums',False))
    if k=='south': return south(o.get('s',320),o.get('labels',True),o.get('asc'))
    return ''

def slide_html(sp, s=1.0):
    F=lambda px: f'{px*s:.1f}px'
    T=lambda px: F(px*TXT)
    t=sp['type']; H=[]
    if sp.get('orb'): H.append(f'<div style="margin-bottom:24px">{orb(sp["orb"])}</div>')
    bs=f'font-size:{T(sp["bodysize"])};' if sp.get('bodysize') else ''
    if sp.get('label'): H.append(f'<div class="lab" style="margin-bottom:22px;{"font-size:"+T(sp["labelsize"]) if sp.get("labelsize") else ""}">{esc(sp["label"])}</div>')
    if t in ('cover','cta','text','list','grid','quote','quotes','steps','sentence','sky','rows','stack','icons','svg'):
        if sp.get('title'):
            cls=sp.get('titleclass') or {'cover':'h1','cta':'h1'}.get(t,'h2' if len(clean(sp['title']))<26 else 'h3')
            H.append(f'<div class="t {cls}">{rich(sp["title"])}</div>')
        if sp.get('subtitle'): H.append(f'<div class="ti sub" style="margin-top:22px">{esc(sp["subtitle"])}</div>')
    if t=='quote':
        H.append('<div class="rule"></div>')
        H.append(f'<div class="ti h3" style="color:{CREAM}">“{esc(sp["quote"])}”</div>')
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
    if t=='rows':
        H.append('<div style="margin-top:30px;width:100%">'+''.join(f'<div class="row"><span class="t" style="font-size:{F(52)};white-space:nowrap">{esc(a)}</span><span class="p" style="text-align:right;font-size:{T(sp.get("bodysize",34))}">{esc(b)}</span></div>' for a,b in sp['items'])+'</div>')
    if t=='grid':
        H.append('<div class="grid2" style="margin-top:22px">'+''.join(f'<div style="padding:20px 0"><div class="lab">{esc(a)}</div><div class="t" style="font-size:{F(50)};line-height:1.1;margin-top:12px">{esc(b)}</div><div class="pi" style="margin-top:4px">{esc(c)}</div></div>' for a,b,c in sp['cells'])+'</div>')
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
    if t=='sentence':
        H.append('<div class="rule"></div>')
        H.append(f'<div class="t h3">{esc(sp["example"])}</div>')
        H.append('<div style="margin-top:28px">'+''.join(f'<div class="p" style="margin-top:10px;{bs}"><span class="lab" style="margin-right:20px">{esc(a)}</span>{esc(b)}</div>' for a,b in sp['rows'])+'</div>')
        if sp.get('conclusion'): H.append(f'<div class="ti sub" style="margin-top:36px">{esc(sp["conclusion"])}</div>')
    if t=='sky':
        H.append('<div class="grid2" style="margin-top:26px;border-top:1px solid rgba(217,165,122,.28);border-bottom:1px solid rgba(217,165,122,.28);padding:6px 0">'+''.join(f'<div style="padding:12px 0"><div class="lab">{esc(a)}</div><div class="p" style="margin-top:10px;font-size:{F(44)};line-height:1.15">{esc(b)}</div></div>' for a,b in sp['cells'])+'</div>')
        H.append(f'<div class="grid2" style="grid-template-columns:1fr 1fr;margin-top:22px"><div><span class="lab">Good for</span><div class="p" style="margin-top:8px;font-size:{F(40)};line-height:1.2">{esc(sp["good"])}</div></div><div><span class="lab">Go slow on</span><div class="p" style="margin-top:8px;font-size:{F(40)};line-height:1.2">{esc(sp["slow"])}</div></div></div>')
    if sp.get('body'):
        H.append('<div style="margin-top:30px">'+''.join(f'<div class="p" style="{bs}">{esc(l)}</div>' for l in sp['body'])+'</div>')
    if sp.get('note'): H.append(f'<div class="src" style="margin-top:28px;letter-spacing:.1em">{esc(sp["note"])}</div>')
    if t=='cta':
        H.append('<div class="rule"></div>'+''.join(f'<div class="p" style="margin-top:6px;{bs}">{esc(l)}</div>' for l in sp.get('lines',[])))
        if sp.get('next'): H.append(f'<div class="src" style="margin-top:28px">{esc(sp["next"])}</div>')
    if sp.get('closing'): H.append(f'<div class="ti sub" style="margin-top:34px">{esc(sp["closing"])}</div>')
    return ''.join(H)

def _bead(x,y,kind,uidp):
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
    return f'<defs><radialGradient id="{g}" cx="38%" cy="34%" r="75%"><stop offset="0" stop-color="#FFFBF2"/><stop offset=".6" stop-color="#EBD3A4"/><stop offset="1" stop-color="#A88152"/></radialGradient></defs><circle cx="{x:.1f}" cy="{y:.1f}" r="16" fill="#F3DDB0" opacity=".10"/><circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="url(#{g})"/>'

def decor(i, seed, dense=False):
    """Quiet moving sky behind every slide: stars, a Sun peeking in at the top right with two orbits,
    and two orbits at the bottom left. The small planets move a few degrees on each slide."""
    r=random.Random(seed*131+7); rr=random.Random(seed*977+i*31); o=[]
    for _ in range(46 if not dense else 0):
        x=rr.uniform(0,1080); y=rr.uniform(0,1350); rad=rr.choice([.6,.8,1,1.2])
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="#FFF1D6" opacity="{rr.uniform(.08,.30):.2f}"/>')
    for _ in range(4):
        x=rr.uniform(40,1040); y=rr.uniform(40,1310)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#FFF1D6" opacity=".07"/><circle cx="{x:.1f}" cy="{y:.1f}" r="1.7" fill="#FFF1D6" opacity=".62"/>')
    # top right: a Sun just inside the corner, two orbits around it
    sx,sy=1110,-34
    o.append(f'<circle cx="{sx}" cy="{sy}" r="120" fill="#EF7A3C" opacity=".07"/><circle cx="{sx}" cy="{sy}" r="74" fill="#EF7A3C" opacity=".10"/><circle cx="{sx}" cy="{sy}" r="44" fill="#F08A4C" opacity=".30"/>')
    for R,kind,a0,step in [(190,'venus',152,-3.5),(318,'mars',108,-1.6)]:
        o.append(f'<circle cx="{sx}" cy="{sy}" r="{R}" fill="none" stroke="{GOLD}" stroke-opacity=".15" stroke-width="1.2"/>')
        a=math.radians(a0+r.uniform(-3,3)+(i-1)*step); o.append(_bead(sx+R*math.cos(a), sy+R*math.sin(a), kind, 'db'))
    # bottom left: two wide orbits with Jupiter and a moon
    cx,cy=-90,1460
    for R,kind,a0,step in [(330,'moon',-60,4.5),(520,'jupiter',-40,3.2)]:
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{R}" ry="{R*0.86:.0f}" fill="none" stroke="{GOLD}" stroke-opacity=".14" stroke-width="1.2"/>')
        a=math.radians(a0+r.uniform(0,4)+(i-1)*step); o.append(_bead(cx+R*math.cos(a), cy+R*0.86*math.sin(a), kind, 'db'))
    return f'<svg class="decor" width="1080" height="1350">{"".join(o)}</svg>'

def page(inner,kicker,s,starfield=None,url='sutram.ca',dec=''):
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{css(s)}</style></head><body><div class="slide">{dec}{starfield or ''}{GRAIN}<div class="kick">{esc(kicker)}</div><div class="body">{inner}</div><div class="foot"><div class="w">Sutram</div><div class="u">{url}</div></div></div></body></html>'''

def render(spec_path):
    spec=json.load(open(spec_path)); pid=spec['id']; out=os.path.join(REPO,'posts',pid); os.makedirs(out,exist_ok=True)
    outs=[]
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
        for i,sp in enumerate(spec['slides'],1):
            kicker=sp.get('kicker',spec.get('kicker','Sutram'))
            sf=stars(seed=i*7+len(pid)) if sp.get('stars') else ''
            dec='' if spec.get('decor') is False else decor(i, sum(map(ord,pid)), dense=bool(sp.get('stars')))
            for s in (1,.96,.92,.88,.84,.8,.76,.72,.68):
                html=page(slide_html(sp,s),kicker,s,sf,dec=dec); fn=os.path.join(out,f'_s{i}.html'); open(fn,'w').write(html)
                pg.goto('file://'+fn); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
                ov=pg.evaluate("()=>{const b=document.querySelector('.body');return b.scrollHeight-b.clientHeight}")
                if ov<=0: break
            if ov>0: print(f'  ! {pid} slide {i} still overflows by {ov}px at scale {s}')
            raw=os.path.join(out,f'_raw{i}.png'); pg.screenshot(path=raw)
            im=Image.open(raw).convert('RGB').resize((1080,1350),Image.LANCZOS)
            o=os.path.join(out,f'{pid}-{i}.jpg'); im.save(o,quality=93,optimize=True,progressive=True); outs.append(o)
            os.remove(raw); os.remove(fn)
        b.close()
    n=len(outs); cols=min(4,n); rows=(n+cols-1)//cols
    sheet=Image.new('RGB',(24+cols*384,24+rows*474),(5,4,3))
    for k,o in enumerate(outs):
        r,c=divmod(k,cols); sheet.paste(Image.open(o).resize((360,450),Image.LANCZOS),(24+c*384,24+r*474))
    sheet.save(os.path.join(out,f'{pid}-overview.jpg'),quality=88)
    print(pid,'->',n,'slides')
    return outs

if __name__=='__main__':
    for a in sys.argv[1:]: render(a)
