"""Sky Patterns graphics for Instagram, drawn from engine data (Swiss Ephemeris, sidereal Lahiri).
Writes SVG files into svg/. Usage: python3 tools/patterns.py
"""
import json, math, os
HERE=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.dirname(HERE)
OUT=os.path.join(REPO,'svg'); os.makedirs(OUT,exist_ok=True)
D=json.load(open(os.path.join(REPO,'plan','paths-2026-10.json')))
CREAM='#F2E6CC'; AMBER='#E09460'; GOLD='#D9A57A'; BG='#0B0806'
ABBR=['ARI','TAU','GEM','CAN','LEO','VIR','LIB','SCO','SAG','CAP','AQU','PIS']

def xy(c,r,deg):   # Aries 0 at the right, longitude increases counter-clockwise
    a=math.radians(deg); return c+r*math.cos(a), c-r*math.sin(a)

def zodiac_ring(c,R,labels='all',lab_r=None,size=21):
    s=[f'<circle cx="{c}" cy="{c}" r="{R}" fill="none" stroke="{GOLD}" stroke-opacity=".38" stroke-width="1.2"/>']
    for i in range(12):
        x1,y1=xy(c,R,i*30); x2,y2=xy(c,R-12,i*30)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.2"/>')
        if labels=='all' or i in labels:
            lx,ly=xy(c,lab_r or R+26,i*30+15)
            s.append(f'<text x="{lx:.1f}" y="{ly+size*0.35:.1f}" text-anchor="middle" font-family="EB Garamond" font-size="{size}" letter-spacing="3" fill="{GOLD}" fill-opacity=".85">{ABBR[i]}</text>')
    return ''.join(s)

def glow_defs(idn,sd):
    return f'<filter id="{idn}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{sd}"/></filter>'

def polyline(pts,c,scale,offset=0):
    return ' '.join(f'{xy(c,(d-offset)*scale,l)[0]:.1f},{xy(c,(d-offset)*scale,l)[1]:.1f}' for l,d in pts)

def venus_rose():
    W=860; c=W/2; scale=200   # px per AU; max distance 1.74 AU -> 347 px
    pts=[(p[0],p[1]) for p in D['venus']['points']]
    n=len(pts); chunks=8; seg=n//chunks
    body=[]
    for k in range(chunks):
        part=pts[k*seg:(k+1)*seg+1] if k<chunks-1 else pts[k*seg:]
        op=0.30+0.60*k/(chunks-1)
        col=CREAM if k==chunks-1 else GOLD
        pl=polyline(part,c,scale)
        body.append(f'<polyline points="{pl}" fill="none" stroke="{col}" stroke-opacity="{op*0.55:.2f}" stroke-width="5" filter="url(#vg)"/>')
        body.append(f'<polyline points="{pl}" fill="none" stroke="{col}" stroke-opacity="{op:.2f}" stroke-width="1.7" stroke-linejoin="round"/>')
    rings=''.join(f'<circle cx="{c}" cy="{c}" r="{r*scale}" fill="none" stroke="{GOLD}" stroke-opacity=".14" stroke-width="1"/>' for r in (0.5,1.0,1.5))
    rings+=f'<text x="{c+4}" y="{c-1.0*scale-8}" font-family="EB Garamond" font-size="19" fill="{GOLD}" fill-opacity=".55" letter-spacing="2">1 AU</text>'
    cj=D['venus_conj']
    star=' '.join(f'{xy(c,x["dist"]*scale,x["lon"])[0]:.1f},{xy(c,x["dist"]*scale,x["lon"])[1]:.1f}' for x in cj)
    marks=[f'<polyline points="{star}" fill="none" stroke="{AMBER}" stroke-opacity=".75" stroke-width="1.6"/>']
    # labels pushed out along each conjunction's direction, on a dark chip
    lab={'26 Oct 2018':None,'03 Jun 2020':'Jun 2020','08 Jan 2022':'Jan 2022','13 Aug 2023':'Aug 2023','22 Mar 2025':'Mar 2025','23 Oct 2026':'Oct 2018 · Oct 2026'}
    for x in cj:
        px,py=xy(c,x['dist']*scale,x['lon']); last=x['date'].endswith('2026')
        if not x['date'].endswith('2018'):
            marks.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{14 if last else 10}" fill="{AMBER if last else CREAM}" opacity=".35" filter="url(#vg)"/>')
        marks.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{7 if last else 5.5}" fill="{AMBER if last else CREAM}"/>')
        t=lab[x['date']]
        if t:
            rr=0.74*scale if not last else 0.80*scale
            lx,ly=xy(c,rr,x['lon']); w=len(t)*11.2+26
            marks.append(f'<rect x="{lx-w/2:.1f}" y="{ly-19:.1f}" width="{w:.1f}" height="36" rx="18" fill="{BG}" fill-opacity=".86" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
            marks.append(f'<text x="{lx:.1f}" y="{ly+7:.1f}" text-anchor="middle" font-family="EB Garamond" font-size="21" fill="{CREAM}" fill-opacity=".92">{t}</text>')
    earth=f'<circle cx="{c}" cy="{c}" r="7" fill="#DCE6EE"/><circle cx="{c}" cy="{c}" r="13" fill="#DCE6EE" opacity=".18"/>'
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}"><defs>{glow_defs("vg",3.2)}</defs>{rings}{zodiac_ring(c,382,lab_r=406,size=20)}{"".join(body)}{"".join(marks)}{earth}</svg>'
    open(os.path.join(OUT,'venus-rose.svg'),'w').write(svg)

def jupiter_loops():
    W=860; c=W/2; scale=55   # px per AU; 3.95-6.45 AU -> 217-355 px
    pts=[(p[0],p[1]) for p in D['jupiter']['points']]
    n=len(pts); chunks=12; seg=n//chunks; body=[]
    for k in range(chunks):
        part=pts[k*seg:(k+1)*seg+1] if k<chunks-1 else pts[k*seg:]
        op=0.95-0.55*k/(chunks-1)
        pl=polyline(part,c,scale)
        body.append(f'<polyline points="{pl}" fill="none" stroke="{GOLD}" stroke-opacity="{op*0.5:.2f}" stroke-width="5" filter="url(#jg)"/>')
        body.append(f'<polyline points="{pl}" fill="none" stroke="{GOLD if k else CREAM}" stroke-opacity="{op:.2f}" stroke-width="1.8" stroke-linejoin="round"/>')
    l0,d0=pts[0]; sx,sy=xy(c,d0*scale,l0)
    start=f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="16" fill="{AMBER}" opacity=".35" filter="url(#jg)"/><circle cx="{sx:.1f}" cy="{sy:.1f}" r="8" fill="{AMBER}"/>'
    lx,ly=xy(c,d0*scale-62,l0+3); t='Oct 2026, enters Leo'; w=len(t)*10.6+28
    start+=f'<rect x="{lx-w/2:.1f}" y="{ly-19:.1f}" width="{w:.1f}" height="36" rx="18" fill="{BG}" fill-opacity=".86" stroke="{GOLD}" stroke-opacity=".35"/><text x="{lx:.1f}" y="{ly+7:.1f}" text-anchor="middle" font-family="EB Garamond" font-size="21" fill="{CREAM}">{t}</text>'
    # highlight Leo sector
    a0,a1=120,150
    x1,y1=xy(c,382,a0); x2,y2=xy(c,382,a1); x3,y3=xy(c,200,a1); x4,y4=xy(c,200,a0)
    sector=f'<path d="M{x1:.1f},{y1:.1f} A382,382 0 0 0 {x2:.1f},{y2:.1f} L{x3:.1f},{y3:.1f} A200,200 0 0 1 {x4:.1f},{y4:.1f} Z" fill="{AMBER}" fill-opacity=".07"/>'
    earth=f'<circle cx="{c}" cy="{c}" r="7" fill="#DCE6EE"/><circle cx="{c}" cy="{c}" r="13" fill="#DCE6EE" opacity=".18"/><text x="{c}" y="{c+38}" text-anchor="middle" font-family="EB Garamond" font-size="19" letter-spacing="3" fill="{CREAM}" fill-opacity=".6">EARTH</text>'
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}"><defs>{glow_defs("jg",3.2)}</defs>{sector}{zodiac_ring(c,382,lab_r=406,size=20)}{"".join(body)}{start}{earth}</svg>'
    open(os.path.join(OUT,'jupiter-loops.svg'),'w').write(svg)


# ---------- November 2026: South Indian chart and month timeline ----------
import datetime as _dt
SOUTH=['Pisces','Aries','Taurus','Gemini','Aquarius',None,None,'Cancer','Capricorn',None,None,'Leo','Sagittarius','Scorpio','Libra','Virgo']
def south_planets(cells, centre, sub, fname, S=680):
    c=S/4; x0=y0=4; out=[]
    for i,sg in enumerate(SOUTH):
        if sg is None: continue
        r,k=divmod(i,4); x=x0+k*c; y=y0+r*c; has=sg in cells
        out.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{AMBER if has else "none"}" fill-opacity="{.07 if has else 0}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.6"/>')
        out.append(f'<text x="{x+14}" y="{y+30}" font-family="EB Garamond" font-size="17" letter-spacing="2.5" fill="{GOLD}" fill-opacity=".75">{sg.upper()}</text>')
        ps=cells.get(sg,[]); n=len(ps); top=y+c/2+28-(n-1)*20
        for j,(nm,retro) in enumerate(ps):
            ty=top+j*40
            if retro:
                out.append(f'<text x="{x+c/2}" y="{ty}" text-anchor="middle" font-family="Cormorant Garamond" font-weight="500" font-size="35" fill="{CREAM}">{nm}<tspan font-style="italic" fill="{AMBER}" font-size="27" dx="5">R</tspan></text>')
            else:
                out.append(f'<text x="{x+c/2}" y="{ty}" text-anchor="middle" font-family="Cormorant Garamond" font-weight="500" font-size="35" fill="{CREAM}">{nm}</text>')
    cx=x0+2*c; cy=y0+2*c
    out.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" font-family="Cormorant Garamond" font-weight="500" font-size="46" fill="{CREAM}">{centre}</text>')
    out.append(f'<text x="{cx}" y="{cy+34}" text-anchor="middle" font-family="EB Garamond" font-size="18" letter-spacing="3" fill="{GOLD}" fill-opacity=".8">{sub}</text>')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S+8} {S+8}" width="{S+8}" height="{S+8}">{"".join(out)}</svg>'
    open(os.path.join(OUT,fname),'w').write(svg)

def month_timeline(fname):
    W,H=900,800; X0,X1=178,876
    m0=_dt.datetime(2026,11,1); m1=_dt.datetime(2026,12,1)
    def X(t): return X0+(t-m0).total_seconds()/(m1-m0).total_seconds()*(X1-X0)
    def T(d,h=0,mi=0): return _dt.datetime(2026,11,d,h,mi)
    o=[]; rows=['Moon','Jupiter','Mars','Sun','Venus','Mercury','Saturn']; top=96; gap=88
    Y={r:top+i*gap for i,r in enumerate(rows)}
    # Friday 13 highlight
    x13=X(T(13,15))
    o.append(f'<rect x="{X(T(13))}" y="{top-60}" width="{X(T(14))-X(T(13))}" height="{Y["Saturn"]-top+92}" fill="{AMBER}" fill-opacity=".07"/>')
    o.append(f'<text x="{x13}" y="{top-70}" text-anchor="middle" font-family="EB Garamond" font-size="21" letter-spacing="2" fill="{AMBER}">FRI 13</text>')
    def label(x,y,t,anchor='middle',col=CREAM,op=.9,size=23,italic=False):
        return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="EB Garamond" font-size="{size}" {"font-style=\"italic\"" if italic else ""} fill="{col}" fill-opacity="{op}">{t}</text>'
    for r in rows:
        y=Y[r]
        o.append(f'<text x="0" y="{y+11}" font-family="Cormorant Garamond" font-weight="500" font-size="38" fill="{CREAM}">{r}</text>')
        if r!='Moon': o.append(f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{GOLD}" stroke-opacity=".16" stroke-width="1"/>')
    def fwd(r,a,b): return f'<line x1="{X(a):.1f}" y1="{Y[r]}" x2="{X(b):.1f}" y2="{Y[r]}" stroke="{GOLD}" stroke-opacity=".85" stroke-width="3" stroke-linecap="round"/>'
    def back(r,a,b): return f'<line x1="{X(a):.1f}" y1="{Y[r]}" x2="{X(b):.1f}" y2="{Y[r]}" stroke="{AMBER}" stroke-width="10" stroke-linecap="round"/>'
    def dia(r,t): x=X(t); y=Y[r]; return f'<rect x="{x-8:.1f}" y="{y-8}" width="16" height="16" transform="rotate(45 {x:.1f} {y})" fill="{CREAM}" stroke="{BG}" stroke-width="3"/>'
    def dot(r,t): x=X(t); y=Y[r]; return f'<circle cx="{x:.1f}" cy="{y}" r="9" fill="{BG}" stroke="{CREAM}" stroke-width="3"/>'
    s=_dt.datetime(2026,11,1); e=_dt.datetime(2026,12,1)
    # Jupiter
    o.append(fwd('Jupiter',s,e)); o.append(label(X1,Y['Jupiter']-20,'in Leo all month','end',GOLD,.95))
    # Mars
    o.append(fwd('Mars',s,e)); o.append(dia('Mars',T(12,9,48))); o.append(label(X(T(12,9,48)),Y['Mars']-20,'enters Leo · 12'))
    # Sun
    o.append(fwd('Sun',s,e)); o.append(dia('Sun',T(16,9,13))); o.append(label(X(T(16,9,13)),Y['Sun']-20,'enters Scorpio · 16'))
    # Venus
    o.append(back('Venus',s,T(13,19,29))); o.append(fwd('Venus',T(13,19,29),e))
    o.append(dia('Venus',T(5,14,34))); o.append(label(X(T(5,14,34)),Y['Venus']+38,'Virgo · 5'))
    o.append(dot('Venus',T(13,19,29))); o.append(label(X(T(13,19,29))+14,Y['Venus']-20,'forward · 13','start'))
    o.append(dia('Venus',T(22,6,51))); o.append(label(X(T(22,6,51)),Y['Venus']+38,'Libra · 22'))
    # Mercury
    o.append(back('Mercury',s,T(13,10,54))); o.append(fwd('Mercury',T(13,10,54),e))
    o.append(dot('Mercury',T(13,10,54))); o.append(label(X(T(13,10,54))+14,Y['Mercury']-20,'forward · 13','start'))
    # Saturn
    o.append(back('Saturn',s,e)); o.append(label(X1,Y['Saturn']-20,'backward until 10 Dec','end',AMBER,.95))
    # Moon row
    xn=X(T(9,2,2)); xf=X(T(24,9,53)); ym=Y['Moon']
    o.append(f'<circle cx="{xn:.1f}" cy="{ym}" r="13" fill="{BG}" stroke="{CREAM}" stroke-width="2.5"/>')
    o.append(label(xn,ym-26,'New Moon · Diwali'))
    o.append(f'<circle cx="{xf:.1f}" cy="{ym}" r="13" fill="{CREAM}"/><circle cx="{xf:.1f}" cy="{ym}" r="22" fill="{CREAM}" opacity=".16"/>')
    o.append(label(xf,ym-30,'Full Moon · 24'))
    # axis
    ya=Y['Saturn']+62
    o.append(f'<line x1="{X0}" y1="{ya}" x2="{X1}" y2="{ya}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    for d in (1,8,15,22,29):
        x=X(T(d,12)); o.append(f'<line x1="{x:.1f}" y1="{ya}" x2="{x:.1f}" y2="{ya+8}" stroke="{GOLD}" stroke-opacity=".5"/>')
        o.append(label(x,ya+34,f'{d} Nov' if d==1 else str(d),'middle',GOLD,.85,22))
    # legend
    yl=ya+86; lx=X0
    o.append(f'<line x1="{lx}" y1="{yl}" x2="{lx+46}" y2="{yl}" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>'+label(lx+58,yl+8,'moving forward','start',CREAM,.85,22))
    lx2=lx+250
    o.append(f'<line x1="{lx2}" y1="{yl}" x2="{lx2+46}" y2="{yl}" stroke="{AMBER}" stroke-width="10" stroke-linecap="round"/>'+label(lx2+60,yl+8,'moving backward','start',CREAM,.85,22))
    lx3=lx2+270; x=lx3+8
    o.append(f'<rect x="{x-8}" y="{yl-8}" width="16" height="16" transform="rotate(45 {x} {yl})" fill="{CREAM}"/>'+label(lx3+28,yl+8,'changes sign','start',CREAM,.85,22))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -24 {W} {H}" width="{W}" height="{H}">{"".join(o)}</svg>'
    open(os.path.join(OUT,fname),'w').write(svg)

def november():
    cells={'Libra':[('Sun',False),('Mercury',True),('Venus',True)],'Leo':[('Jupiter',False),('Ketu',False)],
           'Cancer':[('Mars',False)],'Pisces':[('Saturn',True)],'Aquarius':[('Rahu',False)]}
    south_planets(cells,'1 November','SIDEREAL · LAHIRI','nov-2026-chart.svg')
    month_timeline('nov-2026-timeline.svg')

if __name__=='__main__':
    venus_rose(); jupiter_loops(); november(); print('ok')

# ---------- Ascendant post: sky scene, two Moons, three lights ----------
def _moon(cx,cy,r,gid):
    return (f'<defs><radialGradient id="{gid}" cx="40%" cy="36%" r="72%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".35" stop-color="#F1EDE8"/>'
            f'<stop offset=".75" stop-color="#D2CBCB"/><stop offset="1" stop-color="#9F989D"/></radialGradient></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*1.6}" fill="#FFF4E6" opacity=".16" filter="url(#soft)"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/>'
            + ''.join(f'<circle cx="{cx+dx*r:.1f}" cy="{cy+dy*r:.1f}" r="{rr*r:.1f}" fill="#8F888D" opacity="{op}"/>' for dx,dy,rr,op in [(-.2,-.12,.16,.16),(.22,.06,.12,.14),(.04,.32,.1,.12)]))
def _sun(cx,cy,r,gid):
    return (f'<defs><radialGradient id="{gid}" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#FFE8CF"/><stop offset=".25" stop-color="#FBB37C"/>'
            f'<stop offset=".62" stop-color="#EE7838"/><stop offset="1" stop-color="#A8401A"/></radialGradient></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*1.9}" fill="#EF7A3C" opacity=".30" filter="url(#soft)"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/>')
def _asc(cx,cy,s,col=GOLD,w=2.4):
    return (f'<path d="M{cx-s*.62},{cy} A{s*.62},{s*.62} 0 0 1 {cx+s*.62},{cy}" fill="none" stroke="{col}" stroke-width="{w}"/>'
            f'<line x1="{cx-s}" y1="{cy}" x2="{cx+s}" y2="{cy}" stroke="{col}" stroke-width="{w}"/>')
def _lab(x,y,t,size=20,col=GOLD,op=.85,anchor='middle',sp=3,italic=False,fam='EB Garamond'):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{fam}" font-size="{size}" letter-spacing="{sp}" {"font-style=\"italic\"" if italic else ""} fill="{col}" fill-opacity="{op}">{t}</text>'

def asc_scene():
    W,H=900,600; hy=470; cx=450; rx=300; ry=330
    o=[f'<defs><filter id="soft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="14"/></filter>'
       f'<filter id="gl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3.5"/></filter>'
       f'<filter id="haze" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="38"/></filter>'
       f'<linearGradient id="hz" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="860" y2="0"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset=".15" stop-color="{GOLD}" stop-opacity=".8"/><stop offset=".85" stop-color="{GOLD}" stop-opacity=".8"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>']
    ax=cx-rx
    o.append(f'<ellipse cx="{ax+40}" cy="{hy-10}" rx="150" ry="90" fill="{AMBER}" opacity=".30" filter="url(#haze)"/>')
    o.append(f'<ellipse cx="{cx}" cy="{hy+40}" rx="330" ry="46" fill="#000" opacity=".35" filter="url(#haze)"/>')
    arc=f'M{cx-rx},{hy} A{rx},{ry} 0 0 1 {cx+rx},{hy}'
    o.append(f'<path d="{arc}" fill="none" stroke="{GOLD}" stroke-opacity=".45" stroke-width="6" filter="url(#gl)"/>')
    o.append(f'<path d="{arc}" fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.8"/>')
    for k in range(1,6):
        a=math.radians(180-k*30); x=cx+rx*math.cos(a); y=hy-ry*math.sin(a)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{CREAM}" opacity=".85"/>')
    o.append(f'<line x1="40" y1="{hy}" x2="{W-40}" y2="{hy}" stroke="url(#hz)" stroke-width="1.8"/>')
    o.append(f'<circle cx="{ax}" cy="{hy}" r="26" fill="{AMBER}" opacity=".5" filter="url(#soft)"/><circle cx="{ax}" cy="{hy}" r="9" fill="{AMBER}"/>')
    o.append(_lab(ax,hy+50,'ASCENDANT',21,AMBER,.95)); o.append(_lab(ax,hy+80,'rising in the east',23,CREAM,.8,sp=0,italic=True))
    o.append(_lab(cx+rx,hy+50,'WEST',19,GOLD,.55))
    a=math.radians(138); mx=cx+rx*math.cos(a); my=hy-ry*math.sin(a); o.append(_moon(mx,my,30,'am')); o.append(_lab(mx-52,my+8,'MOON',19,CREAM,.75,'end'))
    a=math.radians(52); sx=cx+rx*math.cos(a); sy=hy-ry*math.sin(a); o.append(_sun(sx,sy,32,'as')); o.append(_lab(sx+56,sy+8,'SUN',19,CREAM,.75,'start'))
    open(os.path.join(OUT,'asc-scene.svg'),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{"".join(o)}</svg>')

def two_moons():
    W,H=900,560; o=['<defs><filter id="soft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="12"/></filter></defs>']
    o.append(f'<line x1="{W/2}" y1="20" x2="{W/2}" y2="{H-20}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1.2"/>')
    for i,(moon,line1,line2) in enumerate([('Moon in Aries','Reacts fast','says it straight'),('Moon in Pisces','Takes in','everyone’s feelings')]):
        x=W/4+i*W/2
        o.append(_lab(x,52,'LEO ASCENDANT',20,GOLD,.9))
        o.append(_asc(x,118,46,GOLD,2.2))
        o.append(_moon(x,236,52,f'tm{i}'))
        o.append(_lab(x,352,moon,44,CREAM,1,sp=0,fam='Cormorant Garamond'))
        o.append(_lab(x,410,line1,30,CREAM,.85,sp=0,italic=True)); o.append(_lab(x,450,line2,30,CREAM,.85,sp=0,italic=True))
    o.append(_lab(W/4,512,'same body, same path',20,GOLD,.6)); o.append(_lab(3*W/4,512,'same body, same path',20,GOLD,.6))
    open(os.path.join(OUT,'asc-two-moons.svg'),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{"".join(o)}</svg>')

def triad():
    W,H=900,580; o=['<defs><filter id="soft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="12"/></filter></defs>']
    S=(450,120); A=(190,400); M=(710,400)
    o.append(f'<polygon points="{S[0]},{S[1]} {A[0]},{A[1]} {M[0]},{M[1]}" fill="{AMBER}" fill-opacity=".05" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.6"/>')
    o.append(_sun(S[0],S[1],46,'ts')); o.append(_moon(M[0],M[1],42,'tm'))
    o.append(f'<circle cx="{A[0]}" cy="{A[1]}" r="58" fill="{BG}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1.4"/>'+_asc(A[0],A[1]+14,52,GOLD,2.6)+f'<circle cx="{A[0]}" cy="{A[1]+14}" r="22" fill="{AMBER}" opacity=".35" filter="url(#soft)"/>')
    for (x,y),t,s in [((S[0],S[1]-78),'SUN','soul and purpose'),((A[0],A[1]+82),'ASCENDANT','body and path'),((M[0],M[1]+82),'MOON','feelings, day to day')]:
        if t=='SUN':
            o.append(_lab(x+92,y+86,t,21,GOLD,.95,'start')); o.append(_lab(x+92,y+116,s,26,CREAM,.85,'start',0,True))
        else:
            o.append(_lab(x,y,t,21,GOLD,.95)); o.append(_lab(x,y+32,s,26,CREAM,.85,sp=0,italic=True))
    open(os.path.join(OUT,'asc-triad.svg'),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{"".join(o)}</svg>')

if __name__=='__main__':
    asc_scene(); two_moons(); triad(); print('asc ok')
