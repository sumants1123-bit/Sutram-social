#!/usr/bin/env python3
"""Week ahead for 30 Nov to 6 Dec 2026: Rahu and Ketu change signs (Sunday 29 Nov, 6:30 PM Toronto).

The first post made under rules_23nov (Sumant, Mon 23 Nov 10:23 PM: 4 or 5 posts a week, "everything has to be well done,
in depth, no shortcuts"). On 23 Nov he picked the weekly lineup (Mon lesson, Wed Sutra, Fri Thread, Sun week ahead, a fifth
on big sky weeks), Awareness on Thursday and "a deep week ahead Sunday" built on this change, and no review step.
One question on the cover; then what Rahu and Ketu are (drawn, moving), where Rahu comes from, what the two stand for,
the change over time, a worked count from a Moon sign (moving), the twelve Moon signs, what it does not mean, your turn.

Engine (tools/sky.py: Swiss Ephemeris, Lahiri, mean node, Toronto time), run 24 Nov 2026:
- Mean Rahu enters Capricorn and Ketu Cancer Sat 5 Dec 2026 12:03 PM. Mean Rahu entered Aquarius about Sun 18 May 2025
  and leaves Capricorn for Sagittarius Fri 23 Jun 2028 about 4 PM. Speed -0.053 degrees a day (a degree in about 19 days).
  Rahu Aquarius 0.3 on Sun 29 Nov 6:30 PM; Capricorn 29.95 on 6 Dec; 28.57 on 1 Jan 2027 (inside 1.5 degrees of the edge
  until early January, so the slides show both signs: from Aquarius into Capricorn).
- True Rahu enters Capricorn Wed 25 Nov 2026 8:46 AM (leaves it 24 May 2028).
- Solar eclipses after 5 Dec: annular Sat 6 Feb 2027 (Sun Capricorn 23.4), total Mon 2 Aug 2027 (Sun Cancer 15.7);
  the next is 26 Jan 2028. So both eclipses of the Sun in 2027 fall in Capricorn and Cancer.
- This week: Mercury into Scorpio Wed 2 Dec 6:58 AM (the Sun is in Scorpio); Moon into Libra Fri 4 Dec 12:33 PM, where
  Venus is (exact meeting Sat 5 Dec 12:20 AM); Saturn turns forward Thu 10 Dec about 8 PM and Jupiter backward Sat 12 Dec
  about 8 PM, both slowing all week. New Moon Tue 8 Dec about 8 PM.
- The drawings put each node in the middle of its sign (Aquarius and Leo before, Capricorn and Cancer after): they show
  which sign, not the degree.

Sources, every one opened 24 Nov 2026:
- Drik Panchang, Rahu transit 2026 (drikpanchang.com): "Rahu transits to Makara: December 5, 2026" and "True Rahu transits
  to Makara: November 25, 2026" (its times are for California; Sutram's engine gives Toronto times, a few hours apart).
- Bhagavata Purana 8.9.24 to 26 (vedabase.io): Svarbhanu, dressed as a god, drank the nectar and was pointed out by the
  Moon and Sun; Hari's razor-sharp disc cut off his head; the body, untouched by the nectar, fell; the head, touched by it,
  became immortal, Brahma made it a graha, and it rushes at the Moon and Sun at the junctions (full and new Moon).
  The Bhagavata does not say the body became Ketu, so the post does not say it either.
- R. G. Rao, Fundamentals of Rao's System of Nadi Astrology (S06), chapter 7, karakatwa table, rows 8 (Dragon Head) and 9
  (Dragon Tail), checked rules of the Nadi bank: Rahu stands for bigness (NADI-M-106), an open mouth (M-029), illusion
  (M-027); Ketu for smallness (M-093), narrowness (M-094), breaks (M-095). "Greed" (M-024) is held, so it is not used.
- Jitender Kumar, Nadi Jyotisha (S02), chapter 8, p. 34: Rahu governs material deeds, the interest in them and growth in
  them (NADI-M-154, checked).
- Phaladeepika 26.24, V. Subrahmanya Sastri's translation (1950, wisdomlib.org; verse text cross-read at siva.sh): Rahu's
  transit from the Janma Rasi gives, house by house, sickness or death, loss of wealth, happiness, sorrow, financial loss,
  happiness, loss, danger to life, loss, gain, happiness, expenditure. So the 3rd, 6th, 10th and 11th are good. The
  chapter gives this list for Rahu only. No health or death words go on the slides; the others are called "harder".
- What Rahu and Ketu are (the two points where the Moon's path crosses the Sun's; eclipses only near them) is plain
  astronomy. The tilt of the Moon's path in the drawing is made larger than the real one so it can be seen.
Sutram's own reading, labelled as such on the slides and in the caption: where Rahu sits you want more, where Ketu sits you
let go; each Moon sign's two lines apply that to the house's matters; a harder house asks for care.

    python3 tools/post_rahu_ketu.py        # writes specs/, captions/, x-drafts/
    python3 tools/render_look.py specs/week-2026-11-29-rk.json --motion
"""
import json, os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PID = 'week-2026-11-29-rk'
SUN = lambda r: dict(kind='sun', r=r, rings=False)
MOON = lambda r: dict(kind='moon', r=r, illum=1.0)
NODE = lambda k, r: dict(kind=k, r=r)

# house areas, as in the week-ahead posts; each Moon sign: (Rahu house, Ketu house, Rahu line, Ketu line)
SIGNS = [('Aries', 10, 4, 'work goals grow', 'home gets simpler'),
         ('Taurus', 9, 3, 'far places call', 'less rushing about'),
         ('Gemini', 8, 2, 'shared money, secrets', 'spend less, say less'),
         ('Cancer', 7, 1, 'partners loom large', 'you step back a little'),
         ('Leo', 6, 12, 'more work, going well', 'spending shrinks'),
         ('Virgo', 5, 11, 'big hopes in love, study', 'a smaller, truer circle'),
         ('Libra', 4, 10, 'home, property plans', 'titles matter less'),
         ('Scorpio', 3, 9, 'bolder effort, courage', 'old beliefs loosen'),
         ('Sagittarius', 2, 8, 'wanting more money', 'quiet inner change'),
         ('Capricorn', 1, 7, 'big personal wants', 'fewer, deeper ties'),
         ('Aquarius', 12, 6, 'spending, travel abroad', 'rivals, debts shrink'),
         ('Pisces', 11, 5, 'gains, wider circles', 'less drama in love')]
GOOD = (3, 6, 10, 11)   # Phaladeepika 26.24, from the Moon
ORD = lambda n: f'{n}{"st" if n == 1 else "nd" if n == 2 else "rd" if n == 3 else "th"}'
for k, (s, r, kt, *_x) in enumerate(SIGNS):   # Capricorn is sign 9 and Cancer sign 3, counted from each Moon sign
    assert r == (9 - k) % 12 + 1 and kt == (3 - k) % 12 + 1, s
cell = lambda s, r, kt, lr, lk: [f'{s} Moon', f'Rahu {ORD(r)} · Ketu {ORD(kt)}', f'Rahu: {lr}\nKetu: {lk}', r in GOOD]
GRID = dict(type='grid', cols=2, cellsize=42, celltext=29, celllab=19, cellpad=22,
            note='Gold: Rahu in a good house, Phaladeepika 26.24 · the lines are Sutram’s reading of Rao’s table')

SPEC = dict(id=PID, look='day', kicker='Week ahead · 30 Nov to 6 Dec', slides=[
    dict(type='cover', art=dict(kind='zodiac', size=660, rahu=285, ketu=105, rahu_from=315, ketu_from=135, lit=[9, 3], mode='shift'),
         title='Rahu and Ketu\nchange signs', titlesize=100, subtitle='Saturday 5 December · what it means for you', subsize=42),
    dict(type='text', art=dict(kind='strip', size=930, mode='orbit'), motion='still', label='What they are', title='Where two paths cross',
         body=['Two points with nothing to see: where the Moon’s path crosses the Sun’s, always exactly opposite each other.',
               'An eclipse can only happen near them.'], bodysize=36),
    dict(type='text', orbs=[SUN(50), NODE('rahu', 40), MOON(38)], orbgap=26, label='The story · Bhagavata Purana 8.9', title='The head that\ndrank the nectar',
         titlesize=82, body=['A demon slipped in among the gods and drank the nectar of immortality. The Sun and Moon gave him away.',
                             'Vishnu’s disc cut off his head, but the nectar had touched it. The head lived on as Rahu, and still rushes at the Sun and Moon.'],
         bodysize=34, closing='The old picture of an eclipse', closingsize=42),
    dict(type='cast', label='What they stand for', title='One wants more,\none lets go', titlesize=80, iconw=150, headsize=50, linesize=31, subsize=20,
         items=[dict(orbs=[NODE('rahu', 44)], head='The magician · Rahu', line='The Dragon Head: bigness, an open mouth, illusion', sub='R. G. Rao’s Nadi table'),
                dict(orbs=[NODE('ketu', 44)], head='The monk · Ketu', line='The Dragon Tail: smallness, narrowness, breaks', sub='R. G. Rao’s Nadi table')],
         closing='Sutram’s reading: where Rahu sits you want more, where Ketu sits you let go', closingsize=40),
    dict(type='stack', label='Saturday 5 December', title='One sign back,\nfor 18 months', titlesize=80, linesize=40,
         items=[['May 2025 to 5 December 2026', 'Rahu in Aquarius · Ketu in Leo'],
                ['5 December 2026 to June 2028', 'Rahu in Capricorn · Ketu in Cancer'],
                ['From June 2028', 'Rahu in Sagittarius · Ketu in Gemini']],
         body=['They always walk backward, one sign in about 18 months.'], bodysize=34,
         note='Rahu’s mean path, as almanacs like Drik Panchang list it · by the true path the change came on 25 November'),
    dict(type='text', art=dict(kind='zodiac', size=600, rahu=285, ketu=105, count_from=0, good=list(GOOD), lit=[9, 3], moon=True, mode='count'),
         motion='still', label='Find your houses', title='Count from your Moon', titlesize=78,
         body=['Your Moon sign is the sign the Moon was in at your birth. Call it 1 and count on. Aries Moon: Capricorn is the 10th, Cancer the 4th.'],
         bodysize=33, closing='Ringed: Rahu’s good houses, 3rd, 6th, 10th, 11th', closingsize=36, note='Phaladeepika 26.24'),
    dict(GRID, label='Your Moon sign · from Saturday', title='Aries to Virgo', cells=[cell(*x) for x in SIGNS[:6]]),
    dict(GRID, label='Your Moon sign · from Saturday', title='Libra to Pisces', cells=[cell(*x) for x in SIGNS[6:]]),
    dict(type='stack', label='What it does not mean', title='Read it wisely', titlesize=82, linesize=38,
         items=[['Not one day', 'They move about a degree every 19 days. It builds over months.'],
                ['Not your whole chart', 'Your rising sign, your dasha (the graha period you are in) and your birth grahas change the picture.'],
                ['Not fixed fate', 'A harder house asks for care in that part of life.']],
         note='Sutram’s reading'),
    dict(type='rows', label='Your turn', title='Check your own chart', titlesize=80,
         items=[['1', 'Find your Moon sign: ask your chart at asksutram.com'],
                ['2', 'Count to Capricorn for Rahu, to Cancer for Ketu'],
                ['3', 'Look for birth grahas in Capricorn or Cancer: Rahu and Ketu will pass over them']],
         closing='Ask what it means for you at asksutram.com', closingsize=40, note='Weekly newsletter · sutram.ca/newsletter'),
])

CAPTION = """Rahu and Ketu change signs on Saturday

What are they? Two points with nothing to see, where the Moon's monthly path crosses the Sun's yearly path, always exactly opposite each other. Eclipses can only happen near them: both eclipses of the Sun in 2027 fall in their new signs, 6 February in Capricorn and 2 August in Cancer.

The Bhagavata Purana (8.9) tells where Rahu comes from. A demon slipped in among the gods and drank the nectar of immortality. The Sun and Moon gave him away, and Vishnu's disc cut off his head. The nectar had touched the head, so it lived on as Rahu, and still rushes at the Sun and Moon.

What they stand for: R. G. Rao's Nadi table calls Rahu the Dragon Head, with bigness, an open mouth and illusion, and Ketu the Dragon Tail, with smallness, narrowness and breaks (Fundamentals of Rao's System of Nadi Astrology, chapter 7). Jitender Kumar adds that Rahu governs material deeds and growth in them (Nadi Jyotisha, chapter 8). Sutram's reading: where Rahu sits you want more, where Ketu sits you let go.

On Saturday 5 December the magician (Rahu) walks back from Aquarius into Capricorn, and the monk (Ketu) from Leo into Cancer, until June 2028. That date follows Rahu's mean path, as almanacs like Drik Panchang list it. By the true path the change came on Wednesday 25 November.

To read it for yourself, count from your Moon sign as house 1. Phaladeepika (26.24) counts Rahu's 3rd, 6th, 10th and 11th from the Moon as good, with happiness and gain, and the other eight as harder. Sutram reads a harder house as a call for care in that part of life. They move about a degree every 19 days, so this builds over months, and your rising sign and your dasha (the graha period you are in) change the picture too.

Also this week: Mercury joins the Sun in Scorpio on Wednesday morning, the Moon joins Venus in Libra on Friday afternoon, and Saturn and Jupiter slow toward their stops on 10 and 12 December.

Which house do they land in for you? Tell us in the comments.

Ask where Rahu and Ketu fall in your chart at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#rahu #ketu #jyotish #vedicastrology #sutram
"""

X = """Rahu and Ketu change signs on Saturday 5 December: Rahu into Capricorn, Ketu into Cancer, until June 2028.

Count from your Moon sign. Phaladeepika 26.24 counts Rahu's 3rd, 6th, 10th and 11th as good houses.

asksutram.com
sutram.ca/newsletter
"""
X_SLIDES = [1, 6, 7, 8]

if __name__ == '__main__':
    json.dump(SPEC, open(os.path.join(REPO, 'specs', f'{PID}.json'), 'w'), indent=1, ensure_ascii=False)
    open(os.path.join(REPO, 'captions', f'{PID}.txt'), 'w').write(CAPTION)
    open(os.path.join(REPO, 'x-drafts', f'{PID}-x.txt'), 'w').write(X)
    c = CAPTION.strip(); n = len(c) + c.count('\n')
    xw = len(X.strip()) - len('asksutram.com') - len('sutram.ca/newsletter') + 2 * 23
    print(PID, len(SPEC['slides']), 'slides;', len(c), 'caption chars,', n, 'as Buffer counts;', xw, 'X chars as X counts them')
    assert n <= 2200 and xw <= 280 and len(SPEC['slides']) <= 10
