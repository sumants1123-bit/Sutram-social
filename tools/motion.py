#!/usr/bin/env python3
"""Moving cover for a Sutram post (v6, 10 Nov 2026).

    python3 tools/motion.py specs/<id>.json [more specs] [--slide 1] [--secs 8] [--preview 0,2.5,4]

Writes posts/<id>/<id>-<slide>.mp4 (1080x1350, 30 fps, H.264 + a silent audio track), built from the same spec
as the still. The first and last frames equal the still slide, so the video loops cleanly and its thumbnail is the cover.

What moves
  the sky behind   stars twinkle, the thread's scale turns, pearls and small planets sway (render.decor with tt)
  each graha       Jupiter's bands drift and its spot comes round, Rahu and Ketu's corona turns with a bead circling,
                   the Sun sends out rings, every glow breathes, every graha floats a little
  the rooms        take the light one after another; a spark can run along the floor from one room to the next
  walking          a slide's "motion": {"from": scene} rewinds the grahas to where they were, then replays the walk slowly
  the title        catches the light once
  the foot         the lit bead breathes and the next beads ripple toward the next slide

Slide key "motion" (all optional):
  "order": [1, 0, ["across", 0]]     which rooms take the light, in turn (numbers are rooms in the main row)
  "spark": [null, ["rooms",0,"rooms",1]]   for each step, a spark from one room to another
  "from":  {"rooms": [...]}          the scene before; grahas are matched by kind and rooms by sign name
  "enter": {"mercury": "ahead"}      a graha missing from "from" walks in from behind (the left); "ahead" brings it in from the right,
                                     for a graha walking backward out of the next sign
"""
import json, os, sys, shutil, subprocess, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from playwright.sync_api import sync_playwright

CSS = """
.mv svg.orbsvg{overflow:visible}
.mv .lite{position:absolute;inset:-1.7px;border-radius:inherit;border:1.7px solid rgba(255,196,150,1);background:radial-gradient(82% 72% at 50% 58%,rgba(224,148,96,.36),rgba(224,148,96,0) 76%);box-shadow:0 0 64px rgba(224,148,96,.40),inset 0 0 40px rgba(224,148,96,.16);opacity:0;pointer-events:none}
.mv .tag{transform-origin:50% 100%}
.mv .spark{position:absolute;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:#FFE9CF;box-shadow:0 0 14px 5px rgba(255,190,130,.9),0 0 46px 16px rgba(224,148,96,.45);opacity:0;pointer-events:none}
.mv .t.sh{background-image:linear-gradient(105deg,#F2E6CC 0%,#F2E6CC 38%,#FFFFFF 50%,#F2E6CC 62%,#F2E6CC 100%);background-size:260% 100%;background-repeat:no-repeat;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.mv .t.sh .ti{-webkit-text-fill-color:#E09460}
.mv .seq{transform-box:fill-box;transform-origin:center}
"""

JS = r"""(cfg)=>{
const TAU=Math.PI*2, cl=(x,a,b)=>Math.max(a,Math.min(b,x)), ez=x=>{x=cl(x,0,1);return x*x*(3-2*x)};
const bump=(t,a,b,ri,fo)=>ez((t-a)/ri)*(1-ez((t-(b-fo))/fo));
const T=cfg.secs, slide=document.querySelector('.slide'); slide.classList.add('mv');
const ctr=e=>{const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2,r.width,r.height]};
// grahas
const orbs=[...document.querySelectorAll('.body svg.orbsvg')].map((sv,k)=>{
  const o={sv,k,kind:sv.dataset.kind,R:+sv.dataset.r,c:+sv.dataset.c,gx:0,gy:0,enter:false};
  o.sc=(sv.getBoundingClientRect().width/sv.width.baseVal.value)||1;
  o.glow=sv.querySelector('.oglow'); o.g0=o.glow?+o.glow.getAttribute('opacity'):0;
  if(o.kind==='sun'){const rg=[...sv.querySelectorAll('.sring')]; if(rg.length){const f=rg[0].cloneNode(); f.dataset.f=(+rg[0].dataset.f-.5).toFixed(2); f.setAttribute('stroke-opacity','0'); rg[0].before(f); o.rings=[f,...rg].map(e=>({e,f:+e.dataset.f,o:+e.getAttribute('stroke-opacity')}))}}
  return o});
// rooms of the first scene that sits directly in the body
const scene=document.querySelector('.body > .scene'); let main=[],across=[];
if(scene){const rows=[...scene.querySelectorAll(':scope > .rooms')], rm=e=>[...e.children].filter(c=>c.classList.contains('room')); main=rm(rows[rows.length-1]); across=rows.length>1?rm(rows[0]):[];
  [...main,...across].forEach(r=>{const a=r.querySelector('.arch'); a.insertAdjacentHTML('afterbegin','<div class="lite"></div>'); r.__lite=a.firstChild; r.__arch=a;
    r.__o=parseFloat(getComputedStyle(r).opacity)||1; r.__tag=r.querySelector('.tag'); r.__ow=a.querySelector(':scope > div[style*="scale"]');
    r.__s0=r.__ow?parseFloat((r.__ow.style.transform.match(/scale\(([\d.]+)\)/)||[0,1])[1]):1; r.__focus=r.classList.contains('focus'); r.__flip=across.includes(r)})}
const all=[...main,...across];
const pick=x=>Array.isArray(x)?(x[0]==='across'?across[x[1]]:main[x[1]]):main[x];
let steps=[];
if(scene){let ord=cfg.order; if(!ord){const idx=main.map((r,i)=>i), f=idx.filter(i=>main[i].__focus); ord=cfg.from?(f.length?f:idx):[...f,...idx.filter(i=>!main[i].__focus),...across.map((r,i)=>['across',i])]}
  steps=ord.map((x,k)=>{const s=cfg.spark&&cfg.spark[k]; return {room:pick(x),spark:s?[(s[0]==='across'?across:main)[s[1]],(s[2]==='across'?across:main)[s[3]]]:null}}).filter(s=>s.room)}
const t0=cfg.from?4.5:1.0, t1=cfg.from?7.0:6.4, L=steps.length?Math.min(2.0,(t1-t0)/steps.length):0;
const sparks=steps.map(s=>{if(!s.spark||!s.spark[0]||!s.spark[1])return null; const [A,B]=s.spark, a=A.__arch.getBoundingClientRect(), b=B.__arch.getBoundingClientRect(); let p,q;
  if(A.__flip===B.__flip){p=[a.left+a.width/2,A.__flip?a.top:a.bottom]; q=[b.left+b.width/2,B.__flip?b.top:b.bottom]}
  else{p=[a.left+a.width/2,A.__flip?a.bottom:a.top]; q=[b.left+b.width/2,B.__flip?b.bottom:b.top]}
  const e=document.createElement('div'); e.className='spark'; slide.appendChild(e); return {e,p,q}});
// walking: where each graha stood before
let glide=false; const moves=[];
if(cfg.fromHTML&&scene){const h=document.createElement('div'); h.style.cssText='position:absolute;left:84px;top:160px;width:912px;visibility:hidden;display:flex;flex-direction:column;align-items:center'; h.innerHTML=cfg.fromHTML; slide.appendChild(h);
  const sig=r=>((r.querySelector('.sg')||{}).textContent||'').trim().toLowerCase(), fr={};
  h.querySelectorAll('.room').forEach(r=>{const ac=ctr(r.querySelector('.arch')); r.querySelectorAll('svg.orbsvg').forEach(sv=>{const c=ctr(sv); fr[sv.dataset.kind]={sign:sig(r),off:[c[0]-ac[0],c[1]-ac[1]]}})});
  const to={}; all.forEach(r=>to[sig(r)]=r);
  orbs.forEach(o=>{const room=o.sv.closest('.room'); if(!room||!scene.contains(room))return; const ac=ctr(room.__arch), c=ctr(o.sv), f=fr[o.kind];
    if(f&&to[f.sign]){const fc=ctr(to[f.sign].__arch); o.gx=fc[0]+f.off[0]-c[0]; o.gy=fc[1]+f.off[1]-c[1]} else {o.gx=((cfg.enter||{})[o.kind]==='ahead'?1:-1)*ac[2]*.95; o.gy=0; o.enter=true}
    moves.push([o.kind,Math.round(o.gx),Math.round(o.gy),o.enter])});
  h.remove(); glide=true}
const titles=[...document.querySelectorAll('.body > .t')]; titles.forEach(e=>e.classList.add('sh'));
const fsvg=document.querySelector('svg.frame'); const bglow=fsvg&&fsvg.querySelector('.bd-glow');
const beads=fsvg?[...fsvg.querySelectorAll('.bd-next')].map(b=>{const r=b.cloneNode(); r.setAttribute('class','bd-rip'); r.setAttribute('fill','#E09460'); r.setAttribute('stroke','none'); r.setAttribute('opacity','0'); b.after(r); return r}):[];
const seqs=[...document.querySelectorAll('.body .seq')]; seqs.forEach(g=>g.__o=+g.firstChild.getAttribute('opacity'));
const pulses=[...document.querySelectorAll('.body .pulse')];
const arcs=[...document.querySelectorAll('.body svg.reach')].map(sv=>({a:[...sv.querySelectorAll('.rarc')],h:[...sv.querySelectorAll('.rhead')],l:[...sv.querySelectorAll('.rlab')]}));
const swp=document.querySelector('.swipe svg');
// a path slide: the graha walks its road, the stops light as it passes
const pd=document.querySelector('.body .pathd'); let P=null;
if(pd){const o=pd.querySelector('.porb'), d=o.dataset, n=k=>+d[k]; P={o,x0:n('x0'),xt:n('xt'),xd:n('xd'),yu:n('yu'),ym:n('ym'),yl:n('yl'),r:n('r'),back:pd.querySelector('.pback'),fwd:pd.querySelector('.pfwd'),lab:k=>pd.querySelector('.plab.'+k)};
  P.at=(u)=>{ // u 0..1 back leg (start -> turn), 1..2 forward leg (turn -> a little past the door)
    const {x0,xt,xd,yu,ym,yl,r}=P; if(u<=1){const s1=(x0-xt-r), s2=Math.PI*r/2, s=u*(s1+s2); if(s<=s1)return [x0-s,yu]; const a=(s-s1)/r; return [xt+r-r*Math.sin(a), yu+r-r*Math.cos(a)]}
    const v=u-1, e=xd+70, s2=Math.PI*r/2, s1=(e-xt-r), s=v*(s1+s2); if(s<=s2){const a=s/r; return [xt+r-r*Math.cos(a), ym+r*Math.sin(a)]} return [xt+r+(s-s2),yl]}}
window.__frame=(a)=>{const tt=a.tt, t=tt*T;
  if(a.dec){const d=document.querySelector('svg.decor'); if(d){d.outerHTML=a.dec; const gl=document.querySelectorAll('svg.decor .gl'); (window.__hid||[]).forEach(k=>{if(gl[k])gl[k].style.display='none'})}}
  if(a.sf){const d=document.querySelector('svg.sf'); if(d)d.outerHTML=a.sf}
  const br1=(1-Math.cos(TAU*tt))/2, br2=(1-Math.cos(2*TAU*tt))/2, sw=Math.sin(TAU*tt);
  const g=!glide?0:(t<.5?0:t<1.2?ez((t-.5)/.7):t<2.2?1:t<4.5?1-ez((t-2.2)/2.3):0), arc=Math.sin(Math.PI*g);
  orbs.forEach(o=>{const k=o.k, R=o.R, c=o.c; let x=0, y=(k%2?-1:1)*3*Math.sin(TAU*(1+k%2)*tt), op=1;
    if(glide&&(o.gx||o.gy)){x+=o.gx*g/o.sc; y+=o.gy*g/o.sc; if(o.enter)op=1-g; else if(o.gx<0)y-=Math.min(30,Math.abs(o.gx)*.42)*arc/o.sc}
    o.sv.style.transform=`translate(${x.toFixed(2)}px,${y.toFixed(2)}px)`; o.sv.style.opacity=op.toFixed(3);
    if(o.glow)o.glow.setAttribute('opacity',(o.g0*(1+.38*(k%2?br1:br2))).toFixed(3));
    if(o.kind==='jupiter'){const d=o.sv.querySelector('.jdrift'); if(d)d.setAttribute('dx',(R*.45*sw).toFixed(2)); const s=o.sv.querySelector('.jspot'); if(s){let off=2.6*R*tt; if(.30*R+off>1.3*R)off-=2.6*R; s.setAttribute('transform',`translate(${off.toFixed(2)} 0)`)}}
    else if(o.kind==='ketu'||o.kind==='rahu'){const dir=o.kind==='ketu'?1:-1, cr=o.sv.querySelector('.ncor'), nb=o.sv.querySelector('.nbead'); if(cr)cr.setAttribute('transform',`rotate(${(dir*26.738*tt).toFixed(3)} ${c} ${c})`); if(nb)nb.setAttribute('transform',`rotate(${(dir*360*tt).toFixed(2)} ${c} ${c})`)}
    else if(o.kind==='venus'||o.kind==='mars'){const d=o.sv.querySelector('.drift'); if(d)d.setAttribute('transform',`translate(${(R*.09*sw).toFixed(2)} 0)`)}
    else if(o.kind==='sun'&&o.rings){const u=(2*tt)%1; o.rings.forEach((r,j)=>{const nx=o.rings[j+1]; r.e.setAttribute('r',(R*(r.f+.5*u)).toFixed(2)); r.e.setAttribute('stroke-opacity',(r.o+((nx?nx.o:0)-r.o)*u).toFixed(3))})}});
  all.forEach(r=>r.__e=0);
  steps.forEach((s,k)=>{const a0=t0+k*L, e=bump(t,a0,a0+L+.25,.35,.6); s.room.__e=Math.max(s.room.__e,e); const sp=sparks[k];
    if(sp){const d=Math.min(.9,L*.6), u=cl((t-(a0-.2))/d,0,1), v=ez(u); sp.e.style.left=(sp.p[0]+(sp.q[0]-sp.p[0])*v).toFixed(1)+'px'; sp.e.style.top=(sp.p[1]+(sp.q[1]-sp.p[1])*v).toFixed(1)+'px'; sp.e.style.opacity=(u>0&&u<1)?Math.pow(Math.sin(Math.PI*u),.5).toFixed(3):'0'}});
  all.forEach(r=>{const e=r.__e; r.__lite.style.opacity=(e*(r.__focus?.6:1)).toFixed(3); r.style.opacity=(r.__o+(1-r.__o)*e).toFixed(3);
    if(r.__tag){r.__tag.style.transform=`scale(${(1+.10*e).toFixed(3)})`; r.__tag.style.textShadow=`0 0 ${(18*e).toFixed(1)}px rgba(224,148,96,${(.8*e).toFixed(2)})`}
    if(r.__ow)r.__ow.style.transform=`scale(${(r.__s0*(1+.07*e)).toFixed(4)})`});
  const sh=cl((t-.5)/1.5,0,1), se=Math.sin(Math.PI*sh); titles.forEach(el=>{el.style.backgroundPosition=`${(100-100*sh).toFixed(1)}% 0`; el.style.textShadow=`0 0 42px rgba(224,148,96,${(.22+.30*se).toFixed(3)})`});
  beads.forEach((b,k)=>{const a0=6.2+k*.09, e=bump(t,a0,a0+.7,.2,.4); b.setAttribute('opacity',e.toFixed(3)); b.setAttribute('r',(3.4+2.4*e).toFixed(2))});
  if(bglow){bglow.setAttribute('r',(15+6*br2).toFixed(2)); bglow.setAttribute('opacity',(.20+.16*br2).toFixed(3))}
  seqs.forEach((gq,k)=>{const a0=1.0+k*.34, e=bump(t,a0,a0+1.0,.25,.6); gq.style.transform=`scale(${(1+.55*e).toFixed(3)})`; gq.firstChild.setAttribute('opacity',(gq.__o+(.75-gq.__o)*e).toFixed(3))});
  pulses.forEach(el=>el.setAttribute('fill-opacity',(.30+.45*br2).toFixed(3)));
  if(arcs.length){const ar=cfg.from?(t<.5?1:t<1.2?1-ez((t-.5)/.7):t<4.3?0:t<5.6?ez((t-4.3)/1.3):1):(t<.3?1:t<.8?1-ez((t-.3)/.5):t<1.2?0:t<2.6?ez((t-1.2)/1.4):1);
    arcs.forEach(q=>{q.a.forEach(e=>e.setAttribute('stroke-dashoffset',(1-ar).toFixed(3))); const ho=cl((ar-.82)/.18,0,1); q.h.forEach(e=>e.setAttribute('opacity',ho.toFixed(3))); q.l.forEach(e=>e.setAttribute('opacity',ez(ar*1.6).toFixed(3)))})}
  if(swp)swp.style.transform=`translateX(${(9*Math.max(0,Math.sin(TAU*3*tt))).toFixed(2)}px)`;
  if(P){let u,op=1; // still, jump to the start, walk back, pause at the turn, walk forward to the door, return to the still
    if(t<.5){u=1} else if(t<1.1){u=1; op=1-ez((t-.5)/.6)} else if(t<1.5){u=0; op=ez((t-1.1)/.4)} else if(t<4.5){u=ez((t-1.5)/3.0)*0+((t-1.5)/3.0)} else if(t<5.2){u=1}
    else if(t<6.7){u=1+(t-5.2)/1.5} else if(t<7.2){u=2; op=1-ez((t-6.7)/.5)} else {u=1; op=ez((t-7.2)/.5)}
    const [x,y]=P.at(u); P.o.style.left=x.toFixed(1)+'px'; P.o.style.top=y.toFixed(1)+'px'; P.o.style.opacity=op.toFixed(3);
    const moving=(t>=1.1&&t<7.2); P.back.style.strokeDasharray='1'; P.fwd.style.strokeDasharray='1';
    P.back.style.strokeDashoffset=moving?(1-cl(u,0,1)).toFixed(3):'0'; P.fwd.style.strokeDashoffset=moving?(1-cl(u-1,0,1)).toFixed(3):'0';
    const hit=(k,on)=>{const g=P.lab(k); if(g){g.style.opacity=(moving?(on?1:.28):1).toFixed(2)}};
    hit('l1',true); hit('l2',x<=P.xd+2||u>=1); hit('l3',u>=.98); hit('l4',u>1&&x>=P.xd-2);
    pd.querySelectorAll('.pbm').forEach(e=>e.style.opacity=(!moving||u>=1||x<=+e.dataset.x)?'1':'0'); pd.querySelectorAll('.pfm').forEach(e=>e.style.opacity=(!moving||u>=1.96)?'1':'0')}};
return {orbs:orbs.map(o=>o.kind),rooms:all.length,steps:steps.length,sparks:sparks.filter(Boolean).length,moves}}"""

def motion(spec_path, slide=1, secs=8.0, fps=30, dsf=2, preview=None):
    spec = json.load(open(spec_path)); pid = spec['id']; out = os.path.join(R.REPO, 'posts', pid); os.makedirs(out, exist_ok=True)
    sp = spec['slides'][slide-1]; mo = sp.get('motion') or {}
    tmp = os.path.join(out, '_mv'); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=dsf)
        s, ov = R.build_slide(pg, spec, slide, out)
        from_html = ''
        if mo.get('from'):
            fs = dict(mo['from'])
            for k in ('w', 'h', 'acrossk'):
                if k in (sp.get('scene') or {}) and k not in fs: fs[k] = sp['scene'][k]
            from_html = R.scene_html(fs, s)
        pg.add_style_tag(content=CSS)
        info = pg.evaluate(JS, {'secs': secs, 'order': mo.get('order'), 'spark': mo.get('spark'), 'from': bool(mo.get('from')), 'fromHTML': from_html, 'enter': mo.get('enter')})
        n = int(round(secs*fps))
        frame = lambda tt: pg.evaluate("(a)=>window.__frame(a)", {'tt': tt, 'dec': R.dec_for(spec, slide, tt), 'sf': R.sf_for(spec, slide, tt)})
        if preview is not None:
            outs = []
            for t in preview:
                frame(t/secs); o = os.path.join(out, f'_mv_{t:.1f}.jpg'); pg.screenshot(path=o, type='jpeg', quality=90); outs.append(o)
            b.close(); shutil.rmtree(tmp, ignore_errors=True); print(pid, 'preview', info); return outs
        for f in range(n):
            frame(f/n); pg.screenshot(path=os.path.join(tmp, f'f{f:04d}.jpg'), type='jpeg', quality=92)
        b.close()
    final = os.path.join(out, f'{pid}-{slide}.mp4'); part = os.path.join(out, f'_{pid}-{slide}.part.mp4')
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(tmp, 'f%04d.jpg'),
           '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000', '-shortest',
           '-vf', 'scale=1080:1350:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '19',
           '-profile:v', 'high', '-level', '4.1', '-g', str(fps), '-keyint_min', str(fps), '-sc_threshold', '0', '-bf', '2', '-flags', '+cgop', '-r', str(fps),
           '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
           '-c:a', 'aac', '-b:a', '96k', '-ar', '48000', '-movflags', '+faststart', part]
    subprocess.run(cmd, check=True); os.replace(part, final); shutil.rmtree(tmp, ignore_errors=True)
    print(pid, f'slide {slide} ->', os.path.basename(final), f'{os.path.getsize(final)/1e6:.2f} MB', info)
    return final

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('specs', nargs='+'); ap.add_argument('--slide', type=int, default=1)
    ap.add_argument('--secs', type=float, default=8.0); ap.add_argument('--dsf', type=float, default=2); ap.add_argument('--preview', default=None)
    a = ap.parse_args()
    for sp in a.specs:
        motion(sp, a.slide, a.secs, 30, a.dsf, [float(x) for x in a.preview.split(',')] if a.preview else None)
