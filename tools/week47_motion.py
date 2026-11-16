#!/usr/bin/env python3
"""Moving covers for the week of 16 to 22 Nov (tools/week47.py): rooms covers through motion.py, drawn covers through
anim_motion.py, sky strips through strip_motion.run with a door that lights when the Moon walks through it."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import strip_motion
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = r"""(cfg)=>{
const D=JSON.parse(document.getElementById('sx-data').textContent);
const X=lon=>Math.max(0,Math.min(D.Wd,(lon-D.base)*D.k));
const kinds=Object.keys(D.track), N=D.days.length, el={};
kinds.forEach(k=>el[k]=document.getElementById('sx-'+k));
const date=document.getElementById('sx-date'), door=document.getElementById('sx-door');
const lon=(kd,k)=>{const i=Math.floor(k), j=Math.min(N-1,i+1), f=k-i; return D.track[kd][i]+(D.track[kd][j]-D.track[kd][i])*f};
const secs=cfg.secs, run0=0.5, run1=6.9, hold1=7.3, DL=__DOOR__;
window.__sx=(t)=>{
  const p=t*secs; let k, vis=1;
  if(p<run0) k=0; else if(p<run1) k=(p-run0)/(run1-run0)*(N-1); else k=N-1;
  if(p>hold1){ const q=(p-hold1)/(secs-hold1); if(q<0.5) vis=1-q*2; else {vis=(q-0.5)*2; k=0} }
  kinds.forEach(kd=>{el[kd].style.left=X(lon(kd,k)).toFixed(1)+'px'; el[kd].style.opacity=vis.toFixed(3)});
  if(date){ date.textContent=D.days[Math.min(N-1,Math.round(k))]; date.style.opacity=vis.toFixed(3) }
  if(door) door.style.opacity=(DL===null?1:(lon('moon',k)>=DL?1:0))*vis;
};
return {days:N};
}"""
def run(pid, door_lon=None, slides=(1,)):
    spec = os.path.join(REPO, 'specs', pid + '.json'); sp = json.load(open(spec))
    for n in slides:
        s = sp['slides'][n - 1]
        if s.get('strip'):
            strip_motion.run(spec, n, js=JS.replace('__DOOR__', 'null' if door_lon is None else str(door_lon)))
        elif s.get('anim'):
            subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'anim_motion.py'), spec, '--slide', str(n)], check=True)
        else:
            subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'motion.py'), spec, '--slide', str(n)], check=True)
if __name__ == '__main__':
    plan = json.load(open(os.path.join(REPO, 'plan', 'week47.json')))
    only = sys.argv[1:]
    for p in plan:
        if only and p['id'] not in only: continue
        run(p['id'], p.get('door_lon'), (1, 3) if p['id'] == 'lesson18-swap' else (1,))
        print('done', p['id'], flush=True)
