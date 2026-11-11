"""Deterministic current-rule extraction from official Ohio chapter HTML.

One rule per act, dated by its own Effective label. Requires lxml.
"""
import argparse
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import re
from lxml import html as LH

def norm(s):
    s = s.replace('\u00a0', ' ').replace('\u200b', '').replace('\ufeff', '').replace('\u00ad', '')
    for a,b in [('‘',"'"),('’',"'"),('“','"'),('”','"'),('–','-'),('—','-'),('‒','-'),('‑','-')]:
        s=s.replace(a,b)
    return re.sub(r'\s+', ' ', s).strip()

def text(el):
    return norm(''.join(el.itertext()))

def cls(el, name):
    return el.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," '+name+' ")]')

def body_lines(el):
    raw=LH.tostring(el, encoding='unicode')
    raw=re.sub(r'<!--.*?-->', '', raw, flags=re.S)
    raw=re.sub(r'<br\s*/?>', '\n', raw, flags=re.I)
    raw=re.sub(r'</(?:p|div|li|tr|h[1-6])>', '\n', raw, flags=re.I)
    raw=re.sub(r'</(?:td|th)>', '  ', raw, flags=re.I)
    raw=re.sub(r'<[^>]+>', '', raw)
    return [norm(html.unescape(x)) for x in raw.split('\n') if norm(html.unescape(x))]

def parse(raw, chapter_url):
    root=LH.fromstring(raw)
    acts=[]
    held=[]
    audit=[]
    rows=cls(root.xpath('//main')[0], 'list-content')
    chapter=text(root.xpath('//main//h1')[0])
    for row in rows:
        link=cls(row, 'content-head-text')[0].xpath('.//a')[0]
        url='https://codes.ohio.gov'+link.get('href')
        number=url.rsplit('/rule-',1)[-1]
        slug='oac-rule-'+number.replace(':','-')
        bodies=cls(row, 'laws-body')
        images=[x.get('src') for b in bodies for x in b.xpath('.//img')]
        entry={'rule':number,'url':url,'chapter_url':chapter_url,'source_images':len(images),
               'referenced_images':0,'omitted_images':0,'image_urls':images}
        try:
            if len(bodies)!=1 or not text(bodies[0]):
                raise ValueError('missing or ambiguous normative body')
            if images or bodies[0].xpath('.//svg|.//canvas|.//object|.//iframe'):
                raise ValueError('normative image or embedded object held for asset review')
            if bodies[0].xpath('.//table'):
                raise ValueError('normative HTML table held for structured table extraction')
            modules=cls(row, 'laws-section-info-module')
            fields={text(cls(m, 'label')[0]).rstrip(':'):text(cls(m, 'value')[0]) for m in modules}
            effective=fields.get('Effective','')
            day=dt.datetime.strptime(effective,'%B %d, %Y').date().isoformat()
            if day>'2026-11-11':
                raise ValueError('future effective date')
            heading=text(link).replace(' | ', ': ')
            lines=body_lines(bodies[0])
            units={'text':{'label':'O.A.C. '+number,'kind':'rule','text':'# '+heading+'\n'+'\n'.join(lines)+'\n'}}
            supplemental=[]
            for k,v in fields.items():
                if k!='PDF' and v:
                    supplemental.append(k+': '+v)
            for section in cls(row, 'laws-additional-information'):
                for label in section.xpath('.//strong'):
                    value=label.getnext()
                    if value is not None and text(value):
                        supplemental.append(text(label)+' '+text(value))
            if supplemental:
                units['source-information']={'label':'Official source information','kind':'metadata',
                     'text':'# Official source information\n'+'\n'.join(supplemental)+'\n'}
            acts.append({'slug':slug,'short':'O.A.C. '+number,'title':'Ohio Administrative Code, '+chapter+', '+heading,
                'url':url,'first_law':None,'earlier_laws':[],
                'versions':[{'from':day,'source_url':chapter_url,'sha256':hashlib.sha256(raw).hexdigest(),
                    'note':'In-force basis: the official rule prints Effective: '+effective+'. Current text; earlier effective dates are source metadata, not reconstructed versions.',
                    'units':units}]})
            entry.update({'date':day,'slug':slug,'body_words':len(norm(' '.join(lines)).split()),'status':'added'})
        except (ValueError,IndexError) as exc:
            entry.update({'status':'held','reason':str(exc)})
            held.append(entry)
        audit.append(entry)
    if not rows:
        held.append({'chapter_url':chapter_url,'reason':'no rule rows'})
    if len(set(a['slug'] for a in acts))!=len(acts):
        raise ValueError('duplicate rule slug')
    return acts,held,audit

def make(evidence, plan, out):
    acts=[]; held=[]; audit=[]
    for row in plan:
        p=evidence/row['file']
        if not p.exists():
            held.append({'chapter_url':row['url'],'reason':'chapter not collected'})
            continue
        a,h,q=parse(p.read_bytes(),row['url'])
        acts.extend(a);held.extend(h);audit.extend(q)
    part={'sources':[{'name':'Ohio Legislative Service Commission, Ohio Administrative Code',
          'url':'https://codes.ohio.gov/ohio-administrative-code','retrieved':'2026-11-11',
          'licence':'Official administrative rules are edicts of government.'}],
          'acts':acts,'decisions':['One current-text act per administrative rule, dated by the rule\'s official Effective label; prior effective dates and statutory authority retained as source metadata.'],
          'ai_use':['No model-authored or model-corrected legal text.']}
    payload=json.dumps(part,ensure_ascii=False,indent=1)+'\n'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(payload,encoding='utf8',newline='\n')
    return {'sha256':hashlib.sha256(payload.encode()).hexdigest(),'acts':len(acts),'held':held,'audit':audit}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('evidence',type=Path);ap.add_argument('plan',type=Path);ap.add_argument('out',type=Path)
    a=ap.parse_args(); result=make(a.evidence,json.loads(a.plan.read_text(encoding='utf8')),a.out)
    (a.evidence/(a.out.stem+'-audit.json')).write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('held','audit')}),flush=True)
