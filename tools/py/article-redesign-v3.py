"""Article redesign v3 — compact layout, no share-inline, back-to-top button.

Changes vs v2:
- Wider boxed body 1180px (matches service pages)
- Remove .sxa-share-inline row (user said: Bagikan dekat CTA hapus)
- Add .sxa-back-top floating button (bottom-right)
- Better horizontal space utilization
- Keep theme hide rules (page-header, comments, theme mid CTAs)
"""
import json, base64, urllib.request, urllib.error, sys, re

WP_USER='admin'
WP_PASS='hCYK JqF1 khdB WDzI LQdQ WEBr'
SITE='https://suriota.com'

MARKER_START='<!-- SURIOTA_REDESIGN_v3_START -->'
MARKER_END='<!-- SURIOTA_REDESIGN_v3_END -->'
OLD_MARKERS=[
  ('<!-- SURIOTA_REDESIGN_v1_START -->','<!-- SURIOTA_REDESIGN_v1_END -->'),
  ('<!-- SURIOTA_REDESIGN_v2_START -->','<!-- SURIOTA_REDESIGN_v2_END -->'),
]

REDESIGN_BLOCK = MARKER_START + '\n<!-- wp:html -->\n' + r'''<style id="sxa-css">@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
.single-post{--sxa-ink:#0F1A1F;--sxa-mute:#5B6F75;--sxa-line:#E8ECEE;--sxa-amber:#F59E0B;--sxa-accent:#0E3942;--sxa-accent-2:#22D3A4;--sxa-surface:#FAFBFC;background:var(--sxa-surface)}
body.single-post .page-header{display:none !important}
body.single-post #comments,body.single-post #respond,body.single-post .comments-area,body.single-post .post-comments,body.single-post .post-tags,body.single-post .tag-links,body.single-post .sx-post-cta,body.single-post .sx-toc:not(.sxa-toc),body.single-post .sx-share-bar,body.single-post .sx-share-label,body.single-post .share-buttons,body.single-post .post-share,body.single-post .social-share{display:none !important}
body.single-post .sxa-hide-theme{display:none !important}
.sxa-hero{background:linear-gradient(135deg,#17505D 0%,#0C2F38 100%);padding:64px 24px 56px;text-align:center;animation:sxaFadeIn .6s ease-out;position:relative;overflow:hidden}
.sxa-hero::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#F59E0B 0%,#22D3A4 50%,#0EA5E9 100%)}
.sxa-hero-inner{max-width:980px;margin:0 auto}
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
body.single-post .page-content{font-family:'Plus Jakarta Sans',system-ui,sans-serif !important;color:var(--sxa-ink);max-width:1180px;margin:0 auto;padding:48px 32px 24px;font-size:17px;line-height:1.78;display:flex;flex-direction:row;gap:64px;align-items:flex-start}
body.single-post .page-content .sxa-main{flex:1 1 auto;min-width:0}
body.single-post .page-content .sxa-toc{flex:0 0 280px;position:sticky;top:100px;align-self:flex-start;max-height:calc(100vh - 130px);overflow:auto}
body.single-post .sxa-main p{margin:0 0 22px;font-weight:400;color:#1F2D33}
body.single-post .sxa-main h2{font:700 30px/1.22 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent) !important;letter-spacing:-.01em;margin:48px 0 16px !important;scroll-margin-top:90px;padding-left:14px;border-left:4px solid var(--sxa-amber);text-align:left}
body.single-post .sxa-main h3{font:700 22px/1.3 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent) !important;margin:32px 0 12px !important;scroll-margin-top:90px;text-align:left}
body.single-post .sxa-main figure,body.single-post .sxa-main .wp-block-image{margin:32px 0}
body.single-post .sxa-main img{border-radius:12px;box-shadow:0 8px 32px rgba(14,57,66,.10);max-width:100%;height:auto;display:block;margin:0 auto}
body.single-post .sxa-main figcaption{font:500 13px/1.5 'IBM Plex Mono',monospace !important;color:var(--sxa-mute) !important;text-align:center;margin-top:10px}
body.single-post .sxa-main blockquote{border:none;border-left:4px solid var(--sxa-amber);background:#fff;padding:18px 22px;margin:32px 0;border-radius:0 8px 8px 0;font:500 18px/1.65 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent);box-shadow:0 4px 18px rgba(14,57,66,.05)}
body.single-post .sxa-main ul,body.single-post .sxa-main ol{padding-left:24px;margin:0 0 22px}
body.single-post .sxa-main li{margin-bottom:8px;line-height:1.7}
body.single-post .sxa-main ul li::marker{color:var(--sxa-amber)}
body.single-post .sxa-main ol li::marker{color:var(--sxa-amber);font-family:'IBM Plex Mono',monospace;font-weight:600}
body.single-post .sxa-main a{color:var(--sxa-accent);text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--sxa-amber);transition:color .15s}
body.single-post .sxa-main a:hover{color:var(--sxa-amber)}
body.single-post .sxa-main strong{color:var(--sxa-accent);font-weight:700}
body.single-post .sxa-main > p:first-of-type::first-letter{font:800 68px/.85 'Plus Jakarta Sans',sans-serif;color:var(--sxa-amber);float:left;margin:6px 14px 0 0}
.sxa-toc{background:#fff;border:1px solid var(--sxa-line);border-radius:12px;padding:20px 18px;box-shadow:0 4px 18px rgba(14,57,66,.04)}
.sxa-toc-title{font:700 11px/1 'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--sxa-accent);margin:0 0 14px;display:flex;align-items:center;gap:8px}
.sxa-toc-title::before{content:"";width:14px;height:2px;background:var(--sxa-amber)}
.sxa-toc ol{list-style:none;padding:0;margin:0;font-size:13px}
.sxa-toc li{margin:0 0 4px}
.sxa-toc a{display:block;padding:6px 0 6px 18px;color:var(--sxa-mute);text-decoration:none;border-left:2px solid transparent;line-height:1.4;transition:all .15s;font-weight:500}
.sxa-toc a:hover{color:var(--sxa-accent)}
.sxa-toc a.active{color:var(--sxa-accent);border-left-color:var(--sxa-amber);font-weight:600;background:rgba(245,158,11,.05)}
.sxa-toc li.lvl-3 a{padding-left:32px;font-size:12px;color:#7A8B91}
.sxa-cta-final{max-width:980px;margin:24px auto 64px;padding:0 32px}
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
.sxa-cta-btn--wa svg{fill:currentColor}
.sxa-cta-trust{display:flex;justify-content:center;flex-wrap:wrap;gap:18px;font:500 13px/1 'Plus Jakarta Sans',sans-serif;color:rgba(255,255,255,.7);margin:0}
.sxa-cta-trust span{white-space:nowrap}
.sxa-back-top{position:fixed;right:24px;bottom:24px;width:46px;height:46px;border-radius:50%;background:#0E3942;color:#fff;display:flex;align-items:center;justify-content:center;text-decoration:none;box-shadow:0 8px 24px rgba(14,57,66,.24);opacity:0;visibility:hidden;transform:translateY(8px);transition:all .2s;z-index:99;border:none;cursor:pointer;padding:0}
.sxa-back-top.show{opacity:1;visibility:visible;transform:translateY(0)}
.sxa-back-top:hover{background:#F59E0B;transform:translateY(-4px);box-shadow:0 12px 28px rgba(245,158,11,.32);color:#fff}
.sxa-back-top svg{width:20px;height:20px}
.sxa-progress{position:fixed;top:0;left:0;right:0;height:3px;background:rgba(14,57,66,.06);z-index:100;pointer-events:none}
.sxa-progress-bar{height:100%;background:linear-gradient(90deg,#F59E0B,#0E3942);width:0;transition:width .1s}
@media (max-width:1024px){
  body.single-post .page-content{flex-direction:column;padding:32px 24px;gap:0;max-width:840px}
  body.single-post .page-content .sxa-toc{display:none}
  .sxa-h1{font-size:clamp(28px,7vw,38px)}
}
@media (max-width:600px){
  .sxa-hero{padding:48px 18px 40px}
  .sxa-cta-final{padding:0 18px}
  .sxa-cta-inner{padding:32px 22px}
  .sxa-cta-h2{font-size:24px !important}
  .sxa-cta-actions{flex-direction:column}
  .sxa-cta-btn{justify-content:center}
  .sxa-cta-trust{flex-direction:column;gap:8px;text-align:center}
  .sxa-back-top{right:16px;bottom:16px;width:42px;height:42px}
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
  document.querySelectorAll('.wp-block-group,.wp-block-cover,.sx-post-cta,.sx-reveal').forEach(function(el){
    var t=el.textContent||'';
    if(/Butuh Solusi|Konsultasi(kan)? kebutuhan engineering/i.test(t) && el.children.length<6){
      el.classList.add('sxa-hide-theme');
    }
  });
  var words=content.innerText.trim().split(/\s+/).length;
  var mins=Math.max(1,Math.round(words/220));
  var hero=document.createElement('section');hero.className='sxa-hero';
  hero.innerHTML='<div class="sxa-hero-inner">'+
    '<nav class="sxa-bread" aria-label="Breadcrumb"><a href="/">Home</a><span class="sxa-sep">/</span><a href="/portfolio/">Portfolio</a><span class="sxa-sep">/</span><span class="sxa-cur">'+(title.length>60?title.slice(0,60)+'\u2026':title)+'</span></nav>'+
    '<h1 class="sxa-h1">'+title+'</h1>'+
    '<div class="sxa-meta">'+
      '<span class="sxa-pill amber">Portfolio</span>'+
      '<span class="sxa-pill teal">SURIOTA Project</span>'+
      (dateText?'<span class="sxa-pill">'+dateText+'</span>':'')+
      '<span class="sxa-pill">'+mins+' min read</span>'+
      '<span class="sxa-pill">'+words.toLocaleString()+' words</span>'+
    '</div>'+
  '</div>';
  content.parentNode.insertBefore(hero,content);
  // Wrap existing content in .sxa-main so we can flex it side-by-side with TOC
  var main=document.createElement('div');main.className='sxa-main';
  while(content.firstChild)main.appendChild(content.firstChild);
  content.appendChild(main);
  var heads=main.querySelectorAll('h2,h3');
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
  var cta=document.createElement('section');cta.className='sxa-cta-final';
  cta.innerHTML='<div class="sxa-cta-inner">'+
    '<span class="sxa-cta-eyebrow">Get Started</span>'+
    '<h2 class="sxa-cta-h2">Need a similar implementation?</h2>'+
    '<p class="sxa-cta-sub">Free initial consultation \u2014 share your scope, our engineering team in Batam responds within 24 hours.</p>'+
    '<div class="sxa-cta-actions">'+
      '<a class="sxa-cta-btn sxa-cta-btn--w" href="https://suriota.com/contact/">Free Consultation <span aria-hidden="true">\u2192</span></a>'+
      '<a class="sxa-cta-btn sxa-cta-btn--wa" href="https://wa.me/6285835672476" target="_blank" rel="noopener"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z"/></svg>WhatsApp</a>'+
    '</div>'+
    '<p class="sxa-cta-trust"><span>\u2713 No obligation</span> <span>\u2713 Response within 24h</span> <span>\u2713 Batam-based engineering team</span></p>'+
  '</div>';
  content.parentNode.insertBefore(cta,content.nextSibling);
  var bt=document.createElement('button');bt.type='button';bt.className='sxa-back-top';bt.setAttribute('aria-label','Back to top');
  bt.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"></polyline></svg>';
  bt.onclick=function(){window.scrollTo({top:0,behavior:'smooth'});};
  document.body.appendChild(bt);
  var pb=document.createElement('div');pb.className='sxa-progress';pb.innerHTML='<div class="sxa-progress-bar"></div>';document.body.appendChild(pb);
  var pbar=pb.firstChild;
  window.addEventListener('scroll',function(){
    var h=document.documentElement,sc=h.scrollTop||document.body.scrollTop,total=h.scrollHeight-h.clientHeight;
    pbar.style.width=(total>0?sc/total*100:0)+'%';
    bt.classList.toggle('show',sc>600);
  },{passive:true});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>
<!-- /wp:html -->
''' + MARKER_END + '\n\n'


def auth_header():
    t=base64.b64encode(f'{WP_USER}:{WP_PASS}'.encode()).decode()
    return {'Authorization':f'Basic {t}','Content-Type':'application/json','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','Accept':'application/json'}


def fetch_post(post_id):
    req=urllib.request.Request(f'{SITE}/wp-json/wp/v2/posts/{post_id}?context=edit', headers=auth_header())
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read())


def update_post(post_id, content_raw):
    data=json.dumps({'content': content_raw}).encode()
    req=urllib.request.Request(f'{SITE}/wp-json/wp/v2/posts/{post_id}', data=data, headers=auth_header(), method='POST')
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read())


def strip_redesign(raw):
    for s,e in OLD_MARKERS+[(MARKER_START,MARKER_END)]:
        pat=re.compile(re.escape(s)+r'.*?'+re.escape(e)+r'\s*',re.DOTALL)
        raw=pat.sub('',raw)
    return raw


def main():
    post_id = int(sys.argv[1]) if len(sys.argv)>1 else 1925
    mode = sys.argv[2] if len(sys.argv)>2 else 'apply'
    post=fetch_post(post_id)
    raw=post['content']['raw']
    cleaned=strip_redesign(raw)
    if mode=='remove':
        new=cleaned
        print(f'Removing v3 redesign from post {post_id}...')
    else:
        new=REDESIGN_BLOCK+cleaned
        print(f'Applying v3 redesign to post {post_id} ({len(raw)} -> {len(new)})')
    res=update_post(post_id,new)
    print(f'OK. Modified: {res.get("modified")}')


if __name__=='__main__':
    main()
