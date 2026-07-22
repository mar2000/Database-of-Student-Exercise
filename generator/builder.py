from __future__ import annotations
import json, re, shutil
from pathlib import Path
from typing import Any
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT/'content'; SITE=ROOT/'site'; BUILD=ROOT/'build'

class ContentError(ValueError): pass

def yload(path:Path)->dict[str,Any]:
    try: data=yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    except Exception as e: raise ContentError(f'Błędny YAML w {path}: {e}')
    if not isinstance(data,dict): raise ContentError(f'YAML musi być mapą: {path}')
    return data

def parse_problem(path:Path, course:dict[str,Any])->dict[str,Any]:
    raw=path.read_text(encoding='utf-8')
    m=re.match(r'\A---\s*\n(.*?)\n---\s*\n(.*)\Z',raw,re.S)
    if not m: raise ContentError(f'Brak nagłówka YAML: {path}')
    meta=yaml.safe_load(m.group(1)) or {}; body=m.group(2)
    for key in ['id','title','topics','difficulty','source']:
        if key not in meta: raise ContentError(f'Brak pola {key}: {path}')
    if not str(meta['id']).startswith(course['id']+'-'): raise ContentError(f'Id zadania nie pasuje do kursu: {path}')
    if path.stem.isdigit() and int(meta.get('number',path.stem))!=int(path.stem): raise ContentError(f'Numer nie zgadza się z nazwą pliku: {path}')
    if meta['difficulty'] not in ['latwe','srednie','trudne']: raise ContentError(f'Błędna trudność: {path}')
    known={t['id'] for t in course.get('topics',[])}; unknown=set(meta.get('topics',[]))-known
    if unknown: raise ContentError(f'Nieznane działy {unknown}: {path}')
    aliases={'treść':'statement','tresc':'statement','wskazówka':'hint','wskazowka':'hint','odpowiedź':'answer','odpowiedz':'answer','rozwiązanie':'solution','rozwiazanie':'solution'}
    parts={v:[] for v in aliases.values()}; current=None
    for line in body.splitlines():
        h=re.match(r'^##\s+(.+?)\s*$',line)
        if h: current=aliases.get(h.group(1).lower())
        elif current: parts[current].append(line)
    out={k:'\n'.join(v).strip() for k,v in parts.items()}
    if not out['statement']: raise ContentError(f'Brak sekcji Treść: {path}')
    return {'id':str(meta['id']),'number':int(meta.get('number',0)),'title':str(meta['title']),'course_id':course['id'],'topics':list(meta.get('topics',[])),'difficulty':meta['difficulty'],'source':meta.get('source') or {},'tags':list(meta.get('tags',[])),'verified':bool(meta.get('verified',False)),'published':bool(meta.get('published',True)),**out}

def collect():
    fields=[yload(p) for p in sorted((CONTENT/'fields').glob('*.yaml')) if yload(p).get('published',True)]
    field_ids={f['id'] for f in fields}; courses=[]; problems=[]; materials=[]; seen=set()
    for cdir in sorted((CONTENT/'courses').glob('*')):
        if not cdir.is_dir() or not (cdir/'course.yaml').exists(): continue
        c=yload(cdir/'course.yaml')
        if c.get('field') not in field_ids: raise ContentError(f'Nieznany kierunek: {cdir}')
        if c.get('id')!=cdir.name: raise ContentError(f'Id kursu musi być nazwą katalogu: {cdir}')
        if not c.get('published',True): continue
        courses.append(c)
        for p in sorted((cdir/'zadania').glob('*.md')):
            item=parse_problem(p,c)
            if item['id'] in seen: raise ContentError(f'Powtórzone id: {item["id"]}')
            seen.add(item['id'])
            if item['published']: problems.append(item)
        for mdir in sorted((cdir/'materialy').glob('*')):
            if not mdir.is_dir() or not (mdir/'material.yaml').exists(): continue
            m=yload(mdir/'material.yaml')
            for key in ['id','title','type','file']:
                if key not in m: raise ContentError(f'Brak pola {key}: {mdir}')
            pdf=mdir/m['file']
            if not pdf.exists() or pdf.suffix.lower()!='.pdf': raise ContentError(f'Brak PDF: {pdf}')
            if set(m.get('topics',[]))-{t['id'] for t in c.get('topics',[])}: raise ContentError(f'Nieznany dział materiału: {mdir}')
            if m.get('published',True):
                m=dict(m); m['course_id']=c['id']; m['_dir']=str(mdir); materials.append(m)
    return fields,courses,problems,materials

def shell(title, body, depth=0, scripts=''):
    pre='../'*depth
    return f'''<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="{pre}assets/style.css"><script>window.MathJax={{tex:{{inlineMath:[["\\\\(","\\\\)"],["$","$"]],displayMath:[["\\\\[","\\\\]"]]}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script></head><body><header><a href="{pre}index.html">Baza zadań studenckich</a><a href="{pre}zestaw/index.html">Mój zestaw <span id="set-count">0</span></a></header><main>{body}</main><footer>Statyczna strona bez kont i panelu administratora.</footer><script src="{pre}assets/common.js"></script>{scripts}</body></html>'''

def build_site():
    fields,courses,problems,materials=collect()
    if BUILD.exists(): shutil.rmtree(BUILD)
    BUILD.mkdir(); shutil.copytree(SITE/'assets',BUILD/'assets'); (BUILD/'data').mkdir()
    for m in materials:
        src=Path(m.pop('_dir')); dst=BUILD/'files'/m['course_id']/m['id']; dst.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src/m['file'],dst/m['file']); m['file_url']=f"files/{m['course_id']}/{m['id']}/{m['file']}"
    catalog={'fields':fields,'courses':courses,'problems':problems,'materials':materials}
    (BUILD/'data/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
    cards=''.join([f'<a class="card" href="kierunki/{f["id"]}/index.html"><span>Kierunek</span><h2>{f["name"]}</h2><p>{f.get("description","")}</p><b>Zobacz przedmioty →</b></a>' for f in fields])
    (BUILD/'index.html').write_text(shell('Wybierz kierunek',f'<section class="hero"><span>Nauka na studiach</span><h1>Wybierz swój kierunek</h1><p>Zadania, rozwiązania i materiały dydaktyczne uporządkowane według kierunku i przedmiotu.</p></section><section class="grid">{cards}</section>'),encoding='utf-8')
    for f in fields:
        cs=[c for c in courses if c['field']==f['id']]
        cards=''.join([f'<a class="card" href="../../przedmioty/{c["id"]}/index.html"><span>Przedmiot</span><h2>{c["name"]}</h2><p>{c.get("description","")}</p><div class="stats">{sum(p["course_id"]==c["id"] for p in problems)} zadań · {sum(m["course_id"]==c["id"] for m in materials)} materiałów</div></a>' for c in cs])
        body=f'<nav><a href="../../index.html">Strona główna</a> › {f["name"]}</nav><section class="page-head"><span>Kierunek</span><h1>{f["name"]}</h1><p>{f.get("description","")}</p></section><section class="grid">{cards}</section>'
        out=BUILD/'kierunki'/f['id']; out.mkdir(parents=True); (out/'index.html').write_text(shell(f['name'],body,2),encoding='utf-8')
    for c in courses:
        f=next(x for x in fields if x['id']==c['field'])
        body=f'''<nav><a href="../../index.html">Strona główna</a> › <a href="../../kierunki/{f['id']}/index.html">{f['name']}</a> › {c['name']}</nav><section class="page-head"><span>Przedmiot</span><h1>{c['name']}</h1><p>{c.get('description','')}</p></section><div class="tabs"><button class="tab active" data-tab="problems">Zadania</button><button class="tab" data-tab="materials">Materiały dydaktyczne</button></div><section id="problems-panel"><div class="filters filters-three"><label>Dział<select id="topic"><option value="">Wszystkie</option></select></label><label>Trudność<select id="difficulty"><option value="">Wszystkie</option><option value="latwe">Łatwe</option><option value="srednie">Średnie</option><option value="trudne">Trudne</option></select></label><label>Pochodzenie<select id="source-type"><option value="">Wszystkie</option><option value="kolokwium">Kolokwium</option><option value="egzamin">Egzamin</option><option value="cwiczenia">Ćwiczenia</option><option value="inne">Inne</option></select></label></div><p id="result-count"></p><div id="problem-list"></div><nav id="pagination" class="pagination" aria-label="Strony zadań"></nav></section><section id="materials-panel" class="hidden"><div class="filters small"><label>Typ<select id="material-type"><option value="">Wszystkie</option></select></label><label>Dział<select id="material-topic"><option value="">Wszystkie</option></select></label></div><div id="material-list"></div></section>'''
        script=f'<script>window.COURSE_ID={json.dumps(c["id"])};window.COURSE_TOPICS={json.dumps(c.get("topics",[]),ensure_ascii=False)};</script><script src="../../assets/course.js"></script>'
        out=BUILD/'przedmioty'/c['id']; out.mkdir(parents=True); (out/'index.html').write_text(shell(c['name'],body,2,script),encoding='utf-8')
    out=BUILD/'zestaw'; out.mkdir(); body='<nav><a href="../index.html">Strona główna</a> › Mój zestaw</nav><section class="page-head set-head"><span>Generator PDF</span><h1>Mój zestaw</h1><p>Ułóż zestaw z wybranych zadań, a następnie pobierz gotowy plik PDF bez otwierania okna drukowania.</p><div class="set-actions"><button id="export-pdf" class="primary">Eksportuj zadania do PDF</button><button id="clear-set">Wyczyść zestaw</button></div><p id="export-status" class="export-status" aria-live="polite"></p></section><div id="set-list"></div><div id="pdf-export-root" aria-hidden="true"></div>'
    pdf_scripts='<script src="https://cdn.jsdelivr.net/npm/html2pdf.js@0.10.1/dist/html2pdf.bundle.min.js"></script><script src="../assets/set.js"></script>'
    (out/'index.html').write_text(shell('Mój zestaw',body,1,pdf_scripts),encoding='utf-8')
    print(f'Zbudowano: {len(fields)} kierunki, {len(courses)} przedmioty, {len(problems)} zadania, {len(materials)} materiały')
    return BUILD

if __name__=='__main__': build_site()
