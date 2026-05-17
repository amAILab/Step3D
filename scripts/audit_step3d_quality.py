#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urldefrag
import re, json, sys, os
ROOT=Path(__file__).resolve().parents[1]
BASE='https://amailab.github.io/Step3D/'
HTML=[p for p in ROOT.rglob('*.html') if '.git' not in p.parts and 'photos_do_not_touch' not in p.parts]
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.imgs=[]; self.forms=[]; self.inputs=[]; self.labels=[]; self.h1=0; self.ids=set(); self.buttons=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs); tag=tag.lower()
        if 'id' in d: self.ids.add(d['id'])
        if tag=='a' and d.get('href'): self.links.append(d.get('href'))
        if tag=='img': self.imgs.append(d)
        if tag=='form': self.forms.append(d)
        if tag in ('input','textarea','select'): self.inputs.append((tag,d))
        if tag=='label': self.labels.append(d)
        if tag=='h1': self.h1+=1
        if tag=='button': self.buttons.append(d)

def parse(p):
    q=P(); q.feed(p.read_text(errors='ignore')); return q
issues=[]; report={'html_files':len(HTML),'internal_links':0,'forms':0,'cta_links':0}
all_ids={}
for p in HTML:
    q=parse(p); rel=p.relative_to(ROOT)

    txt=p.read_text(errors='ignore')
    if 'step3d-common.css' not in txt or 'step3d-common.js' not in txt:
        issues.append(f'{rel}: common header/footer/search assets not connected')
    all_ids[str(rel)]=q.ids
    if q.h1!=1: issues.append(f'{rel}: expected exactly one h1, got {q.h1}')
    for img in q.imgs:
        if 'alt' not in img: issues.append(f'{rel}: image without alt {img.get("src","")[:80]}')
        if 'loading' not in img and img.get('fetchpriority')!='high': issues.append(f'{rel}: image without lazy/high priority {img.get("src","")[:80]}')
    report['forms']+=len(q.forms)
    for form in q.forms:
        action=form.get('action','')
        if action and not (action.startswith('https://formsubmit.co/') or action.startswith('/') or action.startswith('../') or action.startswith('#')):
            issues.append(f'{rel}: suspicious form action {action}')
    for href in q.links:
        if href.startswith(('mailto:','tel:','https://t.me/','http://','https://','#')):
            pass
        else:
            report['internal_links']+=1
        if any(x in (href.lower()) for x in ['brief','app/#app-brief','t.me/step_3d_mngr','formsubmit']): report['cta_links']+=1
        if href.startswith(('http://','https://','mailto:','tel:')): continue
        path,frag=urldefrag(href)
        path=path.split('?',1)[0]
        if not path or path.startswith('#'):
            target=p
        else:
            target=(p.parent/path).resolve()
            if target.is_dir(): target=target/'index.html'
        try: target=target.relative_to(ROOT)
        except Exception: continue
        target_path=ROOT/target
        if not target_path.exists(): issues.append(f'{rel}: broken internal link {href} -> {target}')
        elif frag:
            ids=all_ids.get(str(target))
            if ids is None: ids=parse(target_path).ids; all_ids[str(target)]=ids
            if frag not in ids: issues.append(f'{rel}: broken anchor {href}')
# SW sanity
sw=(ROOT/'service-worker.js').read_text(errors='ignore')
if 'step3d-pwa-v5' not in sw: issues.append('service-worker.js: cache version is not v5')
if 'Promise.allSettled' not in sw: issues.append('service-worker.js: install may fail on one missing asset')
if 'step3d-premium-system.css' not in sw: issues.append('service-worker.js: premium CSS not precached')
if 'step3d-common.js' not in sw or 'step3d-common.css' not in sw: issues.append('service-worker.js: common header/search assets not precached')
# sitemap/robots
sitemap=(ROOT/'sitemap.xml').read_text(errors='ignore')
robots=(ROOT/'robots.txt').read_text(errors='ignore')
if BASE not in sitemap: issues.append('sitemap.xml: expected canonical base missing')
if 'Sitemap:' not in robots: issues.append('robots.txt: Sitemap directive missing')
print(json.dumps(report,ensure_ascii=False,indent=2))
if issues:
    print('ISSUES:')
    print('\n'.join(issues[:200]))
    sys.exit(1)
print('QUALITY_AUDIT_OK')
