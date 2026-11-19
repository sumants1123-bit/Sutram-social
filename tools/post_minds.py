#!/usr/bin/env python3
"""Know yourself: "Seven kinds of mind" (draft for Sumant's review, 19 Nov 2026).

Sumant, 19 Nov 10:42 AM: "Make a post around what kind of minds there are at broader level as per Jyotish. There's a Mula,
deep-seated mind, there's Ardhara, etc. I don't know. And that's a mind that people use. We are just part of that mind.
It's like small slice of a bigger slice. Something like this."
Read here as: the Moon is the mind, and the Moon's star at birth (one of 27, Mula and Ardra among them) is your slice of
a bigger mind; the classics sort the 27 stars into seven natures. He has not confirmed this reading yet.

Sources opened on 19 Nov 2026:
- Rig Veda 10.90.13, Griffith: "The Moon was gendered from his mind, and from his eye the Sun had birth" (intratext.com).
- Brihat Parashara Hora Shastra 3.12: "manah kumudabandhavah", the Moon is the mind (enjoylearningsanskrit.com).
- Brihat Samhita ch. 98, verses 6 to 11, N. C. Iyer's translation (wisdomlib.org): dhruva (stable) for coronations, planting trees,
  building towns, lasting undertakings; tikshna (sharp) for punishment, incantations, acts of separation; ugra (severe) for
  destruction, poison, burning, armed beating; laghu (light) for sales, acquiring knowledge, arts, medicine; mridu (soft) for
  friendship, clothes, ornaments, music; mridu-tikshna (soft and sharp), mixed; and stars for "works of a moving character".
  Which star sits in which group: tools/look_art.py (the usual panchang lists; Iyer prints Hasta where they have Punarvasu).
Reading a star's nature as a kind of mind is Sutram's reading, and the slides and caption say so.

    python3 tools/post_minds.py     # writes specs/know-seven-minds.json, captions/know-seven-minds.txt, x-drafts/know-seven-minds-x.txt
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import look_art as A
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PID = 'know-seven-minds'
stars = lambda n: '\u00a0· '.join(x.replace(' ', '\u00a0') for x in A.STARS[n])   # break only after a dot, never inside a name
icon = lambda **k: dict(kind='wheel', size=140, hole=.5, **k)
LAB = 'The seven natures · Brihat Samhita, ch. 98'
KIND = {
 'steady': ('The steady mind', 'Builds what lasts. The texts pick these stars for foundations, planting and crowning kings.'),
 'moving': ('The moving mind', 'Thinks on the move. Picked for trips and anything that travels.'),
 'light': ('The light mind', 'Quick hands, quick study. Picked for trade, learning, craft and medicine.'),
 'soft': ('The soft mind', 'Warm and tactful. Picked for friendship, music, clothes and celebrations.'),
 'fierce': ('The fierce mind', 'Heat and nerve. Picked for battles and for breaking what must go.'),
 'sharp': ('The sharp mind', 'Cuts to the root. Picked for cutting ties, strict discipline and mantra work.'),
 'mixed': ('The soft-and-sharp mind', 'Gentle and cutting by turns. The texts call its results mixed.'),
}
card = lambda n: dict(art=icon(lit=n), head=KIND[n][0], line=KIND[n][1], sub=stars(n))

SPEC = dict(id=PID, look='day', kicker='Sutram · Know yourself', slides=[
    dict(type='cover', art=dict(kind='wheel', size=560, mode='sweep', moon=84), title='Seven kinds\nof mind', titlesize=104, subtitle='Your mind is one slice of a bigger one', motion='wheel'),
    dict(type='text', orbs=[dict(kind='moon', r=74)], label='Rig Veda 10.90', title='The Moon was born\nfrom a mind',
         body=['The Purusha Sukta pictures the whole cosmos as one great Person. Of that Person it says: “The Moon was gendered from his mind.”'],
         closing='So the mind you use is a slice of a bigger one', note='Rig Veda 10.90.13, tr. Griffith'),
    dict(type='text', art=dict(kind='wheel', size=430, mode='pick', pick='Mula', lit=[], quarters=True, dot=True), label='In your chart', title='Twenty-seven slices',
         body=['In your chart the Moon is the mind. Its road round the sky is cut into 27 stars, the nakshatras, and at your birth the Moon stood in one of them. That star is your slice.'],
         bodysize=37, closing='Each star has four quarters: a slice of a slice', closingsize=42, note='Brihat Parashara Hora Shastra, ch. 3', motion='wheel'),
    dict(type='cast', label=LAB, title='Steady, moving, light', items=[card('steady'), card('moving'), card('light')], headsize=56, linesize=33, subsize=28, iconw=150),
    dict(type='cast', label=LAB, title='Soft and fierce', items=[card('soft'), card('fierce')], headsize=60, linesize=35, subsize=30, iconw=150),
    dict(type='cast', label=LAB, title='Sharp, and both at once', items=[card('sharp'), card('mixed')], headsize=60, linesize=35, subsize=30, iconw=150,
         note='The texts sort the stars this way to choose a day for a task. Reading them as kinds of mind is Sutram’s reading.'),
    dict(type='cast', label='For example', title='Two sharp minds', items=[
        dict(art=icon(lit=[], pick='Mula'), head='Mula, the root', line='A mind that digs. It keeps asking why until it reaches the bottom of a thing.'),
        dict(art=icon(lit=[], pick='Ardra'), head='Ardra, the moist one', line='Moist, like the ground after rain. A mind that feels the storm fully, then starts fresh.')],
         headsize=60, linesize=36, iconw=150, note='Sutram’s reading, from the stars’ names and their nature'),
    dict(type='rows', label='In real life', title='Work with the grain', items=[['1', 'A steady mind hates being rushed: give it time'], ['2', 'A moving mind thinks best on a walk'], ['3', 'A sharp mind wants the real reason: say it straight']]),
    dict(type='cta', art=dict(kind='wheel', size=230, hole=.56), title='Which kind of mind\nis yours?', titlesize=88, subtitle='Find your Moon’s star at asksutram.com', lines=['Weekly newsletter at sutram.ca/newsletter']),
])

CAPTION = """Seven kinds of mind

The Rig Veda pictures the whole cosmos as one great Person, and says of that Person: "The Moon was gendered from his mind" (10.90.13, tr. Griffith). So the mind you use every day is a slice of a bigger one.

In your chart the Moon is the mind (Brihat Parashara Hora Shastra, chapter 3). The Moon's road round the sky is cut into 27 stars, the nakshatras, and at your birth the Moon stood in one of them. That star is your slice. Each star has four quarters, so yours is a slice of a slice.

The classics sort the 27 stars into seven natures (Brihat Samhita, chapter 98):
""" + '\n'.join(f'{n}: {", ".join(A.STARS[k])}' for n, k in (('Steady', 'steady'), ('Moving', 'moving'), ('Light', 'light'), ('Soft', 'soft'), ('Fierce', 'fierce'), ('Sharp', 'sharp'), ('Soft and sharp', 'mixed'))) + """

The texts use these natures to choose a day for a task: steady stars for foundations, moving stars for travel, soft stars for friendship and music. Reading them as kinds of mind is Sutram's reading.

Take two sharp minds. Mula means the root, a mind that keeps asking why until it reaches the bottom of a thing. Ardra means moist, like the ground after rain, a mind that feels the storm fully and then starts fresh.

In real life, work with the grain. A steady mind hates being rushed. A moving mind thinks best on a walk. A sharp mind wants the real reason.

Which kind of mind is yours? Tell us in the comments.

Ask which star your Moon is in at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#nakshatra #jyotish #moon #vedicastrology #sutram
"""
X = """Seven kinds of mind

The Rig Veda says the Moon was born from the mind of the cosmic Person (10.90.13). In your chart the Moon is your mind, and its star, one of 27, is your slice. The classics sort the 27 into seven natures. Which is yours?

asksutram.com
sutram.ca/newsletter
"""

if __name__ == '__main__':
    json.dump(SPEC, open(os.path.join(REPO, 'specs', f'{PID}.json'), 'w'), indent=1, ensure_ascii=False)
    open(os.path.join(REPO, 'captions', f'{PID}.txt'), 'w').write(CAPTION)
    open(os.path.join(REPO, 'x-drafts', f'{PID}-x.txt'), 'w').write(X)
    print(PID, len(SPEC['slides']), 'slides;', len(CAPTION.strip()), 'caption chars;', len(X.strip()), 'X chars')
