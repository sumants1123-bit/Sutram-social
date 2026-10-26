"""Daily sky data for Toronto from Swiss Ephemeris (sidereal, Lahiri). Engine-grade values only.

Usage: .venv/bin/python tools/sky.py YYYY-MM-DD [days]   -> JSON list, one object per day
Also lists ingresses and retrograde stations in the next 14 days ("shifts").
"""
import swisseph as swe, datetime as dt, json, sys
from zoneinfo import ZoneInfo
TZ=ZoneInfo('America/Toronto'); UTC=dt.timezone.utc
F=swe.FLG_MOSEPH|swe.FLG_SIDEREAL|swe.FLG_SPEED
swe.set_sid_mode(swe.SIDM_LAHIRI)
SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
# name, English meaning, deity, ruler, muhurta class (Muhurta Chintamani)
NAK=[('Ashwini','the horse twins','the Ashwini twins','Ketu','swift'),('Bharani','the bearer','Yama','Venus','fierce'),
('Krittika','the cutters','Agni','Sun','mixed'),('Rohini','the red one','Brahma','Moon','fixed'),('Mrigashira',"the deer's head",'Soma','Mars','soft'),
('Ardra','the moist one','Rudra','Rahu','sharp'),('Punarvasu','return of the light','Aditi','Jupiter','movable'),('Pushya','the nourisher','Brihaspati','Saturn','swift'),
('Ashlesha','the embrace','the Nagas','Mercury','sharp'),('Magha','the mighty','the ancestors','Ketu','fierce'),('Purva Phalguni','the former red one','Bhaga','Venus','fierce'),
('Uttara Phalguni','the latter red one','Aryaman','Sun','fixed'),('Hasta','the hand','Savitr','Moon','swift'),('Chitra','the bright one','Tvashtr','Mars','soft'),
('Swati','the independent one','Vayu','Rahu','movable'),('Vishakha','the forked branch','Indra and Agni','Jupiter','mixed'),('Anuradha','after Radha','Mitra','Saturn','soft'),
('Jyeshtha','the eldest','Indra','Mercury','sharp'),('Mula','the root','Nirriti','Ketu','sharp'),('Purva Ashadha','the early victory','the waters','Venus','fierce'),
('Uttara Ashadha','the later victory','the Vishvedevas','Sun','fixed'),('Shravana','hearing','Vishnu','Moon','movable'),('Dhanishta','the wealthiest','the Vasus','Mars','movable'),
('Shatabhisha','a hundred healers','Varuna','Rahu','movable'),('Purva Bhadrapada','the former lucky feet','Aja Ekapada','Jupiter','fierce'),
('Uttara Bhadrapada','the latter lucky feet','Ahir Budhnya','Saturn','fixed'),('Revati','the wealthy','Pushan','Mercury','soft')]
CLASS_GOOD={'fixed':'foundations, building, planting, long-term commitments','movable':'travel, vehicles, change, starting journeys',
'fierce':'bold action, competition, facing hard things','mixed':'routine work, everyday tasks','swift':'trade, medicine, learning, short trips, skilled work',
'soft':'arts, music, friendship, romance, gentle beginnings','sharp':'endings, separations, research, deep inner work'}
TITHI=['Pratipada','Dwitiya','Tritiya','Chaturthi','Panchami','Shashthi','Saptami','Ashtami','Navami','Dashami','Ekadashi','Dwadashi','Trayodashi','Chaturdashi']
WD=['Moon','Mars','Mercury','Jupiter','Venus','Saturn','Sun']   # Monday=0
TOR=(-79.38,43.65,0)
def jd(u): return swe.julday(u.year,u.month,u.day,u.hour+u.minute/60+u.second/3600)
def u_from_jd(j):
    y,m,d,h=swe.revjul(j); return dt.datetime(y,m,d,tzinfo=UTC)+dt.timedelta(hours=h)
def lon(u,b): return swe.calc_ut(jd(u),b,F)[0]
def L(u): return u.astimezone(TZ).strftime('%-I:%M %p')
def LD(u,day): x=u.astimezone(TZ); return x.strftime('%-I:%M %p')+('' if x.date()==day else x.strftime(' %a'))
def tithi_no(u):
    return int(((lon(u,swe.MOON)[0]-lon(u,swe.SUN)[0])%360)//12)+1
def day(d):
    mid=dt.datetime(d.year,d.month,d.day,tzinfo=TZ).astimezone(UTC)
    sr=u_from_jd(swe.rise_trans(jd(mid),swe.SUN,swe.CALC_RISE|swe.BIT_DISC_CENTER,TOR,0,0,swe.FLG_MOSEPH)[1][0])
    ss=u_from_jd(swe.rise_trans(jd(mid),swe.SUN,swe.CALC_SET|swe.BIT_DISC_CENTER,TOR,0,0,swe.FLG_MOSEPH)[1][0])
    seg=(ss-sr)/8; part={0:2,1:7,2:5,3:6,4:4,5:3,6:8}[d.weekday()]; rk0=sr+seg*(part-1)
    t=dt.datetime(d.year,d.month,d.day,7,tzinfo=TZ).astimezone(UTC)
    m=lon(t,swe.MOON)[0]; n=int(m//(360/27)); sg=int(m//30); ti=tithi_no(sr)
    tt=t
    while int(lon(tt,swe.MOON)[0]//(360/27))==n: tt+=dt.timedelta(minutes=10)
    ch=None; tc=t
    while tc<t+dt.timedelta(hours=24):
        if int(lon(tc,swe.MOON)[0]//30)!=sg: ch=tc; break
        tc+=dt.timedelta(minutes=10)
    ph=swe.pheno_ut(jd(t),swe.MOON,swe.FLG_MOSEPH); illum=ph[1]
    waxing=((m-lon(t,swe.SUN)[0])%360)<180
    paksha='Waxing' if ti<=15 else 'Waning'; k=ti if ti<=15 else ti-15
    tname='Purnima, full Moon' if ti==15 else ('Amavasya, new Moon' if ti==30 else f'{paksha} {k}{"st" if k==1 else "nd" if k==2 else "rd" if k==3 else "th"}, {TITHI[k-1]}')
    retro=[nm for nm,b in [('Mercury',swe.MERCURY),('Venus',swe.VENUS),('Mars',swe.MARS),('Jupiter',swe.JUPITER),('Saturn',swe.SATURN)] if lon(t,b)[3]<0]
    pos={nm:f"{SIGNS[int(lon(t,b)[0]//30)]} {lon(t,b)[0]%30:.0f}°" for nm,b in [('Sun',swe.SUN),('Moon',swe.MOON),('Mercury',swe.MERCURY),('Venus',swe.VENUS),('Mars',swe.MARS),('Jupiter',swe.JUPITER),('Saturn',swe.SATURN),('Rahu',swe.MEAN_NODE)]}
    nk=NAK[n]
    return dict(date=d.isoformat(),weekday=d.strftime('%A'),day_ruler=WD[d.weekday()],moon_sign=SIGNS[sg],moon_deg=round(m%30,1),
        nakshatra=nk[0],nak_meaning=nk[1],nak_deity=nk[2],nak_ruler=nk[3],nak_class=nk[4],nak_class_good_for=CLASS_GOOD[nk[4]],
        nak_ends=LD(tt,d),moon_enters=(SIGNS[(sg+1)%12]+' at '+LD(ch,d)) if ch else None,
        tithi_at_sunrise=tname,tithi_number=ti,rikta=(k in (4,9,14)),illumination=round(illum,3),waxing=waxing,
        sunrise=L(sr),sunset=L(ss),rahu_kaal=f"{L(rk0)} to {L(rk0+seg)}",retrograde=retro,positions=pos)
def shifts(d,days=14):
    out=[]; t=dt.datetime(d.year,d.month,d.day,tzinfo=TZ).astimezone(UTC); end=t+dt.timedelta(days=days)
    for nm,b in [('Sun',swe.SUN),('Mercury',swe.MERCURY),('Venus',swe.VENUS),('Mars',swe.MARS),('Jupiter',swe.JUPITER),('Saturn',swe.SATURN),('Rahu',swe.MEAN_NODE)]:
        u=t; p=lon(u,b); step=dt.timedelta(hours=1)
        while u<end:
            u2=u+step; q=lon(u2,b)
            if int(q[0]//30)!=int(p[0]//30): out.append(dict(when=u2.astimezone(TZ).strftime('%a %d %b %-I:%M %p'),event=f'{nm} enters {SIGNS[int(q[0]//30)]}'))
            if nm not in ('Sun','Rahu') and (q[3]<0)!=(p[3]<0): out.append(dict(when=u2.astimezone(TZ).strftime('%a %d %b %-I:%M %p'),event=f'{nm} turns {"retrograde" if q[3]<0 else "direct"} in {SIGNS[int(q[0]//30)]}'))
            u,p=u2,q
    return out
if __name__=='__main__':
    d0=dt.date.fromisoformat(sys.argv[1]); n=int(sys.argv[2]) if len(sys.argv)>2 else 1
    print(json.dumps(dict(days=[day(d0+dt.timedelta(days=i)) for i in range(n)],shifts_next_14_days=shifts(d0)),indent=1,ensure_ascii=False))
