#!/usr/bin/env python3
"""Sunday batch for Mon 23 to Sun 29 Nov 2026, in the cream look (tools/render_look.py), run Sun 22 Nov 7 PM.

The stored prompt (plan/batch_22nov_prompt.txt) asks for: Lesson 20 remade for Monday, Sutras on Tuesday and Thursday,
Lessons 21 to 24, The Thread part 5, Read the sky on Friday, Krishna the Moon on Saturday, the week ahead on Sunday,
and the two philosophy posts already built (phil-breath, phil-eclipse), which are only scheduled.

Look: rules_18nov in plan/state.json. Sumant has not picked a mark, border or grid yet, so every spec uses foot "word" and
border "arcs" (the gemstone post he approved), and Grid X counts Instagram posts from Mon 23 Nov 12 PM: posts 2, 5, 8, 11, 14
are dark. "Awareness is you" (Thu 26 Nov 6:30 PM, cream, approved by Sumant on 21 Nov) is post 9, so Thursday has three posts and
Saturday evening's dark philosophy post lands on a cream number: one tile off the pattern, said in the message.

Every position, time and speed below comes from tools/sky.py (Swiss Ephemeris, Moshier, Lahiri, mean node, Toronto time),
run on 22 Nov 2026 (scratch eng.py and eng2.py):
  Mon 23 Nov noon: Jupiter Leo 2°11′ (Magha), Ketu Leo 0°38′, Mars Leo 4°51′; Mars passed Leo 3°20′ on Thu 19 Nov evening
  Tue 24 Nov noon: Sun Scorpio 8°11′ in Anuradha (lord Saturn); Saturn Pisces 13°56′ in Uttara Bhadrapada (lord Saturn)
  Moon into Cancer Fri 27 Nov 8:55 PM, into Leo Sun 29 Nov 11:15 PM, into Libra Fri 4 Dec 12:35 PM
  Saturn turned backward about 26 Jul (Pisces 20.5°), turns forward Thu 10 Dec 8 PM (Pisces 13°42′);
  speed 1.84′ a day on 23 Nov, 0.58′ on 5 Dec, 0.03′ on 10 Dec
  Jupiter turns backward Sat 12 Dec 8 PM (Leo 2°47′), forward again Tue 13 Apr 2027 (Cancer 22.75°); Mars turns backward Sun 10 Jan 2027
  Mercury into Scorpio Wed 2 Dec 6:58 AM; mean Rahu into Capricorn (Ketu into Cancer) Sat 5 Dec 12:03 PM
  New Moon in Scorpio Tue 8 Dec 8:00 PM
Rahu in Aquarius and Ketu in Leo carry no reading from 24 Nov on (Monday's doorway lesson is the last post that names Ketu in Leo).

Sources opened on 22 Nov 2026 before use:
  BPHS 3.23 to 3.29 (enjoylearningsanskrit.com): Sun pitta, Moon vata and kapha, Mars pitta, Mercury pitta, kapha and vata,
    Jupiter kapha, Venus kapha and vata, Saturn vata. BPHS 3.24: the Moon has kind eyes, sweet speech, a restless nature.
  BPHS 11.11 (10th house, vyomasthana: status, livelihood, honour, the father, living abroad, debts) and 11.12 (11th house:
    gains of many kinds, income, growth, livestock), enjoylearningsanskrit.com
  Ashtanga Hridayam, Sutrasthana 1.6 (satyori.com): in brief, the three doshas are vata, pitta and kapha
  Bhagavata Purana 10.3.1 (vedabase.io): Krishna's birth under Rohini; 10.1.1 with purport (vedabase.com): the Yadu line came from Soma
  KP (astrosage KP system FAQ): a planet gives results as per its star lord
  Nadi rule bank (claude/nadi-thread/thread.md, checked rules only): M-144 and the karakatwa table (Rao), C-030 and C-013/C-024
    (Jitender Kumar, Nadi Jyotisha, ch. 4), C-023 (ch. 3), C-038 (ch. 5), W-013 (ch. 4), M-106 and M-093 (Rao's table)

    python3 tools/week48.py      # writes specs/<id>.json, captions/<id>.txt, x-drafts/<id>-x.txt and plan/week48.json
"""
import json, os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
ORD = {1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th', 6: '6th', 7: '7th', 8: '8th', 9: '9th', 10: '10th', 11: '11th', 12: '12th'}
HOUSE = {1: 'You in focus', 2: 'Savings, family, food', 3: 'Effort, short trips', 4: 'Home, mother, repairs', 5: 'Kids, study, romance', 6: 'Routine, debts, fitness',
         7: 'Partner, clients, deals', 8: 'Quiet change', 9: 'Luck, teachers, travel', 10: 'Work and standing', 11: 'Gains and good friends', 12: 'Spending, travel, rest'}
SHORT = {1: 'you in focus', 2: 'savings, family', 3: 'effort, short trips', 4: 'home', 5: 'kids, study, romance', 6: 'routine, debts', 7: 'partner, deals',
         8: 'quiet change', 9: 'luck, teachers', 10: 'work, standing', 11: 'gains, friends', 12: 'spending, rest'}
house_from = lambda moon, sign: (SIGNS.index(sign) - SIGNS.index(moon)) % 12 + 1
O = lambda kind, r, **k: dict(kind=kind, r=r, **({'rings': False} if kind == 'sun' else {}), **k)
ASK = 'Weekly newsletter at sutram.ca/newsletter'
LOOK = dict(foot='word', border='arcs')
KNOTS = ['Ashlesha', 'Magha', 'Jyeshtha', 'Mula', 'Revati', 'Ashwini']
POSTS, CAP, X, PLAN = {}, {}, {}, []


def post(pid, look, kicker, slides, caption, x, ig, xw, xs, xalt, family):
    POSTS[pid] = dict(id=pid, look=look, kicker=kicker, **LOOK, slides=slides)
    CAP[pid] = caption.strip() + '\n'
    X[pid] = x.strip() + '\n'
    PLAN.append(dict(id=pid, look=look, ig=ig, x=xw, x_slides=xs, x_alt=xalt, family=family))


# ------------------------------------------------------------------ Mon 23 · 12 PM · Lesson 20, rule 10 (post 1, cream)
post('lesson20-doorway-c', 'day', 'Lesson 20 · Nadi rules', [
    dict(type='cover', art=dict(kind='wheel', size=500, lit=KNOTS, mode='pick', pick='Magha', quarters=True, dot=True),
         title='Where water\nmeets fire', titlesize=104, subtitle='The doorway the classics call Gandanta', subsize=46),
    dict(type='text', label='Rule 10', title='Three doorways', body=['Three times round the zodiac a water sign ends and a fire sign begins.'],
         closing='Cancer to Leo, Scorpio to Sagittarius, Pisces to Aries'),
    dict(type='text', label='The knot', title='Gandanta', titlesize=96,
         body=['The last degrees of a water sign and the first of a fire sign. A graha here stands between two worlds.'],
         closing='What is ending and what is starting get tangled'),
    dict(type='rows', label='How to read it', title='Is it in a doorway?', items=[['1', 'Is the graha in a water or a fire sign?'], ['2', 'Is it near the end of water or the start of fire?'], ['3', 'Then it stands in a doorway']]),
    dict(type='cast', label='Monday 23 November', title='Two in Leo’s\ndoorway', headsize=54, linesize=34, iconw=140, items=[
        dict(orbs=[O('ketu', 40)], head='The monk (Ketu)', line='Just over half a degree into Leo, walking backward toward Cancer.'),
        dict(orbs=[O('jupiter', 46)], head='The teacher (Jupiter)', line='About 2 degrees into Leo, and slowing down.')],
         note='The soldier (Mars) walked out on Thursday 19 November'),
    dict(type='text', orbs=[O('jupiter', 52), O('ketu', 42)], orbgap=40, label='Coming up', title='Both stay\nat the door',
         body=['On Saturday 5 December, about noon, the monk walks back through it into Cancer.', 'On 12 December the teacher stops there and turns backward.'], bodysize=38),
    dict(type='text', label='In real life', title='Finish the old first', body=['Like closing one tab before you open the next.'], closing='Then start the new'),
    dict(type='cta', orbs=[O('jupiter', 40), O('ketu', 34)], orbgap=24, title='Is any graha in your\nchart in a doorway?', titlesize=80,
         subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Tuesday · Rule 11, whose star'),
], """Nadi rule 10: the doorway, Gandanta

Three times around the zodiac a water sign ends and a fire sign begins: Cancer into Leo, Scorpio into Sagittarius, Pisces into Aries. The classics call these joints Gandanta, the knot. The last few degrees of the water sign and the first few of the fire sign make the doorway.

They are also the only three places where a sign and one of the Moon's 27 stars end at the same point. Signs are 30 degrees wide and stars 13 degrees 20 minutes, so their edges meet only every 120 degrees.

A graha in the doorway stands between two worlds: what is ending and what is starting get tangled. Go slow at the door.

To read it, check whether the graha sits in a water or a fire sign, then whether it is near the end or the start of it.

This week the teacher (Jupiter) and the monk (Ketu) stand inside Leo's doorway. The monk, just over half a degree in, walks backward through the knot into Cancer on Saturday 5 December at about noon. The teacher is slowing down, stops there on 12 December and turns backward. The soldier (Mars) walked out of it on Thursday 19 November.

Finish the old before you start the new, like closing one tab before you open the next.

Is any graha in your chart near a doorway? Tell us in the comments.

Next: Tuesday, rule 11, whose star

Ask whether any graha in your chart sits in a doorway at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#jyotish #gandanta #nadiastrology #vedicastrology #sutram""", """Nadi rule 10: the doorway

Where water meets fire: Cancer to Leo, Scorpio to Sagittarius, Pisces to Aries. Jupiter and Ketu stand in Leo's doorway now. Ketu walks back into Cancer on 5 December, Jupiter stops there on 12 December

asksutram.com
sutram.ca/newsletter""", '2026-11-23T12:00:00-05:00', '2026-11-23T13:00:00-05:00', [1, 2, 5, 6],
     ['Where water meets fire. The doorway the classics call Gandanta', 'Three doorways: Cancer to Leo, Scorpio to Sagittarius, Pisces to Aries',
      'Two in Leo’s doorway: the monk (Ketu) and the teacher (Jupiter)', 'Both stay at the door: Ketu into Cancer on 5 December, Jupiter stops on 12 December'], 'lesson')

# ------------------------------------------------------------------ Tue 24 · 10 AM · Sutra, the 11th house (post 3, cream)
post('sutra-11th-house', 'day', 'Sutra · The 11th house', [
    dict(type='cover', orbs=[O('venus', 92), O('mercury', 70)], orbgap=40, title='The 11th house', titlesize=112, subtitle='Where your gains come from', motion='rise'),
    dict(type='quote', label='Brihat Parashara Hora Shastra 11.12', quote='Read income and growth\nfrom the house of gains.', quotesize=72,
         sanskrit='āyaṃ vṛddhiṃ paśūnāṃ ca bhavasthānānnirīkṣaṇam', sanskritsize=34, body=['Parashara adds livestock, the wealth of his day.'], bodysize=36),
    dict(type='stack', label='What lives here', title='Gains of every kind', items=[['Income', 'Money that comes in, from any side'], ['Growth', 'What keeps adding up over the years'], ['Many kinds of gain', 'Things and chances that come your way']], linesize=42),
    dict(type='text', label='Why after the 10th', title='What your work\nbrings home', body=['The 10th house is your work. The 11th comes right after it, so it shows what your work brings back.'],
         note='Sutram’s reading, built on the classical meanings'),
    dict(type='cast', label='Two grahas to check', title='Wealth and friends', items=[
        dict(orbs=[O('venus', 46)], head='The lover (Venus)', line='In Nadi she stands for wealth.'),
        dict(orbs=[O('mercury', 40)], head='The messenger (Mercury)', line='He stands for friends and business.')],
         note='R. G. Rao, Fundamentals, chapter 7'),
    dict(type='text', label='In your chart', title='Who sits in\nyour 11th?', body=['Count to the 11th sign from your rising sign. The grahas there, and the lord of that sign, show how gains reach you.']),
    dict(type='rows', label='In real life', title='Your income has\na network', items=[['1', 'Most gains arrive through someone'], ['2', 'A referral, a client, a friend of a friend'], ['3', 'This week, thank one person who sent work your way']]),
    dict(type='cta', orbs=[O('venus', 44), O('mercury', 36)], orbgap=24, title='Where do your\ngains come from?', titlesize=86, subtitle='Ask your chart at asksutram.com', lines=[ASK]),
], """The 11th house: where your gains come from

Parashara gives each house its matters. For the 11th, the house of gains, he lists gains of many kinds, income and growth, and, in his day, livestock (Brihat Parashara Hora Shastra 11.12).

What lives here:
Income: money that comes in, from any side
Growth: what keeps adding up over the years
Many kinds of gain: things and chances that come your way

Why the 11th? The 10th house is your work, and the 11th comes right after it, so it shows what your work brings home. That is Sutram's reading, built on the classical meanings. It is also one of the four houses that grow (upachaya), with the 3rd, 6th and 10th, so gains here tend to build slowly, like savings.

Two grahas to check with it. In Nadi the lover (Venus) stands for wealth and the messenger (Mercury) for friends and business (R. G. Rao, Fundamentals of Rao's System of Nadi Astrology, chapter 7).

In your chart, count to the 11th sign from your rising sign. The grahas there, and the lord of that sign, show how gains reach you.

In real life your income has a network. Most gains arrive through someone: a referral, a client, a friend of a friend. This week, thank one person who sent work your way.

Who brought you your best chance this year? Tell us in the comments.

Ask what your 11th house says about where your gains come from at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#jyotish #vedicastrology #11thhouse #sutra #sutram""", '', '2026-11-24T10:00:00-05:00', None, [], [], 'sutra')

# ------------------------------------------------------------------ Tue 24 · 12 PM · Lesson 21, rule 11 (post 4, cream)
post('lesson21-whose-star', 'day', 'Lesson 21 · Nadi rules', [
    dict(type='cover', art=dict(kind='wheel', size=500, mode='pick', pick='Anuradha'), title='Whose star\nis it in?', titlesize=104, subtitle='Every graha works for a star lord', subsize=46),
    dict(type='text', label='Rule 11', title='27 stars, 9 lords', body=['The Moon’s road is cut into 27 stars, the nakshatras. Each star has a lord, one of the nine grahas.'],
         closing='Three rounds of the same nine lords'),
    dict(type='rows', label='How to read it', title='Three steps', items=[['1', 'Find the star the graha stands in'], ['2', 'Find that star’s lord'], ['3', 'Read the graha through its lord and the house it sits in']]),
    dict(type='text', orbs=[O('sun', 58), O('saturn', 42)], orbgap=30, label='This week', title='The king works\nfor the auditor',
         body=['The Sun stands in Anuradha, one of Saturn’s stars. Read the king through the auditor: bosses want patience and careful work.']),
    dict(type='text', orbs=[O('saturn', 54)], label='In its own star', title='Saturn answers\nto Saturn',
         body=['Saturn stands in Uttara Bhadrapada, one of its own stars, so it carries its own work.'], closing='Slow, steady, checked twice'),
    dict(type='text', label='In your chart', title='Your birth star\nstarts your clock', body=['The star your Moon was born in has a lord. That lord runs the first dasha of your life.']),
    dict(type='text', label='In real life', title='Like a job title', body=['A sales manager still reports to someone. Whose star a graha stands in tells you who it reports to.']),
    dict(type='cta', orbs=[O('moon', 46)], title='Whose star is\nyour Moon in?', titlesize=86, subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Wednesday · Rule 12, start with its graha'),
], """Rule 11: whose star a graha stands in

The Moon's road through the sky is cut into 27 stars, the nakshatras. Each star has a lord, one of the nine grahas, in the order of the Vimshottari dasha:
Ketu: Ashwini, Magha, Mula
Venus: Bharani, Purva Phalguni, Purva Ashadha
Sun: Krittika, Uttara Phalguni, Uttara Ashadha
Moon: Rohini, Hasta, Shravana
Mars: Mrigashira, Chitra, Dhanishta
Rahu: Ardra, Swati, Shatabhisha
Jupiter: Punarvasu, Vishakha, Purva Bhadrapada
Saturn: Pushya, Anuradha, Uttara Bhadrapada
Mercury: Ashlesha, Jyeshtha, Revati

The rule: read a graha through the lord of its star. Its results come through that lord and the house it sits in. K. S. Krishnamurti made this star-lord reading the heart of his KP system, and Sutram reads every chart with it.

This week the king (Sun) stands in Anuradha, one of the auditor's (Saturn's) stars, so read the king through the auditor: bosses want patience and careful work. Saturn itself stands in Uttara Bhadrapada, one of its own stars, so it carries its own work: slow, steady, checked twice.

In your chart, the lord of the star your Moon was born in runs the first dasha of your life.

In real life it works like a job title. A sales manager still reports to someone. Whose star a graha stands in tells you who it reports to.

Whose star is your Moon in? Tell us in the comments.

Next: Wednesday, rule 12, start with its graha

Ask whose star each of your grahas stands in at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#jyotish #nakshatra #nadiastrology #vedicastrology #sutram""", """Rule 11: whose star

27 stars, 9 lords. Read a graha through the lord of its star. This week the Sun stands in Anuradha, one of Saturn's stars: bosses want patience and careful work

asksutram.com
sutram.ca/newsletter""", '2026-11-24T12:00:00-05:00', '2026-11-24T13:00:00-05:00', [1, 3, 4, 6],
     ['Whose star is it in? The wheel of the Moon’s 27 stars', 'Three steps: find the star, find its lord, read the graha through its lord',
      'The king works for the auditor: the Sun in Anuradha, a Saturn star', 'Your birth star starts your clock: its lord runs your first dasha'], 'lesson')

# ------------------------------------------------------------------ Wed 25 · 12 PM · Lesson 22, rule 12 (post 5, dark)
post('lesson22-its-graha', 'night', 'Lesson 22 · Nadi rules', [
    dict(type='cover', orbs=[O('saturn', 70), O('venus', 66), O('mercury', 54)], orbgap=30, title='Start with\nits graha', titlesize=110, subtitle='Every part of life has a graha that carries it', motion='rise'),
    dict(type='text', label='Rule 12', title='Find the carrier\nfirst', body=['To study one matter of life, Nadi first finds the graha that signifies it, its karaka. Then it reads everything from there.'],
         note='R. G. Rao, Bhrigu Nandi Nadi, introduction'),
    dict(type='cast', label='Rao’s table · family', title='Home and family', items=[
        dict(orbs=[O('sun', 40)], head='The Sun', line='Your father'),
        dict(orbs=[O('moon', 40)], head='The Moon', line='Your mother'),
        dict(orbs=[O('jupiter', 40)], head='Jupiter', line='Children, teachers and guides')]),
    dict(type='cast', label='Rao’s table · work and life', title='Work and life', items=[
        dict(orbs=[O('saturn', 32)], head='Saturn', line='Your work'),
        dict(orbs=[O('mercury', 34)], head='Mercury', line='Education and business'),
        dict(orbs=[O('venus', 38)], head='Venus', line='Wealth, and the graha looked to for marriage')]),
    dict(type='text', label='Then look around it', title='Who is near\nyour graha?', body=['Who sits with it, who stands behind and ahead of it, and who faces it.'], closing='Rules 1, 2 and 4 do the rest'),
    dict(type='text', label='In your chart', title='One question,\none graha', body=['Asking about work? Find Saturn in your chart first. Asking about study? Find Mercury.']),
    dict(type='text', label='In real life', title='Call the right desk', body=['A question about a bill goes to billing. A question about a delivery goes to shipping. Each part of life has its own desk.']),
    dict(type='cta', orbs=[O('saturn', 40)], title='Which graha carries\nyour question?', titlesize=84, subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Thursday · Rule 13, walking backward'),
], """Rule 12: start with the graha that carries it

To study one matter of life, Nadi first finds the graha that signifies it, its karaka, and reads everything from there (R. G. Rao, Bhrigu Nandi Nadi, introduction).

Rao's table gives each graha its matters (Fundamentals of Rao's System of Nadi Astrology, chapter 7). A few to start with:
Sun: your father
Moon: your mother
Jupiter: children, teachers and guides
Saturn: your work
Mercury: education and business
Venus: wealth, and the graha looked to for marriage

Once you have the graha, look around it: who sits with it (rule 1), who stands behind and ahead of it (rule 2), and who faces it (rule 4). The other rules of this series do the rest.

In your chart, ask one question and find its graha first. Asking about work? Start with Saturn. Asking about study? Start with Mercury.

In real life it is like calling the right desk. A question about a bill goes to billing, and a question about a delivery goes to shipping. Each part of life has its own desk.

Which question would you bring to your chart first? Tell us in the comments.

Next: Thursday, rule 13, walking backward

Ask which graha carries your question, and what it says, at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#jyotish #karaka #nadiastrology #vedicastrology #sutram""", """Rule 12: start with its graha

To read one part of life, Nadi first finds the graha that carries it. Work: Saturn. Study: Mercury. Father: Sun. Mother: Moon. Wealth and marriage: Venus

asksutram.com
sutram.ca/newsletter""", '2026-11-25T12:00:00-05:00', '2026-11-25T13:00:00-05:00', [1, 2, 3, 4],
     ['Start with its graha. Every part of life has a graha that carries it', 'Rule 12: find the carrier first, the karaka', 'Home and family: Sun the father, Moon the mother, Jupiter children and guides',
      'Work and life: Saturn work, Mercury education and business, Venus wealth and marriage'], 'lesson')

# ------------------------------------------------------------------ Wed 25 · 6:30 PM · The Thread, part 5 (post 6, cream)
post('thread-ep5-body', 'day', 'The Thread · Episode 5', [
    dict(type='cover', orbs=[O('sun', 70), O('jupiter', 64), O('saturn', 52)], orbgap=30, title='Your body type', titlesize=112, subtitle='Three doshas, and the grahas that carry them', motion='rise'),
    dict(type='text', label='Ayurveda', title='Three doshas', body=['Ayurveda, India’s old science of life, says three doshas run the body: vata, pitta and kapha.'], closing='Each of us is born with our own mix'),
    dict(type='stack', label='The three', title='Air, fire and water', items=[['Vata · air and space', 'Movement, dryness, a busy mind'], ['Pitta · fire', 'Heat, drive, a quick temper'], ['Kapha · earth and water', 'Steadiness, weight, calm']], linesize=42),
    dict(type='cast', label='Brihat Parashara Hora Shastra · ch. 3', title='One dosha each', headsize=50, linesize=34, iconw=120, items=[
        dict(orbs=[O('sun', 36)], head='The king (Sun)', line='Pitta'), dict(orbs=[O('mars', 32)], head='The soldier (Mars)', line='Pitta'),
        dict(orbs=[O('jupiter', 38)], head='The teacher (Jupiter)', line='Kapha'), dict(orbs=[O('saturn', 28)], head='The auditor (Saturn)', line='Vata')]),
    dict(type='cast', label='Brihat Parashara Hora Shastra · ch. 3', title='Two, or all three', items=[
        dict(orbs=[O('moon', 40)], head='The mother (Moon)', line='Vata and kapha'), dict(orbs=[O('venus', 38)], head='The lover (Venus)', line='Kapha and vata'),
        dict(orbs=[O('mercury', 34)], head='The messenger (Mercury)', line='All three')]),
    dict(type='text', label='In your chart', title='Your rising lord\nand your Moon', body=['Find them in your free chart. Which dosha do they lean to?']),
    dict(type='rows', label='In real life', title='This winter', keyw=190, items=[['Vata', 'Scattered? Warm food and a fixed bedtime'], ['Pitta', 'Running hot? Cool down before you reply'], ['Kapha', 'Heavy? Move first thing in the morning']],
         note='Sutram’s reading. Not medical advice'),
    dict(type='quote', label='Ashtanga Hridayam · Sutrasthana 1.6', quote='In brief, the doshas\nare three.', quotesize=80, sanskrit='vāyuḥ pittaṃ kaphaśceti trayo doṣāḥ samāsataḥ', sanskritsize=36,
         body=['Vata, pitta and kapha.'], bodysize=38),
    dict(type='cta', orbs=[O('sun', 40), O('jupiter', 36), O('saturn', 30)], orbgap=20, title='Which one sounds\nlike you?', titlesize=88, subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Next Wednesday · The Thread, part 6'),
], """The Thread, Episode 5: Your body type

Ayurveda, India's old science of life, says three doshas run the body: "in brief, the doshas are three, vata, pitta and kapha" (Ashtanga Hridayam, Sutrasthana 1.6). Each of us is born with our own mix:
Vata, air and space: movement, dryness, a busy mind
Pitta, fire: heat, drive, a quick temper
Kapha, earth and water: steadiness, weight, calm

Jyotish gives each graha a dosha too, in Parashara's own pictures of the grahas (Brihat Parashara Hora Shastra, chapter 3, verses 23 to 29):
The king (Sun): pitta
The mother (Moon): vata and kapha
The soldier (Mars): pitta
The messenger (Mercury): all three
The teacher (Jupiter): kapha
The lover (Venus): kapha and vata
The auditor (Saturn): vata

In your chart, find the lord of your rising sign and your Moon in your free chart. Which dosha do they lean to?

In real life, try a checklist this winter. Scattered? Warm food and a fixed bedtime. Running hot? Cool down before you reply. Heavy? Move first thing in the morning. This is Sutram's reading, and it is not medical advice.

Which one sounds like you? Tell us in the comments.

Next Wednesday: The Thread, part 6

Ask which dosha your rising lord and Moon lean to at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#ayurveda #doshas #jyotish #vedicastrology #sutram""", """The Thread, part 5: your body type

Ayurveda's three doshas, and Parashara's dosha for each graha (BPHS 3.23 to 29). Pitta: Sun, Mars. Kapha: Jupiter. Vata: Saturn. Moon and Venus have two, Mercury all three

asksutram.com
sutram.ca/newsletter""", '2026-11-25T18:30:00-05:00', '2026-11-25T20:00:00-05:00', [1, 3, 4, 5],
     ['Your body type. Three doshas, and the grahas that carry them', 'Vata air and space, pitta fire, kapha earth and water',
      'One dosha each: Sun and Mars pitta, Jupiter kapha, Saturn vata', 'Two, or all three: Moon and Venus vata and kapha, Mercury all three'], 'thread')

# ------------------------------------------------------------------ Thu 26 · 10 AM · Sutra, the 10th house (post 7, cream)
post('sutra-10th-house', 'day', 'Sutra · The 10th house', [
    dict(type='cover', orbs=[O('sun', 104)], title='The 10th house', titlesize=112, subtitle='Your work, your name, your place in the sky', motion='rise'),
    dict(type='quote', label='Brihat Parashara Hora Shastra 11.11', quote='From the 10th, read status,\nlivelihood, honour\nand the father.', quotesize=68,
         sanskrit='rājyaṃ cākāśaṃvṛttiṃ ca mānaṃ caiva pitustathā', sanskritsize=34, body=['Parashara calls it the place in the sky.'], bodysize=36),
    dict(type='stack', label='What lives here', title='Work and name', items=[['Livelihood', 'What you do for a living'], ['Status', 'Your place among others'], ['Honour', 'What people call you when you leave the room'], ['The father', 'The 10th is read for him too']], linesize=40),
    dict(type='text', orbs=[O('sun', 60)], label='Why the top', title='The highest point\nof your chart', body=['At noon the Sun stands high in the sky. The 10th house is that high point: the part of you everyone can see.'],
         note='Sutram’s reading, built on the classical meanings'),
    dict(type='text', label='In your chart', title='Who sits in\nyour 10th?', body=['Count to the 10th sign from your rising sign. The grahas there, and the lord of that sign, show the work you are known for.']),
    dict(type='rows', label='In real life', title='Your name at work', items=[['1', 'Do one thing people can point to'], ['2', 'Finish it where others can see'], ['3', 'Let it speak when you are not in the room']]),
    dict(type='cta', orbs=[O('sun', 46)], title='What do people call\nyou at work?', titlesize=86, subtitle='Ask your chart at asksutram.com', lines=[ASK]),
], """The 10th house: your work and your name

Parashara calls the 10th house the place in the sky. From it he reads status, livelihood, honour and the father, and also time spent abroad and debts (Brihat Parashara Hora Shastra 11.11).

What lives here:
Livelihood: what you do for a living
Status: your place among others
Honour: what people call you when you leave the room
The father: the 10th is read for him too

Why the top? At noon the Sun stands high in the sky, and the 10th house is that high point of your chart, the part of you everyone can see. That is Sutram's reading, built on the classical meanings. The 10th is also one of the four houses that grow (upachaya), so a good name built here keeps growing.

In your chart, count to the 10th sign from your rising sign. The grahas there, and the lord of that sign, show the work you are known for.

In real life, do one thing people can point to, finish it where others can see, and let it speak for you when you are not in the room.

What would you like people to say about your work? Tell us in the comments.

Ask what your 10th house says about your work at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#jyotish #vedicastrology #10thhouse #sutra #sutram""", '', '2026-11-26T10:00:00-05:00', None, [], [], 'sutra')

# ------------------------------------------------------------------ Thu 26 · 12 PM · Lesson 23, rule 13 (post 8, dark)
post('lesson23-backward', 'night', 'Lesson 23 · Nadi rules', [
    dict(type='cover', orbs=[O('saturn', 92)], title='Walking backward', titlesize=108, subtitle='Why the fruits of the past come sooner'),
    dict(type='text', label='Rule 13', title='The past comes\nback sooner', body=['When a graha walks backward, the fruits of past actions come quickly.'], note='Jitender Kumar, Nadi Jyotisha, chapter 4'),
    dict(type='text', label='What backward means', title='A trick of the view', body=['Seen from Earth, a graha now and then slows, stops and seems to walk back through the signs.'], closing='The classics call it retrograde'),
    dict(type='text', label='A picture for it', title='Looking back', body=['Someone walking home looks back, sees a person in trouble, and turns round to help. Walking backward is that turn.']),
    dict(type='text', orbs=[O('saturn', 58)], label='In the sky now', title='The auditor\nwalks back', body=['Saturn has walked backward in Pisces since late July. It turns forward on Thursday 10 December, about 8 PM.'],
         closing='Old work comes back for a second look'),
    dict(type='stack', label='Nadi Jyotisha · chapter 4', title='Who walks back', items=[['Never', 'The Sun and the Moon'], ['Now and then', 'Mars, Mercury, Jupiter, Venus and Saturn'], ['Next to turn', 'Jupiter on 12 December, Mars on 10 January']], linesize=40),
    dict(type='text', label='In your chart', title='An R beside\na graha', body=['A graha marked R in your birth chart was walking backward when you were born. By this rule its fruits come sooner.']),
    dict(type='cta', orbs=[O('saturn', 40)], title='Which of your grahas\nwalks backward?', titlesize=84, subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Friday · Rule 14, standing still'),
], """Rule 13: walking backward brings the past back sooner

Seen from Earth, a graha now and then slows down, stops and seems to walk back through the signs. The classics call it retrograde. In Nadi a graha walking backward shows that the fruits of past actions come quickly (Jitender Kumar, Nadi Jyotisha, chapter 4).

A picture for it: someone walking home looks back, sees a person in trouble, and turns round to help. Walking backward is that turn.

Who walks backward:
Never: the Sun and the Moon (same chapter)
Now and then: Mars, Mercury, Jupiter, Venus and Saturn
Next to turn: Jupiter on 12 December, Mars on 10 January

In the sky now, the auditor (Saturn) has walked backward in Pisces since late July. It turns forward on Thursday 10 December at about 8 PM. Until then, old work comes back for a second look.

In your chart, a graha marked R was walking backward when you were born. By this rule its fruits come sooner.

What came back to you this month that you thought was finished? Tell us in the comments.

Next: Friday, rule 14, standing still

Ask which of your grahas walks backward, and what it brings back, at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#jyotish #retrograde #nadiastrology #vedicastrology #sutram""", """Rule 13: walking backward

When a graha walks backward (retrograde), the fruits of past actions come quickly (Jitender Kumar, Nadi Jyotisha). Saturn walks back in Pisces until 10 December: old work comes back for a second look

asksutram.com
sutram.ca/newsletter""", '2026-11-26T12:00:00-05:00', '2026-11-26T13:00:00-05:00', [1, 2, 5, 6],
     ['Walking backward. Why the fruits of the past come sooner', 'Rule 13: when a graha walks backward, the fruits of past actions come quickly',
      'The auditor walks back: Saturn in Pisces until 10 December', 'Who walks back: never the Sun and the Moon; next Jupiter on 12 December, Mars on 10 January'], 'lesson')

# ------------------------------------------------------------------ Fri 27 · 12 PM · Lesson 24, rule 14 (post 10, cream)
post('lesson24-standing-still', 'day', 'Lesson 24 · Nadi rules', [
    dict(type='cover', orbs=[O('saturn', 72), O('jupiter', 84)], orbgap=40, title='Standing still', titlesize=112, subtitle='Two grahas stop in December'),
    dict(type='text', label='Rule 14', title='Before it turns,\nit stops', body=['A graha about to change direction slows down and seems to stand still for days.'],
         closing='Nadi counts that stop as a key factor in its strength', note='Jitender Kumar, Nadi Jyotisha, chapter 3'),
    dict(type='cast', label='In the sky', title='Two stops,\ntwo days apart', items=[
        dict(orbs=[O('saturn', 36)], head='The auditor (Saturn)', line='Stops in Pisces and turns forward on Thursday 10 December, about 8 PM.'),
        dict(orbs=[O('jupiter', 42)], head='The teacher (Jupiter)', line='Stops in Leo and turns backward on Saturday 12 December, about 8 PM.')]),
    dict(type='rows', label='Saturn, slower every day', title='How far it moves', keyw=250, items=[['Mon 23 Nov', 'About 2 minutes of arc a day'], ['Sat 5 Dec', 'About half a minute a day'], ['Thu 10 Dec', 'Still, then forward']],
         note='A minute of arc is a sixtieth of a degree'),
    dict(type='text', orbs=[O('saturn', 46), O('jupiter', 52)], orbgap=30, label='What stands still', title='Work and guidance\nweigh more',
         body=['Saturn stands for work, Jupiter for guides and teachers. While they stand still, those matters move slowly and count for more.'], note='Sutram’s reading, built on the rule'),
    dict(type='text', label='In your chart', title='Inside the\nbackward stretch', body=['Saturn walked back over Pisces 21° to 14°. Jupiter will walk back over Leo 3° to Cancer 23° by April. Birth grahas in those stretches feel them more.'],
         bodysize=38, note='Jitender Kumar, Nadi Jyotisha, chapter 4'),
    dict(type='text', label='In real life', title='Give slow things\na few more days', body=['Big decisions about work and study can wait for the turn.']),
    dict(type='cta', orbs=[O('saturn', 36), O('jupiter', 40)], orbgap=20, title='Which of your grahas\nfeels the stop?', titlesize=84, subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Monday · Rule 15'),
], """Rule 14: standing still

Before a graha changes direction, it slows down and seems to stand still for days. Nadi counts that stop as a key factor in how strongly the graha acts on the others (Jitender Kumar, Nadi Jyotisha, chapter 3).

Two grahas stop in December, two days apart:
The auditor (Saturn) stops in Pisces and turns forward on Thursday 10 December, about 8 PM
The teacher (Jupiter) stops in Leo and turns backward on Saturday 12 December, about 8 PM

You can watch Saturn slow down. On Monday it moved about 2 minutes of arc a day (a minute is a sixtieth of a degree). By 5 December it moves about half a minute, and on 10 December it stands still.

Saturn stands for work and Jupiter for guides and teachers. While they stand still, those matters move slowly and count for more. That is Sutram's reading, built on the rule.

In your chart, look at the stretch each one walks backward over. Saturn walked back from Pisces 21° to 14°, and Jupiter will walk back from Leo 3° to Cancer 23° by April. A birth graha inside that stretch feels them more (same book, chapter 4).

In real life, give slow things a few more days. Big decisions about work and study can wait for the turn.

Do you have a graha in one of those stretches? Tell us in the comments.

Next: Monday, rule 15

Ask whether Saturn's or Jupiter's stop touches your chart at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#jyotish #saturn #jupiter #nadiastrology #sutram""", """Rule 14: standing still

Before a graha turns, it slows and stands still, and Nadi counts that stop as a key factor in its strength (Jitender Kumar, Nadi Jyotisha). Saturn stops on 10 December, Jupiter on 12 December

asksutram.com
sutram.ca/newsletter""", '2026-11-27T12:00:00-05:00', '2026-11-27T13:00:00-05:00', [1, 2, 3, 6],
     ['Standing still. Two grahas stop in December', 'Rule 14: before it turns, a graha stops, a key factor in its strength',
      'Two stops: Saturn turns forward on 10 December, Jupiter backward on 12 December', 'Inside the backward stretch: Pisces 21° to 14°, and Leo 3° to Cancer 23°'], 'lesson')

# ------------------------------------------------------------------ Fri 27 · 6:30 PM · Read the sky (post 11, dark)
cells = [[f'{m} Moon', f'{ORD[house_from(m, "Cancer")]} house', HOUSE[house_from(m, 'Cancer')]] for m in SIGNS]
post('sky-2026-11-27', 'night', 'Read the sky · 27 November', [
    dict(type='cover', orbs=[O('moon', 122, illum=.83, waxing=False)], title='The Moon\ncomes home', titlesize=108, subtitle='Friday about 9 PM, into Cancer', motion='rise'),
    dict(type='text', label='Friday 27 November', title='Home in Cancer', body=['At about 9 PM Toronto time the mother (the Moon) walks into Cancer, her own sign, and stays until Sunday night.'],
         closing='At home, a graha is generally strong', note='Jitender Kumar, Nadi Jyotisha, chapter 5'),
    dict(type='cast', label='Nadi rule 6', title='The water family', headsize=50, linesize=33, items=[
        dict(orbs=[O('moon', 40, illum=.83, waxing=False)], head='The mother in Cancer', line='Home, where feelings run warm.'),
        dict(orbs=[O('sun', 38)], head='The king in Scorpio', line='Another water sign: the boss is family.'),
        dict(orbs=[O('saturn', 30)], head='The auditor in Pisces', line='Water too, walking backward to recheck old work.')]),
    dict(type='text', orbs=[O('jupiter', 56), O('mars', 44)], orbgap=30, label='Nadi rule 2', title='Who walks ahead', body=['In Leo, the sign just ahead of her, walk the teacher (Jupiter) and the soldier (Mars).'],
         closing='Good advice and a push are close by'),
    dict(type='grid', label='This weekend', title='Find your Moon sign', cells=cells[:6], celllab=22, cellsize=62, celltext=33, cellpad=28, note='Count Cancer from the sign your Moon was in at birth'),
    dict(type='grid', label='This weekend', title='Find your Moon sign', cells=cells[6:], celllab=22, cellsize=62, celltext=33, cellpad=28, note='Don’t know your Moon sign? Ask at asksutram.com'),
    dict(type='rows', label='In real life', title='This weekend', items=[['1', 'Cook something at home'], ['2', 'Call your mother, or someone who mothers you'], ['3', 'Rest before Monday']]),
    dict(type='cta', orbs=[O('moon', 50, illum=.83, waxing=False)], title='Where does the Moon\nland for you?', titlesize=84, subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Sunday · The week ahead'),
], """The Moon comes home to Cancer

On Friday at about 9 PM Toronto time the mother (Moon) walks into Cancer, her own sign, and stays until Sunday at about 11 PM. A graha at home is generally strong (Jitender Kumar, Nadi Jyotisha, chapter 5), so the weekend's feelings run warm and close to family.

The water family is all here. The king (Sun) sits in Scorpio and the auditor (Saturn) in Pisces, the other two water signs. Signs 5th and 9th apart act together like family (rule 6): the boss is on the mother's side, and duty keeps rechecking old work as Saturn walks backward.

Ahead of her, in Leo, walk the teacher (Jupiter) and the soldier (Mars) (rule 2). Good advice and a push are close by.

To see where it lands for you, count Cancer from your Moon sign:
""" + '\n'.join(f'{m} Moon, {ORD[house_from(m, "Cancer")]}: {HOUSE[house_from(m, "Cancer")].lower()}' for m in SIGNS) + """

This weekend, cook something at home, call your mother or someone who mothers you, and rest before Monday.

Where will you spend this weekend? Tell us in the comments.

Next, on Sunday evening, the week ahead

Ask where the Moon in Cancer lands for your Moon sign at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#jyotish #moon #cancer #vedicastrology #sutram""", """Read the sky: the Moon comes home

Friday about 9 PM Toronto the Moon walks into Cancer, her own sign, with the Sun in Scorpio and Saturn in Pisces as her water family. A warm weekend, close to home

asksutram.com
sutram.ca/newsletter""", '2026-11-27T18:30:00-05:00', '2026-11-27T20:00:00-05:00', [1, 3, 5, 6],
     ['The Moon comes home. Friday about 9 PM, into Cancer', 'The water family: the Moon in Cancer, the Sun in Scorpio, Saturn in Pisces',
      'This weekend for Aries to Virgo Moon', 'This weekend for Libra to Pisces Moon'], 'sky')

# ------------------------------------------------------------------ Sat 28 · 10 AM · Avatars and grahas 2 (post 12, cream)
AV = [('Sun', 'Rama', 'sun'), ('Moon', 'Krishna', 'moon'), ('Mars', 'Narasimha', 'mars'), ('Mercury', 'Buddha', 'mercury'), ('Jupiter', 'Vamana', 'jupiter'),
      ('Venus', 'Parashurama', 'venus'), ('Saturn', 'Kurma', 'saturn'), ('Rahu', 'Varaha', 'rahu'), ('Ketu', 'Matsya', 'ketu')]
post('avatar-krishna-moon', 'day', 'Sutram · Avatars and grahas', [
    dict(type='cover', orbs=[O('moon', 116)], title='Krishna is\nthe Moon', titlesize=108, subtitle='Why the old texts pair the flute player and the mind', motion='rise'),
    dict(type='grid', cols=3, label='Brihat Parashara Hora Shastra · ch. 2', title='Nine avatars, nine grahas', titlesize=72, cells=[[g, a, '', g == 'Moon'] for g, a, _ in AV],
         cellorbs=[O(k, 30 if k == 'saturn' else 36) for _, _, k in AV], cellsize=50, celllab=20, cellpad=20, closing='Parashara pairs them, one by one', closingsize=44),
    dict(type='text', label='The story', title='Born under\nthe Moon’s star', body=['Krishna was born under Rohini, a star in Taurus, the sign where the Moon is at her best.'], note='Bhagavata Purana 10.3.1'),
    dict(type='text', label='His family', title='The Moon’s\nfamily line', body=['His people, the Yadus, came down from Soma, the Moon. Rama, the Sun’s avatar, came from the Sun’s line.'], note='Bhagavata Purana 10.1.1'),
    dict(type='text', orbs=[O('moon', 66)], label='Brihat Parashara Hora Shastra · ch. 3', title='Kind eyes,\nsweet words', body=['Parashara draws the Moon with kind eyes, sweet speech and a restless nature. The Moon is also the mind.'],
         closing='The child everyone loved'),
    dict(type='text', label='In your chart', title='Your Moon’s house', body=['The house of your Moon shows where your heart goes, and where people feel at home with you.'], note='Sutram’s reading, built on the classical meanings'),
    dict(type='text', label='In real life', title='Try it today', closing='Say one kind, true thing you usually keep to yourself', closingsize=52),
    dict(type='cta', orbs=[O('moon', 56)], title='What does your Moon’s\nhouse ask of you?', titlesize=84, subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Next Saturday · Narasimha, Mars'),
], """Krishna is the Moon

Parashara pairs each avatar of Vishnu with a graha (Brihat Parashara Hora Shastra, chapter 2). Last Saturday it was Rama and the Sun. This week, Krishna and the Moon.

Why Krishna for the Moon? He was born under Rohini, a star in Taurus, the sign where the Moon is at her best (Bhagavata Purana 10.3.1). His people, the Yadus, came down from Soma, the Moon, just as Rama came from the Sun's line (Bhagavata Purana 10.1.1).

Parashara draws the Moon with kind eyes, sweet speech and a restless nature (chapter 3, verse 24), and calls the Moon the mind (verse 12). That is the child everyone loved in the Bhagavata's tenth book: the butter thief of the village, the flute player everyone stopped to hear.

In your chart, the house of your Moon shows where your heart goes, and where people feel at home with you. That is Sutram's reading, built on the classical meanings.

In real life, try it today and say one kind, true thing you usually keep to yourself.

Who in your life has the Moon's sweet words? Tell us in the comments.

Every Saturday morning, one avatar and one graha. Next Saturday, Narasimha and Mars

Ask what your Moon's house asks of you at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#krishna #jyotish #moon #vedicastrology #sutram""", """Krishna is the Moon

Parashara pairs Krishna with the Moon (BPHS ch. 2). Born under Rohini, in the Moon's best sign, of the Moon's own family line. Kind eyes, sweet words, a restless heart

asksutram.com
sutram.ca/newsletter""", '2026-11-28T10:00:00-05:00', '2026-11-28T13:00:00-05:00', [1, 2, 3, 5],
     ['Krishna is the Moon. Why the old texts pair the flute player and the mind', 'Nine avatars, nine grahas: Krishna is the Moon’s',
      'Born under the Moon’s star: Rohini, in Taurus', 'Kind eyes, sweet words: Parashara’s Moon'], 'avatar')

# ------------------------------------------------------------------ Sun 29 · 6:30 PM · Week ahead 30 Nov to 6 Dec (post 15, cream)
nodes = []
for m in SIGNS:
    r, k = house_from(m, 'Capricorn'), house_from(m, 'Cancer')
    nodes.append([f'{m} Moon', f'Rahu {ORD[r]} · Ketu {ORD[k]}', f'More: {SHORT[r]}\nLess: {SHORT[k]}'])
post('week-2026-11-29', 'day', 'Week ahead · 30 November to 6 December', [
    dict(type='cover', orbs=[O('rahu', 84), O('ketu', 72)], orbgap=60, title='Rahu and Ketu\nchange signs', titlesize=104, subtitle='Saturday, about noon', motion='rise'),
    dict(type='text', orbs=[O('rahu', 52), O('ketu', 46)], orbgap=150, label='Saturday 5 December, about noon', title='Into Capricorn\nand Cancer',
         body=['The magician (Rahu) walks backward into Capricorn, and the monk (Ketu) into Cancer. They stay about a year and a half.']),
    dict(type='text', label='Rao’s Nadi table', title='One grows,\none narrows', body=['Rahu stands for bigness, Ketu for smallness. Where Rahu lands, a matter grows. Where Ketu lands, it gets smaller and simpler.'],
         note='R. G. Rao, Fundamentals, ch. 7 · Sutram’s reading'),
    dict(type='grid', label='From Saturday', title='Find your Moon sign', cells=nodes[:6], celllab=21, cellsize=44, celltext=30, cellpad=22, note='Count Capricorn and Cancer from your Moon sign'),
    dict(type='grid', label='From Saturday', title='Find your Moon sign', cells=nodes[6:], celllab=21, cellsize=44, celltext=30, cellpad=22, note='Don’t know your Moon sign? Ask at asksutram.com'),
    dict(type='stack', label='Also this week', title='Mark your calendar', linesize=36, items=[
        ['Wednesday, about 7 AM', 'The messenger (Mercury) walks into Scorpio and joins the king (Sun)'],
        ['All week', 'Saturn and Jupiter slow toward a stop: Saturn turns forward on 10 December, Jupiter backward on 12 December'],
        ['Friday, about 12:30 PM', 'The Moon walks into Libra and meets the lover (Venus), at home there'],
        ['Next Tuesday, about 8 PM', 'New Moon in Scorpio']]),
    dict(type='text', orbs=[O('rahu', 50), O('ketu', 44)], orbgap=40, label='In real life', title='Before Saturday', body=['Notice what you keep chasing, and what you are ready to put down.'], closing='Rahu chases. Ketu lets go'),
    dict(type='cta', orbs=[O('rahu', 44), O('ketu', 38)], orbgap=24, title='Where do Rahu and\nKetu land for you?', titlesize=84, subtitle='Ask your chart at asksutram.com', lines=[ASK], next='Monday · Rule 15'),
], """Week ahead: Rahu and Ketu change signs, for your Moon sign

On Saturday 5 December at about noon Toronto time the magician (Rahu) walks backward into Capricorn and the monk (Ketu) into Cancer. They stay in these signs for about a year and a half.

In Rao's Nadi table Rahu stands for bigness and Ketu for smallness (R. G. Rao, Fundamentals of Rao's System of Nadi Astrology, chapter 7). So where Rahu lands, a matter grows, and where Ketu lands, it gets smaller and simpler. That is Sutram's reading of the table.

To see where they land for you, count Capricorn and Cancer from your Moon sign, the sign the Moon was in when you were born:
""" + '\n'.join(f'{m} Moon: Rahu {ORD[house_from(m, "Capricorn")]}, {SHORT[house_from(m, "Capricorn")]}; Ketu {ORD[house_from(m, "Cancer")]}, {SHORT[house_from(m, "Cancer")]}' for m in SIGNS) + """

Also this week:
Wednesday, about 7 AM: the messenger (Mercury) walks into Scorpio and joins the king (Sun)
All week: the auditor (Saturn) and the teacher (Jupiter) slow toward a stop. Saturn turns forward on 10 December and Jupiter backward on 12 December
Friday, about 12:30 PM: the Moon walks into Libra and meets the lover (Venus), who is home there
Next Tuesday, about 8 PM: a new Moon in Scorpio

Before Saturday, notice what you keep chasing, and what you are ready to put down.

What are you ready to put down this year? Tell us in the comments.

Ask where Rahu and Ketu land for your Moon sign at asksutram.com
Weekly newsletter: sutram.ca/newsletter

#rahu #ketu #jyotish #vedicastrology #sutram""", """Week ahead: Rahu and Ketu change signs

Saturday about noon Toronto, Rahu walks into Capricorn and Ketu into Cancer for about a year and a half. Where Rahu lands a matter grows, where Ketu lands it gets simpler

asksutram.com
sutram.ca/newsletter""", '2026-11-29T18:30:00-05:00', '2026-11-29T20:00:00-05:00', [1, 2, 4, 5],
     ['Rahu and Ketu change signs. Saturday, about noon', 'Into Capricorn and Cancer, for about a year and a half',
      'From Saturday, for Aries to Virgo Moon', 'From Saturday, for Libra to Pisces Moon'], 'week')

# the philosophy library posts, built 15 Nov by tools/philosophy.py (old dark look); only scheduled here
PHIL = [dict(id='phil-breath', ig='2026-11-28T18:30:00-05:00', x='2026-11-28T19:00:00-05:00', x_slides=[1, 3, 4, 7]),
        dict(id='phil-eclipse', ig='2026-11-29T10:00:00-05:00', x='2026-11-29T10:30:00-05:00', x_slides=[1, 3, 5, 6])]


# rows for the site feed (site/content_pages.json and .csv, written by tools/site_feed.py)
SITE = {
    'lesson20-doorway-c': ('lesson-20-nadi-rule-10-the-doorway', 'Lesson 20: Bhrigu Nandi Nadi, rule 10: the doorway, Gandanta', 'Does any graha in my chart sit in a doorway?'),
    'sutra-11th-house': ('the-11th-house-where-your-gains-come-from', 'The 11th house: where your gains come from', 'What does my 11th house say about where my gains come from?'),
    'lesson21-whose-star': ('lesson-21-rule-11-whose-star', 'Lesson 21, rule 11: whose star a graha stands in', 'Whose star does each of my grahas stand in?'),
    'lesson22-its-graha': ('lesson-22-nadi-rule-12-start-with-its-graha', 'Lesson 22: Bhrigu Nandi Nadi, rule 12: start with the graha that carries it', 'Which graha carries my question, and what does it say?'),
    'thread-ep5-body': ('your-body-type', 'The Thread: your body type', 'Which dosha do my rising lord and Moon lean to?'),
    'sutra-10th-house': ('the-10th-house-your-work-and-your-name', 'The 10th house: your work and your name', 'What does my 10th house say about my work?'),
    'lesson23-backward': ('lesson-23-nadi-rule-13-walking-backward', 'Lesson 23: Nadi rule 13: walking backward brings the past back sooner', 'Which of my grahas walks backward, and what does it bring back?'),
    'lesson24-standing-still': ('lesson-24-nadi-rule-14-standing-still', 'Lesson 24: Nadi rule 14: standing still', 'Does Saturn’s or Jupiter’s stop touch my chart?'),
    'sky-2026-11-27': ('the-moon-comes-home-to-cancer-27-november-2026', 'The Moon comes home to Cancer', 'Where does the Moon in Cancer land for my Moon sign?'),
    'avatar-krishna-moon': ('krishna-is-the-moon', 'Avatars and grahas: Krishna is the Moon', 'What does my Moon’s house ask of me?'),
    'week-2026-11-29': ('week-ahead-30-november-6-december-2026', 'Week ahead: Rahu and Ketu change signs', 'Where do Rahu and Ketu land for my Moon sign?'),
}
for p in PLAN:
    slug, title, ask = SITE[p['id']]
    p['site'] = dict(slug=slug, title=title, ask=ask, family={'avatar': 'thread', 'week': 'sky'}.get(p['family'], p['family']))


def x_weight(t):
    t = t.strip()
    for link in ('sutram.ca/newsletter', 'asksutram.com'):
        if link in t: t = t.replace(link, '', 1); t += 'x' * 23
    return len(t)


if __name__ == '__main__':
    for pid, spec in POSTS.items():
        assert len(spec['slides']) <= 10, pid
        json.dump(spec, open(os.path.join(REPO, 'specs', f'{pid}.json'), 'w'), indent=1, ensure_ascii=False)
        open(os.path.join(REPO, 'captions', f'{pid}.txt'), 'w').write(CAP[pid])
        xw = x_weight(X[pid])
        if [p for p in PLAN if p['id'] == pid][0]['x']:
            assert xw <= 280, (pid, xw)
            open(os.path.join(REPO, 'x-drafts', f'{pid}-x.txt'), 'w').write(X[pid])
        print(f'{pid:26s} {spec["look"]:5s} {len(spec["slides"])} slides  caption {len(CAP[pid].strip())}  X {xw}')
    json.dump(dict(made='2026-11-22 Sunday batch for 23 to 29 Nov', posts=PLAN, phil=PHIL), open(os.path.join(REPO, 'plan', 'week48.json'), 'w'), indent=1, ensure_ascii=False)
