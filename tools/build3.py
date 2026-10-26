import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/7585c9d0-90d4-572f-bf7f-e3180b29fe46/scratchpad/thread')
from sutram_theme3 import *

def cta(lines):
    return ''.join(f'<div class="p" style="margin-top:6px">{l}</div>' for l in lines)

# ================= INTRO =================
I=[]
I.append(page(f'''
<div style="margin-top:40px">{moon(R=150, illum=1.0)}</div>
<div class="t" style="font-size:150px;line-height:.95;margin-top:10px">Who are you?</div>
<div class="ti" style="font-size:52px;line-height:1.2;margin-top:34px">The oldest question<br>Your birth chart is one honest way in</div>
''','Sutram · Start here', stars(seed=3)))
I.append(page(f'''
<div class="lab" style="margin-top:50px">What Sutram means</div>
<div class="t" style="font-size:170px;line-height:1;margin-top:26px">Thread</div>
<div style="margin-top:10px">{orbit(w=700,h=150,beads=5,tilt=-6)}</div>
<div class="ti" style="font-size:54px;line-height:1.2;margin-top:10px">“All this is strung on me,<br>like pearls on a thread”</div>
<div class="src" style="margin-top:22px">Bhagavad Gita 7.7</div>
<div class="p" style="margin-top:44px">Your chart shows the pearls<br>Philosophy points to the thread</div>
''','Sutram'))
def blk(lab,title,txt):
    return f'<div style="padding:36px 0"><div class="lab">{lab}</div><div class="t" style="font-size:66px;line-height:1.05;margin-top:18px">{title}</div><div class="p" style="margin-top:12px">{txt}</div></div>'
I.append(page(f'''
<div class="t" style="font-size:96px;line-height:1;margin-top:40px">Two old instruments<br>One question</div>
<div style="margin-top:30px;width:100%">
{blk('Philosophy','The question and the method','The Upanishads, the Tao, the Buddha, the Stoics')}
<div class="rule" style="margin:0 auto"></div>
{blk('Jyotish','The personal detail','Your own chart, read the classical way')}
</div>
<div class="ti" style="font-size:58px;margin-top:20px">Together, know yourself</div>
''','Sutram'))
def item(t,txt): return f'<div style="padding:20px 0"><div class="t" style="font-size:58px;line-height:1.05">{t}</div><div class="p" style="font-size:31px;margin-top:4px">{txt}</div></div>'
I.append(page(f'''
<div class="t" style="font-size:100px;line-height:1;margin-top:30px">Every day here</div>
<div class="rule" style="margin:34px auto 10px"></div>
{item('Today’s Sky','Each morning, the Moon, the lunar day and the hours to use')}
{item('Daily lesson','Jyotish from the ground up, with the classical sources')}
{item('The Thread','Every Wednesday, one idea from philosophy, read through your chart')}
{item('Vākya','A dated prediction each week, graded in public')}
{item('Big shifts','Major transits, explained for every Moon sign')}
''','Sutram'))
def step(n,t,txt): return f'<div style="padding:22px 0"><div class="ti" style="font-size:64px;line-height:1">{n}</div><div class="t" style="font-size:62px;line-height:1.05;margin-top:6px">{t}</div><div class="p" style="margin-top:8px">{txt}</div></div>'
I.append(page(f'''
<div class="t" style="font-size:100px;line-height:1;margin-top:30px">How to use this page</div>
<div class="rule" style="margin:34px auto 6px"></div>
{step('i','Get your chart','Free at sutram.ca, no card needed')}
{step('ii','Keep it open','Read each lesson with your own chart beside you')}
{step('iii','Join the Letter','Every Tuesday, one lesson read through your chart')}
''','Sutram'))
I.append(page(f'''
<div style="margin-top:-40px">{sun(R=95)}</div>
<div class="t" style="font-size:128px;line-height:.95;margin-top:-50px">Who is reading?</div>
<div class="ti" style="font-size:50px;line-height:1.25;margin-top:30px">Your chart shows the pearls<br>Philosophy points to the thread</div>
<div class="rule" style="margin:44px auto 26px"></div>
{cta(['Free chart at sutram.ca','Follow for the daily lesson'])}
''','Sutram'))
render('intro', I)

# ================= EPISODE 1 =================
E=[]
E.append(page(f'''
<div style="margin-top:120px">{orbit(w=760,h=170,beads=5,tilt=-8)}</div>
<div class="t" style="font-size:150px;line-height:1;margin-top:40px">Know yourself</div>
<div class="ti" style="font-size:54px;line-height:1.2;margin-top:30px">The first instruction, in every tradition</div>
<div class="p" style="margin-top:60px;font-size:30px;color:rgba(242,230,204,.6)">A weekly series on philosophy, astrology<br>and the question of who you are</div>
''','The Thread · Episode 1', stars(seed=11)))
E.append(page(f'''
<div class="lab" style="margin-top:80px">Greece · The temple at Delphi</div>
<div class="ti" style="font-size:150px;line-height:1;margin-top:46px;color:#F2E6CC">Know thyself</div>
<div class="p" style="margin-top:40px">Carved at the entrance to Apollo’s temple<br>Socrates built a whole life on it</div>
<div class="rule" style="margin:60px auto 46px"></div>
<div class="ti" style="font-size:62px;line-height:1.15">“The unexamined life<br>is not worth living”</div>
<div class="src" style="margin-top:26px">Plato, Apology 38a</div>
''','The Thread · Episode 1'))
def q(lab,text,src): return f'<div style="padding:34px 0"><div class="lab">{lab}</div><div class="ti" style="font-size:58px;line-height:1.15;margin-top:18px;color:#F2E6CC">“{text}”</div><div class="src" style="margin-top:16px">{src}</div></div>'
E.append(page(f'''
<div class="t" style="font-size:96px;line-height:1;margin-top:30px">The same words,<br>everywhere</div>
<div style="margin-top:24px;width:100%">
{q('The Upanishads','Know that one Self, and leave other words','Mundaka Upanishad 2.2.5')}
<div class="rule" style="margin:0 auto"></div>
{q('The Tao Te Ching','He who knows himself is intelligent','Chapter 33 · James Legge')}
<div class="rule" style="margin:0 auto"></div>
{q('The Sufis','Whoever knows himself knows his Lord','A saying the Sufis treasure')}
</div>''','The Thread · Episode 1'))
E.append(page(f'''
<div style="margin-top:50px">{chart(330)}</div>
<div class="lab" style="margin-top:56px">Your chart</div>
<div class="t" style="font-size:88px;line-height:1.05;margin-top:22px">The most personal map<br>you will ever hold</div>
<div class="p" style="margin-top:34px">The sky at the minute you were born, set out in twelve houses<br>Your body, drive, mind and joys, and when each comes forward</div>
''','The Thread · Episode 1'))
E.append(page(f'''
<div class="t" style="font-size:88px;line-height:1;margin-top:20px">How The Thread works</div>
<div class="ti" style="font-size:48px;margin-top:18px">One idea each week, in three steps</div>
<div class="rule" style="margin:26px auto 0"></div>
{step('i','The idea','What a tradition says about who you are')}
{step('ii','The mirror','Where that shows up in your chart')}
{step('iii','Your pattern','What your own chart says, and one question to ask yourself')}
''','The Thread · Episode 1'))
def row(icon,t,txt): return f'<div style="display:flex;align-items:center;gap:34px;padding:16px 0;text-align:left;width:780px">{icon}<div><div class="t" style="font-size:58px;line-height:1">{t}</div><div class="p" style="font-size:31px;margin-top:6px">{txt}</div></div></div>'
mini_moon=f'<div style="width:120px;display:flex;justify-content:center;margin:-60px -24px">{moon(R=34,illum=1.0)}</div>'
mini_sun=f'<div style="width:120px;display:flex;justify-content:center;margin:-60px -24px">{sun(R=34,rings=False)}</div>'
asc=f'<div style="width:72px;display:flex;justify-content:center">{asc_icon(78)}</div>'
E.append(page(f'''
<div class="t" style="font-size:120px;line-height:1;margin-top:20px">Find yours</div>
<div class="ti" style="font-size:52px;margin-top:20px">Open your chart and find three things</div>
<div style="margin-top:50px;display:flex;flex-direction:column;align-items:center">
{row(asc,'Your Ascendant','The body, how you meet the world')}
{row(mini_moon,'Your Moon','The mind, how you feel')}
{row(mini_sun,'Your Sun','The soul, what you’re here for')}
</div>
<div class="src" style="margin-top:34px;letter-spacing:.14em">Parashara read a chart from all three</div>
<div class="ti" style="font-size:58px;line-height:1.15;margin-top:40px">Which of the three feels most like you?</div>
''','The Thread · Episode 1'))
E.append(page(f'''
<div style="margin-top:100px">{orbit(w=700,h=150,beads=5,tilt=-6)}</div>
<div class="t" style="font-size:132px;line-height:.95;margin-top:30px">Who is reading?</div>
<div class="ti" style="font-size:50px;line-height:1.25;margin-top:30px">Your chart shows the pearls<br>Philosophy points to the thread</div>
<div class="rule" style="margin:44px auto 26px"></div>
{cta(['Free chart at sutram.ca','The Letter, every Tuesday'])}
<div class="src" style="margin-top:30px">Next Wednesday · Pearls on a thread</div>
''','The Thread · Episode 1'))
render('ep01', E)

# ================= LESSON 1 =================
L=[]
L.append(page(f'''
<div style="margin-top:-10px">{sun(R=88)}</div>
<div class="t" style="font-size:128px;line-height:.98;margin-top:-30px">What<br>How<br><span class="ti" style="font-size:136px">Where</span></div>
<div class="ti" style="font-size:50px;line-height:1.2;margin-top:28px">Every placement in your chart<br>has three parts</div>
''','Daily lesson · 01', stars(seed=21,ymax=700)))
def pl(n,t): return f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:14px 0;border-bottom:1px solid rgba(217,165,122,.22)"><span class="t" style="font-size:50px">{n}</span><span class="pi" style="font-size:31px">{t}</span></div>'
L.append(page(f'''
<div class="lab" style="margin-top:20px">What</div>
<div class="t" style="font-size:120px;line-height:1;margin-top:18px">The planet</div>
<div class="ti" style="font-size:50px;margin-top:14px">The actor, one part of you</div>
<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:70px;width:100%;margin-top:36px;text-align:left">
<div>{pl('Sun','self')}{pl('Moon','mind')}{pl('Mars','drive')}{pl('Mercury','thinking')}{pl('Jupiter','wisdom')}</div>
<div>{pl('Venus','love')}{pl('Saturn','patience')}{pl('Rahu','hunger')}{pl('Ketu','letting go')}</div>
</div>
<div class="src" style="margin-top:30px;letter-spacing:.14em">Rahu and Ketu are the Moon’s two shadow points</div>
''','Daily lesson · 01'))
def el(n,s,t): return f'<div style="padding:22px 0"><div class="lab">{n}</div><div class="t" style="font-size:46px;line-height:1.1;margin-top:12px">{s}</div><div class="pi" style="font-size:31px;margin-top:4px">{t}</div></div>'
L.append(page(f'''
<div class="lab" style="margin-top:20px">How</div>
<div class="t" style="font-size:120px;line-height:1;margin-top:18px">The sign</div>
<div class="ti" style="font-size:50px;margin-top:14px">The climate a planet lives in</div>
<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:50px;width:100%;margin-top:24px">
<div>{el('Fire','Aries, Leo, Sagittarius','quick, bold, direct')}{el('Earth','Taurus, Virgo, Capricorn','steady, practical')}</div>
<div>{el('Air','Gemini, Libra, Aquarius','thinking, connecting')}{el('Water','Cancer, Scorpio, Pisces','feeling, protecting')}</div>
</div>
<div class="ti" style="font-size:46px;line-height:1.25;margin-top:20px">Mars in Aries charges ahead<br>Mars in Cancer fights for home</div>
''','Daily lesson · 01'))
H=['Self, body','Money, family','Effort, courage','Home, peace','Children, creativity','Work, health','Partner, marriage','Change, secrets','Luck, teachers','Career, standing','Gains, friends','Loss, rest']
def hs(n,t): return f'<div style="display:flex;align-items:baseline;gap:18px;padding:13px 0;border-bottom:1px solid rgba(217,165,122,.2)"><span class="ti" style="font-size:44px;width:58px">{n}</span><span class="p" style="font-size:32px">{t}</span></div>'
L.append(page(f'''
<div class="lab" style="margin-top:20px">Where</div>
<div class="t" style="font-size:120px;line-height:1;margin-top:18px">The house</div>
<div class="ti" style="font-size:50px;margin-top:14px">The area of life where it plays out</div>
<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:60px;width:100%;margin-top:30px;text-align:left">
<div>{''.join(hs(i+1,H[i]) for i in range(6))}</div><div>{''.join(hs(i+1,H[i]) for i in range(6,12))}</div>
</div>''','Daily lesson · 01'))
L.append(page(f'''
<div class="t" style="font-size:104px;line-height:1;margin-top:20px">Read it as one sentence</div>
<div class="ti" style="font-size:48px;margin-top:20px">Planet, sign, house: what, how, where</div>
<div class="rule" style="margin:44px auto"></div>
<div class="t" style="font-size:78px;line-height:1.05">Mars in Leo in the 10th house</div>
<div style="margin-top:36px">
<div class="p"><span class="lab" style="margin-right:22px">What</span>Mars, your drive</div>
<div class="p" style="margin-top:10px"><span class="lab" style="margin-right:22px">How</span>Leo, proud and ready to lead</div>
<div class="p" style="margin-top:10px"><span class="lab" style="margin-right:22px">Where</span>10th house, your career</div>
</div>
<div class="ti" style="font-size:52px;line-height:1.2;margin-top:46px">Your drive acts with pride<br>and shows up in your work</div>
''','Daily lesson · 01'))
L.append(page(f'''
<div style="margin-top:30px">{moon(R=110, illum=1.0)}</div>
<div class="t" style="font-size:130px;line-height:1;margin-top:-10px">Try yours</div>
<div class="ti" style="font-size:52px;line-height:1.25;margin-top:26px">Find your Moon, its sign and its house<br>Write it as one sentence</div>
<div class="rule" style="margin:44px auto 26px"></div>
{cta(['Free chart at sutram.ca','The full course at learnsutram.com'])}
<div class="src" style="margin-top:30px">Next lesson · The Sun</div>
''','Daily lesson · 01'))
render('lesson01', L)

# ================= TODAY'S SKY Wed 28 Oct =================
def cell(l,v): return f'<div style="padding:12px 0"><div class="lab">{l}</div><div class="p" style="margin-top:10px;font-size:34px">{v}</div></div>'
S=[page(f'''
<div style="margin-top:-36px">{moon(R=128, illum=0.927, waxing=False)}</div>
<div class="t" style="font-size:112px;line-height:1;margin-top:-50px">Moon in Rohini</div>
<div class="ti" style="font-size:48px;margin-top:12px">Taurus 12°, where the Moon is strongest</div>
<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:40px;width:100%;margin-top:34px;border-top:1px solid rgba(217,165,122,.25);border-bottom:1px solid rgba(217,165,122,.25);padding:10px 0">
{cell('Lunar day','Waning 3rd, Tritiya')}{cell('Day ruler','Mercury, retrograde')}
{cell('Rahu Kaal, Toronto','1:00 to 2:18 PM')}{cell('Retrograde','Mercury, Venus, Saturn')}
</div>
<div style="display:grid;grid-template-columns:1.35fr 1fr;column-gap:40px;width:100%;margin-top:26px">
<div><span class="lab">Good for</span><div class="p" style="margin-top:8px;font-size:31px">steady work, planting,<br>cooking, beauty, family</div></div>
<div><span class="lab">Go slow on</span><div class="p" style="margin-top:8px;font-size:31px">new contracts<br>and launches</div></div></div>
''','Today’s Sky · Wednesday 28 October')]
render('sky-2026-10-28', S)
