import json,sys,os
src=open('sky-machine.src.html').read()
data=open('sky-data.json').read()
os.makedirs('dist',exist_ok=True); os.makedirs('test',exist_ok=True)
cdn=('https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js','https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/')
loc=('/node_modules/three/build/three.module.js','/node_modules/three/examples/jsm/')
for out,(a,b) in [('dist/sky-machine.html',cdn),('test/sky-machine.html',loc)]:
    h=src.replace('__SKYDATA__',data).replace('__THREE__',a).replace('__ADDONS__',b)
    if out.startswith('test'):
        h='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'+h+'</body></html>'
    open(out,'w').write(h)
print('built', os.path.getsize('dist/sky-machine.html'))
src=open('dasha-gearbox.src.html').read()
for out,(a,b) in [('dist/dasha-gearbox.html',cdn),('test/dasha-gearbox.html',loc)]:
    h=src.replace('__THREE__',a).replace('__ADDONS__',b)
    if out.startswith('test'):
        h='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'+h+'</body></html>'
    open(out,'w').write(h)
print('built gearbox', os.path.getsize('dist/dasha-gearbox.html'))
