#!/usr/bin/env python3
"""Add a week's posts to the site feed (site/content_pages.json, then site/content_pages.csv rebuilt from it).

    python3 tools/site_feed.py plan/week48.json

Each post in the plan file carries "site": {slug, title, ask, family} and "ig" (its Instagram time, the published_at).
A row whose slug is already in the feed is replaced, so a remade post (lesson20-doorway-c) takes over its old row.
The body is the caption without its title, its comment question, its "Next" line, its two link lines and its hashtags."""
import csv, json, os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = 'https://raw.githubusercontent.com/sumants1123-bit/Sutram-social/main/posts'
COLS = ['family', 'slug', 'lang', 'title', 'h1', 'meta_description', 'summary', 'body_md', 'facts', 'faq', 'sources', 'ask_question', 'image_urls', 'published_at', 'source_post']


def row(p):
    pid, s = p['id'], p['site']
    lines = open(os.path.join(REPO, 'captions', f'{pid}.txt')).read().strip().split('\n')
    paras, cur = [], []
    for l in lines[1:] + ['']:
        if l.strip(): cur.append(l)
        elif cur: paras.append('\n'.join(cur)); cur = []
    keep = [q for q in paras if not (q.startswith(('Next', 'Ask ', 'Weekly newsletter', '#', 'Every Saturday')) or q.endswith('Tell us in the comments.'))]
    summary = keep[0]
    meta = summary if len(summary) <= 155 else summary[:152].rsplit(' ', 1)[0] + '…'
    n = len([f for f in os.listdir(os.path.join(REPO, 'posts', pid)) if f.startswith(pid + '-') and f.endswith('.jpg') and 'overview' not in f])
    return dict(family=s['family'], slug=s['slug'], lang='en', title=s['title'], h1=s['title'], meta_description=meta, summary=summary,
                body_md='\n\n'.join(keep), facts='{}', faq='[]', sources='[]', ask_question=s['ask'],
                image_urls=json.dumps([f'{RAW}/{pid}/{pid}-{i}.jpg' for i in range(1, n + 1)]), published_at=p['ig'], source_post=pid)


if __name__ == '__main__':
    plan = json.load(open(sys.argv[1])); fj = os.path.join(REPO, 'site', 'content_pages.json')
    feed = json.load(open(fj)); index = {r['slug']: k for k, r in enumerate(feed)}
    for p in plan['posts']:
        r = row(p)
        if r['slug'] in index: feed[index[r['slug']]] = r; print('replaced', r['slug'])
        else: feed.append(r); index[r['slug']] = len(feed) - 1; print('added  ', r['slug'])
    json.dump(feed, open(fj, 'w'), indent=1, ensure_ascii=False)
    with open(os.path.join(REPO, 'site', 'content_pages.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_ALL); w.writeheader(); [w.writerow(r) for r in feed]
    print(len(feed), 'rows')
