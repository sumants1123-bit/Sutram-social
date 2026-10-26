"""Print the Metricool `info` JSON for a rendered post.
Usage: python3 tools/payload.py <post-id> <YYYY-MM-DDTHH:MM>
Reads captions/<post-id>.txt and counts posts/<post-id>/<post-id>-<n>.jpg.
Also prints the `date` argument with the correct Toronto UTC offset.
"""
import json, os, sys, glob, datetime as dt
from zoneinfo import ZoneInfo
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE='https://raw.githubusercontent.com/sumants1123-bit/Sutram-social/main/posts/'
pid, when = sys.argv[1], sys.argv[2]
n=len(glob.glob(os.path.join(REPO,'posts',pid,f'{pid}-[0-9]*.jpg')))
assert n>0, 'no slides rendered'
text=open(os.path.join(REPO,'captions',f'{pid}.txt')).read().strip()
assert len(text)<=2200, f'caption too long: {len(text)}'
local=dt.datetime.fromisoformat(when).replace(tzinfo=ZoneInfo('America/Toronto'))
info={"autoPublish":True,"descendants":[],"draft":False,"firstCommentText":"","hasNotReadNotes":False,
 "media":[f"{BASE}{pid}/{pid}-{i}.jpg" for i in range(1,n+1)],"mediaAltText":[],
 "providers":[{"network":"instagram"}],"publicationDate":{"dateTime":local.strftime('%Y-%m-%dT%H:%M:00'),"timezone":"America/Toronto"},
 "shortener":False,"smartLinkData":{"ids":[]},"text":text,
 "instagramData":{"type":"POST","collaborators":[],"showReelOnFeed":True,"isAiGenerated":False}}
print('DATE:', local.isoformat(timespec='seconds'))
print('INFO:', json.dumps(info,ensure_ascii=False))
