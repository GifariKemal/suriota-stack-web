"""Build Elementor Theme Builder Single-Post template 5062.

Writes _elementor_data + _elementor_page_settings + _elementor_conditions via
WP REST API directly (MCP import-template did not persist for this template id).

Structure:
- Hero container (full-width, dark teal gradient)
  - Breadcrumb HTML
  - theme-post-title widget (dynamic H1)
  - Meta pills HTML
- Body container (boxed 1180px, row, gap 56)
  - Main sub-container (flex-grow 1) — theme-post-content
  - Side sub-container (280px) — table-of-contents widget
- CTA container (boxed 960px)
  - sx-cta-final HTML
- Back-to-top floating HTML

Plus page-level Custom CSS that:
- Hides theme's default hero (.page-header), comments, tags
- Styles post-content typography
- Layout grid responsiveness
- back-to-top + progress bar visuals + animation
"""
import json, base64, urllib.request, urllib.error, sys

WP_USER='admin'
WP_PASS='hCYK JqF1 khdB WDzI LQdQ WEBr'
SITE='https://suriota.com'
TEMPLATE_ID=5062

def auth():
    t=base64.b64encode(f'{WP_USER}:{WP_PASS}'.encode()).decode()
    return {'Authorization':f'Basic {t}','User-Agent':'Mozilla/5.0','Content-Type':'application/json','Accept':'application/json'}

# ---------- HTML widgets content ----------

HERO_BREAD = '<nav class="sxa-bread" aria-label="Breadcrumb"><a href="https://suriota.com/">Home</a><span class="sxa-sep">/</span><a href="https://suriota.com/portfolio/">Portfolio</a><span class="sxa-sep">/</span><span class="sxa-cur" id="sxa-bread-current">Article</span></nav>'

HERO_META = '<div class="sxa-meta" id="sxa-meta-row"><span class="sxa-pill amber">Portfolio</span><span class="sxa-pill teal">SURIOTA Project</span><span class="sxa-pill" id="sxa-meta-read">— min read</span><span class="sxa-pill" id="sxa-meta-words">— words</span></div>'

CTA_WA_PATH = "M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z"

CTA_HTML = f'''<section class="sxa-cta-final"><div class="sxa-cta-inner"><span class="sxa-cta-eyebrow">Get Started</span><h2 class="sxa-cta-h2">Need a similar implementation?</h2><p class="sxa-cta-sub">Free initial consultation — share your scope, our engineering team in Batam responds within 24 hours.</p><div class="sxa-cta-actions"><a class="sxa-cta-btn sxa-cta-btn--w" href="https://suriota.com/contact/">Free Consultation <span aria-hidden="true">→</span></a><a class="sxa-cta-btn sxa-cta-btn--wa" href="https://wa.me/6285835672476" target="_blank" rel="noopener" aria-label="WhatsApp"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{CTA_WA_PATH}"/></svg>WhatsApp</a></div><p class="sxa-cta-trust"><span>✓ No obligation</span><span>✓ Response within 24h</span><span>✓ Batam-based engineering team</span></p></div></section><a href="#" class="sxa-back-top" id="sxa-back-top" aria-label="Back to top"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"></polyline></svg></a><script>(function(){{
  function init(){{
    if(!document.body.classList.contains("single-post"))return;
    var content=document.querySelector(".elementor-widget-theme-post-content .elementor-widget-container")||document.querySelector(".page-content");
    if(!content)return;
    var t=document.querySelector(".sxa-h1 .elementor-heading-title")||document.querySelector(".entry-title");
    var title=t?t.textContent.trim():document.title;
    var cur=document.getElementById("sxa-bread-current");if(cur)cur.textContent=title.length>60?title.slice(0,60)+"…":title;
    var words=content.innerText.trim().split(/\\s+/).length;
    var mins=Math.max(1,Math.round(words/220));
    var r=document.getElementById("sxa-meta-read");if(r)r.textContent=mins+" min read";
    var w=document.getElementById("sxa-meta-words");if(w)w.textContent=words.toLocaleString()+" words";
    // back-to-top show on scroll
    var bt=document.getElementById("sxa-back-top");
    if(bt){{bt.addEventListener("click",function(e){{e.preventDefault();window.scrollTo({{top:0,behavior:"smooth"}});}});
    window.addEventListener("scroll",function(){{bt.classList.toggle("show",window.scrollY>600);}},{{passive:true}});}}
    // Progress bar
    var pb=document.createElement("div");pb.className="sxa-progress";pb.innerHTML='<div class="sxa-progress-bar"></div>';document.body.appendChild(pb);
    var pbar=pb.firstChild;
    window.addEventListener("scroll",function(){{var h=document.documentElement,sc=h.scrollTop||document.body.scrollTop,total=h.scrollHeight-h.clientHeight;pbar.style.width=(total>0?sc/total*100:0)+"%";}},{{passive:true}});
  }}
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
}})();</script>'''

# ---------- Elementor data structure ----------
ED = [
  {
    "id": "sxahero1", "elType": "container", "isInner": False,
    "settings": {
      "content_width": "full", "flex_direction": "column", "align_items": "center",
      "padding": {"unit": "px", "top": "64", "right": "24", "bottom": "56", "left": "24", "isLinked": False},
      "background_background": "gradient",
      "background_color": "#17505D",
      "background_color_b": "#0C2F38",
      "background_gradient_angle": {"unit": "deg", "size": 135},
      "gap": {"column": "18", "row": "18", "unit": "px", "isLinked": True}
    },
    "elements": [
      {"id": "sxabread1", "elType": "widget", "widgetType": "html", "settings": {"html": HERO_BREAD}},
      {"id": "sxatit1", "elType": "widget", "widgetType": "theme-post-title", "settings": {"header_size": "h1", "align": "center", "_element_id": "sxa-h1"}},
      {"id": "sxameta1", "elType": "widget", "widgetType": "html", "settings": {"html": HERO_META}}
    ]
  },
  {
    "id": "sxabody1", "elType": "container", "isInner": False,
    "settings": {
      "content_width": "boxed",
      "boxed_width": {"unit": "px", "size": 1180},
      "flex_direction": "row",
      "flex_wrap": "nowrap",
      "align_items": "flex-start",
      "gap": {"column": "56", "row": "56", "unit": "px", "isLinked": True},
      "padding": {"unit": "px", "top": "48", "right": "24", "bottom": "32", "left": "24", "isLinked": False},
      "_element_id": "sxa-body"
    },
    "elements": [
      {
        "id": "sxamain1", "elType": "container", "isInner": True,
        "settings": {
          "content_width": "full",
          "_element_id": "sxa-main",
          "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
        },
        "elements": [
          {"id": "sxapc1", "elType": "widget", "widgetType": "theme-post-content", "settings": {"_element_id": "sxa-post-content"}}
        ]
      },
      {
        "id": "sxaside1", "elType": "container", "isInner": True,
        "settings": {
          "content_width": "full",
          "width": {"unit": "px", "size": 280},
          "flex_grow": 0,
          "flex_shrink": 0,
          "_element_id": "sxa-side",
          "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
        },
        "elements": [
          {
            "id": "sxatoc1", "elType": "widget", "widgetType": "table-of-contents",
            "settings": {
              "title": "On this page",
              "headings_by_tags": ["h2", "h3"],
              "marker_view": "numbers",
              "hierarchical_view": "yes",
              "_element_id": "sxa-toc-w"
            }
          }
        ]
      }
    ]
  },
  {
    "id": "sxactawrap1", "elType": "container", "isInner": False,
    "settings": {
      "content_width": "boxed",
      "boxed_width": {"unit": "px", "size": 960},
      "padding": {"unit": "px", "top": "0", "right": "24", "bottom": "64", "left": "24", "isLinked": False},
      "_element_id": "sxa-cta-wrap"
    },
    "elements": [
      {"id": "sxactahtml1", "elType": "widget", "widgetType": "html", "settings": {"html": CTA_HTML}}
    ]
  }
]

# ---------- Page-level Custom CSS ----------
CUSTOM_CSS = '''@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
:root{--sxa-ink:#0F1A1F;--sxa-mute:#5B6F75;--sxa-line:#E8ECEE;--sxa-amber:#F59E0B;--sxa-accent:#0E3942;--sxa-surface:#FAFBFC}
body.single-post{background:var(--sxa-surface)}
body.single-post .page-header,body.single-post #comments,body.single-post #respond,body.single-post .comments-area,body.single-post .post-tags,body.single-post .tag-links,body.single-post .sx-post-cta,body.single-post .sx-toc:not(.sxa-toc-w):not(.elementor-widget-table-of-contents){display:none !important}
.sxa-bread{display:flex;justify-content:center;gap:8px;align-items:center;flex-wrap:wrap;margin:0;font:500 12.5px/1 'IBM Plex Mono',monospace;color:rgba(255,255,255,.55)}
.sxa-bread a{color:rgba(255,255,255,.65);text-decoration:none;transition:color .15s}
.sxa-bread a:hover{color:#fff}
.sxa-bread .sxa-sep{color:rgba(255,255,255,.28)}
.sxa-bread .sxa-cur{color:#fff;font-weight:600}
.elementor-element-sxa-h1 .elementor-heading-title{font:800 clamp(30px,4.4vw,52px)/1.1 'Plus Jakarta Sans',sans-serif !important;color:#fff !important;letter-spacing:-.02em !important;margin:0 !important;text-align:center;max-width:920px}
.sxa-meta{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin:0}
.sxa-pill{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;background:rgba(255,255,255,.10);color:#fff;font:600 11px/1 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;border-radius:999px;border:1px solid rgba(255,255,255,.16)}
.sxa-pill.amber{background:rgba(245,158,11,.18);color:#FBBF24;border-color:rgba(251,191,36,.24)}
.sxa-pill.teal{background:rgba(34,211,164,.16);color:#5EEAD4;border-color:rgba(34,211,164,.24)}
.elementor-element-sxa-body{position:relative}
.elementor-element-sxa-side{position:sticky;top:100px;align-self:flex-start;max-height:calc(100vh - 120px);overflow:auto}
.elementor-element-sxa-post-content{font-family:'Plus Jakarta Sans',system-ui,sans-serif !important;color:var(--sxa-ink);font-size:17px;line-height:1.78}
.elementor-element-sxa-post-content p{margin:0 0 22px;font-weight:400;color:#1F2D33}
.elementor-element-sxa-post-content h2{font:700 28px/1.25 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent) !important;letter-spacing:-.01em;margin:48px 0 16px !important;scroll-margin-top:90px;padding-left:14px;border-left:4px solid var(--sxa-amber);text-align:left}
.elementor-element-sxa-post-content h3{font:700 21px/1.3 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent) !important;margin:32px 0 12px !important;scroll-margin-top:90px;text-align:left}
.elementor-element-sxa-post-content figure,.elementor-element-sxa-post-content .wp-block-image{margin:32px 0}
.elementor-element-sxa-post-content img{border-radius:12px;box-shadow:0 8px 32px rgba(14,57,66,.10);max-width:100%;height:auto;display:block;margin:0 auto}
.elementor-element-sxa-post-content figcaption{font:500 13px/1.5 'IBM Plex Mono',monospace !important;color:var(--sxa-mute) !important;text-align:center;margin-top:10px}
.elementor-element-sxa-post-content blockquote{border:none;border-left:4px solid var(--sxa-amber);background:#fff;padding:18px 22px;margin:32px 0;border-radius:0 8px 8px 0;font:500 18px/1.65 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent);box-shadow:0 4px 18px rgba(14,57,66,.05)}
.elementor-element-sxa-post-content ul,.elementor-element-sxa-post-content ol{padding-left:24px;margin:0 0 22px}
.elementor-element-sxa-post-content li{margin-bottom:8px;line-height:1.7}
.elementor-element-sxa-post-content ul li::marker{color:var(--sxa-amber)}
.elementor-element-sxa-post-content ol li::marker{color:var(--sxa-amber);font-family:'IBM Plex Mono',monospace;font-weight:600}
.elementor-element-sxa-post-content a{color:var(--sxa-accent);text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--sxa-amber)}
.elementor-element-sxa-post-content a:hover{color:var(--sxa-amber)}
.elementor-element-sxa-post-content strong{color:var(--sxa-accent);font-weight:700}
.elementor-element-sxa-post-content > p:first-of-type::first-letter{font:800 64px/.85 'Plus Jakarta Sans',sans-serif;color:var(--sxa-amber);float:left;margin:6px 14px 0 0}
.elementor-element-sxa-toc-w .elementor-toc__header{padding:14px 16px;background:#fff;border-bottom:1px solid var(--sxa-line)}
.elementor-element-sxa-toc-w .elementor-toc__header-title{font:700 11px/1 'IBM Plex Mono',monospace !important;letter-spacing:.14em;text-transform:uppercase;color:var(--sxa-accent);margin:0;display:flex;align-items:center;gap:8px}
.elementor-element-sxa-toc-w .elementor-toc__header-title::before{content:"";width:14px;height:2px;background:var(--sxa-amber)}
.elementor-element-sxa-toc-w{background:#fff;border:1px solid var(--sxa-line);border-radius:12px;box-shadow:0 4px 18px rgba(14,57,66,.04);overflow:hidden}
.elementor-element-sxa-toc-w .elementor-toc__body{padding:8px 4px 12px}
.elementor-element-sxa-toc-w .elementor-toc__list-item-text{color:var(--sxa-mute);font:500 13px/1.4 'Plus Jakarta Sans',sans-serif;padding:6px 10px;display:block;text-decoration:none;border-left:2px solid transparent}
.elementor-element-sxa-toc-w .elementor-toc__list-item-text:hover{color:var(--sxa-accent)}
.elementor-element-sxa-toc-w .elementor-toc__list-item.elementor-item-active > .elementor-toc__list-item-text-wrapper .elementor-toc__list-item-text{color:var(--sxa-accent);border-left-color:var(--sxa-amber);font-weight:600;background:rgba(245,158,11,.05)}
.elementor-element-sxa-toc-w .elementor-toc__list-wrapper{list-style:none;padding:0;margin:0;counter-reset:sxatoc}
.elementor-element-sxa-toc-w .elementor-toc__list-item{counter-increment:sxatoc;list-style:none;margin:0}
.elementor-element-sxa-toc-w .elementor-toc__list-item .elementor-toc__list-item .elementor-toc__list-item-text{padding-left:22px;font-size:12px;color:#7A8B91}
.sxa-cta-final{margin:24px auto 0}
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
.sxa-back-top{position:fixed;right:24px;bottom:24px;width:44px;height:44px;border-radius:50%;background:#0E3942;color:#fff;display:flex;align-items:center;justify-content:center;text-decoration:none;box-shadow:0 8px 24px rgba(14,57,66,.24);opacity:0;visibility:hidden;transform:translateY(8px);transition:all .2s;z-index:99}
.sxa-back-top.show{opacity:1;visibility:visible;transform:translateY(0)}
.sxa-back-top:hover{background:#F59E0B;transform:translateY(-4px);box-shadow:0 12px 28px rgba(245,158,11,.32)}
.sxa-progress{position:fixed;top:0;left:0;right:0;height:3px;background:rgba(14,57,66,.06);z-index:100;pointer-events:none}
.sxa-progress-bar{height:100%;background:linear-gradient(90deg,#F59E0B,#0E3942);width:0;transition:width .1s}
@media (max-width:980px){
  .elementor-element-sxa-body{flex-direction:column !important}
  .elementor-element-sxa-side{display:none !important}
}
@media (max-width:600px){
  .sxa-cta-inner{padding:32px 22px}
  .sxa-cta-h2{font-size:24px !important}
  .sxa-cta-actions{flex-direction:column}
  .sxa-cta-btn{justify-content:center}
  .sxa-cta-trust{flex-direction:column;gap:8px;text-align:center}
}
'''

PAGE_SETTINGS={
  'custom_css': CUSTOM_CSS,
  'hide_title': 'yes'
}

# Conditions: apply to all single posts
CONDITIONS=[
  {"type":"include","name":"singular","sub_name":"post"}
]


def post_meta(meta_dict):
    data=json.dumps({'meta':meta_dict}).encode()
    req=urllib.request.Request(f'{SITE}/wp-json/wp/v2/elementor_library/{TEMPLATE_ID}',data=data,headers=auth(),method='POST')
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read())


def main():
    print('Setting _elementor_data ...')
    res=post_meta({'_elementor_data': json.dumps(ED)})
    print('  modified:', res.get('modified'))
    print('  _elementor_data length:', len(res.get('meta',{}).get('_elementor_data','')))

    print('Setting _elementor_page_settings ...')
    res=post_meta({'_elementor_page_settings': json.dumps(PAGE_SETTINGS)})
    print('  page_settings keys:', list(json.loads(res.get('meta',{}).get('_elementor_page_settings','{}')).keys()))

    print('Setting _elementor_conditions ...')
    # WordPress meta API for arrays
    res=post_meta({'_elementor_conditions': ['include/singular/post']})
    print('  conditions:', res.get('meta',{}).get('_elementor_conditions'))


if __name__=='__main__':
    main()
