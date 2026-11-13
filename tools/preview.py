"""Carousel preview page for a private Artifact, so a post can be swiped through before it is scheduled.
Usage: python3 tools/preview.py specs/<id>.json <out.html> [--title "Name"] [--lead "One line"] [--notes notes.json]
notes.json is a list of [text, slide_number]. Prints the Artifact files map (published path -> source path) as JSON."""
import sys, json, os, html
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def esc(t): return html.escape(str(t), quote=True)

def build(spec_path, out, title=None, lead=None, notes=None):
    sp=json.load(open(spec_path)); pid=sp['id']; S=sp['slides']; n=len(S); parts=sp.get('parts') or []
    d=os.path.join(ROOT,'posts',pid); files={}; cells=[]; labs=[]
    for i,s in enumerate(S,1):
        jpg=os.path.join(d,f'{pid}-{i}.jpg'); mp4=os.path.join(d,f'{pid}-{i}.mp4'); files[f's/{i}.jpg']=jpg
        p=s.get('part')
        lab='Cover' if i==1 and not p else (f'Part {p} · {parts[p-1]}' if p and p<=len(parts) else ('Closing' if i==n else ''))
        labs.append(lab)
        if os.path.exists(mp4):
            files[f's/{i}.mp4']=mp4
            media=f'<video id="v{i}" src="s/{i}.mp4" poster="s/{i}.jpg" muted loop playsinline preload="metadata"></video><span class="mv">Moving slide</span>'
        else: media=f'<img src="s/{i}.jpg" alt="Slide {i}" loading="{"eager" if i<3 else "lazy"}">'
        cells.append(f'<li class="cell" data-i="{i}">{media}</li>')
    jumps=[]; seen=set()
    for i,l in enumerate(labs,1):
        if l and l not in seen: seen.add(l); jumps.append(f'<button type="button" class="jump" id="j{i}" data-go="{i}">{esc(l.split(" · ")[-1])}</button>')
    cap=''; cp=os.path.join(ROOT,'captions',pid+'.txt')
    if os.path.exists(cp): cap=f'<details class="cap"><summary>Caption that goes with it</summary><pre>{esc(open(cp).read().strip())}</pre></details>'
    nl=''
    if notes: nl='<section class="notes"><h2>What changed</h2><ol>'+''.join(f'<li><button type="button" class="nb" id="n{k}" data-go="{g}">Slide {g}</button><span>{esc(t)}</span></li>' for k,(t,g) in enumerate(notes))+'</ol></section>'
    title=title or sp.get('kicker',pid); lead=lead or f'{n} slides. Swipe sideways, the way it will read on Instagram.'
    page=f'''<title>{esc(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=EB+Garamond:wght@400;500&display=swap">
<style>
/* Layout: one phone-width column. The carousel is the page; everything else is a quiet margin note. Single dark look, Sutram's own. */
:root{{color-scheme:dark;--bg:#0B0806;--panel:#17110c;--cream:#F2E6CC;--amber:#E09460;--gold:#D9A57A;--mute:#a8957d;--line:rgba(217,165,122,.3);
--display:'Cormorant Garamond','EB Garamond',Georgia,serif;--text:'EB Garamond',Georgia,'Times New Roman',serif}}
body{{background:var(--bg);color:var(--cream);font:400 18px/1.5 var(--text);padding-block:28px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
main{{max-width:480px;margin:0 auto;display:flex;flex-direction:column;gap:22px}}
header{{display:flex;flex-direction:column;gap:6px}}
.eyebrow{{font:500 13px/1.2 var(--text);letter-spacing:.24em;text-transform:uppercase;color:var(--gold)}}
h1{{font:500 38px/1.05 var(--display);margin:0;text-wrap:balance}}
.lead{{margin:0;color:var(--mute)}}
.stage{{display:flex;flex-direction:column;gap:12px}}
.rail{{list-style:none;margin:0;padding:0;display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;border:1px solid var(--line);border-radius:6px;background:var(--panel)}}
.rail::-webkit-scrollbar{{display:none}}
.cell{{flex:0 0 100%;scroll-snap-align:center;scroll-snap-stop:always;position:relative;aspect-ratio:4/5;max-width:100%}}
.cell img,.cell video{{display:block;width:100%;height:100%;object-fit:cover}}
.mv{{position:absolute;left:10px;bottom:10px;font:500 12px/1 var(--text);letter-spacing:.14em;text-transform:uppercase;color:var(--bg);background:var(--amber);padding:6px 9px;border-radius:3px}}
.bar{{display:flex;align-items:center;justify-content:space-between;gap:12px}}
.where{{display:flex;flex-direction:column;gap:2px;min-width:0}}
.count{{font:500 22px/1 var(--display);font-variant-numeric:tabular-nums}}
.part{{font:500 13px/1.2 var(--text);letter-spacing:.16em;text-transform:uppercase;color:var(--amber);min-height:16px}}
.nav{{display:flex;gap:8px}}
button{{font:inherit;color:inherit;background:none;border:1px solid var(--line);border-radius:4px;cursor:pointer}}
button:focus-visible,summary:focus-visible{{outline:2px solid var(--amber);outline-offset:2px}}
.nav button{{width:48px;height:44px;font-size:22px;line-height:1}}
.nav button:disabled{{opacity:.3;cursor:default}}
.jumps{{display:flex;flex-wrap:wrap;gap:8px}}
.jump{{padding:7px 12px;font-size:15px;color:var(--mute)}}
.jump.on{{color:var(--bg);background:var(--amber);border-color:var(--amber)}}
h2{{font:500 13px/1.2 var(--text);letter-spacing:.24em;text-transform:uppercase;color:var(--gold);margin:0 0 10px}}
.notes ol{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}}
.notes li{{display:grid;grid-template-columns:86px 1fr;gap:12px;align-items:start}}
.notes span{{min-width:0}}
.nb{{padding:5px 0;font-size:15px;color:var(--amber);font-variant-numeric:tabular-nums}}
.cap summary{{cursor:pointer;color:var(--gold);font:500 13px/1.2 var(--text);letter-spacing:.24em;text-transform:uppercase}}
.cap pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:400 16px/1.5 var(--text);color:var(--cream);margin:12px 0 0;padding:14px;border:1px solid var(--line);border-radius:6px;background:var(--panel)}}
@media (prefers-reduced-motion:reduce){{.rail{{scroll-behavior:auto}}}}
</style>
<main>
<header><div class="eyebrow">Sutram · preview</div><h1>{esc(title)}</h1><p class="lead">{esc(lead)}</p></header>
<section class="stage" aria-label="Slides">
<ul class="rail" id="rail" tabindex="0">{''.join(cells)}</ul>
<div class="bar"><div class="where"><div class="count" id="count">1 / {n}</div><div class="part" id="part">{esc(labs[0])}</div></div>
<div class="nav"><button type="button" id="prev" aria-label="Previous slide">&#8592;</button><button type="button" id="next" aria-label="Next slide">&#8594;</button></div></div>
<div class="jumps">{''.join(jumps)}</div>
</section>
{nl}
{cap}
</main>
<script>
const rail=document.getElementById('rail'),cells=[...rail.children],N=cells.length,labs={json.dumps(labs)};
const count=document.getElementById('count'),part=document.getElementById('part'),prev=document.getElementById('prev'),next=document.getElementById('next');
const jumps=[...document.querySelectorAll('.jump')];let cur=0;
function go(i,smooth){{i=Math.max(1,Math.min(N,i));rail.scrollTo({{left:cells[i-1].offsetLeft-rail.offsetLeft,behavior:smooth===false?'auto':'smooth'}})}}
function show(i){{if(i===cur)return;cur=i;count.textContent=i+' / '+N;part.textContent=labs[i-1]||'';prev.disabled=i===1;next.disabled=i===N;
  let on=null;jumps.forEach(j=>{{if(+j.dataset.go<=i)on=j}});jumps.forEach(j=>j.classList.toggle('on',j===on));
  cells.forEach((c,k)=>{{const v=c.querySelector('video');if(!v)return;if(k===i-1){{v.currentTime=0;const p=v.play();if(p&&p.catch)p.catch(()=>{{}})}}else v.pause()}})}}
rail.addEventListener('scroll',()=>{{const w=rail.clientWidth||1;show(Math.round(rail.scrollLeft/w)+1)}},{{passive:true}});
prev.addEventListener('click',()=>go(cur-1));next.addEventListener('click',()=>go(cur+1));
rail.addEventListener('keydown',e=>{{if(e.key==='ArrowRight'){{e.preventDefault();go(cur+1)}}if(e.key==='ArrowLeft'){{e.preventDefault();go(cur-1)}}}});
document.querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click',()=>{{go(+b.dataset.go);rail.scrollIntoView({{block:'center',behavior:'smooth'}})}}));
show(1);
</script>
'''
    open(out,'w').write(page); return files

if __name__=='__main__':
    a=sys.argv[1:]; opt={}
    for k in ('--title','--lead','--notes'):
        if k in a: j=a.index(k); opt[k[2:]]=a[j+1]; del a[j:j+2]
    notes=json.load(open(opt['notes'])) if 'notes' in opt else None
    print(json.dumps(build(a[0],a[1],opt.get('title'),opt.get('lead'),notes)))
