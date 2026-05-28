"""Phase 3 schema consolidation.
1. Update snippet 5639 OfferCatalog Offers to pure @id refs (no duplicate @type:Service)
2. Create snippet for 3 missing pillar Service schemas (Modbus/SaaS/Energy)
"""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
SNIPPETS = "https://suriota.com/wp-json/wp/v2/elementor_snippet"

# ===== 1. Strip 5639 Offers to pure @id refs =====
SNIPPET_5639_CODE = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "OfferCatalog",
      "@id": "https://suriota.com/#service-catalog",
      "name": "Suriota Industrial IoT, Automation & Energy Services",
      "provider": { "@id": "https://suriota.com/#organization" },
      "itemListElement": [
        {
          "@type": "Offer",
          "itemOffered": { "@id": "https://suriota.com/industrial-iot-system-integration/#service" }
        },
        {
          "@type": "Offer",
          "itemOffered": { "@id": "https://suriota.com/suriota-modbus-gateway/#service" }
        },
        {
          "@type": "Offer",
          "itemOffered": { "@id": "https://suriota.com/surge-saas-platform/#service" }
        },
        {
          "@type": "Offer",
          "itemOffered": { "@id": "https://suriota.com/industrial-engineering-automation/#service" }
        },
        {
          "@type": "Offer",
          "itemOffered": { "@id": "https://suriota.com/surge-energy-mapping/#service" }
        }
      ]
    }
  ]
}
</script>
'''

print("=== 1. Update snippet 5639 OfferCatalog to pure @id refs ===")
r = requests.post(f"{SNIPPETS}/5639", auth=AUTH, json={
    "meta": {
        "_elementor_code": SNIPPET_5639_CODE,
        "_elementor_location": "elementor_head",
        "_elementor_priority": 3
    }
}, timeout=30)
print(f"  status={r.status_code}  code_len={len(SNIPPET_5639_CODE)}")
assert r.status_code == 200, r.text[:300]

# ===== 2. Sitewide URL-conditional Service schema for 3 missing pillars =====
# JS injects per-pillar Service JSON-LD on matching URL
PILLAR_SERVICES_CODE = '''<script>
(function(){
  var canonical = location.pathname;
  // Map: pathname pattern -> full Service JSON-LD
  var services = {
    "/suriota-modbus-gateway/": {
      "@context": "https://schema.org",
      "@type": "Service",
      "@id": "https://suriota.com/suriota-modbus-gateway/#service",
      "name": "Suriota Modbus Gateway (RTU / TCP / MQTT)",
      "serviceType": "Modbus RTU and TCP gateway over MQTT, IoT field connectivity",
      "description": "ESP32-based industrial Modbus RTU/TCP-to-MQTT gateway. Bridges legacy PLC, energy meters, and sensors into cloud SCADA across manufacturing, oil & gas, and utility sites in Indonesia.",
      "url": "https://suriota.com/suriota-modbus-gateway/",
      "provider": { "@id": "https://suriota.com/#organization" },
      "areaServed": { "@type": "Country", "name": "Indonesia" },
      "audience": { "@type": "BusinessAudience", "audienceType": "Industrial OT engineers, automation integrators" },
      "offers": { "@type": "Offer", "availability": "https://schema.org/InStock", "priceCurrency": "IDR" }
    },
    "/surge-saas-platform/": {
      "@context": "https://schema.org",
      "@type": "Service",
      "@id": "https://suriota.com/surge-saas-platform/#service",
      "name": "SURGE SaaS Monitoring Platform",
      "serviceType": "Cloud SaaS monitoring, dashboards, alerts, multi-site IoT data",
      "description": "SURGE is a multi-tenant industrial IoT monitoring SaaS \\u2014 energy mapping, water analytics, vessel tracking, fleet/asset monitoring with real-time dashboards and KLHK SPARING compliance.",
      "url": "https://suriota.com/surge-saas-platform/",
      "provider": { "@id": "https://suriota.com/#organization" },
      "areaServed": { "@type": "Country", "name": "Indonesia" },
      "audience": { "@type": "BusinessAudience", "audienceType": "Plant managers, sustainability teams, fleet operators" },
      "offers": { "@type": "Offer", "availability": "https://schema.org/InStock", "priceCurrency": "IDR" }
    },
    "/surge-energy-mapping/": {
      "@context": "https://schema.org",
      "@type": "Service",
      "@id": "https://suriota.com/surge-energy-mapping/#service",
      "name": "Renewable Energy & Energy Mapping",
      "serviceType": "Solar PV, renewable energy mapping, water treatment automation",
      "description": "Solar PV PLTS design, hybrid PLTS-PLTB systems, smart street light (PJU), energy mapping for kWh + power factor + KLHK SPARING wastewater monitoring across Indonesian industrial sites.",
      "url": "https://suriota.com/surge-energy-mapping/",
      "provider": { "@id": "https://suriota.com/#organization" },
      "areaServed": { "@type": "Country", "name": "Indonesia" },
      "audience": { "@type": "BusinessAudience", "audienceType": "Industrial facilities, utilities, government" },
      "offers": { "@type": "Offer", "availability": "https://schema.org/InStock", "priceCurrency": "IDR" }
    }
  };
  // Match pathname (with or without trailing slash)
  var key = Object.keys(services).find(function(k){
    return canonical === k || canonical === k.replace(/\\/$/, '');
  });
  if (!key) return;
  // Inject as JSON-LD script tag in head
  var s = document.createElement('script');
  s.type = 'application/ld+json';
  s.textContent = JSON.stringify(services[key]);
  (document.head || document.documentElement).appendChild(s);
})();
</script>
'''

print("\n=== 2. Create snippet: URL-conditional pillar Service schemas ===")
payload = {
    "title": "SX / Pillar Service Schema (Modbus, SaaS, Energy)",
    "status": "publish",
    "meta": {
        "_elementor_location": "elementor_head",
        "_elementor_priority": 4,
        "_elementor_code": PILLAR_SERVICES_CODE
    }
}
r = requests.post(SNIPPETS, auth=AUTH, json=payload, timeout=30)
print(f"  status={r.status_code}")
if r.status_code in (200, 201):
    d = r.json()
    print(f"  created snippet id={d.get('id')} slug={d.get('slug')}")
    print(f"  code_len={len(d.get('meta',{}).get('_elementor_code',''))}")
else:
    print(f"  body: {r.text[:300]}")
