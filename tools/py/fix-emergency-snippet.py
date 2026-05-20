"""Rewrite emergency snippet 5153 with:
- All 10 services in Our Services dropdown (4 old + 6 new)
- All 10 services in footer Our Services column
- Dark teal dropdown hover (NOT pink/light)
- Keep existing structure for header/footer
"""
import json, base64, urllib.request, urllib.error

PASS='hCYK JqF1 khdB WDzI LQdQ WEBr'
AUTH=base64.b64encode(f'admin:{PASS}'.encode()).decode()
H={'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Accept':'application/json','Content-Type':'application/json'}

# Services list (10 total — 6 new + 4 old, ordered as in WP nav menu)
HEADER_SERVICES = [
    ('Internet of Things',     '/internet-of-things/'),
    ('System Integration',     '/system-integration/'),
    ('Digital Consulting',     '/digital-consulting/'),
    ('Artificial Intelligence','/artificial-intelligence/'),
    ('Data Analytics',         '/data-analytics/'),
    ('Software as a Service',  '/software-as-a-service/'),
    ('Electrical',             '/electrical/'),
    ('Automation',             '/automation/'),
    ('Water Treatment',        '/water-treatment/'),
    ('Renewable Energy',       '/renewable-energy/'),
]

PRODUCTS = [
    ('Modbus Gateway IIoT',  '/suriota-modbus-gateway/'),
    ('Waste Water Logger',   '/waste-water-loger/'),
    ('SURGE-Energy Mapping', '/surge-energy-mapping/'),
    ('SURGE-Vessel Tracking','/surge-vessel-tracking/'),
    ('SURGE-Water Analytic', '/surge-water-analytic/'),
    ('ISO-M485 Series',      '/iso-m485-series/'),
    ('PM1611-WD',            '/pm1611-wd/'),
    ('RS-485 Surge Protector','/rs-485-surge-protector-spd-t485-105/'),
]

# Build the snippet — use vanilla concat strings to avoid template-literal compatibility issues
def js_link(label, path, color_rgba='rgba(255,255,255,0.85)'):
    return f"'<li><a href=\"' + base + '{path}\" style=\"color:{color_rgba};text-decoration:none;font-size:14px;\">{label}</a></li>' +"

footer_services_html = '\n              '.join(js_link(l,p) for l,p in HEADER_SERVICES)
footer_products_html = '\n              '.join(js_link(l,p) for l,p in PRODUCTS)
header_services_html = '\n              '.join("'<a href=\"' + base + '" + p + "\">" + l + "</a>' +" for l,p in HEADER_SERVICES)
header_products_html = '\n              '.join("'<a href=\"' + base + '" + p + "\">" + l + "</a>' +" for l,p in PRODUCTS)

CODE = '''<script id="sx-emergency-header-footer-v3">
(function() {
  'use strict';
  if (window.sxEmergencyHFv3) return;
  window.sxEmergencyHFv3 = true;

  /* Remove older injectors (v1, v2) */
  ['header.sx-emergency','footer.sx-emergency','header.sx-hf-v2','footer.sx-hf-v2'].forEach(function(sel){
    var el = document.querySelector(sel);
    if (el) el.remove();
  });

  var base = 'https://suriota.com';
  var svgs = {
    wa: '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z"/></svg>',
    ig: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>',
    li: '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.063 2.063 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
    em: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    tk: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>'
  };

  function injectHeader() {
    if (document.querySelector('header.sx-hf-v3')) return;
    var header = document.createElement('header');
    header.className = 'sx-hf-v3';
    header.style.cssText = 'background:#3C7D47;position:relative;z-index:9999;font-family:Poppins,sans-serif;';
    header.innerHTML =
      '<div style="max-width:1200px;margin:0 auto;padding:14px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px;">' +
        '<a href="' + base + '/" style="flex-shrink:0;line-height:0;">' +
          '<img src="' + base + '/wp-content/uploads/2023/01/Logo-Suriota-Putih-512x109.png" alt="SURIOTA" style="height:38px;width:auto;display:block;">' +
        '</a>' +
        '<nav id="sx-hf-v3-nav" class="sx-hf-v3-nav">' +
          '<a href="' + base + '/about-us/">About Us</a>' +
          '<a href="' + base + '/portfolio/">Portfolio</a>' +
          '<a href="' + base + '/internship/">Internship</a>' +
          '<div class="sx-hf-v3-dropdown">' +
            '<button class="sx-hf-v3-dropbtn" aria-haspopup="true" aria-expanded="false">Our Services <span style="font-size:10px;">&#9662;</span></button>' +
            '<div class="sx-hf-v3-dropcontent">' +
              ''' + header_services_html + '''
            '</div>' +
          '</div>' +
          '<div class="sx-hf-v3-dropdown">' +
            '<button class="sx-hf-v3-dropbtn" aria-haspopup="true" aria-expanded="false">Product <span style="font-size:10px;">&#9662;</span></button>' +
            '<div class="sx-hf-v3-dropcontent">' +
              ''' + header_products_html + '''
            '</div>' +
          '</div>' +
        '</nav>' +
        '<button id="sx-hf-v3-toggle" class="sx-hf-v3-toggle" aria-label="Toggle menu">&#9776;</button>' +
      '</div>' +
      '<style>' +
        '.sx-hf-v3-nav{display:flex;align-items:center;gap:28px;}' +
        'header.sx-hf-v3 .sx-hf-v3-nav>a,header.sx-hf-v3 .sx-hf-v3-dropbtn{color:#fff!important;text-decoration:none!important;font-size:14px!important;font-weight:500!important;font-family:Poppins,sans-serif!important;white-space:nowrap!important;background:transparent!important;background-color:transparent!important;border:none!important;cursor:pointer!important;padding:8px 0!important;transition:opacity .15s!important;outline:none!important;box-shadow:none!important;}' +
        'header.sx-hf-v3 .sx-hf-v3-nav>a:hover,header.sx-hf-v3 .sx-hf-v3-nav>a:focus,header.sx-hf-v3 .sx-hf-v3-nav>a:active,header.sx-hf-v3 .sx-hf-v3-dropbtn:hover,header.sx-hf-v3 .sx-hf-v3-dropbtn:focus,header.sx-hf-v3 .sx-hf-v3-dropbtn:focus-visible,header.sx-hf-v3 .sx-hf-v3-dropbtn:active,header.sx-hf-v3 .sx-hf-v3-dropdown:hover .sx-hf-v3-dropbtn{opacity:.85!important;background:transparent!important;background-color:transparent!important;color:#fff!important;outline:none!important;box-shadow:none!important;}' +
        '.sx-hf-v3-dropdown{position:relative;}' +
        '.sx-hf-v3-dropcontent{display:none;position:absolute;top:100%;left:0;background:#0E3942;min-width:220px;box-shadow:0 12px 32px rgba(0,0,0,0.22);border-radius:8px;padding:8px 0;z-index:10000;margin-top:4px;border:1px solid rgba(255,255,255,.06);}' +
        '.sx-hf-v3-dropcontent::before{content:"";position:absolute;top:-3px;left:0;right:0;height:3px;background:linear-gradient(90deg,#F59E0B 0%,#22D3A4 50%,#0EA5E9 100%);border-radius:8px 8px 0 0;}' +
        '.sx-hf-v3-dropcontent a{display:block;padding:10px 18px;color:rgba(255,255,255,.88);text-decoration:none;font-size:13.5px;font-family:Poppins,sans-serif;white-space:nowrap;transition:all .12s;}' +
        '.sx-hf-v3-dropcontent a:hover{background:rgba(245,158,11,.18);color:#FBBF24;padding-left:22px;}' +
        '.sx-hf-v3-dropdown:hover .sx-hf-v3-dropcontent,.sx-hf-v3-dropdown.open .sx-hf-v3-dropcontent{display:block;}' +
        '.sx-hf-v3-toggle{display:none;background:none;border:none;color:#fff;font-size:22px;cursor:pointer;padding:4px;}' +
        '@media(max-width:900px){' +
          '.sx-hf-v3-nav{display:none;position:absolute;top:100%;left:0;right:0;background:#2a5e33;flex-direction:column;align-items:stretch;padding:12px 24px;gap:0;max-height:80vh;overflow-y:auto;}' +
          '.sx-hf-v3-nav.open{display:flex;}' +
          '.sx-hf-v3-nav>a,.sx-hf-v3-dropdown,.sx-hf-v3-dropbtn{padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.1);width:100%;text-align:left;}' +
          '.sx-hf-v3-dropcontent{position:static;box-shadow:none;background:transparent;padding:4px 0 4px 16px;display:none;border:none;}' +
          '.sx-hf-v3-dropcontent::before{display:none;}' +
          '.sx-hf-v3-dropcontent a{color:rgba(255,255,255,0.85);padding:8px 0;border:none;}' +
          '.sx-hf-v3-dropcontent a:hover{background:transparent;color:#fff;padding-left:0;}' +
          '.sx-hf-v3-dropdown.open .sx-hf-v3-dropcontent{display:block;}' +
          '.sx-hf-v3-toggle{display:block !important;}' +
        '}' +
      '</style>';
    document.body.insertBefore(header, document.body.firstChild);

    var toggle = document.getElementById('sx-hf-v3-toggle');
    var nav = document.getElementById('sx-hf-v3-nav');
    if (toggle && nav) {
      toggle.addEventListener('click', function() { nav.classList.toggle('open'); });
    }
    document.querySelectorAll('.sx-hf-v3-dropdown .sx-hf-v3-dropbtn').forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        if (window.innerWidth <= 900) {
          e.preventDefault();
          var parent = btn.parentElement;
          parent.classList.toggle('open');
          btn.setAttribute('aria-expanded', parent.classList.contains('open'));
        }
      });
    });
  }

  function injectFooter() {
    if (document.querySelector('footer.sx-hf-v3')) return;
    var footer = document.createElement('footer');
    footer.className = 'sx-hf-v3';
    footer.style.cssText = 'background:#0F5132;color:#fff;font-family:Lato,sans-serif;';
    footer.innerHTML =
      '<div style="max-width:1200px;margin:0 auto;padding:48px 24px 24px;">' +
        '<div class="sx-hf-v3-foot-grid" style="display:grid;grid-template-columns:1.3fr 1.3fr 1.1fr 1fr;gap:32px;margin-bottom:40px;">' +
          '<div>' +
            '<h4 style="font-family:Poppins,sans-serif;font-size:13px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;margin:0 0 20px;color:#fff;border-bottom:2px solid #F59E0B;padding-bottom:10px;display:inline-block;">Our Services</h4>' +
            '<ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px;">' +
              ''' + footer_services_html + '''
            '</ul>' +
          '</div>' +
          '<div>' +
            '<h4 style="font-family:Poppins,sans-serif;font-size:13px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;margin:0 0 20px;color:#fff;border-bottom:2px solid #F59E0B;padding-bottom:10px;display:inline-block;">Products</h4>' +
            '<ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px;">' +
              ''' + footer_products_html + '''
            '</ul>' +
          '</div>' +
          '<div>' +
            '<h4 style="font-family:Poppins,sans-serif;font-size:13px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;margin:0 0 20px;color:#fff;border-bottom:2px solid #F59E0B;padding-bottom:10px;display:inline-block;">Connect with Us</h4>' +
            '<div style="display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;">' +
              '<a href="https://wa.me/6285835672476" target="_blank" rel="noopener" aria-label="WhatsApp" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.10);display:flex;align-items:center;justify-content:center;color:#fff;text-decoration:none;transition:all .2s;">' + svgs.wa + '</a>' +
              '<a href="https://www.instagram.com/Suriota.official" target="_blank" rel="noopener" aria-label="Instagram" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.10);display:flex;align-items:center;justify-content:center;color:#fff;text-decoration:none;transition:all .2s;">' + svgs.ig + '</a>' +
              '<a href="https://linkedin.com/company/suriota" target="_blank" rel="noopener" aria-label="LinkedIn" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.10);display:flex;align-items:center;justify-content:center;color:#fff;text-decoration:none;transition:all .2s;">' + svgs.li + '</a>' +
              '<a href="mailto:admin@suriota.com" aria-label="Email" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.10);display:flex;align-items:center;justify-content:center;color:#fff;text-decoration:none;transition:all .2s;">' + svgs.em + '</a>' +
              '<a href="https://www.tokopedia.com/suriota" target="_blank" rel="noopener" aria-label="Tokopedia" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.10);display:flex;align-items:center;justify-content:center;color:#fff;text-decoration:none;transition:all .2s;">' + svgs.tk + '</a>' +
            '</div>' +
            '<p style="font-family:Poppins,sans-serif;font-size:11px;font-weight:600;letter-spacing:1.2px;text-transform:uppercase;margin:0 0 10px;color:rgba(255,255,255,0.7);">Stay Updated</p>' +
            '<form action="' + base + '/contact/" method="get" style="display:flex;gap:0;">' +
              '<input type="email" name="email" placeholder="your@email.com" required style="flex:1;min-width:0;padding:9px 12px;border:1px solid rgba(255,255,255,0.18);border-radius:6px 0 0 6px;background:rgba(255,255,255,0.06);color:#fff;font-size:13px;outline:none;">' +
              '<button type="submit" style="padding:9px 14px;border:none;border-radius:0 6px 6px 0;background:#F59E0B;color:#fff;font-size:14px;cursor:pointer;font-weight:700;">&#8594;</button>' +
            '</form>' +
          '</div>' +
          '<div style="text-align:center;">' +
            '<a href="' + base + '/" style="display:inline-block;margin-bottom:12px;">' +
              '<img src="' + base + '/wp-content/uploads/2023/01/Logo-Suriota-Putih-512x109.png" alt="SURIOTA" style="width:200px;height:auto;display:block;">' +
            '</a>' +
            '<p style="font-family:Poppins,sans-serif;font-size:11px;font-weight:600;letter-spacing:1.8px;text-transform:uppercase;margin:0 0 16px;color:rgba(255,255,255,0.85);">Next Gen. Industrial Partner</p>' +
            '<div style="display:flex;flex-direction:column;gap:8px;align-items:center;font-size:13px;">' +
              '<span style="display:flex;align-items:center;gap:8px;color:rgba(255,255,255,0.85);"><span style="width:24px;height:24px;border-radius:6px;background:rgba(255,255,255,0.14);display:flex;align-items:center;justify-content:center;color:#F59E0B;font-size:12px;">&#9742;</span><a href="tel:+6285835672476" style="color:#fff;text-decoration:none;">+62 858-3567-2476</a></span>' +
              '<span style="display:flex;align-items:center;gap:8px;color:rgba(255,255,255,0.85);"><span style="width:24px;height:24px;border-radius:6px;background:rgba(255,255,255,0.14);display:flex;align-items:center;justify-content:center;color:#F59E0B;font-size:12px;">&#9993;</span><a href="mailto:admin@suriota.com" style="color:#fff;text-decoration:none;">admin@suriota.com</a></span>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div style="border-top:1px solid rgba(255,255,255,0.1);padding:20px 24px;">' +
        '<div style="max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;font-size:13px;">' +
          '<p style="margin:0;color:rgba(255,255,255,0.7);">&copy; 2026 <strong style="color:#fff;">PT Surya Inovasi Prioritas</strong>. All rights reserved.</p>' +
          '<div style="display:flex;gap:20px;">' +
            '<a href="' + base + '/privacy-policy/" style="color:rgba(255,255,255,0.7);text-decoration:none;">Privacy Policy</a>' +
            '<a href="' + base + '/terms-of-service/" style="color:rgba(255,255,255,0.7);text-decoration:none;">Terms of Service</a>' +
            '<a href="' + base + '/sitemap/" style="color:rgba(255,255,255,0.7);text-decoration:none;">Sitemap</a>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<style>' +
        '.sx-hf-v3-foot-grid a[href]{transition:color .15s,transform .15s;}' +
        '.sx-hf-v3-foot-grid a[href]:hover{color:#FBBF24 !important;transform:translateX(2px);}' +
        '.sx-hf-v3-foot-grid > div:nth-child(3) a[aria-label]:hover{background:rgba(245,158,11,.22) !important;transform:translateY(-2px);}' +
        '@media(max-width:1024px){.sx-hf-v3-foot-grid{grid-template-columns:repeat(2,1fr) !important;}}' +
        '@media(max-width:540px){.sx-hf-v3-foot-grid{grid-template-columns:1fr !important;}}' +
      '</style>';
    document.body.appendChild(footer);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){ injectHeader(); injectFooter(); });
  } else {
    injectHeader(); injectFooter();
  }
})();
</script>'''


def post(url, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=H, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:300].decode('utf-8','replace')


# Update snippet 5153 content
res = post('https://suriota.com/wp-json/wp/v2/elementor_snippet/5153', {
    'meta': {'_elementor_code': CODE}
})
print('Update snippet 5153:', res[0] if isinstance(res,tuple) else res)
print('Code length:', len(CODE))
