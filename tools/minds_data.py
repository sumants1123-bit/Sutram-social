#!/usr/bin/env python3
"""The content behind "Which kind of mind is yours?" (the page for asksutram.com/mind and the post know-seven-minds).

Sumant, 19 Nov 2026, 11:03 AM, after loving the post: "I want to make a category maybe on asksutram.com where people go on
asksutram.com direct link and then it shows what's their mind like, and that page is so nice and beautiful and attracts people and
gives explanation and details ... that analysis is combination of few other things, right? ... that can get into a real product
later on, paid one, that's a different story ... it can end with like, see which mind you have as this link ... Then which all
things it's really good for." At 11:14 AM he added his own example: "probably I have a moving mind ... I search while moving, I work
while moving, brainstorm while moving, I do everything while walking ... somebody like study". That example sits under the moving
kind here; the steady kind gets the study example. (His own Moon star is listed as soft and his Moon sign is movable; he was told.)

One home for the words: this file writes site/minds.json, and both the working page and the app read that file.
Which star sits in which kind: tools/look_art.py. Each star's span, lord, deity, symbol and quarter signs: site/nakshatras.json.
Each sign's element and type: site/signs.json.

Sources opened on 19 Nov 2026:
- Brihat Samhita ch. 98, verses 6 to 11, tr. N. C. Iyer (wisdomlib.org/hinduism/book/brihat-samhita/d/doc229361.html): what each
  group of stars is chosen for. Stable: coronation of kings, expiatory ceremonies, planting of trees, the building of towns, works
  for the public good, sowing seed, lasting undertakings. Sharp: punishment, incantations, raising of goblins, imprisonment,
  inflicting pain, rites that separate or join people. Severe: acts of disgrace, destruction, deceit, imprisonment, poison,
  burning, striking with weapons. Light: sales, acts of love, acquiring knowledge, wearing ornaments, the arts, craft, medicine.
  Soft: acts of friendship, union, buying clothes, wearing or making ornaments, auspicious undertakings, music. Soft and sharp:
  mixed results. Moving: works of a moving character. The page names the mildest of the harsh acts and leaves the rest out.
- The Sanskrit of the moving verse (de.wisdomlib.org/hinduism/book/brihat-samhita-sanskrit/d/doc1220823.html): see tools/post_minds.py.
- Meanings of the star names: the table in Wikipedia's "List of Nakshatras" (read through wikiwand.com). Ardra as "wet, moist,
  fresh": Monier-Williams and Apte (wisdomlib.org/definition/ardra). Shravana has no meaning in that table; "the ear" is its symbol.
- Brihat Parashara Hora Shastra 3.12: the Moon is the mind. 4.5: the signs are movable, fixed and dual
  (enjoylearningsanskrit.com/scriptures/parashara/chapter-4). The four elements follow site/signs.json; the text itself does not
  give one element per sign, so the page does not cite it for elements.
Every "reading" line (what a mind is like, what it is good for in a week, each star's line, the quarter, the Moon's light, the
grahas beside the Moon) is Sutram's reading, and the page says so.

    python3 tools/minds_data.py     # writes site/minds.json
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import look_art as A
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KINDS = [
 dict(key='steady', name='The steady mind', a='a steady mind', sanskrit='dhruva', line='Builds what lasts',
      like='Your mind settles on a thing and stays with it. It can sit with one book for hours, it likes to finish what it starts, and it gets better with time.',
      texts='The texts pick these stars for crowning a king, planting trees, building a town, sowing seed, and anything meant to last.',
      good=['Long projects', 'Saving and investing', 'Keeping a promise', 'Building a home or a team'],
      grain=['Give it time. A steady mind hates being rushed', 'Let it finish one thing before the next', 'Ask it for the long view'],
      watch='It can hold on after it is time to let go'),
 dict(key='moving', name='The moving mind', a='a moving mind', sanskrit='chara', line='Thinks on the move',
      like='Your mind works best in motion. It searches, plans and brainstorms on its feet, and a walk often solves what sitting still could not.',
      texts='The texts pick these stars for travel and for any work that has to move.',
      good=['Travel and moving house', 'Meeting new people', 'Work that changes every day', 'Starting again somewhere new'],
      grain=['Walk while you think', 'Change the room when you are stuck', 'Keep one fixed habit as an anchor'],
      watch='It can leave before the work is done'),
 dict(key='light', name='The light mind', a='a light mind', sanskrit='laghu', line='Quick hands, quick study',
      like='Your mind is quick and light on its feet. It picks up a skill fast and likes work it can finish in one sitting.',
      texts='The texts pick these stars for trade, learning, craft, the arts and medicine.',
      good=['Learning a new skill', 'Buying and selling', 'Work with your hands', 'Short tasks with a clear finish'],
      grain=['Give it short tasks with a clear finish', 'Let it learn by doing', 'Pair it with someone who finishes'],
      watch='It can move on when the spark goes'),
 dict(key='soft', name='The soft mind', a='a soft mind', sanskrit='mridu', line='Warm and tactful',
      like='Your mind is gentle and reads a room well. It looks for what is pleasant and for what brings people together.',
      texts='The texts pick these stars for friendship and love, music, new clothes, ornaments and celebrations.',
      good=['Making and keeping friends', 'Music, art and design', 'Hosting and celebrations', 'Calming a tense room'],
      grain=['Give it good company and a pleasant room', 'Bring hard news gently', 'Let it make things beautiful'],
      watch='It can put off a hard talk for too long'),
 dict(key='fierce', name='The fierce mind', a='a fierce mind', sanskrit='ugra', line='Heat and nerve',
      like='Your mind runs hot and does not back down. Pressure wakes it up, and it can do the hard thing that others put off.',
      texts='The texts give these stars the fiercest work, such as battle, fire, and tearing down what must go.',
      good=['A fight worth having', 'Ending what should end', 'Work under pressure', 'Hard training'],
      grain=['Give it a real challenge', 'Be direct. It respects that', 'Let it cool down before a big talk'],
      watch='It can come on too strong'),
 dict(key='sharp', name='The sharp mind', a='a sharp mind', sanskrit='tikshna', line='Cuts to the root',
      like='Your mind goes straight to what is underneath. It notices what others miss and does not accept the easy answer.',
      texts='The texts give these stars the cutting work, such as strict discipline, mantra practice, and breaking a tie or binding one.',
      good=['Research and finding the cause', 'Editing and cutting what is not needed', 'Breaking a habit', 'Deep practice, such as mantra or meditation'],
      grain=['Give it the real reason', 'Hand it the hard problem', 'Let it work alone when it needs to'],
      watch='Its words can cut deeper than it means'),
 dict(key='mixed', name='The soft-and-sharp mind', a='a soft-and-sharp mind', sanskrit='mridu-tikshna', line='Gentle and cutting by turns',
      like='Your mind has two hands. One is gentle and one cuts, and you choose which a moment needs. People meet your kindness first and your edge later.',
      texts='The texts call these two stars soft and sharp at once and say their results are mixed. Both belong to Agni, the fire.',
      good=['Honest feedback, given kindly', 'Teaching and coaching', 'Cooking and any work with fire', 'Jobs that need care and a firm line'],
      grain=['Tell it which hand you need today', 'Give it work that needs both care and a cut', 'Expect warmth first and the edge after'],
      watch='People cannot always tell which hand is coming'),
]

# name -> (what the name means, Sutram's reading of that star as a mind)
STAR = {
 'Ashwini': ('the twin healers', 'A mind that is first out of the gate. It moves before others have decided, and it likes to fix things fast.'),
 'Bharani': ('the bearer', 'A mind that can carry what is heavy. It sees a hard thing through to the end.'),
 'Krittika': ('the Pleiades', 'A mind like a kitchen fire. It warms and feeds, and it burns away what is false.'),
 'Rohini': ('the red one', 'A mind that grows things. It is patient and fond of beauty, and it makes a place feel like home.'),
 'Mrigashira': ('the deer’s head', 'A mind that searches. Curious and gentle, it follows a scent from one thing to the next.'),
 'Ardra': ('the moist one', 'Moist, like the ground after rain. A mind that feels the storm fully, then starts fresh.'),
 'Punarvasu': ('the restorers', 'A mind that comes back. It can lose its way and find it again, and it returns from every trip with something good.'),
 'Pushya': ('the nourisher', 'A mind that feeds others. It teaches, looks after people, and does small useful things every day.'),
 'Ashlesha': ('the embrace', 'A mind that coils around a thing and holds it. Watchful and hard to fool, it sees what is hidden.'),
 'Magha': ('the bountiful', 'A mind that remembers where it comes from. It carries itself with pride and wants to be worthy of its people.'),
 'Purva Phalguni': ('the first red one', 'A mind that loves life. It wants play, pleasure and good company, and it goes after them with full heat.'),
 'Uttara Phalguni': ('the second red one', 'A mind that keeps its word. It is the friend who stays, and it likes a clear agreement.'),
 'Hasta': ('the hand', 'A mind in the hands. It learns by making, and it is clever, quick and good with detail.'),
 'Chitra': ('the bright one', 'A mind with an eye for design. It sees how a thing could look and wants to make it beautiful.'),
 'Swati': ('the very good one', 'A mind like a young shoot in the wind. It bends and does not break, and it needs room to move on its own.'),
 'Vishakha': ('the forked one', 'A mind with one goal and two roads to it. It is patient until the goal is close, then it pushes hard.'),
 'Anuradha': ('following Radha', 'A mind made for friendship. It is loyal, works well with others, and blooms in hard places like a lotus.'),
 'Jyeshtha': ('the eldest', 'A mind that takes charge. It feels responsible for others and guards what is its own.'),
 'Mula': ('the root', 'A mind that digs. It keeps asking why until it reaches the bottom of a thing.'),
 'Purva Ashadha': ('the first unbeaten one', 'A mind that does not accept defeat. It believes it can win, and that belief carries other people along.'),
 'Uttara Ashadha': ('the later unbeaten one', 'A mind that wins slowly and for good. It takes the long road and does things the right way.'),
 'Shravana': ('the ear', 'A mind that listens. It learns by hearing, remembers what was said, and travels to learn more.'),
 'Dhanishta': ('the most famous', 'A mind with rhythm. It keeps time, moves well with a group, and likes to be seen doing it.'),
 'Shatabhisha': ('a hundred physicians', 'A mind that keeps to itself and thinks in systems. It wants to find what truly fixes a thing.'),
 'Purva Bhadrapada': ('the first of the blessed feet', 'A mind of strong conviction. It can burn for an idea and give up comfort for it.'),
 'Uttara Bhadrapada': ('the second of the blessed feet', 'A mind with depth. Calm on the surface and slow to anger, it holds steady when things get rough.'),
 'Revati': ('the prosperous one', 'A mind that looks after others on the road. Kind and dreamy, it helps people get where they are going.'),
}
assert sorted(STAR) == sorted(A.NAK)

TYPE = {'cardinal': 'movable', 'fixed': 'fixed', 'mutable': 'dual'}       # site/signs.json uses the Western words
ELEMENT = {'fire': 'A fire sign. Your mind runs on belief and energy.', 'earth': 'An earth sign. Your mind runs on what is real and useful.',
           'air': 'An air sign. Your mind runs on ideas and people.', 'water': 'A water sign. Your mind runs on feeling.'}
MODE = {'movable': 'It is a movable sign, so your mind likes to be on the move and to start things.', 'fixed': 'It is a fixed sign, so your mind likes to stay put and hold its ground.',
        'dual': 'It is a dual sign, so your mind likes to keep two roads open.'}
QUARTER = {'fire': 'It adds drive. You act on what you think.', 'earth': 'It adds patience. You want your thinking to be useful.',
           'air': 'It adds talk. You think by sharing ideas.', 'water': 'It adds feeling. Your heart weighs in first.'}
# the Moon's light at birth, by the angle from the Sun to the Moon (0 new, 180 full); from/to in degrees, new wraps round zero
LIGHT = [
 dict(key='new', label='Near the new Moon', born='near the new Moon', frm=324, to=36, line='A dark Moon keeps its light inside. Your mind does its best work in private.'),
 dict(key='waxing', label='A growing Moon', born='under a growing Moon', frm=36, to=144, line='The Moon was filling. Your mind reaches outward and builds as it goes.'),
 dict(key='full', label='Near the full Moon', born='near the full Moon', frm=144, to=216, line='A full Moon shows everything. Your feelings are easy to read, for you and for others.'),
 dict(key='waning', label='A waning Moon', born='under a waning Moon', frm=216, to=324, line='The Moon was emptying. Your mind sorts, lets go, and knows what to keep.'),
]
COMPANY = {
 'Sun': ('the king', 'Your mind stays close to your purpose and wants its work to matter.'),
 'Mars': ('the soldier', 'Your mind is quick to act and likes a challenge.'),
 'Mercury': ('the messenger', 'Your mind thinks in words and works things out by talking or writing.'),
 'Jupiter': ('the teacher', 'Your mind looks for the lesson and the bigger picture.'),
 'Venus': ('the lover', 'Your mind is drawn to beauty, comfort and people.'),
 'Saturn': ('the auditor', 'Your mind checks things twice and takes its duties seriously.'),
 'Rahu': ('the magician', 'Your mind is hungry for the new and makes big whatever it looks at.'),
 'Ketu': ('the monk', 'Your mind lets go easily and needs time alone.'),
}
PAGE = dict(
 path='/mind', kicker='Know yourself', title='Which kind of mind is yours?',
 sub='Your mind is one slice of a bigger one. Jyotish reads it from the star the Moon was in when you were born.',
 cta='Find my mind', form_title='Your birth details', form_note='Free. No sign-up.', submit='Show my mind',
 result_kicker='Your mind', result_star='Your Moon was in {star}, {means}.', result_quarter='{nth} quarter of four.',
 like_h='What it is like', good_h='Really good for', texts_h='In the old texts', star_h='Your star', quarter_h='Your quarter',
 quarter_line='Each star is cut into four quarters, so yours is a slice of a slice. Yours belongs to {sign}, {article} {element} sign.',
 more_h='A few more things shape it', sign_h='Your Moon sign', light_h='The Moon when you were born', company_h='Who sits with your Moon',
 company_one='{graha}, {role}, shares your Moon’s sign.', company_none='No other graha shares your Moon’s sign. Your mind keeps its own company.',
 together_h='Put together', together='{kind}, in {article} {type} {element} sign, born {born}{company}.', together_company=', with {names} beside it',
 grain_h='Work with the grain', watch_h='Watch for', share_h='Share it', share_line='I have {a}', share_ask='Which kind of mind is yours?',
 ask='Ask Sutram about my mind', ask_prompt='What does my Moon in {star} say about how I think, and what should I use it for?',
 how_h='How Jyotish reads the mind',
 how=[['The Moon is the mind', 'In a birth chart the Moon stands for the mind.'],
      ['Its road has 27 stars', 'The Moon circles the sky in about 27 days and spends about a day in each star.'],
      ['The stars come in seven kinds', 'An old text sorts them by nature: steady, moving, light, soft, fierce, sharp, and soft and sharp at once.']],
 kinds_h='The seven kinds of mind', kinds_sub='Tap one to read it.',
 no_time='Add your birth time to see your quarter.', two_stars='The Moon changed star that day. Pick the part of the day you were born in.',
 window_first='Born before {time}', window_last='Born after {time}', window_mid='Born between {from} and {to}',
 astro_h='Show the astrology',
 sources_h='Where this comes from',
 sources=['The Moon as the mind: Brihat Parashara Hora Shastra 3.12. The great Person whose mind became the Moon: Rig Veda 10.90.13.',
          'The seven natures of the stars: Brihat Samhita, chapter 98. The text sorts the stars to choose a day for a task.',
          'Movable, fixed and dual signs: Brihat Parashara Hora Shastra 4.5.',
          'Reading all of this as a kind of mind is Sutram’s reading. It is for reflection and is no substitute for medical or psychological advice.'],
)


def build():
    nak = {n['name']: n for n in json.load(open(os.path.join(REPO, 'site', 'nakshatras.json')))}
    sig = {s['name']: s for s in json.load(open(os.path.join(REPO, 'site', 'signs.json')))}
    kinds = [dict(k, color=A.COL['day'][k['key']], color_dark=A.COL['night'][k['key']], stars=A.STARS[k['key']]) for k in KINDS]
    stars = []
    for i, name in enumerate(A.NAK):
        n = nak[name]; assert n['index'] == i + 1
        stars.append(dict(index=i + 1, name=name, means=STAR[name][0], kind=A.NATURE_OF[name], reading=STAR[name][1], symbol=n['symbol'], deity=n['deity'], lord=n['lord'],
                          start=n['start'], end=n['end'], quarter_signs=n['pada_signs']))
    signs = [dict(name=s['name'], element=s['element'], type=TYPE[s['quality']]) for s in sig.values()]
    out = dict(version='2026-11-19', note='Content for asksutram.com/mind. Written by tools/minds_data.py in the Sutram-social repo. Positions never come from this file: the engine gives the Moon’s star, quarter, sign, the Sun and the other grahas.',
               page=PAGE, kinds=kinds, stars=stars, signs=signs, element=ELEMENT, sign_type=MODE, quarter=QUARTER, light=LIGHT,
               company={g: dict(role=r, line=l) for g, (r, l) in COMPANY.items()})
    return out


if __name__ == '__main__':
    out = build(); fn = os.path.join(REPO, 'site', 'minds.json')
    json.dump(out, open(fn, 'w'), indent=1, ensure_ascii=False)
    txt = json.dumps(out, ensure_ascii=False)
    bad = [w for w in ('—', '!', 'journey', 'cosmic', 'sacred', 'planet') if w in txt.replace('cosmic Person', '')]
    print(fn, len(txt), 'chars;', len(out['kinds']), 'kinds;', len(out['stars']), 'stars;', 'flagged words:', bad or 'none')
