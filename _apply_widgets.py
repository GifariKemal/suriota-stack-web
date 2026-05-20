import json, urllib.request, base64

auth = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
hdrs = {'Authorization':f'Basic {auth}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

req = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5184?context=edit', headers=hdrs)
d = json.loads(urllib.request.urlopen(req).read())
code = d['meta']['_elementor_code']

# ===== 1) REMOVE the // WHY SURIOTA floating tag =====
remove_block = '''body.single-post .sxa-main .wp-block-group[style*="#eef6ff"]::before,
body.single-post .sxa-main .wp-block-group[style*="border-left-color:#1a6aab"]::before{
  content:"// WHY SURIOTA";
  position:absolute;
  top:-10px;left:24px;
  background:#C8851F;color:#fff;
  font-family:'IBM Plex Mono',monospace;
  font-size:10px;font-weight:600;
  letter-spacing:0.12em;
  padding:4px 10px;border-radius:2px;
}'''
before_len = len(code)
code = code.replace(remove_block, '')
print('WHY SURIOTA removed:', before_len != len(code))

# ===== 2) Add CSS for Artikel Lainnya button + Continue Reading section =====
add_css = """
/* === Artikel Lainnya button (3rd CTA option) === */
.sxa-cta-btn--more{background:transparent !important;color:#fff !important;border:1px solid rgba(255,255,255,0.32) !important}
.sxa-cta-btn--more:hover{background:rgba(255,255,255,0.10) !important;border-color:#fff !important;transform:translateY(-2px)}

/* === Continue Reading / Related Articles === */
.sxa-related{max-width:min(96vw,1400px);margin:48px auto 80px;padding:0 clamp(12px,2vw,32px)}
.sxa-related-head{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:28px;gap:24px;flex-wrap:wrap;border-bottom:1px solid var(--sxa-line);padding-bottom:16px}
.sxa-related-title{font:700 22px/1.2 'Plus Jakarta Sans',sans-serif;color:var(--sxa-accent);margin:0;letter-spacing:-0.012em}
.sxa-related-title small{display:block;font:600 11px/1 'IBM Plex Mono',monospace;color:#C8851F;letter-spacing:0.16em;text-transform:uppercase;margin-bottom:6px}
.sxa-related-all{font:600 12px/1 'IBM Plex Mono',monospace;color:var(--sxa-accent);text-decoration:none;letter-spacing:0.08em;text-transform:uppercase;display:inline-flex;align-items:center;gap:6px;border-bottom:1px solid #C8851F;padding-bottom:3px;transition:color .15s}
.sxa-related-all:hover{color:#C8851F}
.sxa-related-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}
.sxa-rel-card{display:flex;flex-direction:column;background:#fff;border:1px solid var(--sxa-line);border-radius:8px;overflow:hidden;text-decoration:none !important;color:inherit;transition:transform .2s,box-shadow .2s,border-color .2s}
.sxa-rel-card:hover{transform:translateY(-4px);box-shadow:0 8px 28px rgba(14,57,66,0.10);border-color:#C8851F}
.sxa-rel-thumb{aspect-ratio:16/10;background-size:cover;background-position:center;background-color:#0E3942;position:relative}
.sxa-rel-thumb::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,transparent 60%,rgba(14,57,66,0.55) 100%)}
.sxa-rel-thumb .sxa-rel-pill{position:absolute;top:12px;left:12px;background:rgba(255,255,255,0.92);color:var(--sxa-accent);font:600 9.5px/1 'IBM Plex Mono',monospace;letter-spacing:0.1em;text-transform:uppercase;padding:5px 10px;border-radius:3px;z-index:2}
.sxa-rel-body{padding:18px 20px;display:flex;flex-direction:column;flex:1;gap:8px}
.sxa-rel-meta{font:500 11px/1 'IBM Plex Mono',monospace;color:var(--sxa-mute);letter-spacing:0.05em}
.sxa-rel-title{font:700 16px/1.32 'Plus Jakarta Sans',sans-serif !important;color:var(--sxa-accent) !important;margin:0 !important;letter-spacing:-0.012em;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.sxa-rel-arrow{margin-top:auto;padding-top:10px;font:600 11.5px/1 'IBM Plex Mono',monospace;color:#C8851F;letter-spacing:0.08em;text-transform:uppercase;display:inline-flex;align-items:center;gap:6px}
.sxa-rel-card:hover .sxa-rel-arrow{gap:10px}
@media (max-width:600px){.sxa-related{margin:32px auto 56px}.sxa-related-grid{grid-template-columns:1fr;gap:18px}.sxa-related-title{font-size:18px}}
"""
code = code.replace('</style>', add_css + '\n</style>', 1)
print('CSS added')

# ===== 3) Add Artikel Lainnya button to CTA JS =====
old_wa_line = "WhatsApp</a>'+\n    '</div>'+"
new_wa_line = "WhatsApp</a>'+\n      '<a class=\"sxa-cta-btn sxa-cta-btn--more\" href=\"/artikel/\">Artikel Lainnya <span aria-hidden=\"true\">\\u2192</span></a>'+\n    '</div>'+"
if old_wa_line in code:
    code = code.replace(old_wa_line, new_wa_line)
    print('Added Artikel Lainnya button to CTA actions')
else:
    print('WARNING: old_wa_line pattern not found, check format')

# ===== 4) Add Continue Reading section JS (insert before back-to-top button creation) =====
related_js = """// === Continue Reading / Related Articles ===
  (function(){
    var bc = document.body.className.match(/postid-(\\d+)/);
    var currentId = bc ? bc[1] : '';
    fetch('/wp-json/wp/v2/posts?per_page=3&exclude='+currentId+'&_embed&_fields=id,title,slug,link,date,featured_media,_links,_embedded')
      .then(function(r){return r.json();})
      .then(function(posts){
        if(!Array.isArray(posts)||!posts.length)return;
        var rel = document.createElement('section');
        rel.className = 'sxa-related';
        var grid = '';
        posts.forEach(function(p){
          var img = '';
          try{
            if(p._embedded && p._embedded['wp:featuredmedia'] && p._embedded['wp:featuredmedia'][0]){
              var media = p._embedded['wp:featuredmedia'][0];
              if(media.media_details && media.media_details.sizes){
                var sizes = media.media_details.sizes;
                img = (sizes.medium_large && sizes.medium_large.source_url) || (sizes.medium && sizes.medium.source_url) || media.source_url || '';
              } else { img = media.source_url || ''; }
            }
          }catch(e){}
          var d = new Date(p.date);
          var dateText = d.toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'});
          grid += '<a class="sxa-rel-card" href="'+p.link+'">'+
            '<div class="sxa-rel-thumb" style="background-image:url(\\''+img+'\\')"><span class="sxa-rel-pill">Portfolio</span></div>'+
            '<div class="sxa-rel-body">'+
              '<span class="sxa-rel-meta">'+dateText+'</span>'+
              '<h3 class="sxa-rel-title">'+p.title.rendered+'</h3>'+
              '<span class="sxa-rel-arrow">Baca Artikel <span aria-hidden="true">\\u2192</span></span>'+
            '</div>'+
          '</a>';
        });
        rel.innerHTML = '<div class="sxa-related-head">'+
          '<h2 class="sxa-related-title"><small>Continue Reading</small>Artikel Lainnya</h2>'+
          '<a class="sxa-related-all" href="/artikel/">Lihat Semua <span aria-hidden="true">\\u2192</span></a>'+
        '</div>'+
        '<div class="sxa-related-grid">'+grid+'</div>';
        var cta = document.querySelector('.sxa-cta-final');
        if(cta) cta.parentNode.insertBefore(rel, cta.nextSibling);
      })
      .catch(function(){});
  })();
  """

insertion_anchor = "var bt=document.createElement('button');bt.type='button';bt.className='sxa-back-top';"
if insertion_anchor in code:
    code = code.replace(insertion_anchor, related_js + insertion_anchor)
    print('Added Continue Reading JS')
else:
    print('WARNING: insertion anchor not found')

# ===== Push =====
payload = json.dumps({'meta': {'_elementor_code': code}}).encode()
req2 = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5184', data=payload, method='POST', headers=hdrs)
r2 = json.loads(urllib.request.urlopen(req2).read())
print('\nModified:', r2.get('modified'), '| New len:', len(code))
