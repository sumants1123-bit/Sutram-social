#!/usr/bin/env python3
"""Play a slide's drawn picture (render.py 'anim') as an 8 s loop and save the mp4 (15 Nov).
    python3 tools/anim_motion.py specs/<id>.json --slide 1 [--preview 1,3,5,7]"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import strip_motion as SM
JS = "(cfg)=>({els: JSON.parse(document.getElementById('an-data').textContent).els.length})"
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('spec'); ap.add_argument('--slide', type=int, default=1)
    ap.add_argument('--secs', type=float, default=8.0); ap.add_argument('--preview', default=None)
    a = ap.parse_args()
    SM.run(a.spec, a.slide, a.secs, 30, 2, [float(x) for x in a.preview.split(',')] if a.preview else None, js=JS, fn='__an')
