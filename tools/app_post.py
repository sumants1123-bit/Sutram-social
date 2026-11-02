"""Ask Sutram posts in the app's own look (asksutram.com): near-black #07060A, Instrument Serif titles,
Inter text, orange accent, real screenshots in a rounded frame. Big text by default (Sumant, 2 Nov: never small).
Usage: python3 tools/app_post.py specs/<id>.json"""
import json, sys, os, base64, html
from playwright.sync_api import sync_playwright
from PIL import Image
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def b64(p): return base64.b64encode(open(os.path.join(REPO,p),'rb').read()).decode()
def esc(s): return html.escape(s).replace('\n','<br>')
FONTS=(f"@font-face{{font-family:'Instrument Serif';src:url(data:font/woff2;base64,{b64('assets/fonts/instrument-serif-latin-400-normal.woff2')}) format('woff2')}}"
       f"@font-face{{font-family:Inter;font-weight:400;src:url(data:font/woff2;base64,{b64('assets/fonts/inter-latin-400-normal.woff2')}) format('woff2')}}"
       f"@font-face{{font-family:Inter;font-weight:600;src:url(data:font/woff2;base64,{b64('assets/fonts/inter-latin-600-normal.woff2')}) format('woff2')}}")
CSS="""*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#07060A;color:#FEFAF1;font-family:Inter,sans-serif;overflow:hidden}
.s{position:relative;width:1080px;height:1350px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 56px 150px;text-align:center;
 background:radial-gradient(ellipse 75% 42% at 50% 26%,rgba(240,122,58,.17),rgba(7,6,10,0) 70%),#07060A}
.rings{position:absolute;left:0;top:0}
.lab{position:relative;font-weight:600;font-size:32px;letter-spacing:.2em;text-transform:uppercase;color:#F28A4E;display:flex;align-items:center;gap:16px;margin-bottom:24px}
.lab:before{content:'';width:14px;height:14px;border-radius:50%;background:#F2793A;box-shadow:0 0 16px #F2793A}
.t{position:relative;font-family:'Instrument Serif',serif;font-size:106px;line-height:1.0;color:#FEFAF1}
.t.sm{font-size:84px;line-height:1.05}
.b{position:relative;font-size:46px;line-height:1.32;color:rgba(254,250,241,.84);margin-top:30px;max-width:960px}
.shot{position:relative;margin-top:44px;border-radius:30px;border:1.5px solid rgba(254,250,241,.16);box-shadow:0 30px 80px rgba(0,0,0,.65),0 0 70px rgba(240,122,58,.12);overflow:hidden;background:#0E0C12}
.shot img{display:block}
.orb{position:relative;width:320px;height:320px;border-radius:50%;margin-bottom:64px;background:radial-gradient(circle at 38% 34%,#FFD6AE 0%,#FBA162 26%,#F2793A 54%,#B9461C 84%,#7A2A10 100%);box-shadow:0 0 90px rgba(242,121,58,.55),0 0 230px rgba(242,121,58,.22)}
.foot{position:absolute;bottom:54px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:18px;font-weight:600;font-size:30px;letter-spacing:.06em;color:rgba(254,250,241,.78)}
.foot i{width:12px;height:12px;border-radius:50%;background:#F2793A;box-shadow:0 0 12px #F2793A}
.cta{position:relative;margin-top:36px;font-family:'Instrument Serif',serif;font-size:100px;color:#F28A4E}
.pill{position:relative;margin-top:44px;font-weight:600;font-size:36px;padding:18px 40px;border-radius:999px;border:1.5px solid rgba(242,121,58,.75);background:rgba(242,121,58,.12)}
.small{position:relative;font-size:36px;color:rgba(254,250,241,.72);margin-top:40px}"""
RINGS='<svg class="rings" width="1080" height="1350">'+''.join(f'<circle cx="540" cy="360" r="{r}" fill="none" stroke="rgba(254,250,241,{op})" stroke-width="1.2"/>' for r,op in [(230,.07),(360,.055),(520,.045),(700,.035)])+'</svg>'
def slide(sp):
    t=sp['type']; h=[RINGS]
    if t=='cover': h.append('<div class="orb"></div>')
    if sp.get('label'): h.append(f'<div class="lab">{esc(sp["label"])}</div>')
    if sp.get('title'): h.append(f'<div class="t{" sm" if sp.get("small") else ""}">{esc(sp["title"])}</div>')
    if t=='shot':
        w=sp.get('width',960); h.append(f'<div class="shot" style="width:{w}px"><img style="width:{w}px" src="data:image/png;base64,{b64(sp["image"])}"></div>')
    if sp.get('body'): h.append(f'<div class="b">{esc(sp["body"])}</div>')
    if t=='cta':
        h.append(f'<div class="cta">{esc(sp["link"])}</div>')
        if sp.get('pill'): h.append(f'<div class="pill">{esc(sp["pill"])}</div>')
        if sp.get('small'): h.append(f'<div class="small">{esc(sp["small"])}</div>')
    if t!='cta': h.append('<div class="foot"><i></i>asksutram.com</div>')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}</style></head><body><div class="s">{"".join(h)}</div></body></html>'
def main(path):
    spec=json.load(open(path)); pid=spec['id']; out=os.path.join(REPO,'posts',pid); os.makedirs(out,exist_ok=True)
    files=[]
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
        for i,sp in enumerate(spec['slides'],1):
            pg.set_content(slide(sp)); pg.wait_for_timeout(250)
            f=os.path.join(out,f'{pid}-{i}.jpg'); pg.screenshot(path=f,type='jpeg',quality=92); files.append(f)
        b.close()
    n=len(files); cols=4; th=(390,488); rows=(n+cols-1)//cols
    ov=Image.new('RGB',(cols*th[0]+(cols+1)*24,rows*th[1]+(rows+1)*24),(0,0,0))
    for k,f in enumerate(files):
        im=Image.open(f).resize(th); ov.paste(im,(24+(k%cols)*(th[0]+24),24+(k//cols)*(th[1]+24)))
    ov.save(os.path.join(out,f'{pid}-overview.jpg'),quality=88); print(pid,'->',n,'slides')
if __name__=='__main__': main(sys.argv[1])
