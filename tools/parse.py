"""Build corpus.json for Ohio from the cached Wikidata facts (no network; deterministic). Metadata only: no law text."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'world-law'))
from state_corpus import sha256_file, write  # noqa: E402

CACHE = os.path.join(HERE, '.cache', 'wikidata.json')
W = json.load(open(CACHE, encoding='utf-8'))
E, L = W['entities'], W['labels']
DAY = '2026-10-29'
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def val(e, p):
    return [(c['mainsnak'].get('datavalue') or {}).get('value') for c in e['claims'].get(p, [])]


def unit(q, extra=()):
    e = E[q]
    lines = [f"# {e['labels']['en']['value']}", e['descriptions']['en']['value'] + '.',
             'Instance of: ' + '; '.join(L.get(v['id'], v['id']) for v in val(e, 'P31') if v) + '.']
    lines += list(extra)
    site = [v for v in val(e, 'P856') if isinstance(v, str)]
    if site:
        lines.append('Official website: ' + site[0])
    lines.append(f'Wikidata: https://www.wikidata.org/wiki/{q}')
    return {'label': e['labels']['en']['value'], 'kind': 'fact', 'text': '\n'.join(lines) + '\n'}


def main():
    t = val(E['Q1397'], 'P571')[0]['time']          # +1803-03-01T00:00:00Z
    y, m, d = int(t[1:5]), int(t[6:8]), int(t[9:11])
    units = {
        'ohio': unit('Q1397', [f'Date of inception given by Wikidata: {d} {MONTHS[m - 1]} {y} (admission to the Union).']),
        'constitution-of-ohio': unit('Q5164222', ['Its text is not in this repository (see the README).']),
        'ohio-revised-code': unit('Q7080878', ['Its text is not in this repository (see the README).']),
        'supreme-court-of-ohio': unit('Q3001112'),
    }
    corpus = {
        'country': {'code': 'US-OH', 'name': 'Ohio', 'slug': 'united-states-ohio', 'lang': 'en', 'tz': 'America/New_York',
                    'future_branch': 'future',
                    'publisher': {'name': 'Wikidata (CC0)', 'email': 'wikidata@wikidata.invalid'},
                    'default_in_force_rule': {'text': 'No law text is held; the single version is dated by the day before retrieval',
                                              'source': 'https://www.wikidata.org/wiki/Q1397'},
                    'licence_note': 'Wikidata facts, CC0 1.0.'},
        'sources': [{'name': 'Wikidata', 'url': 'https://www.wikidata.org/wiki/Q1397', 'retrieved': W['retrieved'], 'requests': 2,
                     'licence': 'CC0 1.0 (structured data in the main, Property and Lexeme namespaces).',
                     'notes': 'wbgetentities for Q1397, Q5164222, Q7080878 and Q3001112.'}],
        'laws': {},
        'acts': [{'slug': 'legal-system', 'short': 'Legal system', 'title': 'Ohio legal system: open facts (metadata only, no law text)',
                  'url': 'https://www.wikidata.org/wiki/Q1397', 'first_law': None, 'earlier_laws': [],
                  'versions': [{'from': DAY, 'source_url': 'https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q1397|Q5164222|Q7080878|Q3001112',
                                'sha256': sha256_file(CACHE), 'units': units,
                                'note': 'Open facts from Wikidata; this is not law text.'}]}],
        'applies': [],
        'decisions': ['Metadata only: the Revised Code and the Constitution of Ohio are published only on codes.ohio.gov, whose robots.txt disallows every crawler, and every Ohio government host timed out from our address on 2026-10-30; neither block was worked around, so no law text is held.',
                      'The version is dated 2026-10-29, the last full day before retrieval, so that no commit is dated ahead of the build.',
                      "The Supreme Court of Ohio's inception date in Wikidata (1841, year precision) is left out as unreliable."],
        'ai_use': ['none']}
    write(os.path.join(HERE, 'corpus.json'), corpus)
    print(len(units))


if __name__ == '__main__':
    main()
