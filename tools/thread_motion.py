#!/usr/bin/env python3
"""Moving cover for a post in the Thread look (tools/render_thread.py), 16 Nov 2026.

    python3 tools/thread_motion.py specs/<id>.json [--out path.mp4] [--secs 8]

Writes posts/<id>/<id>-1.mp4: 1080x1350, 30 fps, H.264 with a silent audio track, 8 s loop whose first frame is the still.
What moves: the orbit's beads travel once round their ellipse, the stars twinkle, any graha drawn on the cover breathes."""
import json, os, sys, shutil, subprocess, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_thread as R
from playwright.sync_api import sync_playwright
from PIL import Image

JS = r"""(function(){
const body=document.querySelector('.body');const orbits=[],others=[];
body.querySelectorAll('svg').forEach(s=>{const e=s.querySelector('ellipse');if(e&&s.querySelectorAll('circle').length>=3&&!s.closest('.row'))orbits.push(s);else if(s.getBoundingClientRect().width>60)others.push(s);});
const beads=[];orbits.forEach(s=>{const e=s.querySelector('ellipse');const cx=+e.getAttribute('cx'),cy=+e.getAttribute('cy'),rx=+e.getAttribute('rx'),ry=+e.getAttribute('ry');
 e.parentNode.querySelectorAll('circle').forEach(c=>{const x=+c.getAttribute('cx'),y=+c.getAttribute('cy');beads.push({c,cx,cy,rx,ry,a0:Math.atan2((y-cy)/ry,(cx-x)/rx)})});});
const stars=[...document.querySelectorAll('.slide > svg circle')].filter(c=>c.getAttribute('fill')==='#FFF1D6').map((c,i)=>({c,o:+c.getAttribute('opacity'),k:1+i%3,p:i*1.37}));
window.__fab=function(t){const w=2*Math.PI*t/8;
 for(const b of beads){const a=b.a0+w;b.c.setAttribute('cx',(b.cx-b.rx*Math.cos(a)).toFixed(2));b.c.setAttribute('cy',(b.cy+b.ry*Math.sin(a)).toFixed(2));}
 for(const s of stars)s.c.setAttribute('opacity',(s.o*(.62+.38*Math.cos(w*s.k+s.p))/(.62+.38*Math.cos(s.p))).toFixed(3));
 const k=1+.018*Math.sin(w);for(const s of others){s.style.transformOrigin='50% 50%';s.style.transform=`scale(${k.toFixed(4)})`;}};
window.__fab(0);})();"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('spec'); ap.add_argument('--out'); ap.add_argument('--secs', type=float, default=8.0); a = ap.parse_args()
    spec = json.load(open(a.spec)); pid = spec['id']; sp = spec['slides'][0]; i = 1
    out = a.out or os.path.join(R.REPO, 'posts', pid, f'{pid}-1.mp4'); tmp = out + '.frames/'; part = out[:-4] + '.part.mp4'
    kicker = sp.get('kicker', spec.get('kicker', 'Sutram'))
    sf = R.stars(seed=i * 7 + len(pid)) if sp.get('stars') else ''
    dec = '' if spec.get('decor') is False else R.decor(i, sum(map(ord, pid)), dense=bool(sp.get('stars')), theme=R.theme_for(spec), hi_phase=R.real_phase(spec))
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=2)
        for s in (1, .96, .92, .88, .84, .8, .76, .72, .68):
            html = R.page(R.slide_html(sp, s), kicker, s, sf, dec=dec).replace('</body>', f'<script>{JS}</script></body>')
            fn = tmp + '_c.html'; open(fn, 'w').write(html); pg.goto('file://' + fn); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            if pg.evaluate("()=>{const b=document.querySelector('.body');return b.scrollHeight-b.clientHeight}") <= 0: break
        n = int(a.secs * 30)
        for f in range(n):
            pg.evaluate('(t)=>window.__fab(t)', f / 30); pg.screenshot(path=tmp + f'f{f:04d}.jpg', type='jpeg', quality=92)
        b.close()
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', tmp + 'f%04d.jpg', '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000', '-shortest',
                    '-vf', 'scale=1080:1350:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-profile:v', 'high', '-level', '4.1', '-g', '30', '-keyint_min', '30',
                    '-sc_threshold', '0', '-bf', '2', '-flags', '+cgop', '-r', '30', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                    '-c:a', 'aac', '-b:a', '96k', '-ar', '48000', '-movflags', '+faststart', part], check=True)
    os.replace(part, out); shutil.rmtree(tmp, ignore_errors=True)
    print(pid, '->', out, f'{os.path.getsize(out) / 1e6:.2f} MB')


if __name__ == '__main__':
    main()
