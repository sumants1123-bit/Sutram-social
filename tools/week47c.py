#!/usr/bin/env python3
"""Three posts of 16 to 22 Nov 2026 remade in the cream look (tools/render_look.py), Wednesday check-in, 18 Nov.

Sumant, 18 Nov 6:39 PM: "this light theme, I love it. I want to have more posts around this light theme."
The words follow the Thread posts he praised on 16 Nov (label, title, a few lines, a short list, a source).
Every fact, source and time is taken from the current version of each post (specs/<id>.json, captions/<id>.txt,
made by tools/week47.py from the engine). Nothing is recomputed here. The one addition is the week-ahead list
"for your Moon sign": Taurus counted from each Moon sign, which is plain counting round the twelve signs.

    python3 tools/week47c.py        # writes specs/<id>-c.json, captions/<id>-c.txt, x-drafts/<id>-c-x.txt
"""
import json, os, shutil
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
ORD = {1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th', 6: '6th', 7: '7th', 8: '8th', 9: '9th', 10: '10th', 11: '11th', 12: '12th'}
# house themes in the words of the 1 to 7 Nov week ahead ("Jupiter in Leo"), without its Jupiter-only notes
HOUSE = {1: 'You in focus', 2: 'Savings, family, food', 3: 'Effort, short trips', 4: 'Home, mother, repairs', 5: 'Kids, study, romance', 6: 'Routine, debts, fitness',
         7: 'Partner, clients, deals', 8: 'Quiet change', 9: 'Luck, teachers, travel', 10: 'Work and standing', 11: 'Gains and good friends', 12: 'Spending, travel, rest'}


def house_from(moon_sign, sign):
    return (SIGNS.index(sign) - SIGNS.index(moon_sign)) % 12 + 1


MOON, SAT, SUN = {'kind': 'moon'}, {'kind': 'saturn'}, {'kind': 'sun', 'rings': False}
o = lambda base, r: dict(base, r=r)
ASK = 'Weekly newsletter at sutram.ca/newsletter'
POSTS = {}

# ------------------------------------------------------------------ Friday's sky
POSTS['sky-2026-11-20-c'] = dict(look='day', kicker='Sutram · Current sky', slides=[
    dict(type='cover', orbs=[o(MOON, 112), o(SAT, 84)], orbgap=10, title='The Moon meets\nSaturn in Pisces', titlesize=100, subtitle='Friday afternoon, about 3:45 PM', motion='meet'),
    dict(type='text', label='Friday 20 November', title='Two grahas,\none sign', body=['At about 3:45 PM Toronto time, the mother (the Moon) passes the auditor (Saturn) in Pisces.'],
         closing='In one sign, two grahas act on each other at full strength', note='Nadi rule 1'),
    dict(type='cast', label='Who is meeting', title='The mother\nand the auditor', headsize=60, linesize=36, iconw=150, items=[
        dict(orbs=[o(MOON, 52)], head='The Moon in Pisces', line='Soft, kind and a little dreamy. Pisces is the teacher’s sign, Jupiter’s.'),
        dict(orbs=[o(SAT, 40)], head='Saturn in Pisces', line='Walking backward since July, forward again on 10 December. Walking backward, the auditor rechecks old work.')]),
    dict(type='text', orbs=[o(MOON, 56), o(SAT, 44)], orbgap=0, label='Together', title='A mood that wants\na job done', body=['The mind and duty sit in one room, and together they make a heavy mood that wants one job done.'],
         closing='Feelings get serious and practical'),
    dict(type='text', orbs=[o(SUN, 60)], label='Nadi rule 6', title='The king is family', body=['The king (the Sun) sits in Scorpio, another water sign. Signs 5th and 9th apart act together, so he is family.'],
         closing='The boss backs the plan'),
    dict(type='rows', label='In real life', title='This evening', items=[['1', 'Finish one chore'], ['2', 'Call your mother'], ['3', 'Let a feeling be, instead of rushing to fix it']]),
    dict(type='cta', orbs=[o(MOON, 44), o(SAT, 36)], orbgap=0, title='What does it mean\nfor your Moon sign?', titlesize=84, subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Sunday · The week ahead'),
])
CAP = {}
CAP['sky-2026-11-20-c'] = """The Moon meets Saturn in Pisces

On Friday at about 3:45 PM Toronto time the mother (Moon) passes the auditor (Saturn) in Pisces. In Nadi, two grahas in one sign act on each other at full strength (rule 1), so the mind and duty sit in one room this afternoon.

Who is meeting:
The Moon in Pisces is soft, kind and a little dreamy. Pisces is the teacher's (Jupiter's) sign
Saturn in Pisces has been walking backward since July and turns forward again on 10 December. Walking backward, the auditor rechecks old work

Together they make a heavy mood that wants one job done. Feelings get serious and practical.

The king (Sun) sits in Scorpio, another water sign, so he is family (rule 6): the boss backs the plan.

This evening, finish one chore, call your mother, and let a feeling be instead of rushing to fix it.

How does your Friday afternoon feel? Tell us in the comments.

Next, on Sunday evening, the week ahead

Ask what the Moon meeting Saturn means for your Moon sign at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#jyotish #moon #saturn #vedicastrology #sutram
"""

# ------------------------------------------------------------------ Saturday: Rama is the Sun
AV = [('Sun', 'Rama', {'kind': 'sun', 'rings': False}), ('Moon', 'Krishna', {'kind': 'moon'}), ('Mars', 'Narasimha', {'kind': 'mars'}), ('Mercury', 'Buddha', {'kind': 'mercury'}), ('Jupiter', 'Vamana', {'kind': 'jupiter'}),
      ('Venus', 'Parashurama', {'kind': 'venus'}), ('Saturn', 'Kurma', {'kind': 'saturn'}), ('Rahu', 'Varaha', {'kind': 'rahu'}), ('Ketu', 'Matsya', {'kind': 'ketu'})]
POSTS['avatar-rama-sun-c'] = dict(look='day', kicker='Sutram · Avatars and grahas', slides=[
    dict(type='cover', orbs=[o(SUN, 116)], title='Rama is\nthe Sun', subtitle='Why the old texts pair two kings', motion='rise'),
    dict(type='grid', cols=3, label='Brihat Parashara Hora Shastra · ch. 2', title='Nine avatars, nine grahas', titlesize=72, cells=[[g, a, ''] for g, a, _ in AV], cellorbs=[dict(k, r=(30 if k['kind'] == 'saturn' else 36)) for _, _, k in AV],
         cellsize=50, celllab=20, cellpad=20, closing='Parashara pairs them, one by one', closingsize=44),
    dict(type='text', label='The story', title='Rama kept his\nfather’s word', body=['He was the king who left his throne to keep it, and he ruled by dharma, the right way.'], closing='The way the Sun gives light to all alike'),
    dict(type='text', orbs=[o(SUN, 70)], label='Brihat Parashara Hora Shastra · ch. 3', title='The Sun is the king,\nthe father, the soul', body=['In Jyotish the Sun is the king of the grahas.'], closing='The light that shines on all alike'),
    dict(type='text', label='In your chart', title='Your Sun’s house', body=['The house of your Sun shows where you are asked to lead and to keep your word.'], note='Sutram’s reading, built on the classical meanings'),
    dict(type='text', label='In real life', title='Try it today', closing='Keep one promise, to someone else or to yourself', closingsize=52),
    dict(type='cta', orbs=[o(SUN, 56)], title='What does your Sun’s\nhouse ask of you?', titlesize=84, subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Next Saturday · Krishna, the Moon'),
])
CAP['avatar-rama-sun-c'] = """Rama is the Sun

Parashara says Vishnu took form through the grahas (Brihat Parashara Hora Shastra, chapter 2):
Rama from the Sun
Krishna from the Moon
Narasimha from Mars
Buddha from Mercury
Vamana from Jupiter
Parashurama from Venus
Kurma from Saturn
Varaha from Rahu
Matsya from Ketu

Why Rama for the Sun? In Jyotish the Sun is the king of the grahas, the father and the soul (chapter 3). Rama was the king who left his throne to keep his father's word, and he ruled by dharma, the right way, the way the Sun gives light to all alike.

In your chart, the house of your Sun shows where you are asked to lead and to keep your word. That is Sutram's reading, built on the classical meanings.

In real life, try it today and keep one promise, to someone else or to yourself.

Which promise will you keep today? Tell us in the comments.

Every Saturday morning, one avatar and one graha. Next Saturday, Krishna, the Moon

Ask what your Sun's house asks of you at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#rama #jyotish #sun #vedicastrology #sutram
"""

# ------------------------------------------------------------------ Sunday: the week ahead
cells = [[f'{m} Moon', f'{ORD[house_from(m, "Taurus")]} house', HOUSE[house_from(m, 'Taurus')]] for m in SIGNS]
POSTS['week-2026-11-22-c'] = dict(look='day', kicker='Week ahead · 22 to 28 November', slides=[
    dict(type='cover', orbs=[o(MOON, 132)], title='A full Moon\nin Taurus', titlesize=104, subtitle='Tuesday, the Moon at her best', motion='rise'),
    dict(type='text', orbs=[o(MOON, 60), o(SUN, 56)], orbgap=150, label='Tuesday, about 10 AM', title='Face to face',
         body=['The Moon is full in Taurus, facing the king (the Sun) in Scorpio. Grahas face to face act on each other directly, so the mind and the self meet in full light.'], note='Nadi rule 4'),
    dict(type='text', orbs=[o(MOON, 70)], label='The Moon’s best sign', title='A calm, kind mind', body=['On Monday night at about 9 PM the mother (the Moon) walks into Taurus, where she is exalted.'],
         closing='Good for hosting, giving and talking things through'),
    dict(type='grid', label='Tuesday’s full Moon', title='Find your Moon sign', cells=cells[:6], celllab=22, cellsize=62, celltext=33, cellpad=28, note='Count Taurus from the sign your Moon was in at birth'),
    dict(type='grid', label='Tuesday’s full Moon', title='Find your Moon sign', cells=cells[6:], celllab=22, cellsize=62, celltext=33, cellpad=28, note='Don’t know your Moon sign? Ask at asksutram.com'),
    dict(type='stack', label='Also this week', title='Mark your calendar', items=[['Monday night, about 9 PM', 'The Moon walks into Taurus'], ['Tuesday, about 10 AM', 'Full Moon in Taurus'],
                                                                              ['All week', 'Venus is home in Libra: comfort, taste and money talks come easier'], ['Friday night', 'The Moon goes home to Cancer: a softer weekend, closer to family']], linesize=40),
    dict(type='text', orbs=[o(MOON, 64)], label='This full Moon', title='Kartik Purnima', closing='Light a lamp, give something away', closingsize=52),
    dict(type='cta', orbs=[o(MOON, 50)], title='What does it mean\nfor your Moon sign?', titlesize=84, subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Monday · Rule 10, where water meets fire'),
])
CAP['week-2026-11-22-c'] = ("""Week ahead: a full Moon in Taurus, for your Moon sign

On Monday night at about 9 PM the mother (Moon) walks into Taurus, her best sign. On Tuesday at about 10 AM Toronto time she is full there, facing the king (Sun) in Scorpio. Grahas face to face act on each other directly (rule 4), so the mind and the self meet in full light. An exalted Moon reads as a calm, kind mind: good for hosting, giving and talking things through.

To see where it lands for you, count Taurus from your Moon sign, the sign the Moon was in when you were born:
""" + '\n'.join(f'{m} Moon, {ORD[house_from(m, "Taurus")]}: {HOUSE[house_from(m, "Taurus")].lower()}' for m in SIGNS) + """

Also this week, the lover (Venus) has been home in Libra since Sunday morning, so comfort, taste and money talks come easier. On Friday night the Moon goes home to Cancer, her own sign, and the weekend feels softer and closer to family.

This full Moon is Kartik Purnima. The tradition is to light a lamp and give something away.

What will you give away this week? Tell us in the comments.

Ask what the full Moon in Taurus means for your Moon sign at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#fullmoon #kartikpurnima #jyotish #vedicastrology #sutram
""")

if __name__ == '__main__':
    for pid, spec in POSTS.items():
        json.dump(dict(id=pid, **spec), open(os.path.join(REPO, 'specs', f'{pid}.json'), 'w'), indent=1, ensure_ascii=False)
        open(os.path.join(REPO, 'captions', f'{pid}.txt'), 'w').write(CAP[pid])
        shutil.copy(os.path.join(REPO, 'x-drafts', f'{pid[:-2]}-x.txt'), os.path.join(REPO, 'x-drafts', f'{pid}-x.txt'))
        print(pid, len(spec['slides']), 'slides', len(CAP[pid].strip()), 'caption chars')
