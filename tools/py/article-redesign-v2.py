"""Article redesign v2 — total redesign matching service-page design system.

Changes vs v1:
- Hide theme's hero (.page-header), inline CTAs (.sx-post-cta, .wp-block-group with "Butuh"), theme TOC (.sx-toc), comments (#comments), tags (.post-tags)
- Inject custom dark-teal gradient hero matching service pages
- 2-column layout: 760px body + 260px sticky TOC
- Single sx-cta-final at bottom
- Wider container 1100px
- All sxa- prefix to avoid collision with theme
"""
import json, base64, urllib.request, urllib.error, sys, os, re

WP_USER = 'admin'
WP_PASS = 'hCYK JqF1 khdB WDzI LQdQ WEBr'
SITE    = 'https://suriota.com'

MARKER_START = '<!-- SURIOTA_REDESIGN_v2_START -->'
MARKER_END   = '<!-- SURIOTA_REDESIGN_v2_END -->'
OLD_MARKER_START = '<!-- SURIOTA_REDESIGN_v1_START -->'
OLD_MARKER_END   = '<!-- SURIOTA_REDESIGN_v1_END -->'

REDESIGN_BLOCK = MARKER_START + '\n<!-- wp:html -->\n' + r'''<style id="sxa-css">@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
.single-post{--sxa-ink:#0F1A1F;--sxa-mute:#5B6F75;--sxa-line:#E8ECEE;--sxa-amber:#F59E0B;--sxa-accent:#0E3942;--sxa-accent-2:#22D3A4;--sxa-surface:#FAFBFC;background:var(--sxa-surface)}
body.single-post .page-header{display:none !important}
body.single-post #comments,body.single-post #respond,body.single-post .comments-area,body.single-post .post-comments,body.single-post .post-tags,body.single-post .tag-links,body.single-post .sx-post-cta,body.single-post .sx-toc:not(.sxa-toc){display:none !important}
body.single-post .sxa-hide-theme{display:none !important}
.sxa-hero{background:linear-gradient(135deg,#17505D 0%,#0C2F38 100%);padding:64px 20px 56px;text-align:center;animation:sxaFadeIn .6s ease-out;position:relative;overflow:hidden}
.sxa-hero::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#F59E0B 0%,#22D3A4 50%,#0EA5E9 100%)}
.sxa-hero-inner{max-width:920px;margin:0 auto}
.sxa-bread{display:flex;justify-content:center;gap:8px;align-items:center;flex-wrap:wrap;margin:0 0 22px;font:500 12.5px/1 'IBM Plex Mono',monospace;color:rgba(255,255,255,.55)}
.sxa-bread a{color:rgba(255,255,255,.65);text-decoration:none;transition:color .15s}
.sxa-bread a:hover{color:#fff}
.sxa-bread .sxa-sep{color:rgba(255,255,255,.28)}
.sxa-bread .sxa-cur{color:#fff;font-weight:600}
.sxa-h1{font:800 clamp(30px,4.4vw,52px)/1.1 'Plus Jakarta Sans',sans-serif;color:#fff;letter-spacing:-.02em;margin:0 0 22px;text-align:center}
.sxa-meta{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin:0}
.sxa-pill{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;background:rgba(255,255,255,.10);color:#fff;font:600 11px/1 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;border-radius:999px;border:1px solid rgba(255,255,255,.16)}
.sxa-pill.amber{background:rgba(245,158,11,.18);color:#FBBF24;border-color:rgba(251,191,36,.24)}
.sxa-pill.teal{background:rgba(34,211,164,.16);color:#5EEAD4;border-color:rgba(34,211,164,.24)}
@keyframes sxaFadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
body.single-post .page-content{font-family:'Plus Jakarta Sans',system-ui,sans-serif !important;color:var(--sxa-ink);max-width:1100px;margin:0 auto;padding:48px 24px 32px;font-size:17px;line-height:1.78;display:grid;grid-template-columns:1fr 260px;gap:56px}
body.single-post .page-content > *{grid-column:1}
body.single-post .page-content .sxa-toc{grid-column:2;grid-row:1 / span 999;position:sticky;top:100px;align-self:start;max-height:calc(100vh - 120px);overflow:auto}
body.single-post .page-content > p{margin:0 0 22px;font-weight:400;color:#1F2D33;max-width:760px}
body.single-post .page-content h2{font:700 28px/1.25 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent) !important;letter-spacing:-.01em;margin:48px 0 16px !important;scroll-margin-top:90px;padding-left:14px;border-left:4px solid var(--sxa-amber);text-align:left;max-width:760px}
body.single-post .page-content h3{font:700 21px/1.3 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent) !important;margin:32px 0 12px !important;scroll-margin-top:90px;text-align:left;max-width:760px}
body.single-post .page-content figure,body.single-post .page-content .wp-block-image{margin:32px 0;max-width:760px}
body.single-post .page-content img{border-radius:12px;box-shadow:0 8px 32px rgba(14,57,66,.10);max-width:100%;height:auto;display:block;margin:0 auto}
body.single-post .page-content figcaption{font:500 13px/1.5 'IBM Plex Mono',monospace !important;color:var(--sxa-mute) !important;text-align:center;margin-top:10px}
body.single-post .page-content blockquote{border:none;border-left:4px solid var(--sxa-amber);background:#fff;padding:18px 22px;margin:32px 0;border-radius:0 8px 8px 0;font:500 18px/1.65 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent);box-shadow:0 4px 18px rgba(14,57,66,.05);max-width:760px}
body.single-post .page-content ul,body.single-post .page-content ol{padding-left:24px;margin:0 0 22px;max-width:760px}
body.single-post .page-content li{margin-bottom:8px;line-height:1.7}
body.single-post .page-content ul li::marker{color:var(--sxa-amber)}
body.single-post .page-content ol li::marker{color:var(--sxa-amber);font-family:'IBM Plex Mono',monospace;font-weight:600}
body.single-post .page-content a{color:var(--sxa-accent);text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--sxa-amber);transition:color .15s}
body.single-post .page-content a:hover{color:var(--sxa-amber)}
body.single-post .page-content strong{color:var(--sxa-accent);font-weight:700}
body.single-post .page-content > p:first-of-type::first-letter{font:800 64px/.85 'Plus Jakarta Sans',sans-serif;color:var(--sxa-amber);float:left;margin:6px 14px 0 0}
.sxa-toc{background:#fff;border:1px solid var(--sxa-line);border-radius:12px;padding:20px 18px;box-shadow:0 4px 18px rgba(14,57,66,.04)}
.sxa-toc-title{font:700 11px/1 'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--sxa-accent);margin:0 0 14px;display:flex;align-items:center;gap:8px}
.sxa-toc-title::before{content:"";width:14px;height:2px;background:var(--sxa-amber)}
.sxa-toc ol{list-style:none;padding:0;margin:0;font-size:13px}
.sxa-toc li{margin:0 0 4px}
.sxa-toc a{display:block;padding:6px 0 6px 18px;color:var(--sxa-mute);text-decoration:none;border-left:2px solid transparent;line-height:1.4;transition:all .15s;font-weight:500}
.sxa-toc a:hover{color:var(--sxa-accent)}
.sxa-toc a.active{color:var(--sxa-accent);border-left-color:var(--sxa-amber);font-weight:600;background:rgba(245,158,11,.05)}
.sxa-toc li.lvl-3 a{padding-left:32px;font-size:12px;color:#7A8B91}
.sxa-share-inline{display:flex;justify-content:center;gap:10px;margin:48px 0 32px;padding:24px 0;border-top:1px solid var(--sxa-line);border-bottom:1px solid var(--sxa-line);max-width:760px}
.sxa-share-inline .lab{font:600 11px/1 'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--sxa-mute);align-self:center;margin-right:8px}
.sxa-share-inline a,.sxa-share-inline button{width:38px;height:38px;border-radius:50%;background:#fff;border:1px solid var(--sxa-line);display:inline-flex;align-items:center;justify-content:center;color:var(--sxa-accent);text-decoration:none;transition:all .15s;cursor:pointer;padding:0}
.sxa-share-inline a:hover,.sxa-share-inline button:hover{background:var(--sxa-accent);color:#fff;border-color:var(--sxa-accent);transform:translateY(-1px)}
.sxa-share-inline svg{width:16px;height:16px}
.sxa-cta-final{max-width:920px;margin:24px auto 64px;padding:0 24px}
.sxa-cta-inner{padding:44px 36px;background:linear-gradient(135deg,#0E3942 0%,#205B69 100%);border-radius:14px;text-align:center;position:relative;overflow:hidden}
.sxa-cta-inner::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#F59E0B 0%,#22D3A4 50%,#0EA5E9 100%)}
.sxa-cta-eyebrow{display:inline-block;font:600 11px/1 'IBM Plex Mono',monospace;letter-spacing:.18em;text-transform:uppercase;color:#FBBF24;background:rgba(251,191,36,.16);padding:6px 12px;border-radius:4px;margin:0 0 16px}
.sxa-cta-h2{margin:0 auto 12px !important;font:700 30px/1.22 'Plus Jakarta Sans',sans-serif !important;color:#fff !important;letter-spacing:-.012em;max-width:600px;text-align:center !important}
.sxa-cta-sub{margin:0 auto 26px !important;max-width:560px;font:500 15.5px/1.6 'Plus Jakarta Sans',sans-serif !important;color:rgba(255,255,255,.84) !important;text-align:center}
.sxa-cta-actions{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin:0 0 20px}
.sxa-cta-btn{display:inline-flex;align-items:center;gap:8px;padding:14px 24px;border-radius:8px;font:700 14.5px/1 'Plus Jakarta Sans',sans-serif;text-decoration:none;transition:all .15s}
.sxa-cta-btn--w{background:#fff;color:#0E3942}
.sxa-cta-btn--w:hover{background:#FBBF24;color:#0E3942;transform:translateY(-2px);box-shadow:0 10px 24px rgba(0,0,0,.2)}
.sxa-cta-btn--wa{background:#075E54;color:#fff}
.sxa-cta-btn--wa:hover{background:#054640;color:#fff;transform:translateY(-2px);box-shadow:0 10px 24px rgba(7,94,84,.4)}
.sxa-cta-btn--wa svg{width:18px;height:18px;fill:currentColor}
.sxa-cta-trust{display:flex;justify-content:center;flex-wrap:wrap;gap:18px;font:500 13px/1 'Plus Jakarta Sans',sans-serif;color:rgba(255,255,255,.7);margin:0}
.sxa-cta-trust span{white-space:nowrap}
.sxa-progress{position:fixed;top:0;left:0;right:0;height:3px;background:rgba(14,57,66,.06);z-index:100;pointer-events:none}
.sxa-progress-bar{height:100%;background:linear-gradient(90deg,#F59E0B,#0E3942);width:0;transition:width .1s}
@media (max-width:980px){
  body.single-post .page-content{grid-template-columns:1fr;padding:32px 20px;gap:0}
  body.single-post .page-content .sxa-toc{display:none}
  .sxa-h1{font-size:clamp(28px,7vw,36px)}
}
@media (max-width:600px){
  .sxa-hero{padding:48px 18px 40px}
  .sxa-cta-inner{padding:32px 22px}
  .sxa-cta-h2{font-size:24px !important}
  .sxa-cta-actions{flex-direction:column}
  .sxa-cta-btn{justify-content:center}
  .sxa-cta-trust{flex-direction:column;gap:8px;text-align:center}
}
</style>
<script id="sxa-js">
(function(){
function init(){
  if(!document.body.classList.contains('single-post'))return;
  var content=document.querySelector('.page-content')||document.querySelector('.entry-content');
  if(!content||content.dataset.sxa)return;
  content.dataset.sxa='1';
  var titleEl=document.querySelector('.entry-title');
  var title=titleEl?titleEl.textContent.trim():document.title;
  var dateEl=document.querySelector('.post-meta-date,.entry-date,.posted-on time,time.entry-date');
  var dateText=dateEl?dateEl.textContent.trim():'';
  // Remove theme legacy inline CTAs (text-matched, since classes vary)
  document.querySelectorAll('.wp-block-group,.wp-block-cover,.sx-post-cta,.sx-reveal').forEach(function(el){
    var t=el.textContent||'';
    if(/Butuh Solusi|Konsultasi(kan)? kebutuhan engineering/i.test(t) && el.children.length<6){
      el.classList.add('sxa-hide-theme');
    }
  });
  // Words + reading time
  var words=content.innerText.trim().split(/\s+/).length;
  var mins=Math.max(1,Math.round(words/220));
  // Build new hero band
  var hero=document.createElement('section');hero.className='sxa-hero';
  hero.innerHTML='<div class="sxa-hero-inner">'+
    '<nav class="sxa-bread" aria-label="Breadcrumb"><a href="/">Home</a><span class="sxa-sep">/</span><a href="/portfolio/">Portfolio</a><span class="sxa-sep">/</span><span class="sxa-cur">'+(title.length>60?title.slice(0,60)+'\u2026':title)+'</span></nav>'+
    '<h1 class="sxa-h1">'+title+'</h1>'+
    '<div class="sxa-meta">'+
      '<span class="sxa-pill amber">Renewable Energy</span>'+
      '<span class="sxa-pill teal">IoT Monitoring</span>'+
      (dateText?'<span class="sxa-pill">'+dateText+'</span>':'')+
      '<span class="sxa-pill">'+mins+' min read</span>'+
      '<span class="sxa-pill">'+words.toLocaleString()+' words</span>'+
    '</div>'+
  '</div>';
  // Insert hero before main wrapper (before .page-content's offsetParent)
  var anchor=content.parentNode;
  anchor.insertBefore(hero,content);
  // Build TOC (placed inside .page-content as grid col 2)
  var heads=content.querySelectorAll('h2,h3');
  if(heads.length>2){
    var toc=document.createElement('aside');toc.className='sxa-toc';toc.setAttribute('aria-label','Table of contents');
    var html='<div class="sxa-toc-title">On this page</div><ol>';
    heads.forEach(function(h,i){
      if(!h.id)h.id='sxa-h-'+i;
      var lvl=h.tagName==='H3'?'lvl-3':'lvl-2';
      html+='<li class="'+lvl+'"><a href="#'+h.id+'">'+h.textContent.trim()+'</a></li>';
    });
    html+='</ol>';toc.innerHTML=html;
    content.appendChild(toc);
    var links=toc.querySelectorAll('a');
    var obs=new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){links.forEach(function(l){l.classList.toggle('active',l.getAttribute('href')==='#'+e.target.id)});}
      });
    },{rootMargin:'-90px 0px -65% 0px'});
    heads.forEach(function(h){obs.observe(h)});
  }
  // Inline share row above CTA
  var url=encodeURIComponent(location.href);
  var t=encodeURIComponent(title);
  var share=document.createElement('div');share.className='sxa-share-inline';
  share.innerHTML='<span class="lab">Share</span>'+
    '<a href="https://api.whatsapp.com/send?text='+t+'%20'+url+'" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z"/></svg></a>'+
    '<a href="https://www.linkedin.com/sharing/share-offsite/?url='+url+'" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg></a>'+
    '<a href="https://twitter.com/intent/tweet?text='+t+'&url='+url+'" target="_blank" rel="noopener" aria-label="X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>'+
    '<button type="button" class="sxa-copy" aria-label="Copy link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg></button>';
  // Insert share inline at end of main column (before TOC + before any CTA)
  var lastP=content.querySelector('p:last-of-type, h2:last-of-type, h3:last-of-type, ul:last-of-type, ol:last-of-type, figure:last-of-type');
  // append share at content end, but before TOC
  var toc=content.querySelector('.sxa-toc');
  if(toc)content.insertBefore(share,toc);else content.appendChild(share);
  var cb=share.querySelector('.sxa-copy');
  if(cb){cb.onclick=function(){if(navigator.clipboard)navigator.clipboard.writeText(location.href);var o=cb.innerHTML;cb.innerHTML='\u2713';setTimeout(function(){cb.innerHTML=o},1400);};}
  // Build single bottom CTA outside .page-content (since grid layout)
  var cta=document.createElement('section');cta.className='sxa-cta-final';
  cta.innerHTML='<div class="sxa-cta-inner">'+
    '<span class="sxa-cta-eyebrow">Get Started</span>'+
    '<h2 class="sxa-cta-h2">Need a similar implementation?</h2>'+
    '<p class="sxa-cta-sub">Free initial consultation \u2014 share your scope, our engineering team in Batam responds within 24 hours.</p>'+
    '<div class="sxa-cta-actions">'+
      '<a class="sxa-cta-btn sxa-cta-btn--w" href="https://suriota.com/contact/">Free Consultation <span aria-hidden="true">\u2192</span></a>'+
      '<a class="sxa-cta-btn sxa-cta-btn--wa" href="https://wa.me/6285835672476" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z"/></svg>WhatsApp</a>'+
    '</div>'+
    '<p class="sxa-cta-trust"><span>\u2713 No obligation</span> <span>\u2713 Response within 24h</span> <span>\u2713 Batam-based engineering team</span></p>'+
  '</div>';
  content.parentNode.insertBefore(cta,content.nextSibling);
  // Progress bar
  var pb=document.createElement('div');pb.className='sxa-progress';pb.innerHTML='<div class="sxa-progress-bar"></div>';document.body.appendChild(pb);
  var pbar=pb.firstChild;
  window.addEventListener('scroll',function(){var h=document.documentElement,sc=h.scrollTop||document.body.scrollTop,total=h.scrollHeight-h.clientHeight;pbar.style.width=(total>0?sc/total*100:0)+'%';},{passive:true});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>
<!-- /wp:html -->
''' + MARKER_END + '\n\n'


def auth_header():
    token = base64.b64encode(f'{WP_USER}:{WP_PASS}'.encode()).decode()
    return {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'application/json',
    }


def fetch_post(post_id):
    req = urllib.request.Request(f'{SITE}/wp-json/wp/v2/posts/{post_id}?context=edit', headers=auth_header())
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def update_post(post_id, content_raw):
    data = json.dumps({'content': content_raw}).encode()
    req = urllib.request.Request(f'{SITE}/wp-json/wp/v2/posts/{post_id}', data=data, headers=auth_header(), method='POST')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def strip_redesign(raw):
    # remove v1 and v2 blocks if present
    for s, e in [(OLD_MARKER_START, OLD_MARKER_END), (MARKER_START, MARKER_END)]:
        pat = re.compile(re.escape(s) + r'.*?' + re.escape(e) + r'\s*', re.DOTALL)
        raw = pat.sub('', raw)
    return raw


def main():
    post_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1925
    mode = sys.argv[2] if len(sys.argv) > 2 else 'apply'
    post = fetch_post(post_id)
    raw = post['content']['raw']
    cleaned = strip_redesign(raw)
    if mode == 'remove':
        new_content = cleaned
        print(f'Removing redesign block from post {post_id}...')
    else:
        new_content = REDESIGN_BLOCK + cleaned
        print(f'Applying v2 redesign to post {post_id} ({len(raw)} -> {len(new_content)} chars)')
    res = update_post(post_id, new_content)
    print(f'OK. Modified: {res.get("modified")}')


if __name__ == '__main__':
    main()
