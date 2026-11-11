"""Build a new Ohio corpus part from unchanged live official chapter HTML."""
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parents[1]
EV = HERE.parent / 'gpt-workers/jobs/q-1584/evidence'
sys.path.insert(0, str(HERE))
from parse import rows_of, sec_key, unit_text
from state_lib import Act, norm

PART = HERE / 'corpus.d/zzzzz-q1584-live-new-chapters.json'
NUMBERS = ('1314', '1316', '1357', '3957', '4151')

def make():
    acts, audit = [], []
    for n in NUMBERS:
        path = EV / f'chapter-{n}.html'
        raw = path.read_bytes()
        page = raw.decode('utf8')
        rows = rows_of(page)
        if not rows or any(not r[4] for r in rows):
            raise ValueError(f'{n}: missing section body')
        law_bodies = re.findall(r'class="laws-body">(.*?)</(?:section|div)>', page, re.S)
        if len(law_bodies) != len(rows):
            raise ValueError(f'{n}: source body count differs from section count')
        if any(re.search(r'<img\b|<svg\b|<canvas\b', block, re.I) for block in law_bodies):
            raise ValueError(f'{n}: source image needs review')
        dates = {dt.datetime.strptime(r[2], '%B %d, %Y').date().isoformat() for r in rows if r[2]}
        if len(dates) != 1 or any(not r[2] for r in rows):
            raise ValueError(f'{n}: multiple or missing effective dates: {dates}')
        title_num = next((int(p.stem.split('-')[1]) for p in EV.glob('title-*.html')
                          if f'href="chapter-{n}"' in p.read_text(encoding='utf8')), None)
        if title_num is None:
            raise ValueError(f'{n}: not listed by official title page')
        tp = (EV / f'title-{title_num}.html').read_text(encoding='utf8')
        th = re.search(r'<h1>(.*?)</h1>', tp, re.S)
        ch = re.search(r'<h1>(.*?)</h1>', page, re.S)
        tname = norm(html.unescape(re.sub(r'<[^>]+>', ' ', th.group(1)))).replace(' | ', ': ')
        cname = norm(html.unescape(re.sub(r'<[^>]+>', ' ', ch.group(1)))).split(' | ', 1)[-1]
        url = f'https://codes.ohio.gov/ohio-revised-code/chapter-{n}'
        a = Act(f'orc-chapter-{int(n):04d}', f'R.C. Chapter {n}',
                f'Ohio Revised Code, {tname}, Chapter {n}: {cname}', url, dates.pop(),
                source_url=url, sha256=hashlib.sha256(raw).hexdigest(),
                note='Current official text; chapter sections share the printed effective date.')
        for number, head, eff, leg, body in rows:
            a.add(sec_key(number), 'R.C. ' + number, 'section', unit_text(head, eff, leg, body))
        if len(a.units) != len(rows):
            raise ValueError(f'{n}: duplicate section keys')
        acts.append(a.as_dict())
        audit.append({'chapter': n, 'source_url': url, 'source_sha256': a.sha256,
                      'sections': len(rows), 'date': a.from_date, 'title': a.title,
                      'source_images': 0, 'referenced_images': 0, 'omitted_images': 0})
    part = {'sources': [{'name': 'Ohio Legislative Service Commission, current Revised Code',
                         'url': 'https://codes.ohio.gov/ohio-revised-code', 'retrieved': '2026-11-11',
                         'licence': 'Ohio statutory text is an edict of government.',
                         'notes': 'Five newly listed chapters; each section states its effective date.'}],
            'acts': acts, 'decisions': ['Five newly listed Ohio Revised Code chapters parsed from live official chapter pages on 2026-11-11; each section in each chapter states one common effective date.'],
            'ai_use': ['No model-authored or model-corrected legal text.']}
    PART.parent.mkdir(exist_ok=True)
    payload = json.dumps(part, ensure_ascii=False, indent=1) + '\n'
    PART.write_text(payload, encoding='utf8', newline='\n')
    (EV / 'new-part-audit.json').write_text(json.dumps(audit, indent=2) + '\n', encoding='utf8')
    print(json.dumps({'part': str(PART), 'sha256': hashlib.sha256(payload.encode()).hexdigest(),
                      'acts': len(acts), 'sections': sum(len(a['versions'][0]['units']) for a in acts)}))

if __name__ == '__main__':
    make()
