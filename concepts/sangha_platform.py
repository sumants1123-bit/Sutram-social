import sys; sys.path.insert(0,'tools')
from app_post import FONTS
from playwright.sync_api import sync_playwright
O='#F2793A'
def sec(t,items): return f'<div class="sec">{t}</div>'+''.join(f'<div class="ch{" on" if a=="on" else ""}">{b}</div>' for a,b in items)
nav=(sec('START HERE',[('','# welcome'),('','# introduce-yourself')])+
 sec('COMMON ROOM',[('','# today-sky <i>auto</i>'),('','# ask-the-sangha'),('','# wins-and-stories')])+
 sec('JYOTISH LAB',[('on','# chart-clinic'),('','# transits-now <i>auto</i>'),('','# vakya-predictions'),('','# muhurta-help')])+
 sec('PHILOSOPHY',[('','# the-thread'),('','# gita-verse-of-the-week')])+
 sec('PRACTICE',[('','# daily-sadhana'),('','# ekadashi-and-new-moon')])+
 sec('SALON',[('','# chess-arena'),('','# book-club')])+
 sec('CHAPTER ROOMS · BY YOUR CHART',[('','♄ The Saturn years'),('','Sade Sati'),('','♃ Jupiter in Leo <i>sky room</i>')])+
 sec('COURSES',[('','▸ Foundations · free'),('','▸ Read your chart · Nov cohort'),('','▸ Nadi rules')])+
 sec('LIVE',[('','◉ Talks and masterclasses'),('','◉ Study rooms · 2 open')])+
 sec('CIRCLES',[('','Circle 7 · Learners · Toronto time')]))
def dia(): return '<svg width="150" height="150" viewBox="-4 -4 168 168"><rect width="160" height="160" fill="none" stroke="rgba(254,250,241,.4)" stroke-width="2"/><path d="M0 0L160 160M160 0L0 160M80 0L160 80L80 160L0 80Z" fill="none" stroke="rgba(254,250,241,.4)" stroke-width="2"/><path d="M120 40L160 80L120 120L80 80Z" fill="#F2793A" opacity=".8"/></svg>'
def msg(who,tag,time,body,extra=''):
    return f'<div class="msg"><div class="av">{who[0]}</div><div><div class="who">{who}<span class="tag">{tag}</span><span class="tm">{time}</span></div><div class="bd">{body}</div>{extra}</div></div>'
center=f'''<div class="chh"># chart-clinic <span class="mu">Jyotish Lab · read a chart, make a dated call, the engine grades it</span></div>
<div class="pin"><div class="lab">📌 CLINIC 12 · OPENED BY SUTRAM AT 9:00 AM</div><div style="display:flex;gap:26px;align-items:center">{dia()}<div class="bd" style="font-size:24px">A teaching chart, shared with consent.<br>Question: <b>when does this person change careers?</b><br><span class="mu">Make your call by Friday. Grades and the answer go up on Sunday.</span></div></div></div>
{msg('Meera','Student','10:14 AM','Spring 2027. The 10th lord’s sub-period starts then, and Jupiter crosses the 10th.','<div class="lock">🔒 Call locked · graded Sunday</div>')}
{msg('Ravi','Practitioner','10:40 AM','I’d say late 2026: Saturn’s pressure on the 10th peaks first.','<div class="lock">🔒 Call locked · graded Sunday</div>')}
{msg('Sutram Guide','AI','10:41 AM','Fact check: the 10th lord’s sub-period begins 14 March 2027. Both readings use real dates; the call is yours.')}
<div class="comp">Write your reading…<span class="mu" style="float:right">Attach my chart: off</span></div>'''
right=f'''<div class="card"><div class="lab">LIVE AND UPCOMING</div>
<div class="ev"><div><b>Study room</b><br><span class="mu">Open now · 6 studying · 25-minute rounds</span></div><span class="btn o">Join</span></div>
<div class="ev"><div><b>Live talk with Sumant</b><br><span class="mu">Fri 20 Nov, 8 PM · 54 going</span></div><span class="btn">RSVP</span></div>
<div class="ev"><div><b>Masterclass: Muhurta</b><br><span class="mu">Guest astrologer · Sat 29 Nov · CA$40</span></div><span class="btn">Ticket</span></div>
<div class="ev" style="border:0"><div><b>Live text hour</b><br><span class="mu">Every Wednesday, 8 PM · run by the Guide</span></div></div></div>
<div class="card"><div class="lab">YOUR COURSE</div><div class="bd"><b>Read your chart</b> · November cohort</div><div class="mu" style="margin:4px 0 10px">Lesson 3 of 8 · next one unlocks Monday · 23 in your cohort</div><div class="prog"><i style="width:38%"></i></div><span class="btn o">Continue</span></div>
<div class="card"><div class="lab">YOUR CIRCLE</div><div class="bd"><b>Circle 7</b> · 6 learners · Thursday 7 PM</div><div class="mu">Agenda posted by the Guide: recap lesson 3, read one chart together</div></div>
<div class="card"><div class="lab">RUNS BY ITSELF TODAY</div>
<div class="log">✓ 6:00 AM · today’s sky posted in # today-sky</div><div class="log">✓ 7:12 AM · Guide answered 3 open questions</div><div class="log">✓ 9:00 AM · Clinic 12 opened</div><div class="log">◷ 6:00 PM · reminders sent for Circle 7</div><div class="log">◷ Sunday · clinic grades, the week’s digest, talk recording filed in the Library</div></div>'''
H=f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:2200px;background:#07060A;color:#FEFAF1;font-family:Inter;font-size:22px;padding-bottom:30px}}
.top{{display:flex;justify-content:space-between;align-items:center;padding:22px 34px;border-bottom:1px solid rgba(254,250,241,.1);background:radial-gradient(ellipse 50% 140% at 50% 0%,rgba(242,121,58,.14),transparent 70%)}}
.brand{{font-family:'Instrument Serif';font-size:44px}}.brand b{{color:{O};font-weight:400}}
.srch{{width:600px;padding:12px 20px;border-radius:14px;border:1px solid rgba(254,250,241,.15);color:rgba(254,250,241,.5);font-size:20px}}
.pill{{border:1.5px solid {O};color:{O};border-radius:99px;padding:8px 20px;font-weight:600;font-size:18px;letter-spacing:.1em}}
.grid{{display:grid;grid-template-columns:380px 1100px 612px;gap:24px;padding:0 30px}}
.nav{{border-right:1px solid rgba(254,250,241,.08);padding:14px 10px 0 4px}}.sec{{font-size:14px;font-weight:600;letter-spacing:.16em;color:rgba(254,250,241,.45);margin:16px 0 4px 14px}}
.ch{{padding:6px 14px;border-radius:10px;font-size:20px;color:rgba(254,250,241,.8)}}.ch.on{{background:rgba(242,121,58,.16);color:#FEFAF1;border:1px solid rgba(242,121,58,.5)}}.ch i{{font-style:normal;font-size:13px;color:{O};margin-left:6px}}
.chh{{font-size:30px;font-weight:600;padding:22px 0 16px;border-bottom:1px solid rgba(254,250,241,.08)}}.mu{{color:rgba(254,250,241,.58);font-size:19px;font-weight:400}}
.pin{{margin:20px 0;padding:22px 26px;border-radius:20px;background:rgba(242,121,58,.08);border:1px solid rgba(242,121,58,.4)}}
.lab{{font-size:15px;font-weight:600;letter-spacing:.16em;color:{O};margin-bottom:12px}}
.msg{{display:flex;gap:18px;padding:18px 0;border-bottom:1px solid rgba(254,250,241,.06)}}.av{{flex:0 0 52px;height:52px;border-radius:50%;background:#2A2230;display:flex;align-items:center;justify-content:center;font-weight:600;color:{O}}}
.who{{font-weight:600;font-size:20px}}.tag{{font-size:13px;color:#F28A4E;border:1px solid rgba(242,121,58,.5);border-radius:99px;padding:2px 9px;margin-left:10px}}.tm{{font-size:15px;color:rgba(254,250,241,.45);margin-left:10px;font-weight:400}}
.bd{{font-size:21px;line-height:1.42;margin-top:4px}}.lock{{display:inline-block;margin-top:8px;font-size:16px;color:#A8E0B2;border:1px solid rgba(123,196,138,.5);border-radius:99px;padding:4px 12px}}
.comp{{margin-top:18px;padding:18px 22px;border-radius:16px;border:1px solid rgba(254,250,241,.16);color:rgba(254,250,241,.5)}}
.card{{background:#110F15;border:1px solid rgba(254,250,241,.1);border-radius:20px;padding:20px 24px;margin-top:22px}}
.ev{{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:12px 0;border-bottom:1px solid rgba(254,250,241,.07);font-size:20px;line-height:1.35}}
.btn{{display:inline-block;padding:8px 18px;border-radius:99px;border:1px solid rgba(254,250,241,.3);font-size:17px;white-space:nowrap;margin-top:10px}}.ev .btn{{margin:0}}.btn.o{{background:{O};border-color:{O};color:#160A04;font-weight:600}}
.prog{{height:10px;border-radius:5px;background:rgba(254,250,241,.12);overflow:hidden}}.prog i{{display:block;height:100%;background:{O}}}
.log{{font-size:18px;padding:6px 0;color:rgba(254,250,241,.85)}}
.foot{{margin:24px 34px 0;padding-top:20px;border-top:1px solid rgba(254,250,241,.12);font-size:24px;line-height:1.45}}.foot b{{color:{O}}}
</style></head><body>
<div class="top"><div class="brand">Sutram <b>Sangha</b></div><div class="srch">Search rooms, lessons, talks… or ask Sutram</div><div class="pill">CONCEPT · SAMPLE DATA</div></div>
<div class="grid"><div class="nav">{nav}</div><div>{center}</div><div>{right}</div></div>
<div class="foot"><b>Rooms and channels</b> by pillar · <b>courses</b> with monthly cohorts · <b>live talks</b> and ticketed masterclasses · <b>study rooms</b> and Circles · <b>chapter rooms</b> set by your chart · an <b>automated staff</b> (sky posts, AI Guide answers, cohort drip, reminders, grading, recordings, digest) so it runs without you</div>
</body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':2200,'height':1300}); pg.set_content(H); pg.wait_for_timeout(300)
    pg.screenshot(path='concepts/sangha-platform.jpg',type='jpeg',quality=90,full_page=True); b.close()
from PIL import Image; im=Image.open('concepts/sangha-platform.jpg'); print(im.size); im.resize((1100,int(im.size[1]/2))).save('/tmp/claude-0/-home-claude/7585c9d0-90d4-572f-bf7f-e3180b29fe46/scratchpad/plat-small.jpg')
