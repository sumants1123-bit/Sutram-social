#!/usr/bin/env python3
"""Know yourself: "Awareness is you" (draft for Sumant's review, 20 Nov 2026).

Sumant, 20 Nov 5:30 PM: "Awareness is your higher self, SELF. You. Does someone else say this?" Then, 5:47 PM:
"make a one post on awareness about it. Mentioning all these scriptures in a nice, beautiful way, not too much text.
Very beautiful. I don't know if astrology connects to awareness with any planet, so maybe add that. If it doesn't, it doesn't."
It is idea 4 of plan/mind_series.md, "The player and the watcher".

Every verse was opened on 20 Nov 2026 before use. The English on the slides is Sutram's own rendering of the Sanskrit.
- Shiva Sutras 1.1, "caitanyam ātmā": Swami Lakshmanjoo Academy, lakshmanjooacademy.org (the first sutra; consciousness is the Self).
- Brihadaranyaka Upanishad 3.7.23, "adṛṣṭo draṣṭā, aśrutaḥ śrotā": wisdomlib.org, the inner ruler is never seen yet is the
  seer, never heard yet the hearer, never thought yet the thinker, never known yet the knower.
- Mandukya Upanishad 7: vedapath.app. The fourth is not inward-knowing, not outward-knowing, not a mass of knowing;
  peaceful, auspicious, non-dual; ends "sa ātmā sa vijñeyaḥ", that is the Self, that is to be known. The three rows for
  waking, dream and deep sleep use the three kinds of knowing this verse negates.
- Yoga Sutras 1.3, "tadā draṣṭuḥ svarūpe 'vasthānam": wisdomlib.org (Vyasa's edition), then the seer rests in its own nature.
- Brihat Parashara Hora Shastra 3.12, "sarvātmā ca divānāthaḥ, manaḥ kumudabāndhavaḥ": enjoylearningsanskrit.com, the Sun
  is the Self of all, the Moon is the mind. This is the astrology link Sumant asked about. That the Moon shines with the
  Sun's light is plain sky; reading it as the mind shining with awareness is Sutram's reading.
- Ramana Maharshi's question "Who am I?", Nisargadatta Maharaj's book I Am That, and Krishnamurti's push-back (thought
  invents a permanent thinker, such as the atman or the soul; the observer is the observed: awakeningtoreality.com excerpts)
  appear in the caption only.

    python3 tools/post_awareness.py      # writes specs/know-awareness.json, captions/know-awareness.txt, x-drafts/know-awareness-x.txt
    python3 tools/render_look.py specs/know-awareness.json --motion
"""
import json, os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PID = 'know-awareness'
SUN = lambda r: dict(kind='sun', r=r, rings=False)
MOON = lambda r, illum=.76: dict(kind='moon', r=r, illum=illum, waxing=False)     # lit on the side that faces the Sun

SPEC = dict(id=PID, look='day', kicker='Sutram · Know yourself', slides=[
    dict(type='cover', orbs=[SUN(118), MOON(60)], orbgap=64, title='Awareness\nis you', titlesize=120,
         subtitle='What the old texts say about the one who sees', subsize=46),
    dict(type='quote', label='Shiva Sutras 1.1 · Kashmir Shaivism', quote='Consciousness is the Self.', quotesize=86,
         sanskrit='caitanyam ātmā', body=['The first line of the Shiva Sutras. Everything after it grows from this.'], bodysize=36),
    dict(type='quote', label='Brihadaranyaka Upanishad 3.7.23', quote='Unseen, it sees.\nUnheard, it hears.\nUnknown, it knows.', quotesize=74,
         sanskrit='adṛṣṭo draṣṭā, aśrutaḥ śrotā', body=['You can never look at it. It is the one doing the looking.'], bodysize=36),
    dict(type='rows', label='Mandukya Upanishad 7', title='The fourth', keyw=300,
         items=[['Waking', 'knowing turned outward'], ['Dream', 'knowing turned inward'], ['Deep sleep', 'knowing folded into one'], ['Turīya', 'none of these. Peaceful, one']],
         closing='sa ātmā · That is the Self', closingsize=44),
    dict(type='quote', label='Yoga Sutras 1.3', quote='Then the seer rests in its own nature.', quotesize=78,
         sanskrit='tadā draṣṭuḥ svarūpe ’vasthānam', body=['When the mind goes quiet, the one who was watching is all that is left.'], bodysize=36),
    dict(type='text', orbs=[SUN(80), MOON(44)], orbgap=44, label='In Jyotish · Brihat Parashara Hora Shastra 3.12',
         title='The Sun is the Self.\nThe Moon is the mind.', titlesize=74, sanskrit='sarvātmā ca divānāthaḥ, manaḥ kumudabāndhavaḥ', sanskritsize=36,
         body=['The Moon has no light of its own. It shines with the Sun’s. So does your mind.'], bodysize=38),
    dict(type='rows', label='Try it · Ramana Maharshi’s question', title='Who am I?',
         items=[['1', 'Notice a thought'], ['2', 'Notice that you noticed it'], ['3', 'Ask who is noticing']],
         closing='The answer is the one who asked'),
    dict(type='cta', orbs=[SUN(66)], title='Thoughts come and go.\nYou stay.', titlesize=86, subtitle='Awareness is you',
         lines=['Weekly newsletter at sutram.ca/newsletter']),
])

CAPTION = """Awareness is you

Thoughts come and go. Feelings come and go. Something notices all of them, and it does not come and go. The old texts call it the Self.

Shiva Sutras 1.1, the first line of Kashmir Shaivism's root text: caitanyam ātmā, consciousness is the Self.

Brihadaranyaka Upanishad 3.7.23: unseen, it sees. Unheard, it hears. You can never look at it, because it is the one doing the looking.

Mandukya Upanishad 7: beyond waking, dream and deep sleep is the fourth, turīya. Sa ātmā: that is the Self

Yoga Sutras 1.3: then the seer rests in its own nature

And in Jyotish, Brihat Parashara Hora Shastra 3.12: the Sun is the Self of all, the Moon is the mind. The Moon has no light of its own. It shines with the Sun's. So does your mind.

Ramana Maharshi turned all of this into one question: Who am I? Nisargadatta Maharaj taught the same in I Am That. Krishnamurti pushed back: for him any higher self is one more idea made by thought. Look for yourself.

Who is aware of this sentence?

Weekly newsletter: sutram.ca/newsletter

#awareness #advaita #kashmirshaivism #jyotish #sutram
"""
X = """Awareness is you

Shiva Sutras 1.1: consciousness is the Self.
Brihadaranyaka 3.7.23: unseen, it sees.
Mandukya 7: the fourth, beyond waking, dream, sleep.
Yoga Sutras 1.3: the seer rests in its own nature.
BPHS 3.12: Sun is the Self, Moon the mind.

sutram.ca/newsletter
"""

if __name__ == '__main__':
    json.dump(SPEC, open(os.path.join(REPO, 'specs', f'{PID}.json'), 'w'), indent=1, ensure_ascii=False)
    open(os.path.join(REPO, 'captions', f'{PID}.txt'), 'w').write(CAPTION)
    open(os.path.join(REPO, 'x-drafts', f'{PID}-x.txt'), 'w').write(X)
    xw = len(X.strip()) - len('sutram.ca/newsletter') + 23          # X counts a link as 23 characters
    assert xw <= 280, xw
    print(PID, len(SPEC['slides']), 'slides;', len(CAPTION.strip()), 'caption chars;', xw, 'X chars as X counts them')
