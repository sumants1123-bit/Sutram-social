#!/usr/bin/env python3
"""The sky at one moment, for 'The sky that day' cases and the real case inside a lesson.
Swiss Ephemeris, sidereal (Lahiri), mean node: the same settings as tools/sky.py. Engine values only.

    python3 tools/case_sky.py 2023-08-23T12:34Z ["label"]

Prints each graha's sign, degree and whether it walks backward, then what the Nadi rules see:
same room (rule 1), ahead and behind (rule 2), who walks in front (rule 3), face to face (rule 4),
looking back (rule 5: a graha walking backward also works from the sign behind it), family (signs 5 and 9 apart).
Also how long each slow pairing lasted, so a case never claims a common sky is rare."""
import swisseph as swe, datetime as dt, json, sys
F=swe.FLG_MOSEPH|swe.FLG_SIDEREAL|swe.FLG_SPEED
swe.set_sid_mode(swe.SIDM_LAHIRI)
SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
B=[('Sun',swe.SUN),('Moon',swe.MOON),('Mars',swe.MARS),('Mercury',swe.MERCURY),('Jupiter',swe.JUPITER),('Venus',swe.VENUS),('Saturn',swe.SATURN),('Rahu',swe.MEAN_NODE)]
CAST={'Sun':'the king','Moon':'the mother','Mars':'the soldier','Mercury':'the messenger','Jupiter':'the teacher','Venus':'the lover','Saturn':'the auditor','Rahu':'the magician','Ketu':'the monk'}
def jd(u): return swe.julday(u.year,u.month,u.day,u.hour+u.minute/60+u.second/3600)
def sky(u):
    out={}
    for nm,b in B:
        p=swe.calc_ut(jd(u),b,F)[0]
        out[nm]=dict(sign=int(p[0]//30),deg=round(p[0]%30,2),retro=(p[3]<0 and nm not in ('Sun','Moon','Rahu')))
    r=swe.calc_ut(jd(u),swe.MEAN_NODE,F)[0][0]
    out['Ketu']=dict(sign=int(((r+180)%360)//30),deg=round((r+180)%30,2),retro=False)
    return out
def rules(s):
    by={}
    for nm,v in s.items(): by.setdefault(v['sign'],[]).append(nm)
    for k in by: by[k].sort(key=lambda n:s[n]['deg'])
    R={'rooms':{SIGNS[k]:v for k,v in sorted(by.items())}}
    R['same_room']=[{'sign':SIGNS[k],'who':v,'in_front':v[-1]} for k,v in sorted(by.items()) if len(v)>1]
    R['face_to_face']=[{'a':SIGNS[k],'who_a':by[k],'b':SIGNS[(k+6)%12],'who_b':by[(k+6)%12]} for k in sorted(by) if (k+6)%12 in by and k<(k+6)%12]
    R['ahead']=[{'of':SIGNS[k],'who':by[k],'ahead_sign':SIGNS[(k+1)%12],'ahead':by[(k+1)%12]} for k in sorted(by) if (k+1)%12 in by]
    R['looking_back']=[{'who':nm,'in':SIGNS[v['sign']],'also_from':SIGNS[(v['sign']-1)%12],'meets_there':by.get((v['sign']-1)%12,[]),'faces_from_there':by.get((v['sign']+5)%12,[])} for nm,v in s.items() if v['retro']]
    R['family']=[{'signs':[SIGNS[k],SIGNS[(k+4)%12]],'who':[by[k],by[(k+4)%12]]} for k in sorted(by) if (k+4)%12 in by]
    return R
def span(u,test,step_h=6,limit_days=4000):
    """How long a condition has held around u: (start, end) as dates."""
    a=u
    while test(sky(a-dt.timedelta(hours=step_h))) and (u-a).days<limit_days: a-=dt.timedelta(hours=step_h)
    b=u
    while test(sky(b+dt.timedelta(hours=step_h))) and (b-u).days<limit_days: b+=dt.timedelta(hours=step_h)
    return a.date().isoformat(), b.date().isoformat()
def show(u,label=''):
    s=sky(u); print('##',label,u.strftime('%Y-%m-%d %H:%M UTC'))
    print('  '+' | '.join(f"{nm} {SIGNS[v['sign']]} {v['deg']:.1f}{' R' if v['retro'] else ''}" for nm,v in s.items()))
    R=rules(s)
    print('  same room:', '; '.join(f"{x['sign']}: {', '.join(x['who'])} (in front: {x['in_front']})" for x in R['same_room']) or 'none')
    print('  face to face:', '; '.join(f"{x['a']} {x['who_a']} <> {x['b']} {x['who_b']}" for x in R['face_to_face']) or 'none')
    print('  ahead:', '; '.join(f"{x['ahead']} in {x['ahead_sign']} ahead of {x['who']} in {x['of']}" for x in R['ahead']) or 'none')
    print('  looking back:', '; '.join(f"{x['who']} in {x['in']} also from {x['also_from']} (meets {x['meets_there']}, faces {x['faces_from_there']})" for x in R['looking_back']) or 'none')
    print('  family:', '; '.join(f"{x['signs'][0]} {x['who'][0]} ~ {x['signs'][1]} {x['who'][1]}" for x in R['family']) or 'none')
    return s,R
if __name__=='__main__':
    u=dt.datetime.fromisoformat(sys.argv[1].replace('Z','+00:00')).astimezone(dt.timezone.utc)
    show(u, sys.argv[2] if len(sys.argv)>2 else '')
