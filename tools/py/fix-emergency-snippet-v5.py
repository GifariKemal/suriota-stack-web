"""Emergency snippet v5 — Mobile/desktop dropdown sync fix.

Issues fixed vs v4:
1. Mobile dropdown wouldn't close after second tap because `:hover` stayed
   active after touch. Solution: wrap the desktop `:hover` open rule in
   @media (hover: hover) and (pointer: fine), so touch devices only use
   the `.open` class toggled by JS.
2. Mobile dropdown panel used dim `rgba(0,0,0,.16)` background and looked
   nothing like the desktop dropdown. Solution: reuse the same blue-teal
   `#0E3942` background and gradient top accent on mobile.
3. Added outside-tap close handler so menu+dropdowns collapse when
   tapping anywhere outside the header.
4. Same auto-close behavior on link click inside dropdown.
"""
import json, base64, urllib.request, urllib.error

PASS = 'hCYK JqF1 khdB WDzI LQdQ WEBr'
AUTH = base64.b64encode(f'admin:{PASS}'.encode()).decode()
H = {
    'Authorization': f'Basic {AUTH}',
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

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
    ('Modbus Gateway IIoT',   '/suriota-modbus-gateway/'),
    ('Waste Water Logger',    '/waste-water-loger/'),
    ('SURGE-Energy Mapping',  '/surge-energy-mapping/'),
    ('SURGE-Vessel Tracking', '/surge-vessel-tracking/'),
    ('SURGE-Water Analytic',  '/surge-water-analytic/'),
    ('ISO-M485 Series',       '/iso-m485-series/'),
    ('PM1611-WD',             '/pm1611-wd/'),
    ('RS-485 Surge Protector','/rs-485-surge-protector-spd-t485-105/'),
]


def link_footer(label, path):
    return "'<li><a href=\"' + base + '" + path + "\">" + label + "</a></li>' +"


def link_header(label, path):
    return "'<a href=\"' + base + '" + path + "\">" + label + "</a>' +"


footer_services_html = '\n              '.join(link_footer(l, p) for l, p in HEADER_SERVICES)
footer_products_html = '\n              '.join(link_footer(l, p) for l, p in PRODUCTS)
header_services_html = '\n              '.join(link_header(l, p) for l, p in HEADER_SERVICES)
header_products_html = '\n              '.join(link_header(l, p) for l, p in PRODUCTS)

CODE = '''<script id="sx-emergency-header-footer-v5">
(function() {
  'use strict';
  if (window.sxEmergencyHFv5) return;
  window.sxEmergencyHFv5 = true;

  /* === Ghost-slug recovery (must run before anything else) ===
     Kimi audit flagged these as 404 — real pages live at corrected slugs. */
  var ghostMap = {
    '/modbus-gateway/':     '/suriota-modbus-gateway/',
    '/modbus-gateway':      '/suriota-modbus-gateway/',
    '/waste-water-loger/':  '/waste-water-logger/',
    '/waste-water-loger':   '/waste-water-logger/'
  };
  var currentPath = window.location.pathname.toLowerCase();
  if (ghostMap[currentPath]) {
    window.location.replace(ghostMap[currentPath]);
    return;
  }

  /* === Duplicate-H1 dedup (Astra entry-title vs Elementor H1) ===
     Remove .entry-title H1 only when a second H1 exists in DOM, so
     pages relying solely on the theme title aren't accidentally headless. */
  function fixDuplicateH1() {
    var titles = document.querySelectorAll('h1.entry-title');
    if (!titles.length) return;
    var totalH1 = document.querySelectorAll('h1').length;
    if (totalH1 < 2) return;
    titles.forEach(function(el) {
      var parent = el.parentNode;
      if (parent) parent.removeChild(el);
    });
  }

  /* Remove older injectors */
  ['header.sx-emergency','footer.sx-emergency','header.sx-hf-v2','footer.sx-hf-v2','header.sx-hf-v3','footer.sx-hf-v3','header.sx-hf-v4','footer.sx-hf-v4'].forEach(function(sel){
    var el = document.querySelector(sel);
    if (el) el.remove();
  });

  var base = 'https://suriota.com';
  var svgs = {
    wa: '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z"/></svg>',
    ig: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>',
    li: '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.063 2.063 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
    em: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    tk: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
    phoneSm: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    mailSm: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'
  };

  function closeAllDropdowns() {
    document.querySelectorAll('.sx-hf-v5-dropdown.open').forEach(function(d){
      d.classList.remove('open');
      var b = d.querySelector('.sx-hf-v5-dropbtn');
      if (b) b.setAttribute('aria-expanded','false');
    });
  }

  function injectHeader() {
    if (document.querySelector('header.sx-hf-v5')) return;
    var header = document.createElement('header');
    header.className = 'sx-hf-v5';
    header.innerHTML =
      '<div class="sx-hf-v5-inner">' +
        '<a class="sx-hf-v5-logo" href="' + base + '/">' +
          '<img src="' + base + '/wp-content/uploads/2023/01/Logo-Suriota-Putih-512x109.png" alt="SURIOTA">' +
        '</a>' +
        '<nav id="sx-hf-v5-nav" class="sx-hf-v5-nav">' +
          '<a href="' + base + '/about-us/">About Us</a>' +
          '<a href="' + base + '/portfolio/">Portfolio</a>' +
          '<a href="' + base + '/internship/">Internship</a>' +
          '<div class="sx-hf-v5-dropdown">' +
            '<button class="sx-hf-v5-dropbtn" aria-haspopup="true" aria-expanded="false">Our Services <span class="sx-hf-v5-caret">&#9662;</span></button>' +
            '<div class="sx-hf-v5-dropcontent">' +
              ''' + header_services_html + '''
            '</div>' +
          '</div>' +
          '<div class="sx-hf-v5-dropdown sx-hf-v5-dropdown-right">' +
            '<button class="sx-hf-v5-dropbtn" aria-haspopup="true" aria-expanded="false">Product <span class="sx-hf-v5-caret">&#9662;</span></button>' +
            '<div class="sx-hf-v5-dropcontent">' +
              ''' + header_products_html + '''
            '</div>' +
          '</div>' +
        '</nav>' +
        '<button id="sx-hf-v5-toggle" class="sx-hf-v5-toggle" aria-label="Toggle menu" aria-expanded="false">&#9776;</button>' +
      '</div>';
    document.body.insertBefore(header, document.body.firstChild);

    var toggle = document.getElementById('sx-hf-v5-toggle');
    var nav = document.getElementById('sx-hf-v5-nav');
    if (toggle && nav) {
      toggle.addEventListener('click', function(e) {
        e.stopPropagation();
        var open = nav.classList.toggle('open');
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (!open) closeAllDropdowns();
      });
    }

    document.querySelectorAll('.sx-hf-v5-dropdown .sx-hf-v5-dropbtn').forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        var isMobile = window.matchMedia('(max-width: 900px)').matches;
        var hasHover = window.matchMedia('(hover: hover)').matches;
        /* On touch / mobile width, ALWAYS toggle via .open class */
        if (isMobile || !hasHover) {
          e.preventDefault();
          e.stopPropagation();
          var parent = btn.parentElement;
          var nowOpen = !parent.classList.contains('open');
          /* close siblings first */
          document.querySelectorAll('.sx-hf-v5-dropdown.open').forEach(function(d){
            if (d !== parent) {
              d.classList.remove('open');
              var b = d.querySelector('.sx-hf-v5-dropbtn');
              if (b) b.setAttribute('aria-expanded','false');
            }
          });
          parent.classList.toggle('open', nowOpen);
          btn.setAttribute('aria-expanded', nowOpen ? 'true' : 'false');
        }
      });
    });

    /* Close dropdowns + nav when tapping outside the header */
    document.addEventListener('click', function(e) {
      if (header.contains(e.target)) return;
      closeAllDropdowns();
      if (nav && nav.classList.contains('open')) {
        nav.classList.remove('open');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      }
    });

    /* Close dropdown after clicking a link inside it (mobile UX) */
    header.querySelectorAll('.sx-hf-v5-dropcontent a').forEach(function(a) {
      a.addEventListener('click', function() {
        closeAllDropdowns();
        if (nav) nav.classList.remove('open');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      });
    });

    /* Reset state when crossing the desktop/mobile breakpoint */
    var mq = window.matchMedia('(max-width: 900px)');
    var onChange = function() {
      closeAllDropdowns();
      if (nav) nav.classList.remove('open');
      if (toggle) toggle.setAttribute('aria-expanded', 'false');
    };
    if (mq.addEventListener) mq.addEventListener('change', onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  function injectFooter() {
    if (document.querySelector('footer.sx-hf-v5')) return;
    var footer = document.createElement('footer');
    footer.className = 'sx-hf-v5';
    footer.innerHTML =
      '<div class="sx-hf-v5-foot-main">' +
        '<div class="sx-hf-v5-foot-grid">' +
          '<div class="sx-hf-v5-col">' +
            '<h4>Our Services</h4>' +
            '<ul>' +
              ''' + footer_services_html + '''
            '</ul>' +
          '</div>' +
          '<div class="sx-hf-v5-col">' +
            '<h4>Products</h4>' +
            '<ul>' +
              ''' + footer_products_html + '''
            '</ul>' +
          '</div>' +
          '<div class="sx-hf-v5-col">' +
            '<h4>Connect with Us</h4>' +
            '<div class="sx-hf-v5-social">' +
              '<a href="https://wa.me/6285835672476" target="_blank" rel="noopener" aria-label="WhatsApp">' + svgs.wa + '</a>' +
              '<a href="https://www.instagram.com/Suriota.official" target="_blank" rel="noopener" aria-label="Instagram">' + svgs.ig + '</a>' +
              '<a href="https://linkedin.com/company/suriota" target="_blank" rel="noopener" aria-label="LinkedIn">' + svgs.li + '</a>' +
              '<a href="mailto:admin@suriota.com" aria-label="Email">' + svgs.em + '</a>' +
              '<a href="https://www.tokopedia.com/suriota" target="_blank" rel="noopener" aria-label="Tokopedia">' + svgs.tk + '</a>' +
            '</div>' +
            '<p class="sx-hf-v5-eyebrow">Stay Updated</p>' +
            '<form class="sx-hf-v5-news" action="' + base + '/contact/" method="get">' +
              '<input type="email" name="email" placeholder="your@email.com" required>' +
              '<button type="submit" aria-label="Subscribe">&#8594;</button>' +
            '</form>' +
          '</div>' +
          '<div class="sx-hf-v5-col sx-hf-v5-brand">' +
            '<a href="' + base + '/" class="sx-hf-v5-brand-logo">' +
              '<img src="' + base + '/wp-content/uploads/2023/01/Logo-Suriota-Putih-512x109.png" alt="SURIOTA">' +
            '</a>' +
            '<p class="sx-hf-v5-tagline">Next Gen. Industrial Partner</p>' +
            '<ul class="sx-hf-v5-contact">' +
              '<li><span class="sx-hf-v5-ico">' + svgs.phoneSm + '</span><a href="tel:+6285835672476">+62 858-3567-2476</a></li>' +
              '<li><span class="sx-hf-v5-ico">' + svgs.mailSm + '</span><a href="mailto:admin@suriota.com">admin@suriota.com</a></li>' +
            '</ul>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div class="sx-hf-v5-foot-bottom">' +
        '<div class="sx-hf-v5-foot-bottom-inner">' +
          '<p>&copy; 2026 <strong>PT Surya Inovasi Prioritas</strong>. All rights reserved.</p>' +
          '<div class="sx-hf-v5-legal">' +
            '<a href="' + base + '/privacy-policy/">Privacy Policy</a>' +
            '<a href="' + base + '/terms-of-service/">Terms of Service</a>' +
            '<a href="' + base + '/sitemap/">Sitemap</a>' +
          '</div>' +
        '</div>' +
      '</div>';
    document.body.appendChild(footer);
  }

  /* STYLES - strictly scoped to .sx-hf-v5 ancestors to prevent CSS bleed */
  var css = `
    header.sx-hf-v5,footer.sx-hf-v5{font-family:'Plus Jakarta Sans',system-ui,-apple-system,Segoe UI,sans-serif !important;-webkit-font-smoothing:antialiased;line-height:1.5;color:#fff;box-sizing:border-box;}
    header.sx-hf-v5 *,footer.sx-hf-v5 *{box-sizing:border-box;}
    header.sx-hf-v5 a,footer.sx-hf-v5 a{text-decoration:none;color:inherit;}

    /* HEADER */
    header.sx-hf-v5{background:#3C7D47;position:relative;z-index:9999;}
    header.sx-hf-v5 .sx-hf-v5-inner{max-width:1200px;margin:0 auto;padding:14px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px;}
    header.sx-hf-v5 .sx-hf-v5-logo{flex-shrink:0;line-height:0;}
    header.sx-hf-v5 .sx-hf-v5-logo img{height:38px;width:auto;display:block;}
    header.sx-hf-v5 .sx-hf-v5-nav{display:flex;align-items:center;gap:28px;}
    header.sx-hf-v5 .sx-hf-v5-nav>a,header.sx-hf-v5 .sx-hf-v5-dropbtn{color:#fff !important;background:transparent !important;background-color:transparent !important;border:none !important;outline:none !important;box-shadow:none !important;font:500 14px/1 'Plus Jakarta Sans',sans-serif !important;text-decoration:none !important;white-space:nowrap;padding:8px 0 !important;cursor:pointer;transition:opacity .15s;display:inline-flex;align-items:center;gap:6px;}
    header.sx-hf-v5 .sx-hf-v5-nav>a:hover,header.sx-hf-v5 .sx-hf-v5-nav>a:focus,header.sx-hf-v5 .sx-hf-v5-nav>a:focus-visible,header.sx-hf-v5 .sx-hf-v5-nav>a:active,header.sx-hf-v5 .sx-hf-v5-dropbtn:hover,header.sx-hf-v5 .sx-hf-v5-dropbtn:focus,header.sx-hf-v5 .sx-hf-v5-dropbtn:focus-visible,header.sx-hf-v5 .sx-hf-v5-dropbtn:active{opacity:.82 !important;background:transparent !important;background-color:transparent !important;color:#fff !important;outline:none !important;box-shadow:none !important;}
    header.sx-hf-v5 .sx-hf-v5-caret{font-size:9px;opacity:.7;transition:transform .2s;}
    header.sx-hf-v5 .sx-hf-v5-dropdown.open .sx-hf-v5-caret{transform:rotate(180deg);}
    header.sx-hf-v5 .sx-hf-v5-dropdown{position:relative;}
    header.sx-hf-v5 .sx-hf-v5-dropcontent{display:none;position:absolute;top:100%;left:0;background:#0E3942;min-width:240px;max-width:calc(100vw - 48px);box-shadow:0 12px 32px rgba(0,0,0,.22);border-radius:8px;padding:8px 0;z-index:10000;margin-top:6px;border:1px solid rgba(255,255,255,.06);overflow:hidden;}
    header.sx-hf-v5 .sx-hf-v5-dropcontent::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#F59E0B 0%,#22D3A4 50%,#0EA5E9 100%);}
    header.sx-hf-v5 .sx-hf-v5-dropdown-right .sx-hf-v5-dropcontent{left:auto;right:0;}
    header.sx-hf-v5 .sx-hf-v5-dropcontent a{display:block;padding:10px 18px;color:rgba(255,255,255,.88) !important;background:transparent !important;font:500 13.5px/1.3 'Plus Jakarta Sans',sans-serif !important;white-space:nowrap;transition:background .12s,color .12s,padding-left .12s;}
    header.sx-hf-v5 .sx-hf-v5-dropdown.open .sx-hf-v5-dropcontent{display:block;}
    header.sx-hf-v5 .sx-hf-v5-toggle{display:none;background:transparent;border:none;color:#fff;font-size:22px;cursor:pointer;padding:4px;}

    /* Desktop-only: open on hover. Wrapped in @media (hover: hover) so touch
       devices don't get a sticky :hover that defeats the .open toggle. */
    @media (hover: hover) and (pointer: fine) {
      header.sx-hf-v5 .sx-hf-v5-dropdown:hover .sx-hf-v5-dropcontent{display:block;}
      header.sx-hf-v5 .sx-hf-v5-dropdown:hover .sx-hf-v5-caret{transform:rotate(180deg);}
      header.sx-hf-v5 .sx-hf-v5-dropcontent a:hover{background:rgba(245,158,11,.18) !important;color:#FBBF24 !important;padding-left:22px;}
    }

    @media(max-width:900px){
      header.sx-hf-v5 .sx-hf-v5-nav{display:none;position:absolute;top:100%;left:0;right:0;background:#2a5e33;flex-direction:column;align-items:stretch;padding:8px 20px 12px;gap:0;max-height:calc(100vh - 60px);overflow-y:auto;border-top:1px solid rgba(255,255,255,.08);}
      header.sx-hf-v5 .sx-hf-v5-nav.open{display:flex;}
      header.sx-hf-v5 .sx-hf-v5-nav>a,header.sx-hf-v5 .sx-hf-v5-dropdown{width:100%;}
      header.sx-hf-v5 .sx-hf-v5-nav>a,header.sx-hf-v5 .sx-hf-v5-dropbtn{padding:12px 4px !important;border-bottom:1px solid rgba(255,255,255,.08);text-align:left;width:100%;justify-content:space-between;}
      /* Mobile dropdown panel — match desktop blue-teal palette */
      header.sx-hf-v5 .sx-hf-v5-dropcontent{position:static;background:#0E3942;box-shadow:none;border-radius:8px;margin:8px 0 10px;padding:10px 0;border:1px solid rgba(255,255,255,.08);max-width:none;overflow:hidden;}
      header.sx-hf-v5 .sx-hf-v5-dropcontent::before{display:block;}
      header.sx-hf-v5 .sx-hf-v5-dropcontent a{color:rgba(255,255,255,.9) !important;padding:11px 18px;font-size:13.5px !important;white-space:normal;border-bottom:1px solid rgba(255,255,255,.04);}
      header.sx-hf-v5 .sx-hf-v5-dropcontent a:last-child{border-bottom:none;}
      header.sx-hf-v5 .sx-hf-v5-dropcontent a:active{background:rgba(245,158,11,.22) !important;color:#FBBF24 !important;}
      header.sx-hf-v5 .sx-hf-v5-toggle{display:block;}
    }

    /* FOOTER */
    footer.sx-hf-v5{background:#0F5132;color:#fff;font-family:'Plus Jakarta Sans',system-ui,sans-serif !important;}
    footer.sx-hf-v5 .sx-hf-v5-foot-main{max-width:1200px;margin:0 auto;padding:48px 24px 36px;}
    footer.sx-hf-v5 .sx-hf-v5-foot-grid{display:grid;grid-template-columns:1.2fr 1.2fr 1.1fr 1.1fr;gap:36px;}
    footer.sx-hf-v5 .sx-hf-v5-col h4{font:700 13px/1 'Plus Jakarta Sans',sans-serif !important;letter-spacing:1.2px;text-transform:uppercase;color:#fff !important;margin:0 0 20px;padding-bottom:10px;border-bottom:2px solid #F59E0B;display:inline-block;}
    footer.sx-hf-v5 .sx-hf-v5-col ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px;}
    footer.sx-hf-v5 .sx-hf-v5-col ul a{display:inline-block;color:rgba(255,255,255,.86) !important;font:500 14px/1.45 'Plus Jakarta Sans',sans-serif !important;text-decoration:none;transition:color .15s,transform .15s;}
    footer.sx-hf-v5 .sx-hf-v5-col ul a:hover{color:#FBBF24 !important;transform:translateX(3px);}

    /* SOCIAL */
    footer.sx-hf-v5 .sx-hf-v5-social{display:flex;gap:10px;margin:0 0 22px;flex-wrap:wrap;}
    footer.sx-hf-v5 .sx-hf-v5-social a{width:38px;height:38px;border-radius:50%;background:rgba(255,255,255,.10);display:inline-flex;align-items:center;justify-content:center;color:#fff !important;transition:all .2s;}
    footer.sx-hf-v5 .sx-hf-v5-social a:hover{background:rgba(245,158,11,.22);color:#FBBF24 !important;transform:translateY(-2px);}

    /* NEWSLETTER */
    footer.sx-hf-v5 .sx-hf-v5-eyebrow{font:600 11px/1 'IBM Plex Mono',monospace !important;letter-spacing:1.4px;text-transform:uppercase;color:#FBBF24 !important;margin:0 0 10px;}
    footer.sx-hf-v5 .sx-hf-v5-news{display:flex;}
    footer.sx-hf-v5 .sx-hf-v5-news input{flex:1;min-width:0;padding:10px 14px;border:1px solid rgba(255,255,255,.20);border-radius:6px 0 0 6px;background:rgba(255,255,255,.08);color:#fff !important;font:500 13.5px/1.3 'Plus Jakarta Sans',sans-serif !important;outline:none;}
    footer.sx-hf-v5 .sx-hf-v5-news input::placeholder{color:rgba(255,255,255,.62) !important;font-weight:400;}
    footer.sx-hf-v5 .sx-hf-v5-news input:focus{border-color:#F59E0B;background:rgba(255,255,255,.12);}
    footer.sx-hf-v5 .sx-hf-v5-news button{padding:10px 16px;border:none;border-radius:0 6px 6px 0;background:#F59E0B;color:#fff !important;font:700 16px/1 'Plus Jakarta Sans',sans-serif !important;cursor:pointer;transition:background .15s;}
    footer.sx-hf-v5 .sx-hf-v5-news button:hover{background:#D97706;}

    /* BRAND */
    footer.sx-hf-v5 .sx-hf-v5-brand{text-align:center;}
    footer.sx-hf-v5 .sx-hf-v5-brand-logo{display:inline-block;margin-bottom:14px;line-height:0;}
    footer.sx-hf-v5 .sx-hf-v5-brand-logo img{width:200px;height:auto;display:block;}
    footer.sx-hf-v5 .sx-hf-v5-tagline{font:600 11px/1.2 'IBM Plex Mono',monospace !important;letter-spacing:1.8px;text-transform:uppercase;color:rgba(255,255,255,.85) !important;margin:0 0 18px;}
    footer.sx-hf-v5 .sx-hf-v5-contact{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px;align-items:center;}
    footer.sx-hf-v5 .sx-hf-v5-contact li{display:flex;align-items:center;gap:10px;font:500 13.5px/1.3 'Plus Jakarta Sans',sans-serif !important;color:rgba(255,255,255,.92);}
    footer.sx-hf-v5 .sx-hf-v5-contact .sx-hf-v5-ico{width:28px;height:28px;border-radius:6px;background:rgba(245,158,11,.15);display:inline-flex;align-items:center;justify-content:center;color:#F59E0B;flex-shrink:0;}
    footer.sx-hf-v5 .sx-hf-v5-contact a{color:#fff !important;text-decoration:none;transition:color .15s;}
    footer.sx-hf-v5 .sx-hf-v5-contact a:hover{color:#FBBF24 !important;}

    /* BOTTOM BAR - darker than main footer */
    footer.sx-hf-v5 .sx-hf-v5-foot-bottom{background:#0A3D24;border-top:1px solid rgba(255,255,255,.06);}
    footer.sx-hf-v5 .sx-hf-v5-foot-bottom-inner{max-width:1200px;margin:0 auto;padding:18px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;font:500 13px/1.4 'Plus Jakarta Sans',sans-serif !important;}
    footer.sx-hf-v5 .sx-hf-v5-foot-bottom-inner p{margin:0;color:rgba(255,255,255,.68);}
    footer.sx-hf-v5 .sx-hf-v5-foot-bottom-inner p strong{color:#fff;font-weight:700;}
    footer.sx-hf-v5 .sx-hf-v5-legal{display:flex;gap:24px;flex-wrap:wrap;}
    footer.sx-hf-v5 .sx-hf-v5-legal a{color:rgba(255,255,255,.68) !important;text-decoration:none;transition:color .15s;}
    footer.sx-hf-v5 .sx-hf-v5-legal a:hover{color:#FBBF24 !important;}

    /* RESPONSIVE */
    @media(max-width:1024px){
      footer.sx-hf-v5 .sx-hf-v5-foot-grid{grid-template-columns:1fr 1fr;gap:32px;}
      footer.sx-hf-v5 .sx-hf-v5-brand{text-align:left;}
      footer.sx-hf-v5 .sx-hf-v5-brand-logo img{margin:0;}
      footer.sx-hf-v5 .sx-hf-v5-contact{align-items:flex-start;}
    }
    @media(max-width:600px){
      footer.sx-hf-v5 .sx-hf-v5-foot-main{padding:36px 20px 28px;}
      footer.sx-hf-v5 .sx-hf-v5-foot-grid{grid-template-columns:1fr;gap:28px;}
      footer.sx-hf-v5 .sx-hf-v5-brand-logo img{width:160px;}
      footer.sx-hf-v5 .sx-hf-v5-foot-bottom-inner{flex-direction:column;align-items:flex-start;text-align:left;gap:10px;padding:16px 20px;}
      footer.sx-hf-v5 .sx-hf-v5-legal{gap:14px;}
    }
  `;
  var st = document.createElement('style');
  st.id = 'sx-hf-v5-css';
  st.textContent = css;
  document.head.appendChild(st);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){ fixDuplicateH1(); injectHeader(); injectFooter(); });
  } else {
    fixDuplicateH1(); injectHeader(); injectFooter();
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
        return e.code, e.read()[:300].decode('utf-8', 'replace')


if __name__ == '__main__':
    res = post('https://suriota.com/wp-json/wp/v2/elementor_snippet/5153', {
        'meta': {'_elementor_code': CODE}
    })
    print('Update snippet 5153 (v5 code):', res[0] if isinstance(res, tuple) else res)
    print('Code length:', len(CODE))
