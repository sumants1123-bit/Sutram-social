import swisseph as swe, datetime as dt, json, sys
F=swe.FLG_MOSEPH|swe.FLG_SIDEREAL|swe.FLG_SPEED
swe.set_sid_mode(swe.SIDM_LAHIRI)
SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
NAKS=['Ashwini','Bharani','Krittika','Rohini','Mrigashira','Ardra','Punarvasu','Pushya','Ashlesha','Magha','Purva Phalguni','Uttara Phalguni','Hasta','Chitra','Swati','Vishakha','Anuradha','Jyeshtha','Mula','Purva Ashadha','Uttara Ashadha','Shravana','Dhanishta','Shatabhisha','Purva Bhadrapada','Uttara Bhadrapada','Revati']
TITHI=['Pratipada','Dwitiya','Tritiya','Chaturthi','Panchami','Shashthi','Saptami','Ashtami','Navami','Dashami','Ekadashi','Dwadashi','Trayodashi','Chaturdashi']
TOR=(-79.38,43.65,0)
def jd(t): return swe.julday(t.year,t.month,t.day,t.hour+t.minute/60+t.second/3600)
def off(d): return 4 if d < dt.date(2026,11,1) else 5
def fromjd(j):
    y,m,d,h=swe.revjul(j); return dt.datetime(y,m,d)+dt.timedelta(hours=h)
def lon(t,b): return swe.calc_ut(jd(t),b,F)[0]
def day(d):
    o=off(d); t0=dt.datetime(d.year,d.month,d.day)+dt.timedelta(hours=o)
    sr=fromjd(swe.rise_trans(jd(t0),swe.SUN,swe.CALC_RISE|swe.BIT_DISC_CENTER,TOR,0,0,swe.FLG_MOSEPH)[1][0])
    ss=fromjd(swe.rise_trans(jd(t0),swe.SUN,swe.CALC_SET|swe.BIT_DISC_CENTER,TOR,0,0,swe.FLG_MOSEPH)[1][0])
    seg=(ss-sr)/8; wd=d.weekday()  # Mon=0
    part={0:2,1:7,2:5,3:6,4:4,5:3,6:8}[wd]
    rk0=sr+seg*(part-1); rk1=rk0+seg
    # at 7:00 local
    t=dt.datetime(d.year,d.month,d.day,7)+dt.timedelta(hours=o)
    m=lon(t,swe.MOON)[0]; s=lon(t,swe.SUN)[0]
    n=int(m//(360/27)); ti=int(((m-s)%360)//12)+1
    # nakshatra end time
    tt=t; 
    while int(lon(tt,swe.MOON)[0]//(360/27))==n: tt+=dt.timedelta(minutes=10)
    # sign change today?
    sg=int(m//30); tc=t; ch=None
    while tc< t+dt.timedelta(hours=24):
        if int(lon(tc,swe.MOON)[0]//30)!=sg: ch=tc; break
        tc+=dt.timedelta(minutes=10)
    paksha='Waxing' if ti<=15 else 'Waning'; k=ti if ti<=15 else ti-15
    name='Purnima (full Moon)' if ti==15 else ('Amavasya (new Moon)' if ti==30 else TITHI[k-1])
    retro=[nm for nm,b in [('Mercury',swe.MERCURY),('Venus',swe.VENUS),('Mars',swe.MARS),('Jupiter',swe.JUPITER),('Saturn',swe.SATURN)] if lon(t,b)[3]<0]
    pos={nm:f"{SIGNS[int(lon(t,b)[0]//30)]} {lon(t,b)[0]%30:.0f}°" for nm,b in [('Sun',swe.SUN),('Mercury',swe.MERCURY),('Venus',swe.VENUS),('Mars',swe.MARS),('Jupiter',swe.JUPITER),('Saturn',swe.SATURN),('Rahu',swe.MEAN_NODE)]}
    L=lambda x:(x-dt.timedelta(hours=o)).strftime('%-I:%M %p')
    return dict(date=d.strftime('%a %d %b %Y'),moon_sign=SIGNS[sg],moon_deg=round(m%30,1),nak=NAKS[n],nak_ends=L(tt)+(' '+(tt-dt.timedelta(hours=o)).strftime('%a') if (tt-dt.timedelta(hours=o)).date()!=d else ''),
        moon_enters=(SIGNS[(sg+1)%12]+' at '+L(ch)+(' '+(ch-dt.timedelta(hours=o)).strftime('%a') if (ch-dt.timedelta(hours=o)).date()!=d else '')) if ch else None,
        tithi=f"{paksha} {name}" if ti not in (15,30) else name, tithi_no=ti, sunrise=L(sr), sunset=L(ss), rahu_kaal=f"{L(rk0)} to {L(rk1)}", retro=retro, pos=pos)
start=dt.date.fromisoformat(sys.argv[1]); n=int(sys.argv[2])
out=[day(start+dt.timedelta(days=i)) for i in range(n)]
print(json.dumps(out,indent=1))
