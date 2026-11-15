#!/usr/bin/env python3
"""Move the seated figure on a slide (render.py 'posture'): slouched, then awareness lights up and the back
straightens by itself, then the light fades and the slouch returns. 8 s loop (15 Nov).
    python3 tools/posture_motion.py specs/<id>.json --slide 1 [--preview 1,3,5,7]"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import strip_motion as SM

JS = r"""(cfg)=>{
const D=JSON.parse(document.getElementById('po-data').textContent), F=D.frames, n=F.length-1;
const sp=document.getElementById('po-spine'), ar=document.getElementById('po-arm'), hd=document.getElementById('po-head');
const gw=document.getElementById('po-glow'), rg=document.getElementById('po-ring'), pl=document.getElementById('po-plumb');
const ease=x=>x<0?0:x>1?1:(x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2);
const seg=(t,a,b)=>ease((t-a)/(b-a));
window.__po=(t)=>{
  const s=t*cfg.secs;
  let g = s<1.0?0 : s<2.0?seg(s,1.0,2.0) : s<6.2?1 : s<7.0?1-seg(s,6.2,7.0) : 0;
  let p = s<1.8?0 : s<3.8?seg(s,1.8,3.8) : s<6.6?1 : s<7.6?1-seg(s,6.6,7.6) : 0;
  if(s>=2.0&&s<6.2) g=0.88+0.12*Math.cos((s-2.0)*1.6);
  const i=Math.round(p*n), f=F[i];
  sp.setAttribute('d',f.s); ar.setAttribute('d',f.a);
  hd.setAttribute('cx',f.hx); hd.setAttribute('cy',f.hy);
  gw.setAttribute('cx',f.hx); gw.setAttribute('cy',f.hy); gw.setAttribute('opacity',g.toFixed(3));
  rg.setAttribute('cx',f.hx); rg.setAttribute('cy',f.hy); rg.setAttribute('r',(56+26*g).toFixed(1)); rg.setAttribute('opacity',(0.7*g).toFixed(3));
  pl.setAttribute('stroke-opacity',(0.12+0.4*p).toFixed(3));
};
return {frames:F.length};
}"""

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('spec'); ap.add_argument('--slide', type=int, default=1)
    ap.add_argument('--secs', type=float, default=8.0); ap.add_argument('--preview', default=None)
    a = ap.parse_args()
    SM.run(a.spec, a.slide, a.secs, 30, 2, [float(x) for x in a.preview.split(',')] if a.preview else None, js=JS, fn='__po')
