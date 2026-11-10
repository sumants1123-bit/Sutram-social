#!/usr/bin/env python3
"""Print what a Buffer create_post / edit_post call needs for one post, pinned to a commit so nothing is cached.
    python3 tools/buffer_assets.py <post-id> <commit-sha> [--video] [--slides 1,3,4,5] [--notext]
--video   slide 1 goes as posts/<id>/<id>-1.mp4 (the moving cover from tools/motion.py), the rest as images
--slides  only these slides (X takes up to 4)
Alt text is the slide's own words, taken from the spec."""
import json, os, sys, re
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def words(sp):
    out=[sp.get('label'),sp.get('title'),sp.get('subtitle'),sp.get('example'),sp.get('quote')]
    for sc in [sp.get('scene')]:
        if sc: out.append('Rooms: '+', '.join(f"{r['sign']} ({' and '.join(o['kind'] for o in r.get('orbs',[])) or 'empty'})" for r in sc.get('across',[])+sc['rooms']))
    out+= [x for x in (sp.get('body') or [])]
    t=sp['type']
    if t in ('rows','list','bodymap'): out+=[f'{it[0]}: {it[1]}' for it in sp['items']]
    if t=='stack': out+=[f'{a}: {b}' for a,b in sp['items']]
    if t=='cast': out+=[f"{it['head']} {it['line']}" for it in sp['items']]
    if t=='grid': out+=[f'{c[0]}: {c[1]}, {c[2]}' for c in sp['cells']]
    if t=='compare': out+=[f"{c.get('label') or ''} {c['head']}: {' '.join(c['lines'])}" for c in sp['columns']]
    if t=='sentence': out+=[f'{a}: {b}' for a,b in sp.get('rows',[])]+[sp.get('conclusion')]
    if t=='cta': out+=sp.get('lines',[])+[sp.get('next')]
    out+=[sp.get('closing'),sp.get('note'),sp.get('source')]
    s='. '.join(re.sub(r'\s+',' ',str(x).replace('*','')).strip().rstrip('.') for x in out if x)
    return re.sub(r'([?!])\. ',r'\1 ',s)
def main():
    a=sys.argv[1:]; pid,sha=a[0],a[1]; video='--video' in a; notext='--notext' in a
    spec=json.load(open(os.path.join(REPO,'specs',f'{pid}.json'))); n=len(spec['slides'])
    pick=[int(x) for x in a[a.index('--slides')+1].split(',')] if '--slides' in a else list(range(1,n+1))
    base=f'https://raw.githubusercontent.com/sumants1123-bit/Sutram-social/{sha}/posts/{pid}/{pid}-'
    assets=[]
    for i in pick:
        if video and i==1 and os.path.exists(os.path.join(REPO,'posts',pid,f'{pid}-1.mp4')):
            assets.append({"video":{"url":base+'1.mp4',"metadata":{"thumbnailOffset":0}}}); continue
        alt=f'Slide {i} of {n}. '+words(spec['slides'][i-1])
        if len(alt)>300: alt=alt[:297].rsplit(' ',1)[0]+'…'
        assert os.path.exists(os.path.join(REPO,'posts',pid,f'{pid}-{i}.jpg'))
        assets.append({"image":{"url":base+f'{i}.jpg',"metadata":{"altText":alt}}})
    out={"assets":assets}
    cap=os.path.join(REPO,'captions',f'{pid}.txt')
    if not notext and os.path.exists(cap): out["text"]=open(cap).read().strip()
    print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__': main()
