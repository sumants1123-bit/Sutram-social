import json, swisseph as swe, datetime as dt
swe.set_sid_mode(swe.SIDM_LAHIRI)
F = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
G = [('Sun',swe.SUN),('Moon',swe.MOON),('Mars',swe.MARS),('Mercury',swe.MERCURY),('Jupiter',swe.JUPITER),('Venus',swe.VENUS),('Saturn',swe.SATURN),('Rahu',swe.MEAN_NODE)]
start = dt.datetime(2026,10,28,0,0,tzinfo=dt.timezone.utc)
end   = dt.datetime(2027,2,1,0,0,tzinfo=dt.timezone.utc)
step = dt.timedelta(hours=6)
def jd(t): return swe.julday(t.year,t.month,t.day,t.hour+t.minute/60)
rows=[]; t=start
while t<=end:
    j=jd(t); r=[]
    for n,p in G:
        x=swe.calc_ut(j,p,F)[0]; r.append([round(x[0],4), 1 if x[3]<0 else 0])
    k=(r[7][0]+180)%360; r.append([round(k,4), 1])   # Ketu opposite Rahu, always backward
    rows.append(r); t+=step
names=[g[0] for g in G]+['Ketu']
# events: ingresses and stations in the window, computed by bisection
def lon(j,p):
    if p=='Ketu': return (swe.calc_ut(j,swe.MEAN_NODE,F)[0][0]+180)%360
    return swe.calc_ut(j,dict(G)[p],F)[0][0]
def spd(j,p): return swe.calc_ut(j,dict(G)[p],F)[0][3]
def toronto(j):
    y,m,d,h=swe.revjul(j); u=dt.datetime(y,m,d,tzinfo=dt.timezone.utc)+dt.timedelta(hours=h)
    off = -4 if u < dt.datetime(2026,11,1,6,tzinfo=dt.timezone.utc) else -5
    return (u+dt.timedelta(hours=off)).isoformat()[:16], u.isoformat()[:16]+'Z'
ev=[]
SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
j0,j1=jd(start),jd(end)
for p in ['Sun','Mars','Mercury','Jupiter','Venus','Saturn','Ketu']:
    j=j0; prev=int(lon(j,p)//30)
    while j<j1:
        j2=j+0.25; s=int(lon(j2,p)//30)
        if s!=prev:
            a,b=j,j2
            for _ in range(40):
                m=(a+b)/2
                (a,b)=(a,m) if int(lon(m,p)//30)!=prev else (m,b)
            ev.append({'t':toronto(b)[1],'local':toronto(b)[0],'kind':'ingress','graha':p,'sign':SIGNS[s]})
            prev=s
        j=j2
for p in ['Mars','Mercury','Jupiter','Venus','Saturn']:
    j=j0; prev=spd(j,p)>0
    while j<j1:
        j2=j+0.25; cur=spd(j2,p)>0
        if cur!=prev:
            a,b=j,j2
            for _ in range(40):
                m=(a+b)/2
                ((a,b)) = (a,m) if (spd(m,p)>0)!=prev else (m,b)
            ev.append({'t':toronto(b)[1],'local':toronto(b)[0],'kind':'direct' if cur else 'retrograde','graha':p})
            prev=cur
        j=j2
ev.sort(key=lambda e:e['t'])
for e in ev: print(e)
out={'start':start.isoformat()[:16]+'Z','stepHours':6,'names':names,'rows':rows,'events':ev,
     'ayanamsa_2026_10_31':round(swe.get_ayanamsa_ut(swe.julday(2026,10,31,12)),5)}
json.dump(out,open('sky-data.json','w'),separators=(',',':'))
print(len(rows),'rows')
# Jupiter-Ketu separation minimum, and triple window
best=None
j=jd(dt.datetime(2026,11,1,tzinfo=dt.timezone.utc))
while j<jd(dt.datetime(2026,12,10,tzinfo=dt.timezone.utc)):
    d=abs((lon(j,'Jupiter')-lon(j,'Ketu')+180)%360-180)
    if best is None or d<best[0]: best=(d,toronto(j)[0])
    j+=1/24
print('Jupiter-Ketu closest',best)
