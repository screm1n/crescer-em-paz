# -*- coding: utf-8 -*-
import json, os, html, re
BASE=os.path.dirname(os.path.abspath(__file__))
M=os.path.join(BASE,'membros')
man=json.load(open(os.path.join(M,'manifest.json'),encoding='utf-8'))

# PLACEHOLDER do checkout do downsell (R$19,90) — trocar quando o usuario criar
CHECKOUT_DOWNSELL="#checkout-downsell-1990"
CSS_VERSION="20260731-netlify-routes"

CAT_LABEL={
 'Emocoes & Autoconhecimento':('Emoções & Autoconhecimento','💛'),
 'Inteligencia Emocional':('Inteligência Emocional','🎓'),
 'Ansiedade & Regulacao':('Ansiedade & Regulação','🌊'),
 'Raiva & Controle':('Raiva & Controle','🌋'),
 'Autoestima & Pensamentos':('Autoestima & Pensamentos','⭐'),
 'Arteterapia':('Arteterapia','🎨'),
 'Recursos para Adolescentes':('Recursos para Adolescentes','🧩'),
 'Jogos':('Jogos Terapêuticos','🎲'),
 'Bonus':('Bônus Especiais','🎁'),
}
ORDER=['Emocoes & Autoconhecimento','Inteligencia Emocional','Ansiedade & Regulacao','Raiva & Controle','Autoestima & Pensamentos','Arteterapia','Recursos para Adolescentes','Jogos','Bonus']

# ---------- style.css ----------
CSS=r"""
:root{--bg:#fff7f2;--card:#fff;--ink:#3a2e33;--muted:#7a6a70;--brand:#e8628a;--brand-dark:#c94873;--accent:#ffb347;--green:#2fae7a;--soft:#fde8ef;--line:#f2dbe3;--shadow:0 8px 24px rgba(201,72,115,.10)}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--ink);line-height:1.5;-webkit-font-smoothing:antialiased}
h1,h2,h3,.brand{font-family:'Space Grotesk','Inter',sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:0 16px}
.topbar{background:linear-gradient(135deg,var(--brand),var(--brand-dark));color:#fff;padding:22px 0 26px}
.topbar .wrap{display:flex;flex-direction:column;gap:6px}
.brand{font-size:1.5rem;font-weight:700;letter-spacing:-.02em;display:flex;align-items:center;gap:8px}
.brand-icon{width:22px;height:22px;stroke-width:2.4;flex:0 0 auto}
.plan-badge{align-self:flex-start;background:rgba(255,255,255,.22);border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:4px 12px;font-size:.78rem;font-weight:600;margin-top:4px}
.sub{opacity:.92;font-size:.92rem}
.sub .count-highlight{color:#8ee6b8;font-weight:800}
.sub-note{max-width:760px;background:#fff;color:var(--ink);border:1px solid rgba(255,255,255,.65);border-radius:12px;padding:10px 12px;margin-top:4px;font-size:.82rem;line-height:1.35;box-shadow:0 8px 22px rgba(91,38,61,.12)}
.notice{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--brand);border-radius:12px;padding:12px 14px;margin:18px 0 6px;color:var(--ink);box-shadow:0 4px 16px rgba(201,72,115,.06)}
.notice strong{color:var(--brand-dark)}
.notice p{font-size:.88rem;line-height:1.45;margin:0}
.notice-upsell{border-left-color:var(--accent);background:#fffaf0;color:#614000}
.member-layout{display:grid;grid-template-columns:240px minmax(0,1fr);gap:22px;align-items:start}
.sidebar{position:sticky;top:16px;margin-top:18px;background:var(--card);border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow);padding:14px}
.sidebar-title{font-family:'Space Grotesk','Inter',sans-serif;font-size:.9rem;font-weight:700;margin-bottom:10px;color:var(--ink)}
.side-nav{display:flex;flex-direction:column;gap:6px}
.mobile-section-menu{display:none}
.side-link{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:8px;min-height:38px;padding:8px 9px;border-radius:11px;color:var(--ink);text-decoration:none;font-size:.82rem;font-weight:700;line-height:1.15}
.side-link:hover{background:var(--soft);color:var(--brand-dark)}
.side-link:focus-visible{outline:3px solid rgba(232,98,138,.28);outline-offset:2px}
.side-icon{font-size:1rem}
.side-text{overflow:hidden;text-overflow:ellipsis}
.side-count{font-size:.72rem;color:var(--muted);font-weight:700;background:#fff7f2;border:1px solid var(--line);border-radius:999px;min-width:28px;padding:2px 6px;text-align:center}
.side-link.is-locked .side-text{color:var(--muted)}
.member-content{min-width:0}
.cat{margin:30px 0 4px}
.cat{scroll-margin-top:20px}
.cat h2{font-size:1.25rem;display:flex;align-items:center;gap:9px;letter-spacing:-.01em}
.cat .count{font-size:.8rem;color:var(--muted);font-weight:500;font-family:'Inter'}
.cat.locked h2 .lockmini{font-size:.72rem;background:var(--brand);color:#fff;border-radius:999px;padding:2px 9px;font-weight:700;letter-spacing:.02em}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:16px;margin-top:14px}
.item{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:var(--shadow);display:flex;flex-direction:column}
.thumb{position:relative;background:var(--soft);aspect-ratio:1/1.29;overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.item h3{font-size:.9rem;line-height:1.25;padding:11px 12px 8px;flex:1}
.actions{display:flex;gap:7px;padding:0 10px 11px}
.btn{flex:1;border:none;border-radius:10px;padding:9px 4px;font-size:.78rem;font-weight:700;font-family:'Inter';cursor:pointer;text-decoration:none;text-align:center;display:inline-flex;align-items:center;justify-content:center;gap:4px;transition:transform .1s,filter .1s}
.btn:active{transform:translateY(1px)}
.btn.is-sharing{filter:saturate(.75);pointer-events:none}
.btn-print{background:linear-gradient(180deg,var(--brand),var(--brand-dark));color:#fff;box-shadow:0 3px 0 var(--brand-dark)}
.btn-wa{background:#25D366;color:#fff;box-shadow:0 3px 0 #1da851}
/* locked */
.item.locked .thumb img{filter:blur(6px) saturate(.7);transform:scale(1.05)}
.item.locked .lockover{position:absolute;inset:0;background:linear-gradient(180deg,rgba(201,72,115,.30),rgba(201,72,115,.55));display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:#fff;text-align:center;padding:10px}
.item.locked .lockover .cad{font-size:1.7rem}
.item.locked .lockover span{font-size:.74rem;font-weight:600;line-height:1.2;text-shadow:0 1px 3px rgba(0,0,0,.25)}
.btn-unlock{background:var(--accent);color:#5a3a00;box-shadow:0 3px 0 #d9902a;width:100%}
footer{text-align:center;color:var(--muted);font-size:.76rem;padding:34px 16px 46px;line-height:1.6}
@media(max-width:860px){
  .member-layout{display:block}
  .sidebar{display:none}
  .mobile-section-menu{display:block;position:sticky;top:0;z-index:8;margin:0 -16px 12px;background:rgba(255,247,242,.96);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);padding:10px 16px}
  .mobile-section-menu summary{list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);padding:12px 14px;color:var(--ink);font-weight:800;cursor:pointer}
  .mobile-section-menu summary::-webkit-details-marker{display:none}
  .menu-label{display:flex;align-items:center;gap:8px;font-family:'Space Grotesk','Inter',sans-serif}
  .menu-chevron{font-size:.9rem;color:var(--brand-dark);transition:transform .16s ease}
  .mobile-section-menu[open] .menu-chevron{transform:rotate(180deg)}
  .mobile-menu-nav{display:grid;grid-template-columns:1fr;gap:6px;background:var(--card);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);margin-top:8px;padding:8px}
  .mobile-menu-nav .side-link{background:#fff;border:1px solid var(--line)}
  .cat{scroll-margin-top:88px}
}
@media(max-width:520px){.grid{grid-template-columns:repeat(2,1fr);gap:12px}.item h3{font-size:.82rem}.btn{font-size:.72rem;padding:8px 3px}.side-link{font-size:.8rem;min-height:38px;padding:8px 9px}.notice{padding:11px 12px}.notice p{font-size:.84rem}}
"""
open(os.path.join(M,'style.css'),'w',encoding='utf-8').write(CSS)

# ---------- imprimir.html ----------
IMPRIMIR=r"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Imprimir — Crescer em Paz</title>
<style>
body{margin:0;font-family:system-ui,sans-serif;background:#3a2e33;color:#fff;display:flex;flex-direction:column;height:100vh}
.bar{background:#c94873;padding:10px 14px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.bar b{font-family:'Space Grotesk',sans-serif;margin-right:auto;font-size:.95rem}
.bar a,.bar button{background:#fff;color:#c94873;border:none;border-radius:9px;padding:9px 14px;font-weight:700;font-size:.85rem;cursor:pointer;text-decoration:none}
.bar .wa{background:#25D366;color:#fff}
iframe{flex:1;border:none;width:100%;background:#fff}
.hint{font-size:.78rem;opacity:.85;padding:6px 14px;background:#2a2024}
</style></head><body>
<div class="bar">
  <b>🖨️ Impressão</b>
  <button onclick="doPrint()">Imprimir agora</button>
  <a id="dl" download>Baixar PDF</a>
  <button id="wa" class="wa" onclick="sharePdf()">WhatsApp</button>
</div>
<div class="hint">Se a janela de impressão não abrir sozinha, clique em <b>Imprimir agora</b>.</div>
<iframe id="fr"></iframe>
<script>
var slug=new URLSearchParams(location.search).get('f')||'';
var url='/membros/pdfs/'+slug+'.pdf';
var fr=document.getElementById('fr'); fr.src=url;
document.getElementById('dl').href=url;
var link=location.origin+url;
function doPrint(){try{fr.contentWindow.focus();fr.contentWindow.print();}catch(e){window.open(url,'_blank');}}
async function sharePdf(){
  var btn=document.getElementById('wa');
  var oldText=btn.textContent;
  btn.textContent='Preparando...';
  btn.disabled=true;
  try{
    var response=await fetch(url);
    if(!response.ok) throw new Error('PDF não encontrado');
    var blob=await response.blob();
    var file=new File([blob],slug+'.pdf',{type:'application/pdf'});
    if(navigator.canShare && navigator.canShare({files:[file]})){
      await navigator.share({title:'Material Crescer em Paz',text:'Material Crescer em Paz',files:[file]});
    }else if(navigator.share){
      await navigator.share({title:'Material Crescer em Paz',text:'Baixe e imprima este material do Crescer em Paz.',url:link});
    }else{
      window.open(url,'_blank','noopener');
    }
  }catch(err){
    if(!err || err.name!=='AbortError') window.open(url,'_blank','noopener');
  }finally{
    btn.textContent=oldText;
    btn.disabled=false;
  }
}
fr.addEventListener('load',function(){setTimeout(doPrint,700);});
</script></body></html>"""
open(os.path.join(M,'imprimir.html'),'w',encoding='utf-8').write(IMPRIMIR)

# ---------- páginas ----------
def esc(s): return html.escape(s)

def cat_id(cat):
    return 'sec-'+re.sub(r'[^a-z0-9]+','-',cat.lower()).strip('-')

def card(it, locked):
    slug=it['slug']; title=esc(it['title'])
    cap='/membros/capas/'+slug+'.jpg'
    if locked:
        return f'''<div class="item locked">
          <div class="thumb"><img src="{cap}" alt="" loading="lazy" onerror="this.style.display='none'">
            <a class="lockover" href="{CHECKOUT_DOWNSELL}"><span class="cad">🔒</span><span>Disponível na Completa</span></a></div>
          <h3>{title}</h3>
          <div class="actions"><a class="btn btn-unlock" href="{CHECKOUT_DOWNSELL}">🔓 Desbloquear por R$19,90</a></div>
        </div>'''
    return f'''<div class="item">
      <div class="thumb"><img src="{cap}" alt="{title}" loading="lazy" onerror="this.style.background='var(--soft)'"></div>
      <h3>{title}</h3>
      <div class="actions">
        <a class="btn btn-print" href="/membros/imprimir.html?f={slug}" target="_blank" rel="noopener">🖨️ Imprimir</a>
        <a class="btn btn-wa" href="/membros/pdfs/{slug}.pdf" data-slug="{slug}" data-title="{title}" onclick="return sharePdf(this)">WhatsApp</a>
      </div>
    </div>'''

def build(plan):
    is_ess = (plan=='essencial')
    plan_name='Biblioteca Essencial' if is_ess else 'Biblioteca Completa'
    unlocked=[it for it in man if not (is_ess and (it['isJogo'] or it['isBonus']))]
    total_disp=len(man)
    secs=''
    nav=''
    for cat in ORDER:
        its=[it for it in man if it['cat']==cat]
        if not its: continue
        label,emo=CAT_LABEL[cat]
        cat_locked = is_ess and all(it['isJogo'] or it['isBonus'] for it in its)
        nav+=f'''<a class="side-link {'is-locked' if cat_locked else ''}" href="#{cat_id(cat)}"><span class="side-icon">{emo}</span><span class="side-text">{esc(label)}</span><span class="side-count">{len(its)}</span></a>'''
        lockmini='<span class="lockmini">🔒 na Completa</span>' if cat_locked else ''
        cards=''.join(card(it, is_ess and (it['isJogo'] or it['isBonus'])) for it in its)
        secs+=f'''<section id="{cat_id(cat)}" class="cat {'locked' if cat_locked else ''}">
          <h2>{emo} {esc(label)} <span class="count">{len(its)} materiais</span> {lockmini}</h2>
          <div class="grid">{cards}</div>
        </section>'''
    unlocked_count=len(unlocked)
    upsell='' if not is_ess else '''<div class="notice notice-upsell"><p><strong>Biblioteca Essencial:</strong> jogos e bônus ficam bloqueados. Desbloqueie a Completa por R$19,90.</p></div>'''
    doc=f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Crescer em Paz — {plan_name}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/membros/style.css?v={CSS_VERSION}">
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js" defer></script>
</head><body>
<div class="topbar"><div class="wrap">
  <div class="brand"><i data-lucide="heart-handshake" class="brand-icon" aria-hidden="true"></i><span>Crescer em Paz</span></div>
  <div class="sub"><span class="count-highlight">{unlocked_count}</span> materiais liberados pra você imprimir</div>
  <div class="sub-note">Cada material reúne várias páginas, fichas, cartões, atividades e jogos. Somando tudo dentro dos PDFs, sua biblioteca passa de 900 ferramentas prontas para usar.</div>
  <div class="plan-badge">✔ {plan_name}</div>
</div></div>
<div class="wrap member-layout">
  <aside class="sidebar" aria-label="Seções da biblioteca">
    <div class="sidebar-title">Seções da biblioteca</div>
    <nav class="side-nav">{nav}</nav>
  </aside>
  <main class="member-content">
    <details class="mobile-section-menu">
      <summary><span class="menu-label">☰ Seções</span><span class="menu-chevron">⌄</span></summary>
      <nav class="mobile-menu-nav">{nav}</nav>
    </details>
    <div class="notice"><p><strong>Imprimir</strong> abre o PDF. <strong>WhatsApp</strong> compartilha o próprio PDF pelo celular.</p></div>
    {upsell}
    {secs}
  </main>
</div>
<footer>Crescer em Paz © 2025 · Material de apoio educativo. Uso pessoal.<br>Acesso vitalício aos materiais da sua biblioteca.</footer>
<script>
async function sharePdf(a){{
  var slug=a.getAttribute('data-slug');
  var title=a.getAttribute('data-title')||'Material Crescer em Paz';
  var url='/membros/pdfs/'+slug+'.pdf';
  var link=location.origin+url;
  var oldText=a.textContent;
  a.classList.add('is-sharing');
  a.setAttribute('aria-busy','true');
  a.textContent='Preparando...';
  try{{
    var response=await fetch(url);
    if(!response.ok) throw new Error('PDF não encontrado');
    var blob=await response.blob();
    var file=new File([blob],slug+'.pdf',{{type:'application/pdf'}});
    if(navigator.canShare && navigator.canShare({{files:[file]}})){{
      await navigator.share({{
        title:title,
        text:title,
        files:[file]
      }});
    }}else if(navigator.share){{
      await navigator.share({{
        title:title,
        text:'Baixe e imprima este material do Crescer em Paz.',
        url:link
      }});
    }}else{{
      window.open(url,'_blank','noopener');
    }}
  }}catch(err){{
    if(!err || err.name!=='AbortError') window.open(url,'_blank','noopener');
  }}finally{{
    a.classList.remove('is-sharing');
    a.removeAttribute('aria-busy');
    a.textContent=oldText;
  }}
  return false;
}}
document.querySelectorAll('.mobile-menu-nav a').forEach(function(link){{
  link.addEventListener('click',function(){{
    var menu=link.closest('details');
    if(menu) menu.open=false;
  }});
}});
window.addEventListener('DOMContentLoaded',function(){{
  if(window.lucide) window.lucide.createIcons();
}});
</script>
</body></html>'''
    folders=[os.path.join(M,'membroessencial' if is_ess else 'membrocompleta')]
    if is_ess:
        folders.append(os.path.join(BASE,'membroessencial'))
    else:
        folders.append(os.path.join(BASE,'membrocompleto'))
        folders.append(os.path.join(BASE,'membrocompleta'))
    for folder in folders:
        os.makedirs(folder,exist_ok=True)
        open(os.path.join(folder,'index.html'),'w',encoding='utf-8').write(doc)
    return unlocked_count

e=build('essencial'); c=build('completa')
print('Essencial: %d liberados | Completa: %d liberados | total %d'%(e,c,len(man)))
