import sys; sys.path.insert(0,'tools')
from app_post import FONTS
from playwright.sync_api import sync_playwright
O='#F2793A'
def dia(hl,op,label):
    return f'<svg width="150" height="150" viewBox="-4 -4 168 168"><rect width="160" height="160" fill="none" stroke="rgba(254,250,241,.35)" stroke-width="2"/><path d="M0 0L160 160M160 0L0 160M80 0L160 80L80 160L0 80Z" fill="none" stroke="rgba(254,250,241,.35)" stroke-width="2"/><path d="M120 40L160 80L120 120L80 80Z" fill="{hl}" opacity="{op}"/><text x="112" y="86" fill="#FEFAF1" font-size="15" font-family="Inter">{label}</text></svg>'
def phone(body,tab):
    tabs=''.join(f'<span class="{"on" if t==tab else ""}">{t}</span>' for t in ['Today','Learn','Rooms','Ask','You'])
    return f'<div class="ph"><div class="sb"><span>9:41</span><span>Sutram</span><span>●●●</span></div><div class="in">{body}</div><div class="tabs">{tabs}</div></div>'
s1=f'''<div class="s" style="font-size:40px;margin-top:10px">Good morning, Asha</div><div class="m">Mon 9 Nov · Toronto</div>
<div class="c"><div class="l">MORNING SKY · EVERYONE</div><div class="s" style="font-size:30px">Mars walks into Leo on Thursday</div><div class="b" style="margin-top:6px">Where do you need to push this week?</div><div class="m" style="margin-top:4px">31 answers</div>
<div class="fy"><div class="l">🔒 FOR YOU</div><div class="b">It lands in your 10th house: work and reputation</div><span class="btn o">Teach me</span><span class="btn">Ask why</span></div></div>
<div class="c"><div class="l">YOUR ROOM</div><div class="b">The Saturn years · <span style="color:{O}">3 new</span></div><div class="m">Meera: “Finally passed, third try”</div></div>
<div class="c"><div class="l">READ YOUR OWN CHART</div><div class="b" style="margin-bottom:8px">7 of 12 parts · next: your 10th house</div><div class="prog"><i style="width:58%"></i></div></div>'''
s2=f'''<div class="m" style="margin-top:10px">← Today</div><div class="s" style="font-size:38px;margin-top:4px">Your 10th house</div><div class="m">Lesson 9 · 4 minutes</div>
<div style="display:flex;justify-content:space-around;margin-top:14px;text-align:center"><div>{dia(O,.85,"Pis")}<div class="m">Yours</div></div><div>{dia('#9AA0B5',.4,"Vir")}<div class="m">Reference</div></div></div>
<div class="b" style="margin-top:12px">The 10th is your work and how people see you. Its lord shows how the work gets done.</div>
<div class="c"><div class="l">CHECK YOURSELF</div><div class="b">Who rules your 10th house?</div><span class="opt ok">Jupiter ✓</span><span class="opt">Saturn</span><span class="opt">Venus</span><div class="m" style="margin-top:8px;color:#A8E0B2">Correct. Jupiter, sitting in Cancer</div></div>
<div class="c"><div class="b" style="margin-bottom:8px">Read your own chart: 8 of 12</div><div class="prog"><i style="width:67%"></i></div><span class="btn">Discuss · 18</span><span class="btn">Ask a follow-up</span></div>'''
s3=f'''<div class="s" style="font-size:38px;margin-top:10px">The Saturn years</div><div class="m">Everyone in Saturn's 19-year chapter · 38 here<br>You're in year 6 of 19</div>
<div class="c" style="border-color:rgba(242,121,58,.45)"><div class="l">THIS WEEK · FROM SUTRAM</div><div class="b">What has Saturn asked you to finish?</div></div>
<div class="post"><div class="who">Meera<span class="badge">Student</span></div><div class="b">Finally passed my CA exams, third try. Year 4 of Saturn</div><div class="m">♥ 42 · 9 replies</div></div>
<div class="post"><div class="who">Ravi<span class="badge">Practitioner</span></div><div class="b">Saturn chapter plus Sade Sati together. How do you pace work?</div><div class="m">Sutram Guide · AI answered in 12 min · 4 replies</div></div>
<div class="c" style="margin-top:12px"><div class="m">Share with the room… your chart stays private</div></div>
<div class="m" style="margin-top:12px">Also yours: Sade Sati · Jupiter in Leo (sky room) · Learner circle</div>'''
wk=[('Mon','Vākya: this week’s sealed prediction'),('Wed','The Thread: live text hour, 8 PM'),('Thu','Mars into Leo: sky room opens'),('Fri','Chart clinic: make your dated call'),('Sun','Week ahead and the digest'),('20 Nov','Live talk with Sumant')]
s4=f'''<div class="s" style="font-size:38px;margin-top:10px">Your week</div><div class="m">The Sangha's rhythm follows the sky</div>
<div class="c">{''.join(f'<div class="wk"><b>{d}</b><span>{t}</span></div>' for d,t in wk)}</div>
<div class="c"><div class="l">YOUR PROGRESS</div><div class="wk"><span>Calls graded</span><span style="margin-left:auto">5 of 8 right</span></div><div class="wk"><span>Streak</span><span style="margin-left:auto">12 days</span></div><div class="wk" style="border:0"><span>Level</span><span style="margin-left:auto">Student → Practitioner at 20 calls</span></div></div>
<div class="c" style="border-color:rgba(242,121,58,.45)"><div class="b">Rhythm+ adds the family room, every clinic and your Year Ahead</div></div>'''
caps=[('1 · Today','The sky post everyone sees, plus one private line for your chart'),('2 · Teach me','Each lesson uses your own chart, beside a reference chart, and checks you'),('3 · Your room','People in the same dasha chapter, sharing what they live through'),('4 · Your week','A rhythm set by the sky: predictions, clinics, rooms, a monthly talk')]
H=f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:2200px;padding:50px 70px 50px;background:radial-gradient(ellipse 60% 25% at 50% 0%,rgba(242,121,58,.15),transparent 70%),#07060A;color:#FEFAF1;font-family:Inter}}
.hd{{display:flex;justify-content:space-between;align-items:flex-end}}.t{{font-family:'Instrument Serif';font-size:64px}}.t b{{color:{O};font-weight:400}}
.pill{{border:1.5px solid {O};color:{O};border-radius:99px;padding:8px 22px;font-weight:600;font-size:20px;letter-spacing:.12em}}
.flow{{margin:22px 0 34px;font-size:26px;color:rgba(254,250,241,.8)}}.flow span{{color:{O}}}
.row{{display:flex;gap:60px}}.ph{{width:470px;height:820px;border-radius:54px;border:2px solid rgba(254,250,241,.18);background:#0A090D;overflow:hidden;position:relative;box-shadow:0 30px 80px rgba(0,0,0,.6)}}
.sb{{display:flex;justify-content:space-between;padding:18px 32px 4px;font-size:15px;font-weight:600;color:rgba(254,250,241,.7)}}.in{{padding:6px 24px}}
.tabs{{position:absolute;bottom:0;left:0;right:0;display:flex;justify-content:space-around;padding:16px 0 26px;border-top:1px solid rgba(254,250,241,.1);font-size:15px;color:rgba(254,250,241,.5);background:#0A090D}}.tabs .on{{color:{O};font-weight:600}}
.c{{background:#141218;border:1px solid rgba(254,250,241,.1);border-radius:20px;padding:14px 18px;margin-top:14px}}.l{{font-size:13px;font-weight:600;letter-spacing:.16em;color:{O};margin-bottom:6px}}
.s{{font-family:'Instrument Serif';line-height:1.05}}.m{{color:rgba(254,250,241,.6);font-size:16px;line-height:1.4}}.b{{font-size:18px;line-height:1.38}}
.fy{{margin-top:12px;background:rgba(242,121,58,.1);border:1px solid rgba(242,121,58,.45);border-radius:14px;padding:12px 14px}}
.btn{{display:inline-block;margin:10px 8px 0 0;padding:8px 16px;border-radius:99px;border:1px solid rgba(254,250,241,.3);font-size:16px}}.btn.o{{background:{O};border-color:{O};color:#160A04;font-weight:600}}
.prog{{height:10px;border-radius:5px;background:rgba(254,250,241,.12);overflow:hidden}}.prog i{{display:block;height:100%;background:{O}}}
.opt{{display:inline-block;padding:7px 14px;border-radius:12px;border:1px solid rgba(254,250,241,.25);margin:8px 6px 0 0;font-size:16px}}.opt.ok{{border-color:#7BC48A;color:#A8E0B2;background:rgba(123,196,138,.12)}}
.post{{padding:12px 0;border-bottom:1px solid rgba(254,250,241,.08)}}.who{{font-size:15px;font-weight:600;margin-bottom:4px}}.badge{{font-size:12px;color:#F28A4E;border:1px solid rgba(242,121,58,.5);border-radius:99px;padding:2px 8px;margin-left:8px}}
.wk{{display:flex;gap:12px;padding:9px 0;border-bottom:1px solid rgba(254,250,241,.08);font-size:16px}}.wk b{{color:#F28A4E;flex:0 0 62px}}
.cap{{width:470px;margin-top:22px}}.cap h3{{font-family:'Instrument Serif';font-weight:400;font-size:38px;color:{O}}}.cap p{{font-size:24px;line-height:1.35;color:rgba(254,250,241,.85);margin-top:4px}}
.foot{{margin-top:40px;padding-top:26px;border-top:1px solid rgba(254,250,241,.12);font-size:26px;line-height:1.5}}.foot b{{color:{O}}}
</style></head><body>
<div class="hd"><div class="t">Sutram <b>Sangha</b> · the daily loop, on your phone</div><div class="pill">CONCEPT · SAMPLE DATA</div></div>
<div class="flow">Instagram post <span>→</span> asksutram.com, guest chart, no sign-up <span>→</span> save your chart <span>→</span> Today <span>→</span> Teach me <span>→</span> your room <span>→</span> the Letter brings you back</div>
<div class="row">{phone(s1,'Today')}{phone(s2,'Learn')}{phone(s3,'Rooms')}{phone(s4,'You')}</div>
<div class="row">{''.join(f'<div class="cap"><h3>{a}</h3><p>{b}</p></div>' for a,b in caps)}</div>
<div class="foot"><b>Runs by itself:</b> the sky writes the agenda (morning post, rooms that open on big transits, Vākya, clinics), members write the stories, and the Guide only fills gaps (any question unanswered for an hour). <b>One account</b> across Ask, Learn, Rhythm and the Letter.</div>
</body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':2200,'height':1500}); pg.set_content(H); pg.wait_for_timeout(300)
    pg.screenshot(path='concepts/sangha-phone-concept.jpg',type='jpeg',quality=90,full_page=True); b.close()
print('ok')
