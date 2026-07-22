let P=[],M=[];
const PAGE_SIZE=25;
let currentPage=1;
const E=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const DL={latwe:'Łatwe',srednie:'Średnie',trudne:'Trudne'};

function sourceCategory(value){
  const normalized=String(value??'').trim().toLocaleLowerCase('pl-PL');
  if(normalized.includes('kolokw')) return 'kolokwium';
  if(normalized.includes('egzamin')) return 'egzamin';
  if(normalized.includes('ćwic')||normalized.includes('cwicz')) return 'cwiczenia';
  return 'inne';
}

fetch('../../data/catalog.json').then(r=>r.json()).then(d=>{
  P=d.problems.filter(x=>x.course_id===COURSE_ID);
  M=d.materials.filter(x=>x.course_id===COURSE_ID);
  COURSE_TOPICS.forEach(t=>{
    topic.add(new Option(t.name,t.id));
    document.getElementById('material-topic').add(new Option(t.name,t.id));
  });
  [...new Set(M.map(x=>x.type))].forEach(x=>document.getElementById('material-type').add(new Option(x,x)));
  document.querySelectorAll('.tab').forEach(b=>b.onclick=()=>{
    document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active',x===b));
    document.getElementById('problems-panel').classList.toggle('hidden',b.dataset.tab!=='problems');
    document.getElementById('materials-panel').classList.toggle('hidden',b.dataset.tab!=='materials');
  });
  ['topic','difficulty','source-type'].forEach(id=>document.getElementById(id).addEventListener('change',()=>{currentPage=1;renderP()}));
  ['material-type','material-topic'].forEach(id=>document.getElementById(id).onchange=renderM);
  renderP();renderM();
});

function filtered(){
  const t=topic.value,d=difficulty.value,s=document.getElementById('source-type').value;
  return P.filter(x=>(!t||x.topics.includes(t))&&(!d||x.difficulty===d)&&(!s||sourceCategory(x.source.type)===s));
}
function show(btn,id){const x=document.getElementById(id);x.classList.toggle('hidden');if(window.MathJax?.typesetPromise)MathJax.typesetPromise([x])}
function normalizeStatementTypography(root){
  if(!root) return;
  const nodes=[root,...root.querySelectorAll('*')];
  for(const el of nodes){
    if(el.matches && (el.matches('strong,b') || el.closest('strong,b'))) continue;
    el.style.setProperty('font-weight','400','important');
    el.style.setProperty('font-synthesis','none','important');
    el.style.setProperty('font-variation-settings','"wght" 400','important');
  }
  root.querySelectorAll('strong,b').forEach(el=>{
    el.style.setProperty('font-weight','700','important');
    el.style.setProperty('font-variation-settings','"wght" 700','important');
  });
}

function card(x){const inset=getSet().includes(x.id);return `<article class="problem" id="p-${E(x.id)}"><div class="top"><div><small>Zadanie ${String(x.number).padStart(4,'0')}</small><h2>${E(x.title)}</h2></div><button class="add ${inset?'on':''}" data-id="${E(x.id)}">${inset?'Usuń z zestawu':'Dodaj do zestawu'}</button></div><div class="badges"><span>${DL[x.difficulty]}</span>${x.verified?'<span>Zweryfikowane</span>':''}</div><div class="math statement">${x.statement}</div><p class="source">Źródło: ${E([x.source.type,x.source.name,x.source.academic_year].filter(Boolean).join(' · '))}</p><div class="buttons">${x.hint?`<button onclick="show(this,'h-${x.id}')">Wskazówka</button>`:''}${x.answer?`<button onclick="show(this,'a-${x.id}')">Odpowiedź</button>`:''}${x.solution?`<button onclick="show(this,'s-${x.id}')">Rozwiązanie</button>`:''}</div>${x.hint?`<div id="h-${x.id}" class="reveal hidden"><h3>Wskazówka</h3>${x.hint}</div>`:''}${x.answer?`<div id="a-${x.id}" class="reveal hidden"><h3>Odpowiedź</h3>${x.answer}</div>`:''}${x.solution?`<div id="s-${x.id}" class="reveal hidden"><h3>Rozwiązanie</h3>${x.solution}</div>`:''}</article>`}
function paginationMarkup(totalPages){
  if(totalPages<=1) return '';
  const visible=[];
  const add=v=>{if(v>=1&&v<=totalPages&&!visible.includes(v))visible.push(v)};
  add(1);add(currentPage-2);add(currentPage-1);add(currentPage);add(currentPage+1);add(currentPage+2);add(totalPages);
  visible.sort((a,b)=>a-b);
  let html=`<button class="page-nav" data-page="${currentPage-1}" ${currentPage===1?'disabled':''}>← Poprzednia</button>`;
  let prev=0;
  for(const page of visible){
    if(prev&&page-prev>1) html+='<span class="page-ellipsis">…</span>';
    html+=`<button class="page-number ${page===currentPage?'active':''}" data-page="${page}" aria-current="${page===currentPage?'page':'false'}">${page}</button>`;
    prev=page;
  }
  html+=`<button class="page-nav" data-page="${currentPage+1}" ${currentPage===totalPages?'disabled':''}>Następna →</button>`;
  return html;
}
function bindPagination(totalPages){
  document.querySelectorAll('#pagination button[data-page]').forEach(btn=>btn.onclick=()=>{
    const page=Number(btn.dataset.page);
    if(!Number.isFinite(page)||page<1||page>totalPages||page===currentPage)return;
    currentPage=page;
    renderP();
    document.getElementById('problems-panel')?.scrollIntoView({behavior:'smooth',block:'start'});
  });
}
function renderP(){
  const a=filtered();
  const totalPages=Math.max(1,Math.ceil(a.length/PAGE_SIZE));
  if(currentPage>totalPages) currentPage=totalPages;
  const start=(currentPage-1)*PAGE_SIZE;
  const pageItems=a.slice(start,start+PAGE_SIZE);
  const from=a.length?start+1:0,to=Math.min(start+PAGE_SIZE,a.length);
  document.getElementById('result-count').textContent=a.length?`Znaleziono: ${a.length} · Wyświetlane: ${from}–${to}`:'Znaleziono: 0';
  document.getElementById('problem-list').innerHTML=pageItems.map(card).join('')||'<div class="empty">Brak zadań.</div>';
  document.getElementById('pagination').innerHTML=paginationMarkup(a.length?totalPages:0);
  bindPagination(totalPages);
  document.querySelectorAll('.add').forEach(b=>b.onclick=()=>{const on=toggleSet(b.dataset.id);b.classList.toggle('on',on);b.textContent=on?'Usuń z zestawu':'Dodaj do zestawu'});
  if(window.MathJax?.typesetPromise)MathJax.typesetPromise();
}
function renderM(){const ty=document.getElementById('material-type').value,to=document.getElementById('material-topic').value,a=M.filter(x=>(!ty||x.type===ty)&&(!to||(x.topics||[]).includes(to)));document.getElementById('material-list').innerHTML=a.map(x=>`<article class="material"><div class="pdf">PDF</div><div><small>${E(x.type)}</small><h2>${E(x.title)}</h2><p>${E(x.description||'')}</p><div class="badges">${[x.author,x.academic_year,x.pages?x.pages+' stron':''].filter(Boolean).map(z=>`<span>${E(z)}</span>`).join('')}</div><p><a class="primary link" target="_blank" href="../../${E(x.file_url)}">Otwórz PDF</a> <a class="link" download href="../../${E(x.file_url)}">Pobierz</a></p></div></article>`).join('')||'<div class="empty">Brak materiałów.</div>'}


function normalizeAllStatements(){
  document.querySelectorAll('.statement').forEach(normalizeStatementTypography);
}
const statementObserver=new MutationObserver(()=>normalizeAllStatements());
statementObserver.observe(document.documentElement,{childList:true,subtree:true});
document.addEventListener('DOMContentLoaded',()=>{
  normalizeAllStatements();
  setTimeout(normalizeAllStatements,0);
  setTimeout(normalizeAllStatements,300);
  setTimeout(normalizeAllStatements,1200);
});
