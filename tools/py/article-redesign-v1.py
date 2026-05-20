"""Article redesign v1 injector.

Prepends a non-content <style>+<script> block (wrapped in marker comments) to a post's content via WP REST API. Original text + images untouched. Safe to remove by stripping between markers.
"""
import json, base64, urllib.request, urllib.error, sys, os, re

WP_USER = 'admin'
WP_PASS = 'hCYK JqF1 khdB WDzI LQdQ WEBr'
SITE    = 'https://suriota.com'

MARKER_START = '<!-- SURIOTA_REDESIGN_v1_START -->'
MARKER_END   = '<!-- SURIOTA_REDESIGN_v1_END -->'

REDESIGN_BLOCK = MARKER_START + '\n<!-- wp:html -->\n' + r'''<style id="sx-art-css">@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
.single-post{--sxa-ink:#0F1A1F;--sxa-mute:#5B6F75;--sxa-line:#E8ECEE;--sxa-amber:#F59E0B;--sxa-accent:#0E3942;--sxa-surface:#FAFBFC;background:var(--sxa-surface)}
.single-post .page-header{max-width:840px;margin:0 auto;padding:48px 20px 0;text-align:left}
.single-post .entry-title{font:800 clamp(30px,4vw,46px)/1.12 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent) !important;letter-spacing:-.02em !important;margin:14px 0 8px !important;text-align:left}
.single-post .page-content{font-family:'Plus Jakarta Sans',system-ui,sans-serif !important;color:var(--sxa-ink);max-width:780px;margin:0 auto;padding:24px 20px 32px;font-size:17px;line-height:1.78}
.single-post .page-content p{margin:0 0 22px;font-weight:400;color:#1F2D33}
.single-post .page-content h2{font:700 28px/1.25 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent) !important;letter-spacing:-.01em;margin:54px 0 16px !important;scroll-margin-top:90px;padding-left:14px;border-left:4px solid var(--sxa-amber);text-align:left}
.single-post .page-content h3{font:700 21px/1.3 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent) !important;margin:36px 0 12px !important;scroll-margin-top:90px;text-align:left}
.single-post .page-content img,.single-post .page-content figure img,.single-post .page-content .wp-block-image img{border-radius:12px;box-shadow:0 8px 32px rgba(14,57,66,.10);max-width:100%;height:auto;display:block;margin:24px auto}
.single-post .page-content figure,.single-post .page-content .wp-block-image{margin:32px 0;text-align:center}
.single-post .page-content figcaption{font:500 13px/1.5 'IBM Plex Mono',monospace !important;color:var(--sxa-mute) !important;text-align:center;margin-top:10px}
.single-post .page-content blockquote{border:none;border-left:4px solid var(--sxa-amber);background:#FFFFFF;padding:18px 22px;margin:32px 0;border-radius:0 8px 8px 0;font:500 18px/1.65 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent);box-shadow:0 4px 18px rgba(14,57,66,.05)}
.single-post .page-content ul,.single-post .page-content ol{padding-left:24px;margin:0 0 22px}
.single-post .page-content li{margin-bottom:8px;line-height:1.7}
.single-post .page-content ul li::marker{color:var(--sxa-amber)}
.single-post .page-content ol li::marker{color:var(--sxa-amber);font-family:'IBM Plex Mono',monospace;font-weight:600}
.single-post .page-content a{color:var(--sxa-accent);text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--sxa-amber);transition:color .15s}
.single-post .page-content a:hover{color:var(--sxa-amber)}
.single-post .page-content strong,.single-post .page-content b{color:var(--sxa-accent);font-weight:700}
.single-post .page-content em,.single-post .page-content i{color:#1F2D33}
.single-post .page-content > p:first-of-type::first-letter{font:800 60px/.85 'Plus Jakarta Sans',sans-serif;color:var(--sxa-amber);float:left;margin:8px 12px 0 0}
.sxa-bar{max-width:840px;margin:18px auto 0;padding:0 20px;font:500 13px/1 'IBM Plex Mono',monospace;display:flex;gap:10px;align-items:center;flex-wrap:wrap;color:var(--sx-mute)}
.sxa-bar a{color:var(--sx-mute);text-decoration:none;transition:color .15s}
.sxa-bar a:hover{color:var(--sx-accent)}
.sxa-bar .sx-sep{color:#C6D0D3}
.sxa-bar .sx-cur{color:var(--sx-accent);font-weight:600}
.sxa-meta{display:flex;gap:8px;flex-wrap:wrap;margin:14px auto 0;max-width:840px;padding:0 20px}
.sxa-pill{display:inline-flex;align-items:center;gap:6px;padding:5px 12px;background:rgba(14,57,66,.06);color:var(--sx-accent);font:600 11px/1 'IBM Plex Mono',monospace;letter-spacing:.1em;text-transform:uppercase;border-radius:999px}
.sxa-pill.amber{background:rgba(245,158,11,.16);color:#92400E}
.sxa-pill.teal{background:rgba(8,145,178,.14);color:#075985}
.sxa-toc{position:fixed;right:24px;top:130px;width:240px;max-height:calc(100vh - 170px);overflow:auto;background:#FFFFFF;border:1px solid var(--sx-line);border-radius:12px;padding:18px 16px;box-shadow:0 8px 32px rgba(14,57,66,.06);z-index:20}
.sxa-toc-title{font:700 11px/1 'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--sx-accent);margin:0 0 14px;display:flex;align-items:center;gap:8px}
.sxa-toc-title::before{content:"";width:14px;height:2px;background:var(--sx-amber)}
.sxa-toc ol{list-style:none;padding:0;margin:0;font-size:13px}
.sxa-toc li{margin:0 0 4px}
.sxa-toc a{display:block;padding:5px 0 5px 18px;color:var(--sx-mute);text-decoration:none;border-left:2px solid transparent;line-height:1.4;transition:all .15s;font-weight:500}
.sxa-toc a:hover{color:var(--sx-accent)}
.sxa-toc a.active{color:var(--sx-accent);border-left-color:var(--sx-amber);font-weight:600;background:rgba(245,158,11,.05)}
.sxa-toc li.lvl-3 a{padding-left:32px;font-size:12px;color:#7A8B91}
@media (max-width:1300px){.sxa-toc{display:none}}
.sxa-share{position:fixed;left:24px;top:200px;display:flex;flex-direction:column;gap:8px;z-index:20}
.sxa-share a,.sxa-share button{width:38px;height:38px;border-radius:50%;background:#FFFFFF;border:1px solid var(--sx-line);display:inline-flex;align-items:center;justify-content:center;color:var(--sx-accent);text-decoration:none;transition:all .15s;cursor:pointer;padding:0}
.sxa-share a:hover,.sxa-share button:hover{background:var(--sx-accent);color:#FFFFFF;border-color:var(--sx-accent);transform:translateY(-2px)}
.sxa-share svg{width:16px;height:16px}
@media (max-width:1300px){.sxa-share{display:none}}
.sxa-end-cta{max-width:780px;margin:48px auto 24px;padding:34px 32px;background:linear-gradient(135deg,#0E3942 0%,#205B69 100%);border-radius:14px;color:#FFFFFF;text-align:center;position:relative;overflow:hidden;box-shadow:0 16px 40px rgba(14,57,66,.18)}
.sxa-end-cta::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#F59E0B 0%,#22D3A4 50%,#0EA5E9 100%)}
.sxa-end-cta-eyebrow{display:inline-block;font:600 11px/1 'IBM Plex Mono',monospace;letter-spacing:.18em;text-transform:uppercase;color:#FBBF24;background:rgba(251,191,36,.16);padding:5px 12px;border-radius:4px;margin:0 0 14px}
.sxa-end-cta h3{font:700 24px/1.25 'Plus Jakarta Sans',sans-serif !important;color:#FFFFFF !important;margin:0 0 10px !important;letter-spacing:-.01em;text-align:center !important}
.sxa-end-cta p{font:500 15px/1.6 'Plus Jakarta Sans',sans-serif !important;color:rgba(255,255,255,.85) !important;margin:0 auto 22px !important;max-width:520px}
.sxa-end-cta .sx-btns{display:flex;justify-content:center;gap:12px;flex-wrap:wrap}
.sxa-end-cta a{display:inline-flex;align-items:center;gap:8px;padding:13px 24px;border-radius:8px;font:700 14px/1 'Plus Jakarta Sans',sans-serif;text-decoration:none;transition:all .15s}
.sxa-end-cta .sx-btn-w{background:#FFFFFF;color:#0E3942}
.sxa-end-cta .sx-btn-w:hover{background:#FBBF24;transform:translateY(-1px)}
.sxa-end-cta .sx-btn-wa{background:#075E54;color:#FFFFFF}
.sxa-end-cta .sx-btn-wa:hover{background:#054640;transform:translateY(-1px)}
@media (max-width:600px){.sxa-end-cta{padding:24px 20px}.sxa-end-cta h3{font-size:20px !important}.sxa-end-cta .sx-btns{flex-direction:column}.sxa-end-cta a{justify-content:center}}
.sxa-progress{position:fixed;top:0;left:0;right:0;height:3px;background:rgba(14,57,66,.08);z-index:100;pointer-events:none}
.sxa-progress-bar{height:100%;background:linear-gradient(90deg,#F59E0B,#0E3942);width:0;transition:width .1s}
</style>
<script id="sx-art-js">
(function(){
function init(){
  if(!document.body.classList.contains('single-post'))return;
  var content=document.querySelector('.page-content')||document.querySelector('.entry-content');
  if(!content||content.dataset.sxr)return;
  content.dataset.sxr='1';
  var pb=document.createElement('div');pb.className='sxa-progress';pb.innerHTML='<div class="sxa-progress-bar"></div>';document.body.appendChild(pb);
  var pbar=pb.firstChild;
  var titleEl=document.querySelector('.entry-title');
  var title=titleEl?titleEl.textContent.trim():document.title;
  var words=content.innerText.trim().split(/\s+/).length;
  var mins=Math.max(1,Math.round(words/220));
  var bar=document.createElement('nav');bar.className='sxa-bar';bar.setAttribute('aria-label','Breadcrumb');
  bar.innerHTML='<a href="/">Home</a><span class="sx-sep">/</span><a href="/portfolio/">Portfolio</a><span class="sx-sep">/</span><span class="sx-cur">'+(title.length>60?title.slice(0,60)+'…':title)+'</span>';
  var meta=document.createElement('div');meta.className='sxa-meta';
  meta.innerHTML='<span class="sxa-pill amber">Renewable Energy</span><span class="sxa-pill teal">IoT Monitoring</span><span class="sxa-pill">'+mins+' MIN READ</span><span class="sxa-pill">'+words+' WORDS</span>';
  var anchor=titleEl?titleEl.closest('.page-header')||titleEl.closest('.entry-header')||titleEl:content;
  anchor.parentNode.insertBefore(bar,anchor);
  anchor.parentNode.insertBefore(meta,anchor.nextSibling);
  var heads=content.querySelectorAll('h2,h3');
  if(heads.length>2){
    var toc=document.createElement('aside');toc.className='sxa-toc';toc.setAttribute('aria-label','Table of contents');
    var html='<div class="sxa-toc-title">On this page</div><ol>';
    heads.forEach(function(h,i){
      if(!h.id)h.id='sx-h-'+i;
      var lvl=h.tagName==='H3'?'lvl-3':'lvl-2';
      html+='<li class="'+lvl+'"><a href="#'+h.id+'">'+h.textContent.trim()+'</a></li>';
    });
    html+='</ol>';toc.innerHTML=html;
    document.body.appendChild(toc);
    var links=toc.querySelectorAll('a');
    var obs=new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){links.forEach(function(l){l.classList.toggle('active',l.getAttribute('href')==='#'+e.target.id)});}
      });
    },{rootMargin:'-80px 0px -70% 0px'});
    heads.forEach(function(h){obs.observe(h)});
  }
  var url=encodeURIComponent(location.href);
  var t=encodeURIComponent(title);
  var share=document.createElement('aside');share.className='sxa-share';share.setAttribute('aria-label','Share');
  share.innerHTML='<a href="https://api.whatsapp.com/send?text='+t+'%20'+url+'" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z"/></svg></a><a href="https://www.linkedin.com/sharing/share-offsite/?url='+url+'" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg></a><a href="https://twitter.com/intent/tweet?text='+t+'&url='+url+'" target="_blank" rel="noopener" aria-label="X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a><button type="button" class="sx-copy" aria-label="Copy link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg></button>';
  document.body.appendChild(share);
  var cb=share.querySelector('.sx-copy');
  if(cb){cb.onclick=function(){if(navigator.clipboard)navigator.clipboard.writeText(location.href);var o=cb.innerHTML;cb.innerHTML='\u2713';setTimeout(function(){cb.innerHTML=o},1400);};}
  var cta=document.createElement('section');cta.className='sxa-end-cta';
  cta.innerHTML='<span class="sxa-end-cta-eyebrow">Get Started</span><h3>Need a similar implementation?</h3><p>Free initial consultation \u2014 share your scope, our engineering team in Batam responds within 24 hours.</p><div class="sx-btns"><a class="sx-btn-w" href="https://suriota.com/contact/">Free Consultation \u2192</a><a class="sx-btn-wa" href="https://wa.me/6285835672476" target="_blank" rel="noopener">WhatsApp</a></div>';
  content.appendChild(cta);
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


def strip_existing(raw):
    pattern = re.compile(re.escape(MARKER_START) + r'.*?' + re.escape(MARKER_END) + r'\s*', re.DOTALL)
    return pattern.sub('', raw)


def main():
    post_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1925
    mode = sys.argv[2] if len(sys.argv) > 2 else 'apply'
    post = fetch_post(post_id)
    raw = post['content']['raw']
    cleaned = strip_existing(raw)
    if mode == 'remove':
        new_content = cleaned
        print(f'Removing redesign block from post {post_id}...')
    else:
        new_content = REDESIGN_BLOCK + cleaned
        print(f'Applying redesign block to post {post_id} (was {len(raw)} chars, now {len(new_content)})...')
    res = update_post(post_id, new_content)
    print(f'OK. New revision: {res.get("modified")}')


if __name__ == '__main__':
    main()
