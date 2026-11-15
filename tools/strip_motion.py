#!/usr/bin/env python3
"""Run the days on a slide's current-sky strip (render.py 'strip') and save it as an 8 s mp4 (15 Nov).
    python3 tools/strip_motion.py specs/<id>.json --slide 1 [--preview 0.5,4,7.5]
The grahas walk to scale, one day at a time, the date runs above the strip, and an exchange arc draws itself
the day both grahas stand in each other's sign. The background moves as in tools/motion.py."""
import argparse, json, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
import motion as M
from playwright.sync_api import sync_playwright

JS = r"""(cfg)=>{
const D=JSON.parse(document.getElementById('sx-data').textContent);
const X=lon=>Math.max(0,Math.min(D.Wd,(lon-D.base)*D.k));
const kinds=Object.keys(D.track), N=D.days.length, el={};
kinds.forEach(k=>el[k]=document.getElementById('sx-'+k));
const arc=document.getElementById('sx-arc'), ha=document.getElementById('sx-ha'), hb=document.getElementById('sx-hb');
const date=document.getElementById('sx-date'), door=document.getElementById('sx-door');
const rooms=[...document.querySelectorAll('.sx-room')];
const lon=(kd,k)=>{const i=Math.floor(k), j=Math.min(N-1,i+1), f=k-i; return D.track[kd][i]+(D.track[kd][j]-D.track[kd][i])*f};
const sgn=l=>Math.floor(((l%360)+360)%360/30);
const own={4:'sun',7:'mars',0:'mars',3:'moon',1:'venus',6:'venus',2:'mercury',5:'mercury',8:'jupiter',11:'jupiter',9:'saturn',10:'saturn'};
const swapped=k=>{ if(!D.arc) return false; const [a,b]=D.arc; return own[sgn(lon(a,k))]===b && own[sgn(lon(b,k))]===a };
let kc=null; for(let k=0;k<N-1;k+=0.02){ if(swapped(k)){kc=k;break} }
const secs=cfg.secs, run0=0.5, run1=6.9, hold1=7.3;
window.__sx=(t)=>{
  const p=t*secs; let k, vis=1;
  if(p<run0) k=0; else if(p<run1) k=(p-run0)/(run1-run0)*(N-1); else k=N-1;
  if(p>hold1){ const q=(p-hold1)/(secs-hold1); if(q<0.5) vis=1-q*2; else {vis=(q-0.5)*2; k=0} }
  const P={}; kinds.forEach(kd=>{P[kd]=X(lon(kd,k)); el[kd].style.left=P[kd].toFixed(1)+'px'; el[kd].style.opacity=vis.toFixed(3)});
  if(date){ date.textContent=D.days[Math.min(N-1,Math.round(k))]; date.style.opacity=vis.toFixed(3) }
  const on=swapped(k); const draw=(on&&kc!==null)?Math.min(1,Math.max(0,(k-kc)/2.2)):0;
  if(arc){
    const [a,b]=D.arc, ya=D.lane[a]-D.r[a]-14, yb=D.lane[b]-D.r[b]-14, xa=P[a], xb=P[b], yt=D.arctop;
    arc.setAttribute('d',`M${xa.toFixed(1)},${ya.toFixed(1)} C${xa.toFixed(1)},${yt} ${xb.toFixed(1)},${yt} ${xb.toFixed(1)},${yb.toFixed(1)}`);
    arc.style.strokeDashoffset=(1-draw).toFixed(3); arc.style.opacity=(draw>0?vis:0).toFixed(3);
    const hd=(x,y)=>`M${(x-11).toFixed(1)},${(y-16).toFixed(1)} L${x.toFixed(1)},${y.toFixed(1)} L${(x+11).toFixed(1)},${(y-16).toFixed(1)} Z`;
    ha.setAttribute('d',hd(xa,ya)); hb.setAttribute('d',hd(xb,yb));
    const ho=Math.max(0,Math.min(1,(draw-0.8)/0.2))*vis; ha.style.opacity=ho.toFixed(3); hb.style.opacity=ho.toFixed(3);
  }
  if(door) door.style.opacity=(kc!==null&&k>=kc?Math.min(1,(k-kc)/1.2):0)*vis;
  rooms.forEach(r=>{ const lit=(r.dataset.sign==='Leo'||r.dataset.sign==='Scorpio'); if(!lit) return;
    r.setAttribute('fill-opacity',(0.05+0.11*draw).toFixed(3)); r.setAttribute('stroke-opacity',(0.45+0.5*draw).toFixed(3)) });
};
return {days:N, crossing:kc};
}"""

def run(spec_path, slide=1, secs=8.0, fps=30, dsf=2, preview=None, js=None, fn='__sx'):
    spec = json.load(open(spec_path)); pid = spec['id']; out = os.path.join(R.REPO, 'posts', pid)
    tmp = os.path.join(out, '_sx'); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=dsf)
        R.build_slide(pg, spec, slide, out)
        pg.add_style_tag(content=M.CSS)
        pg.evaluate(M.JS, {'secs': secs, 'order': None, 'spark': None, 'from': False, 'fromHTML': '', 'enter': None, 'lift': None})
        info = pg.evaluate(js or JS, {'secs': secs})
        def frame(t):
            pg.evaluate("(a)=>window.__frame(a)", {'tt': t, 'dec': R.dec_for(spec, slide, t), 'sf': R.sf_for(spec, slide, t)})
            pg.evaluate(f"(t)=>window.{fn}(t)", t)
        if preview is not None:
            outs = []
            for t in preview:
                frame(t/secs); o = os.path.join(out, f'_sx_{t:.1f}.jpg'); pg.screenshot(path=o, type='jpeg', quality=90); outs.append(o)
            b.close(); shutil.rmtree(tmp, ignore_errors=True); print(pid, 'preview', info, outs); return outs
        n = int(round(secs*fps))
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
    ap = argparse.ArgumentParser(); ap.add_argument('spec'); ap.add_argument('--slide', type=int, default=1)
    ap.add_argument('--secs', type=float, default=8.0); ap.add_argument('--preview', default=None)
    a = ap.parse_args()
    run(a.spec, a.slide, a.secs, 30, 2, [float(x) for x in a.preview.split(',')] if a.preview else None)
