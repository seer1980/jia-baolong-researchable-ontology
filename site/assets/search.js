
(function(){
  const input=document.getElementById('search-input');
  const button=document.getElementById('search-button');
  const status=document.getElementById('search-status');
  const results=document.getElementById('search-results');
  if(!input||!button||!status||!results)return;
  const english=document.documentElement.lang.startsWith('en');
  const copy=english?{
    prompt:'Enter a keyword to search the full English Markdown archive.',
    found:n=>`${n} related page${n===1?'':'s'} found`,
    empty:'No matching pages found.',
    loading:n=>`Search ${n} English Markdown documents.`,
    failed:'The search index could not be loaded. Please browse the paper index directly.'
  }:{
    prompt:'输入关键词搜索全部 Markdown 文档的 HTML 页面。',
    found:n=>`找到 ${n} 个相关页面`,
    empty:'没有找到匹配内容。',
    loading:n=>`输入关键词搜索 ${n} 个 Markdown 文档的 HTML 页面。`,
    failed:'搜索索引加载失败，请直接浏览论文索引。'
  };
  let index=[];
  const normalize=s=>(s||'').toLocaleLowerCase().replace(/\s+/g,' ');
  function score(item,q){
    const query=normalize(q); if(!query)return 0;
    const fields=[normalize(item.title),normalize(item.keywords),normalize(item.description),normalize(item.source),normalize(item.content)];
    let n=0; if(fields[0].includes(query))n+=100; if(fields[1].includes(query))n+=35; if(fields[2].includes(query))n+=15; if(fields[3].includes(query))n+=10; if(fields[4].includes(query))n+=8;
    query.split(/[\s,，、。/]+/).filter(Boolean).forEach(t=>fields.forEach((f,i)=>{if(f.includes(t))n+=(i===0?18:i===4?1:3)})); return n;
  }
  function render(){
    const q=input.value.trim(); if(!q){status.textContent=copy.prompt;results.innerHTML='';return;}
    const found=index.map(item=>({item,s:score(item,q)})).filter(x=>x.s>0).sort((a,b)=>b.s-a.s).slice(0,50);
    status.textContent=copy.found(found.length);
    results.innerHTML=found.length?found.map(({item})=>`<article class="search-result"><h3><a href="${item.url}">${escapeHtml(item.title)}</a></h3><div class="result-meta">${escapeHtml(item.source)} · ${escapeHtml(item.section)}</div><p>${escapeHtml(item.description)}</p></article>`).join(''):`<p>${copy.empty}</p>`;
  }
  function escapeHtml(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  fetch('search.json').then(r=>r.json()).then(data=>{index=data;const q=new URLSearchParams(location.search).get('q');if(q){input.value=q;render()}else{status.textContent=copy.loading(index.length)}}).catch(()=>status.textContent=copy.failed);
  button.addEventListener('click',render); input.addEventListener('keydown',e=>{if(e.key==='Enter')render()});
})();
