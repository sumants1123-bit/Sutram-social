import sys; sys.path.insert(0,'tools')
from app_post import FONTS
from playwright.sync_api import sync_playwright
O='#F2793A'
def dia(hl,op):
    return f'''<svg width="170" height="170" viewBox="-5 -5 170 170"><rect x="0" y="0" width="160" height="160" fill="none" stroke="rgba(254,250,241,.35)" stroke-width="2"/><path d="M0 0L160 160M160 0L0 160M80 0L160 80L80 160L0 80Z" fill="none" stroke="rgba(254,250,241,.35)" stroke-width="2"/><path d="M120 40L160 80L120 120L80 80Z" fill="{hl}" opacity="{op}"/><text x="128" y="86" fill="#FEFAF1" font-size="15" font-family="Inter">10</text></svg>'''
def m(n): return f'<span class="mk">{n}</span>'
H=f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:2080px;padding-bottom:30px;background:radial-gradient(ellipse 60% 30% at 50% 0%,rgba(242,121,58,.16),transparent 70%),#07060A;color:#FEFAF1;font-family:Inter;font-size:22px}}
.top{{display:flex;justify-content:space-between;align-items:center;padding:26px 48px;border-bottom:1px solid rgba(254,250,241,.1)}}
.brand{{font-family:'Instrument Serif';font-size:40px}} .brand b{{color:{O};font-weight:400}}
.pill{{border:1.5px solid {O};color:{O};border-radius:99px;padding:8px 22px;font-weight:600;font-size:20px;letter-spacing:.12em}}
.wrap{{display:grid;grid-template-columns:330px 1000px 560px;gap:30px;padding:30px 40px 0}}
.nav div{{padding:13px 18px;border-radius:14px;margin-bottom:4px;color:rgba(254,250,241,.82)}} .nav .on{{background:rgba(242,121,58,.16);color:#FEFAF1;border:1px solid rgba(242,121,58,.5)}}
.sec{{font-size:16px;font-weight:600;letter-spacing:.2em;color:rgba(254,250,241,.45);margin:22px 0 8px 18px}}
.new{{font-size:15px;color:{O};margin-left:8px}} .lock{{opacity:.5}}
.card{{position:relative;background:#110F15;border:1px solid rgba(254,250,241,.1);border-radius:22px;padding:26px 30px;margin-bottom:22px}}
.lab{{font-size:16px;font-weight:600;letter-spacing:.18em;color:{O};margin-bottom:10px}}
.ti{{font-family:'Instrument Serif';font-size:42px;line-height:1.05;margin-bottom:10px}}
.mu{{color:rgba(254,250,241,.62);font-size:20px}}
.fy{{margin-top:18px;background:rgba(242,121,58,.1);border:1px solid rgba(242,121,58,.45);border-radius:16px;padding:16px 20px}}
.btn{{display:inline-block;margin:12px 10px 0 0;padding:9px 20px;border-radius:99px;border:1px solid rgba(254,250,241,.3);font-size:19px}} .btn.o{{background:{O};border-color:{O};color:#160A04;font-weight:600}}
.loop{{display:flex;gap:12px;align-items:center;font-size:20px}} .loop span{{padding:12px 16px;border-radius:14px;border:1px solid rgba(254,250,241,.18)}} .loop .on{{border-color:{O};background:rgba(242,121,58,.14)}}
.mk{{position:absolute;top:-14px;right:-14px;width:44px;height:44px;border-radius:50%;background:{O};color:#160A04;font-weight:700;font-size:24px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 22px rgba(242,121,58,.6)}}
.row{{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid rgba(254,250,241,.07)}}
.leg{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px 40px;margin:8px 40px 0;padding:24px 34px;border-top:1px solid rgba(254,250,241,.12)}}
.leg div{{font-size:24px;line-height:1.3;display:flex;gap:14px}} .leg b{{flex:0 0 40px;height:40px;border-radius:50%;background:{O};color:#160A04;display:flex;align-items:center;justify-content:center}}
</style></head><body>
<div class="top"><div class="brand">Sutram <b>Sangha</b> <span class="mu" style="font-family:Inter;font-size:20px">inside asksutram.com</span></div><div class="pill">CONCEPT · NOT BUILT</div></div>
<div class="wrap">
<div class="nav"><div class="sec">YOUR DAY</div><div class="on">◐ Today</div><div>✦ Ask Sutram</div><div>▤ Your lesson · 4 of 12</div>
<div class="sec">ROOMS</div><div>◈ Commons</div><div>⊕ Chart clinic · Tue, Fri</div><div>☉ Vākya · predictions</div><div>♃ Jupiter in Leo<span class="new">sky room</span></div><div>♄ Sade Sati room</div><div>◷ Gatherings · monthly talk</div>
<div class="sec">CIRCLES</div><div class="lock">🔒 Your Circle · opens at 12</div>
<div class="sec">YOU</div><div>Chart badge: <b style="color:{O}">Off</b></div><div>Depth: Learner</div></div>
<div>
<div style="margin:6px 0 22px"><div class="ti" style="font-size:58px">Good morning, Asha</div><div class="mu">Monday 9 November · Toronto</div></div>
<div class="card">{m(1)}<div class="lab">● MORNING SKY · EVERYONE SEES THIS</div><div class="ti">Mars walks into Leo on Thursday</div><div class="mu">The soldier joins the teacher and the monk. Today's question: where do you need to push?</div><div class="mu" style="margin-top:8px">38 replies</div>
<div class="fy"><div class="lab" style="margin:0 0 6px">🔒 FOR YOU · ONLY YOU SEE THIS</div>It lands in your 10th house: work, and how people see you.<br><span class="btn o">Teach me</span><span class="btn">Ask why</span><span class="btn">Discuss</span></div></div>
<div class="card"><div class="lab">● YOUR PATH TODAY</div><div class="loop"><span>1 Insight</span>→<span class="on">2 Lesson on your chart</span>→<span>3 Ask a follow-up</span>→<span>4 Discuss</span></div></div>
<div class="card">{m(2)}<div class="lab">● LESSON 4 · THE 12 HOUSES</div><div style="display:flex;gap:40px;align-items:center"><div style="text-align:center">{dia(O,.85)}<div class="mu">Your chart</div></div><div style="text-align:center">{dia('#9AA0B5',.4)}<div class="mu">Reference chart</div></div><div style="font-size:24px;line-height:1.35">Your 10th house is Pisces.<br>In the reference chart it's Virgo.<br><span class="mu">Same house, different sign</span><br><span class="btn">14 discussing</span></div></div></div>
<div class="card">{m(3)}<div class="lab">● ANSWERED BY SUTRAM GUIDE · AI</div><div style="font-size:24px">“Does Saturn in my 4th mean I'll move house?”</div><div class="mu" style="margin:6px 0 10px">Ravi · asked 52 minutes ago</div><div style="font-size:22px;line-height:1.4">Not by itself. Saturn in the 4th slows home matters and asks for repairs. A move needs the 4th lord and your dasha to agree.</div><span class="btn">Mark a better answer</span></div>
</div>
<div>
<div class="card"><div class="lab">● YOUR CHART TODAY</div><div class="row"><span class="mu">One theme</span><span>Career and home</span></div><div class="row"><span class="mu">One change</span><span>Venus forward, Friday</span></div><div class="row" style="border:0"><span class="mu">One lesson</span><span>The 12 houses</span></div></div>
<div class="card">{m(4)}<div class="lab">● SKY ROOM · OPENED BY THE SKY</div><div class="ti" style="font-size:36px">Jupiter in Leo</div><div class="mu">For Leo, Aries and Sagittarius Moons<br>46 inside · closes 24 January</div></div>
<div class="card">{m(5)}<div class="lab">● CHART CLINIC · FRIDAY</div><div style="font-size:24px">When does this person change jobs?</div><div class="mu" style="margin-top:6px">Make your dated call. The engine grades it.</div><span class="btn o">Make my call</span></div>
<div class="card"><div class="lab">● VĀKYA</div><div class="row"><span class="mu">This week</span><span>Sealed Monday</span></div><div class="row" style="border:0"><span class="mu">Last week</span><span style="color:#9FD7A6">Hit ✓</span></div></div>
<div class="card lock">{m(6)}<div class="lab">● YOUR CIRCLE</div><div style="font-size:23px">🔒 Opens when 12 people at your level and time zone join</div></div>
</div></div>
<div class="leg"><div><b>1</b>Same post for everyone, plus a private line for your chart</div><div><b>2</b>Teach me: the lesson on your chart, beside a reference chart</div><div><b>3</b>Every question answered within an hour, labelled AI</div><div><b>4</b>Sky rooms open by themselves on big transits, then close</div><div><b>5</b>Chart clinic: make a dated call, the engine grades it</div><div><b>6</b>Circles unlock by numbers, not dates</div></div>
</body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':2080,'height':1400}); pg.set_content(H); pg.wait_for_timeout(300)
    pg.screenshot(path='concepts/sangha-concept.jpg',type='jpeg',quality=90,full_page=True); b.close()
print('ok')
