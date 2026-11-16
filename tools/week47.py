#!/usr/bin/env python3
"""The week of 16 to 22 Nov 2026 (Sunday batch, 15 Nov 7 PM), in Sumant's 15 Nov format:
a pill naming the kind of post, a plain title and one line on every cover; one picture and one short line a slide;
captions of about 1,000 to 1,200 characters without part headers. Sky facts from the engine (tools/sky.py, Toronto time).
    python3 tools/week47.py            # writes specs/, captions/, x-drafts/ for all eleven posts
"""
import json, os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swisseph as swe
import sky
from zoneinfo import ZoneInfo
from philosophy import C, Pth, T, glow, ring
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = ZoneInfo('America/Toronto'); UTC = dt.timezone.utc
BODY = {'sun': swe.SUN, 'moon': swe.MOON, 'mars': swe.MARS, 'mercury': swe.MERCURY, 'jupiter': swe.JUPITER, 'venus': swe.VENUS, 'saturn': swe.SATURN}

def lon(kind, when):
    return swe.calc_ut(sky.jd(when.astimezone(UTC)), BODY[kind], sky.F)[0][0]

def series(kind, start, hours, n, unwrap_from=None):
    out = []
    for i in range(n):
        v = lon(kind, start + dt.timedelta(hours=hours * i))
        if unwrap_from is not None and v < unwrap_from: v += 360
        out.append(round(v, 3))
    return out

def labels(start, hours, n, fmt='%a %-d · %-I %p'):
    return [(start + dt.timedelta(hours=hours * i)).strftime(fmt) for i in range(n)]

def at(y, m, d, h=0, mi=0): return dt.datetime(y, m, d, h, mi, tzinfo=TZ)

# ---------- slide helpers ----------
def O(kind, r, **k): return dict(kind=kind, r=r, **k)
def R(sign, orbs=(), **k): return dict(sign=sign, orbs=list(orbs), **k)
SP = {'spacer': True, 'wide': 0.3}
def scene(rooms, w=340, h=226, **k): return dict(w=w, h=h, rooms=rooms, **k)
def cover(tag, title, sub, size=108, **vis):
    return dict(type='cover', kicker='Sutram', stars=True, swipe=True, tag=tag, title=title, titleclass='h1', titlesize=size,
                subtitle=sub, subsize=54, **vis)
def txt(title, closing=None, size=90, **vis):
    s = dict(type='text', title=title, titleclass='h2', titlesize=size, **vis)
    if closing: s.update(closing=closing, closingsize=56)
    return s
def steps(title, heads, size=62): return dict(type='nsteps', title=title, titleclass='h2', steps=[{'head': h} for h in heads], headsize=size, stepsmt=44)
def rows(title, items, orbs=None, size=58):
    s = dict(type='rows', title=title, titleclass='h2', items=items, namesize=size)
    if orbs: s['roworbs'] = orbs
    return s
def cta(title, nxt, orbs): return dict(type='cta', orbs=orbs, title=title, titleclass='h2', next=nxt)

P = []
def post(**p): P.append(p); return p

# ---------- engine facts used on the slides ----------
VEN = [('Virgo', round(lon('venus', at(2026, 11, d, 12)) - 150, 2)) for d in range(17, 22)] + [('Libra', round(lon('venus', at(2026, 11, 22, 12)) - 180, 2))]
VEN_NOW = round(lon('venus', at(2026, 11, 16, 12)) - 150, 2)
def deg_txt(x): d = int(x); m = int(round((x - d) * 60)); return f"{d}°{m:02d}′"
def leo(when): return {k: round(lon(k, when) - 120, 2) for k in ('jupiter', 'mars')}
KETU = lambda when: round(((swe.calc_ut(sky.jd(when.astimezone(UTC)), swe.MEAN_NODE, sky.F)[0][0] + 180) % 360) - 120, 2)
THU, FRI = at(2026, 11, 19, 12), at(2026, 11, 20, 12)
L19 = dict(leo(THU), ketu=KETU(THU)); L20 = dict(leo(FRI), ketu=KETU(FRI))
MOON_TAU = [('Aries' if v < 30 else 'Taurus', round(v if v < 30 else v - 30, 2)) for v in [lon('moon', at(2026, 11, 23, 12) + dt.timedelta(hours=6 * i)) for i in range(10)]]
MOON_DOOR = [('Pisces' if v >= 330 else 'Aries', round(v - 330 if v >= 330 else v, 2)) for v in [lon('moon', at(2026, 11, 20, 18) + dt.timedelta(hours=6 * i)) for i in range(7)]]

# 1. Monday 10 AM · Sutra: own sign
post(id='sutra-own-sign', when='2026-11-16T10:00:00-05:00', slides=[
    cover('Sutra', 'A graha in\nits own sign', 'At home: relaxed, steady, sure',
          scene=scene([R('Virgo'), R('Libra', [O('venus', 50)], state='focus', tag="Venus's own sign")], w=330, h=220),
          motion={'order': [0, 1], 'lift': 60, 'from': {'rooms': [R('Virgo', [O('venus', 50)]), R('Libra', state='focus', tag="Venus's own sign")]}}),
    rows('Who owns which sign', [['Sun', 'Leo'], ['Moon', 'Cancer'], ['Mars', 'Aries · Scorpio'], ['Mercury', 'Gemini · Virgo']],
         [O('sun', 30, rings=False), O('moon', 28), O('mars', 28), O('mercury', 26)]),
    rows('And the rest', [['Jupiter', 'Sagittarius · Pisces'], ['Venus', 'Taurus · Libra'], ['Saturn', 'Capricorn · Aquarius']],
         [O('jupiter', 32), O('venus', 30), O('saturn', 30)]),
    txt('At home, a graha\nacts with confidence', 'Like you in your own place', scene=scene([R('Libra', [O('venus', 58)], state='focus', tag='Home')], w=470, h=250)),
    txt('This month two\nare guests', 'Sun and Mars, in each other’s homes',
        scene=scene([R('Leo', [O('mars', 44)], state='focus', tag="Sun's home"), SP, R('Scorpio', [O('sun', 46, rings=False)], state='focus', tag="Mars's home")])),
    txt('Sunday, the lover\nwalks home', 'Venus enters Libra, her own sign',
        cross={'left': {'sign': 'Virgo', 'from': 27}, 'right': {'sign': 'Libra', 'to': 2}, 'kind': 'venus', 'r': 32, 'at': ['Virgo', VEN_NOW],
               'days': VEN, 'door': ['Sun 22 Nov', 'about 6:50 AM']}),
    txt('Make your space\nbeautiful', 'And make peace after a fight', size=96, orbs=[O('venus', 52)]),
    cta('A graha at home\ngives freely', 'Noon · Rule 6, family', [O('venus', 40), O('sun', 38, rings=False, dx=140)]),
], caption="""A graha in its own sign

Every graha owns one or two signs. The Sun owns Leo and the Moon owns Cancer. Mars owns Aries and Scorpio, Mercury owns Gemini and Virgo, Jupiter owns Sagittarius and Pisces, Venus owns Taurus and Libra, and Saturn owns Capricorn and Aquarius.

A graha in a sign it owns is at home. Think of yourself at home: relaxed, sure of yourself, in charge of the space. That is how the classics read it, and its results come with that same confidence.

This month the Sun and Mars stay in each other's homes: the Sun in Scorpio and Mars in Leo, from today until 15 December. Nadi reads a swap like that by sending each graha back home and reading it there.

On Sunday at about 6:50 AM the lover (Venus) walks home into Libra, her own sign. Comfort, taste and money talks get easier. A good week to make your space beautiful and to make peace after a fight.

Look at your own chart: which grahas sit in a sign they own?""",
    ask='Ask which of your grahas sit in their own sign, and what they give you, at asksutram.com',
    tags='#jyotish #vedicastrology #sutra #venus #sutram', x=None, xs=None)

# 2. Monday 12 PM · Lesson 16: Nadi rule 6, family
WATER = [R('Cancer'), R('Scorpio', [O('sun', 44, rings=False)], state='focus', names='Sun'), R('Pisces', [O('saturn', 40)], state='focus', names='Saturn')]
post(id='lesson16-family', when='2026-11-16T12:00:00-05:00', slides=[
    cover('Nadi rule 6', 'Grahas in\none family', 'Signs 5th and 9th apart act together',
          scene=scene(WATER, w=300, h=200, reach=[[1, 2, '']]), motion={'order': [1, 2, 0]}),
    txt('One element,\none family', 'Fire, earth, air, water: three signs each',
        scene=scene([R('Aries'), R('Leo', state='focus'), R('Sagittarius')], w=300, h=200, reach=[[0, 1, ''], [1, 2, '']], caption='The fire family')),
    txt('Family acts at\nabout 75 percent', 'Read them almost as one room',
        scene=scene([R('Scorpio', [O('sun', 44, rings=False)], state='focus'), SP, R('Pisces', [O('saturn', 40)], state='focus')], reach=[[0, 2, '75%', 'both']], reachpad=64)),
    steps('How to read it', ['Find the graha', 'Count 5 and 9 signs on', 'Who lives there?']),
    txt('From today: a\nwater family', 'The king in Scorpio, the auditor in Pisces', scene=scene(WATER, w=300, h=200, reach=[[1, 2, '']])),
    txt('Authority meets\nthe rulebook', 'Bosses check the details', size=96, orbs=[O('sun', 46, rings=False), O('saturn', 42, dx=150)]),
    txt('Friday, the mother\njoins them', 'Finish one duty, then rest',
        scene=scene([R('Scorpio', [O('sun', 42, rings=False)], state='focus'), SP, R('Pisces', [O('saturn', 36), O('moon', 34, dx=80)], state='focus', names='Saturn · Moon')], reach=[[0, 2, '']])),
    cta('Family signs\nact together', 'Tomorrow · Rule 7, helpers', [O('sun', 40, rings=False), O('saturn', 38, dx=140)]),
], caption="""Nadi rule 6: grahas in the same family

The twelve signs come in four families of three, one for each element. Fire: Aries, Leo, Sagittarius. Earth: Taurus, Virgo, Capricorn. Air: Gemini, Libra, Aquarius. Water: Cancer, Scorpio, Pisces. Family signs sit 5th and 9th from each other.

In Nadi, two grahas in one family act on each other at about 75 percent of the strength of sharing a sign, because they share an element (Jitender Kumar, Nadi Jyotisha, chapter 2). Read them almost as if they sat together.

To read it, find the graha, count 5 and 9 signs on, and see who lives there.

From today at about 9:15 AM the king (Sun) walks into Scorpio, a water sign. The auditor (Saturn) already sits in Pisces, also water. So the king and the auditor act as one family: authority meets the rulebook. Bosses check the details, offices ask for the right form, and work done properly gets noticed.

On Friday afternoon the mother (Moon) joins the auditor in Pisces, so feelings join the family too. Finish one duty, then rest.""",
    ask='Ask what the king and the auditor in one family mean for your work at asksutram.com',
    tags='#jyotish #bhrigunandinadi #nadiastrology #vedicastrology #sutram',
    x="""Nadi rule 6: grahas in one family

Signs 5th and 9th apart share an element and act on each other at about 75 percent. From today the Sun in Scorpio and Saturn in Pisces are one water family: authority meets the rulebook""", xs=[1, 3, 5, 6])

# 3. Tuesday 12 PM · Lesson 17: Nadi rule 7, helpers
LEO_LIB = [R('Leo', [O('mars', 34), O('jupiter', 38, dx=70)], state='focus', names='Mars · Jupiter'), SP, R('Libra', [O('mercury', 34)], state='focus', names='Mercury')]
post(id='lesson17-helpers', when='2026-11-17T12:00:00-05:00', slides=[
    cover('Nadi rule 7', 'The helpers:\n3rd and 11th', 'Grahas that push from across the chart',
          scene=scene(LEO_LIB, w=300, h=200, reach=[[0, 2, '3rd']], reachpad=60), motion={'order': [0, 2]}),
    txt('3rd is effort,\n11th is gains', 'Count from any graha',
        scene=scene([R('3rd', state='focus'), R('The graha', [O('mars', 40)]), R('11th', state='focus')], w=280, h=190)),
    txt('They help from\nthe other side', 'About half strength, some say a quarter', orbs=[O('mercury', 40), O('mars', 40, dx=150)]),
    steps('How to read it', ['Find the graha', 'Count 3 and 11 signs on', 'Who lives there?']),
    txt('This week:\nMercury in Libra', 'Libra is 3rd from Leo', scene=scene(LEO_LIB, w=300, h=200, reach=[[0, 2, '3rd']], reachpad=60)),
    txt('Words move effort\nand advice', 'The clear email gets the project going', size=96, orbs=[O('mercury', 44), O('jupiter', 46, dx=150)]),
    txt('From Libra, Leo\nis the 11th', 'The messenger gains from them', scene=scene(LEO_LIB, w=300, h=200, reach=[[2, 0, '11th']], reachpad=60)),
    cta('The 3rd and 11th\nare your helpers', 'Wednesday · Rule 8, swapped houses', [O('mercury', 36), O('mars', 36, dx=140), O('jupiter', 40, dx=140)]),
], caption="""Nadi rule 7: the helpers, 3rd and 11th

Count from any graha. The sign 3rd from it is effort, the push. The sign 11th from it is gains, what comes back. Grahas sitting there work on it from across the chart.

Nadi reads the 3rd and 11th with the 7th, the sign opposite: they all act on the graha from the other side. One Nadi book gives them half the strength of sharing a sign (Jitender Kumar, Nadi Jyotisha, chapter 3); another source puts the 3rd and 11th at a quarter. Either way, they help.

To read it, find the graha, count 3 and 11 signs on, and see who lives there.

This week the messenger (Mercury) walks through Libra. Libra is 3rd from Leo, where the soldier (Mars) and the teacher (Jupiter) sit. So the messenger helps them: words move effort and advice. The clear email gets the project going, and the mentor's tip turns into a plan.

From the other side, Leo is 11th from Libra: the messenger gains from the soldier and the teacher.""",
    ask='Ask which signs are your helpers, the 3rd and 11th from your Moon, at asksutram.com',
    tags='#jyotish #bhrigunandinadi #nadiastrology #vedicastrology #sutram',
    x="""Nadi rule 7: the helpers, 3rd and 11th

The 3rd from a graha is effort, the 11th is gains. This week Mercury in Libra is 3rd from Mars and Jupiter in Leo: words move effort and advice""", xs=[1, 2, 5, 6])

# 4. Wednesday 12 PM · Lesson 18: Nadi rule 8, swapped houses
SWAP = [R('Leo', [O('mars', 46)], state='focus', tag="Sun's sign"), SP, R('Scorpio', [O('sun', 48, rings=False)], state='focus', tag="Mars's sign")]
HOME = [R('Leo', [O('sun', 48, rings=False)], state='focus', tag='Home'), SP, R('Scorpio', [O('mars', 46)], state='focus', tag='Home')]
post(id='lesson18-swap', when='2026-11-18T12:00:00-05:00', slides=[
    cover('Nadi rule 8', 'Two grahas\nswap signs', 'Their stories tie together',
          scene=scene(SWAP, reach=[[0, 2, '', 'both']], reachpad=64), motion={'order': [0, 2]}),
    txt('Step 1: each sits in\nthe other’s sign', 'Sun in Scorpio, Mars in Leo', scene=scene(SWAP, reach=[[0, 2, '', 'both']], reachpad=64)),
    txt('Step 2: send\neach one home', 'Then read it there', scene=scene(HOME),
        motion={'order': [0, 2], 'lift': 74, 'from': {'rooms': SWAP}}),
    txt('Step 3: one step\nfurther', 'What one stands for pulls in the other',
        scene=scene([R('Father · boss', [O('sun', 46, rings=False)], state='focus'), SP, R('Brother · property', [O('mars', 44)], state='focus')], reach=[[0, 2, '', 'both']], reachpad=64)),
    rows('Where it shows', [['Home', 'Father and brother talk'], ['Work', 'The boss sees your push'], ['Papers', 'Property moves']],
         [O('sun', 28, rings=False), O('mars', 28), O('mars', 28)], size=54),
    txt('In your chart:\nany two lords swapped?', 'Find yours at asksutram.com', size=84, orbs=[O('sun', 40, rings=False), O('mars', 38, dx=150)]),
    cta('Swapped signs\ntie two stories', 'Thursday · Rule 9, stuck in the middle', [O('sun', 42, rings=False), O('mars', 40, dx=150)]),
], caption="""Nadi rule 8: two grahas swap signs

On Sunday we showed the Sun and Mars swapping signs: until 15 December the Sun sits in Scorpio, Mars's sign, and Mars sits in Leo, the Sun's sign. Here is the rule behind it, with one step further.

Step 1: each graha sits in the other's sign. Step 2: send each one home and read it there, the Sun in Leo and Mars in Scorpio. Step 3: go one step further.

When two grahas swap signs, what they stand for gets tied together, a karmic bond (Jitender Kumar, Nadi Jyotisha, chapter 5). The king (Sun) stands for the father, the boss and the government. The soldier (Mars) stands for brothers, property and courage. Tied together, they show up as a talk between father and brother, a boss who notices your hard push, or papers for a property or a car.

In your own chart, a swap means the lord of one sign sits in a second sign, and the lord of that second sign sits in the first.""",
    ask='Ask whether any two grahas swap signs in your chart at asksutram.com',
    tags='#jyotish #bhrigunandinadi #nadiastrology #vedicastrology #sutram',
    x="""Nadi rule 8: two grahas swap signs

The Sun in Scorpio and Mars in Leo, until 15 December. Send each one home to read it, then see what ties them: father and brother, the boss and your push, property papers""", xs=[1, 3, 4, 5])

# 5. Wednesday 6:30 PM · The Thread, Ep 4: the three strands
def rope(phase):
    import math
    out = []
    for s in range(3):
        pts = []
        for i in range(0, 25):
            x = 60 + i * 20; y = 260 + 70 * math.sin(i / 3.1 + phase + s * 2.094)
            pts.append(f"{x},{y:.1f}")
        out.append('M' + ' L'.join(pts))
    return out
RK = [rope(0), rope(2.1), rope(4.2), rope(6.283)]
STR = ['AMBER', 'SKY', 'ROSE']
ROPE = dict(w=600, h=520, k=1.1, els=[glow(300, 260, 260, [[0, {'opacity': .35}], [8, {'opacity': .35}]], 'anW')] + [
    dict(t='path', a={'fill': 'none', 'stroke': STR[s], 'stroke-width': 9, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'opacity': .92},
         k=[[0, {'d': RK[0][s]}], [2.67, {'d': RK[1][s]}], [5.33, {'d': RK[2][s]}], [8, {'d': RK[3][s]}]], e='lin') for s in range(3)])
post(id='thread-ep4-strands', when='2026-11-18T18:30:00-05:00', slides=[
    cover('The Thread', 'The three\nstrands of you', 'Clear, restless, heavy', anim=dict(ROPE, at=0, mt=30)),
    txt('Guna means\na strand', 'Three strands, one rope: you', anim=dict(ROPE, at=1.3, mt=0, mb=16)),
    txt('Clear: the king,\nthe mother, the teacher', 'Light and calm', size=84, orbs=[O('sun', 40, rings=False), O('moon', 38, dx=140), O('jupiter', 42, dx=140)]),
    txt('Restless: the\nmessenger, the lover', 'Wants more, keeps moving', size=84, orbs=[O('mercury', 38), O('venus', 40, dx=150)]),
    txt('Heavy: the soldier,\nthe auditor', 'Slows down, holds on', size=84, orbs=[O('mars', 40), O('saturn', 40, dx=150)]),
    rows('Today', [['Restless?', 'One thing, then walk'], ['Heavy?', 'Start small, move'], ['Clear?', 'Study and decide']], size=56),
    dict(type='quote', label='Bhagavad Gita 14.5', labelsize=34, quote='Clear, restless, heavy: born of nature, they bind the one in the body',
         quotesize=74, source='Sutram’s rendering'),
    txt('Read it in\nyour chart', 'Your rising lord and Moon: which strand?', size=96, orbs=[O('moon', 44)]),
    cta('Which strand runs\nstrongest in you?', 'Next Wednesday · Two birds, one tree', [O('sun', 36, rings=False), O('mercury', 34, dx=140), O('saturn', 36, dx=140)]),
], caption="""The three strands of you

In the Bhagavad Gita, Krishna tells Arjuna that three gunas, born of nature, bind the one who lives in the body (14.5). Guna means a strand of a rope. Three strands, twisted into one rope: you.

Clear (sattva) is light and calm. Restless (rajas) wants more and keeps moving. Heavy (tamas) slows down and holds on.

The classics give each graha a strand (Brihat Parashara Hora Shastra, chapter 3). Clear: the king (Sun), the mother (Moon) and the teacher (Jupiter). Restless: the messenger (Mercury) and the lover (Venus). Heavy: the soldier (Mars) and the auditor (Saturn).

A checklist for today. Restless? Do one thing at a time, then walk. Heavy? Start small and move your body. Clear? Use it: study and decide.

Read it in your chart: find the lord of your rising sign and your Moon in your free chart. Which strand do they belong to?

Which strand runs strongest in you? Tell us in the comments.""",
    ask='Ask which strand your rising lord and your Moon belong to at asksutram.com',
    tags='#bhagavadgita #gunas #jyotish #vedanta #sutram',
    x="""The three strands of you

The Gita's three gunas are strands of one rope (14.5). Clear: Sun, Moon, Jupiter. Restless: Mercury, Venus. Heavy: Mars, Saturn (BPHS, chapter 3). Which strand runs strongest in you?""", xs=[1, 3, 4, 5])

# 6. Thursday 10 AM · Sutra: exalted
post(id='sutra-exalted', when='2026-11-19T10:00:00-05:00', slides=[
    cover('Sutra', 'A graha\nat its best', 'Exalted: the sign where it shines most',
          scene=scene([R('Aries'), R('Taurus', [O('moon', 52)], state='focus', tag="Moon's best sign")], w=330, h=220),
          motion={'order': [0, 1], 'lift': 60, 'from': {'rooms': [R('Aries', [O('moon', 52)]), R('Taurus', state='focus', tag="Moon's best sign")]}}),
    rows('The best signs', [['Sun', 'Aries'], ['Moon', 'Taurus'], ['Mars', 'Capricorn'], ['Mercury', 'Virgo']],
         [O('sun', 30, rings=False), O('moon', 28), O('mars', 28), O('mercury', 26)]),
    rows('And the rest', [['Jupiter', 'Cancer'], ['Venus', 'Pisces'], ['Saturn', 'Libra']], [O('jupiter', 32), O('venus', 30), O('saturn', 30)]),
    txt('The sign across\nis its weakest', 'Moon best in Taurus, weakest in Scorpio',
        scene=scene([R('Taurus', [O('moon', 44)], state='focus', tag='Best'), SP, R('Scorpio', tag='Weakest')], reach=[[0, 2, '', 'both']], reachpad=64)),
    txt('Exalted is your\nbest day', 'Clear, generous, at full strength', size=96, orbs=[O('moon', 54)]),
    txt('Next week: the Moon\nin her best sign', 'Full in Taurus, Tuesday about 10 AM',
        cross={'left': {'sign': 'Aries', 'from': 25}, 'right': {'sign': 'Taurus', 'to': 30}, 'kind': 'moon', 'r': 30,
               'at': ['Taurus', round(lon('moon', at(2026, 11, 24, 9, 55)) - 30, 2)], 'days': MOON_TAU, 'door': ['Mon 23', 'about 9 PM']}),
    txt('Look in your chart', 'Any graha in its best sign?', size=104, orbs=[O('sun', 40, rings=False), O('moon', 38, dx=140)]),
    cta('Exalted means\nat its best', 'Noon · Rule 9, stuck in the middle', [O('moon', 42)]),
], caption="""A graha at its best: exalted

Every graha has one sign where it shines most, its exaltation. The Sun is exalted in Aries, the Moon in Taurus, Mars in Capricorn, Mercury in Virgo, Jupiter in Cancer, Venus in Pisces and Saturn in Libra (Brihat Parashara Hora Shastra, chapter 3). The sign straight across is where it is weakest, its debilitation.

Exalted is like you on your best day, clear and generous and at full strength.

Next week the mother (Moon) walks through Taurus, her best sign, from Monday night to Wednesday night. On Tuesday at about 10 AM she is full there, facing the king (Sun) in Scorpio. That full Moon is Kartik Purnima. A calm, kind mind: good for hosting, giving and talking things through.

Look at your own chart: does any graha sit in its sign of exaltation?""",
    ask='Ask which of your grahas are exalted and what that gives you at asksutram.com',
    tags='#jyotish #vedicastrology #sutra #fullmoon #sutram', x=None, xs=None)

# 7. Thursday 12 PM · Lesson 19: Nadi rule 9, stuck in the middle
post(id='lesson19-middle', when='2026-11-19T12:00:00-05:00', slides=[
    cover('Nadi rule 9', 'Stuck in\nthe middle', 'Hard grahas on both sides squeeze it',
          scene=scene([R('One side', [O('mars', 38)]), R('Its sign', [O('jupiter', 44)], state='focus'), R('Other side', [O('saturn', 38)])], w=270, h=188),
          motion={'order': [1, 0, 2]}),
    txt('The scissors of\nthe hard ones', 'Papakartari, by sign: 12th and 2nd',
        scene=scene([R('12th', [O('mars', 38)]), R('The graha', [O('jupiter', 44)], state='focus'), R('2nd', [O('saturn', 38)])], w=270, h=188)),
    txt('The hard ones', 'Sun, Mars, Saturn, Rahu, Ketu', size=104,
        orbs=[O('sun', 34, rings=False), O('mars', 32, dx=120), O('saturn', 32, dx=120), O('rahu', 32, dx=120), O('ketu', 32, dx=120)]),
    steps('How to read it', ['Find the graha', 'Look at both sides', 'Are both neighbours hard?']),
    txt('Right now in Leo,\nby degree', 'The teacher between the monk and the soldier',
        ruler={'sign': 'Leo', 'from': 0, 'to': 4, 'ticks': [[1, '1°'], [2, '2°'], [3, '3°']],
               'items': [{'kind': 'ketu', 'who': 'The monk', 'deg': L19['ketu'], 'd': deg_txt(L19['ketu']), 'r': 30},
                         {'kind': 'jupiter', 'who': 'The teacher', 'deg': L19['jupiter'], 'd': deg_txt(L19['jupiter']), 'r': 36},
                         {'kind': 'mars', 'who': 'The soldier', 'deg': L19['mars'], 'd': deg_txt(L19['mars']), 'r': 30}]}),
    txt('Advice gets\nsqueezed', 'Between quitting and fighting', size=100, orbs=[O('ketu', 38), O('jupiter', 46, dx=130), O('mars', 38, dx=130)]),
    txt('Give the wise\nvoice room', 'Decide slowly this week', size=100, orbs=[O('jupiter', 52)]),
    cta('Stuck in the middle\nmeans squeezed', 'Friday · Rule 10, the doorway', [O('ketu', 36), O('jupiter', 42, dx=130), O('mars', 36, dx=130)]),
], caption="""Nadi rule 9: stuck in the middle

When hard grahas sit on both sides of a graha, it gets squeezed. The classics call it papakartari, the scissors of the hard ones. The hard grahas are the king (Sun), the soldier (Mars), the auditor (Saturn), the magician (Rahu) and the monk (Ketu).

By sign, look at the sign behind a graha (the 12th from it) and the sign ahead of it (the 2nd). Inside one sign, Sutram also reads it by degree: who walks just behind and who walks just ahead.

To read it, find the graha, look at both sides, and check whether both neighbours are hard.

Right now in Leo the teacher (Jupiter) stands between the monk (Ketu) just behind him and the soldier (Mars) just ahead. Advice gets squeezed between quitting and fighting: the mentor caught between two tempers, the judge between two sides. Give the wise voice room and decide slowly.

The monk sits right at the door of Leo and backs out of it on 5 December.""",
    ask='Ask whether any graha in your chart is stuck between two hard ones at asksutram.com',
    tags='#jyotish #bhrigunandinadi #nadiastrology #vedicastrology #sutram',
    x="""Nadi rule 9: stuck in the middle

Hard grahas on both sides squeeze a graha. Right now in Leo the teacher (Jupiter) stands between the monk (Ketu) and the soldier (Mars): give the wise voice room""", xs=[1, 2, 5, 6])

# 8. Friday 12 PM · Lesson 20: Nadi rule 10, the doorway (strip cover: the Moon walks through the Pisces door)
S20 = at(2026, 11, 20, 18); N20 = 13
post(id='lesson20-doorway', when='2026-11-20T12:00:00-05:00', door_lon=360.0, slides=[
    cover('Nadi rule 10', 'Where water\nmeets fire', 'The doorway the classics call Gandanta', size=104,
          strip={'signs': ['Pisces', 'Aries'], 'days': labels(S20, 4, N20), 'track': {'moon': series('moon', S20, 4, N20, unwrap_from=300), 'saturn': series('saturn', S20, 4, N20)},
                 'day': 6, 'label': 'Sat 21 Nov, about 7:30 PM', 'owner': {'Pisces': 'Water', 'Aries': 'Fire'}, 'focus': ['Pisces', 'Aries'],
                 'names': {'moon': 'Moon', 'saturn': 'Saturn'}, 'r': {'moon': 40, 'saturn': 34}, 'lanes': {'moon': -1, 'saturn': 1}, 'lanegap': 62, 'h': 440, 'mt': 96}),
    txt('Three doorways', 'Cancer to Leo, Scorpio to Sagittarius, Pisces to Aries', size=104,
        scene=scene([R('Cancer'), R('Leo', state='focus')], w=330, h=220, reach=[[0, 1, '']])),
    txt('The knot', 'The last degrees of water, the first of fire', size=110, orbs=[O('moon', 44)]),
    steps('How to read it', ['Water or fire sign?', 'Near its end or start?', 'That is a doorway']),
    txt('Two stand in\nLeo’s doorway', 'The soldier walked out on Thursday night',
        ruler={'sign': 'Leo', 'from': 0, 'to': 4, 'ticks': [[1, '1°'], [2, '2°'], [3.333, '3°20′']],
               'items': [{'kind': 'ketu', 'who': 'The monk', 'deg': L20['ketu'], 'd': deg_txt(L20['ketu']), 'r': 30},
                         {'kind': 'jupiter', 'who': 'The teacher', 'deg': L20['jupiter'], 'd': deg_txt(L20['jupiter']), 'r': 36},
                         {'kind': 'mars', 'who': 'The soldier', 'deg': L20['mars'], 'd': deg_txt(L20['mars']), 'r': 30}]}),
    txt('Saturday night the\nMoon crosses', 'From Pisces into Aries, about 7:30 PM',
        cross={'left': {'sign': 'Pisces', 'from': 20}, 'right': {'sign': 'Aries', 'to': 10}, 'kind': 'moon', 'r': 30,
               'at': ['Pisces', round(lon('moon', at(2026, 11, 21, 12)) - 330, 2)], 'days': MOON_DOOR, 'door': ['Sat 21', 'about 7:30 PM']}),
    txt('Finish the old\nfirst', 'Then start the new', size=104, orbs=[O('moon', 44), O('jupiter', 44, dx=150)]),
    cta('Gandanta is\nthe doorway', 'Monday · Rule 11, whose star', [O('jupiter', 40), O('ketu', 34, dx=130)]),
], caption="""Nadi rule 10: the doorway, Gandanta

Three times around the zodiac a water sign ends and a fire sign begins: Cancer into Leo, Scorpio into Sagittarius, Pisces into Aries. The classics call these joints Gandanta, the knot. The last few degrees of the water sign and the first few of the fire sign make the doorway.

A graha in the doorway stands between two worlds: what is ending and what is starting get tangled. Go slow at the door.

To read it, check whether the graha sits in a water or a fire sign, then check whether it is near the end or the start of it.

This week the teacher (Jupiter) and the monk (Ketu) stand inside Leo's doorway, in its first few degrees. The soldier (Mars) walked out of it on Thursday night. On Saturday at about 7:30 PM the mother (Moon) crosses the Pisces doorway into Aries.

Finish the old before you start the new, like closing one tab before you open the next.""",
    ask='Ask whether any graha in your chart sits in a doorway at asksutram.com',
    tags='#jyotish #gandanta #nadiastrology #vedicastrology #sutram',
    x="""Nadi rule 10: the doorway

Where water meets fire: Cancer to Leo, Scorpio to Sagittarius, Pisces to Aries. This week Jupiter and Ketu stand in Leo's doorway, and on Saturday night the Moon crosses into Aries""", xs=[1, 2, 5, 6])

# 9. Friday 6:30 PM · Current sky: the Moon meets Saturn (strip cover)
S9 = at(2026, 11, 18, 6); N9 = 16
post(id='sky-2026-11-20', when='2026-11-20T18:30:00-05:00', door_lon=330.0, slides=[
    cover('Current sky', 'The Moon meets\nSaturn in Pisces', 'Friday afternoon, about 3:45 PM', size=100,
          strip={'signs': ['Aquarius', 'Pisces'], 'days': labels(S9, 6, N9), 'track': {'moon': series('moon', S9, 6, N9), 'saturn': series('saturn', S9, 6, N9)},
                 'day': 10, 'label': 'Fri 20 Nov', 'owner': {'Pisces': "Jupiter's sign"}, 'focus': ['Pisces'],
                 'names': {'moon': 'Moon', 'saturn': 'Saturn'}, 'r': {'moon': 40, 'saturn': 36}, 'lanes': {'moon': -1, 'saturn': 1}, 'lanegap': 62, 'h': 440, 'mt': 96, 'door': ['Pisces', 'Thu 2:30 PM']}),
    txt('One room,\nfull strength', 'The mind and duty, side by side',
        scene=scene([R('Pisces', [O('saturn', 44), O('moon', 42, dx=96)], state='focus', tag="Jupiter's sign", names='Saturn · Moon')], w=470, h=250)),
    txt('The Moon in Pisces', 'Soft, kind, a little dreamy', size=96, scene=scene([R('Pisces', [O('moon', 56)], state='focus')], w=470, h=250)),
    txt('Saturn in Pisces,\nwalking backward', 'The auditor rechecks old work', size=90, scene=scene([R('Pisces', [O('saturn', 52)], state='focus', note='◂ walking backward')], w=470, h=250)),
    txt('Together: a mood\nthat wants a job done', 'Feelings get serious and practical', size=84, orbs=[O('moon', 44), O('saturn', 44, dx=150)]),
    txt('The king is family', 'The Sun in Scorpio, water too: the boss backs the plan', size=100,
        scene=scene([R('Scorpio', [O('sun', 42, rings=False)], state='focus'), SP, R('Pisces', [O('saturn', 36), O('moon', 34, dx=80)], state='focus')], reach=[[0, 2, '']])),
    rows('This evening', [['Do', 'Finish one chore'], ['Call', 'Your mother'], ['Rest', 'Let the feeling be']], [O('saturn', 28), O('moon', 28), O('moon', 28)]),
    cta('Learn to read\nthe sky with Sutram', 'Sunday · The week ahead', [O('moon', 40), O('saturn', 38, dx=140)]),
], caption="""The Moon meets Saturn in Pisces

On Friday at about 3:45 PM Toronto time the mother (Moon) passes the auditor (Saturn) in Pisces. In Nadi two grahas in one sign act on each other at full strength, so the mind and duty sit in one room this afternoon.

The Moon in Pisces is soft, kind and a little dreamy. Pisces is the teacher's (Jupiter's) sign.

Saturn in Pisces has been walking backward since July and turns forward again on 10 December. Walking backward, the auditor rechecks old work.

Together they make a heavy mood that wants one job done. Feelings get serious and practical.

The king (Sun) sits in Scorpio, another water sign, so he is family (rule 6): the boss backs the plan.

This evening, finish one chore, call your mother, and let a feeling be instead of rushing to fix it.""",
    ask='Ask what the Moon meeting Saturn means for your Moon sign at asksutram.com',
    tags='#jyotish #moon #saturn #vedicastrology #sutram',
    x="""The Moon meets Saturn in Pisces

Friday about 3:45 PM Toronto: the mind and duty in one room, with the Sun in Scorpio as family. Finish one chore, call your mother, let the feeling be""", xs=[1, 2, 5, 7])

# 10. Saturday 10 AM · Avatars and grahas 1: Rama, the Sun
SUNRISE = dict(w=600, h=520, k=1.1, els=[
    glow(300, 330, 300, [[0, {'opacity': 0}], [3.5, {'opacity': .9}], [8, {'opacity': .9}]], 'anG'),
    dict(t='circle', a={'cx': 300, 'cy': 330, 'r': 84, 'fill': 'url(#anS)'}, k=[[0, {'ty': 120, 'opacity': 0}], [4.2, {'ty': 0, 'opacity': 1}], [8, {'ty': 0, 'opacity': 1}]], e='out'),
    Pth('M40,420 L560,420', stroke='GOLD', **{'stroke-width': 3, 'stroke-opacity': .8})])
post(id='avatar-rama-sun', when='2026-11-21T10:00:00-05:00', slides=[
    cover('Avatars and grahas', 'Rama is\nthe Sun', 'Why the old texts pair two kings', anim=dict(SUNRISE, at=7.5, mt=30)),
    txt('Nine avatars,\nnine grahas', 'Parashara pairs them, one by one', size=100, orbs=[O('sun', 40, rings=False), O('moon', 36, dx=130), O('mars', 34, dx=120)]),
    txt('Rama kept his\nfather’s word', 'He left his throne to keep it', size=100, anim=dict(SUNRISE, at=7.5, mt=0, mb=16)),
    txt('The Sun is the king,\nthe father, the soul', 'The light that shines on all alike', size=84, orbs=[O('sun', 58, rings=False)]),
    txt('Your Sun’s house', 'Where you lead and keep your word', size=104, orbs=[O('sun', 50, rings=False)]),
    txt('Try it today', 'Keep one promise, to someone or to yourself', size=112),
    cta('Rama is the Sun', 'Next Saturday · Krishna, the Moon', [O('sun', 46, rings=False)]),
], caption="""Rama is the Sun

Parashara says Vishnu took form through the grahas: Rama from the Sun, Krishna from the Moon, Narasimha from Mars, Buddha from Mercury, Vamana from Jupiter, Parashurama from Venus, Kurma from Saturn, Varaha from Rahu and Matsya from Ketu (Brihat Parashara Hora Shastra, chapter 2).

Why Rama for the Sun? In Jyotish the Sun is the king of the grahas, the father and the soul (Brihat Parashara Hora Shastra, chapter 3). Rama was the king who left his throne to keep his father's word, and he ruled by dharma, the right way, the way the Sun gives light to all alike.

In your chart, the house of your Sun shows where you are asked to lead and to keep your word. That is Sutram's reading, built on the classical meanings.

Try it today, and keep one promise, to someone else or to yourself.

Every Saturday morning, one avatar and one graha. Next week: Krishna, the Moon.""",
    ask="Ask what your Sun's house asks of you at asksutram.com",
    tags='#rama #jyotish #sun #vedicastrology #sutram',
    x="""Rama is the Sun

Parashara pairs nine avatars with nine grahas (BPHS, chapter 2). Rama, the king who kept his father's word, is the Sun: the king, the father, the soul. Keep one promise today""", xs=[1, 2, 3, 6])

# 11. Sunday 6:30 PM · Week ahead, 23 to 29 Nov (strip cover: the Moon walks into Taurus)
S11 = at(2026, 11, 22, 6); N11 = 15
post(id='week-2026-11-22', when='2026-11-22T18:30:00-05:00', door_lon=30.0, slides=[
    cover('Week ahead', 'A full Moon\nin Taurus', 'Tuesday, the Moon at her best', size=104,
          strip={'signs': ['Aries', 'Taurus'], 'days': labels(S11, 6, N11), 'track': {'moon': series('moon', S11, 6, N11)},
                 'day': 9, 'label': 'Full Moon, Tue 24 Nov', 'owner': {'Taurus': "Moon's best sign"}, 'focus': ['Taurus'],
                 'names': {'moon': 'Moon'}, 'r': {'moon': 44}, 'h': 440, 'mt': 96, 'door': ['Taurus', 'Mon 9 PM']}),
    txt('Face to face', 'The Moon in Taurus, the Sun in Scorpio', size=110,
        scene=scene([R('Taurus', [O('moon', 48)], state='focus'), SP, R('Scorpio', [O('sun', 46, rings=False)], state='focus')], reach=[[0, 2, '', 'both']], reachpad=64)),
    txt('Exalted Moon:\na calm, kind mind', 'Good for hosting and giving', size=90, orbs=[O('moon', 56)]),
    txt('Venus is home\nin Libra', 'Comfort and money talks come easier', size=96, scene=scene([R('Libra', [O('venus', 54)], state='focus', tag='Her own sign')], w=470, h=250)),
    txt('Friday night, the\nMoon goes home', 'Into Cancer, her own sign', size=90, scene=scene([R('Gemini'), R('Cancer', [O('moon', 48)], state='focus', tag='Her own sign')], w=330, h=220)),
    rows('Mark these', [['Mon', 'Moon into Taurus, night'], ['Tue', 'Full Moon, about 10 AM'], ['Fri', 'Moon into Cancer, night']],
         [O('moon', 28), O('moon', 30), O('moon', 28)], size=56),
    txt('Kartik Purnima', 'Light a lamp, give something away', size=110, orbs=[O('moon', 50)]),
    cta('Learn to read\nthe sky with Sutram', 'Monday · Rule 11, whose star', [O('moon', 44), O('venus', 38, dx=140)]),
], caption="""Week ahead: a full Moon in Taurus

On Monday night at about 9 PM the mother (Moon) walks into Taurus, her best sign. On Tuesday at about 10 AM Toronto time she is full there, facing the king (Sun) in Scorpio. Grahas face to face act on each other directly (rule 4), so the mind and the self meet in full light. This full Moon is Kartik Purnima.

An exalted Moon reads as a calm, kind mind: good for hosting, giving and talking things through.

The lover (Venus) has been home in Libra since Sunday morning, so comfort, taste and money talks come easier all week.

On Friday night the Moon goes home to Cancer, her own sign, and the weekend feels softer and closer to family.

On Kartik Purnima the tradition is to light a lamp and give something away.

So mark Monday night for the Moon into Taurus, Tuesday about 10 AM for the full Moon, and Friday night for the Moon into Cancer.""",
    ask='Ask what the full Moon in Taurus means for your Moon sign at asksutram.com',
    tags='#fullmoon #kartikpurnima #jyotish #vedicastrology #sutram',
    x="""Week ahead: a full Moon in Taurus

Tuesday about 10 AM Toronto, Kartik Purnima: the Moon at her best, facing the Sun in Scorpio. Venus home in Libra all week. Light a lamp, give something away""", xs=[1, 2, 4, 6])

def write(p):
    spec = {'id': p['id'], 'kicker': 'Sutram', 'decor_theme': 'thread', 'slides': p['slides']}
    json.dump(spec, open(os.path.join(REPO, 'specs', p['id'] + '.json'), 'w'), ensure_ascii=False, indent=1)
    cap = p['caption'].strip() + '\n\n' + p['ask'] + '\nWeekly newsletter: sutram.ca/newsletter\n\n' + p['tags'] + '\n'
    open(os.path.join(REPO, 'captions', p['id'] + '.txt'), 'w').write(cap)
    if p.get('x'):
        open(os.path.join(REPO, 'x-drafts', p['id'] + '-x.txt'), 'w').write(p['x'].strip() + '\n\nasksutram.com\nsutram.ca/newsletter\n')

if __name__ == '__main__':
    only = sys.argv[1:]
    for p in P:
        if not only or p['id'] in only: write(p)
    json.dump([{k: p.get(k) for k in ('id', 'when', 'xs', 'door_lon')} for p in P], open(os.path.join(REPO, 'plan', 'week47.json'), 'w'), indent=1)
    print(len(P), 'posts written')
