"""Check captions against Sutram's voice rules. Usage: python3 tools/check_caption.py captions/<id>.txt ..."""
import sys, re
BANNED=['journey','delve','tapestry','realm','unlock','unleash','elevate','embrace','navigate','resonate','profound','essence',
 'transformative','cosmic','celestial','align','manifest','sacred','timeless','deep dive','explore','discover','insight',
 'sit with','hold space','at its core','goes deeper','dive into','vibrant','seamless','intricate','crucial','pivotal','foster',
 'empower','harness','illuminate','beacon','nestled','testament','embark','game-changer','holistic','universe is telling']
ok=True
for f in sys.argv[1:]:
    t=open(f).read().strip(); low=t.lower(); issues=[]
    if len(t)>2200: issues.append(f'{len(t)} chars (max 2200)')
    if '—' in t: issues.append('em dash')
    hits=[w for w in BANNED if re.search(r'\b'+re.escape(w),low)]
    if hits: issues.append('banned words: '+', '.join(hits))
    if re.search(r"\bnot (just|only|merely)\b.*\bbut\b",low): issues.append('"not X but Y" construction')
    first=t.splitlines()[0]
    if first.endswith('.'): issues.append('first line ends with a period')
    for line in t.splitlines():
        if ':' in line[:40] and line.endswith('.') and len(line)<120: issues.append(f'list line ends with a period: {line[:50]}')
    print(f, 'OK' if not issues else 'FIX: '+'; '.join(issues)); ok=ok and not issues
sys.exit(0 if ok else 1)
