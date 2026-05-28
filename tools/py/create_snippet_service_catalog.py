"""Create new sitewide snippet: OfferCatalog @id=#service-catalog linking to 5 pillar Services."""
import os
import requests, json
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
BASE = "https://suriota.com/wp-json/wp/v2/elementor_snippet"

CODE = '''<script type="application/ld+json">
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
          "itemOffered": {
            "@type": "Service",
            "@id": "https://suriota.com/industrial-iot-system-integration/#service",
            "name": "Industrial IoT & System Integration",
            "url": "https://suriota.com/industrial-iot-system-integration/",
            "serviceType": "Industrial IoT, system integration, edge gateway deployment",
            "provider": { "@id": "https://suriota.com/#organization" },
            "areaServed": { "@type": "Country", "name": "Indonesia" }
          }
        },
        {
          "@type": "Offer",
          "itemOffered": {
            "@type": "Service",
            "@id": "https://suriota.com/suriota-modbus-gateway/#service",
            "name": "Modbus Gateway (RTU / TCP / MQTT)",
            "url": "https://suriota.com/suriota-modbus-gateway/",
            "serviceType": "Modbus RTU and TCP gateway over MQTT, IoT field connectivity",
            "provider": { "@id": "https://suriota.com/#organization" },
            "areaServed": { "@type": "Country", "name": "Indonesia" }
          }
        },
        {
          "@type": "Offer",
          "itemOffered": {
            "@type": "Service",
            "@id": "https://suriota.com/surge-saas-platform/#service",
            "name": "SURGE SaaS Monitoring Platform",
            "url": "https://suriota.com/surge-saas-platform/",
            "serviceType": "Cloud SaaS monitoring, dashboards, alerts, multi-site IoT data",
            "provider": { "@id": "https://suriota.com/#organization" },
            "areaServed": { "@type": "Country", "name": "Indonesia" }
          }
        },
        {
          "@type": "Offer",
          "itemOffered": {
            "@type": "Service",
            "@id": "https://suriota.com/industrial-engineering-automation/#service",
            "name": "Industrial Engineering & SCADA Automation",
            "url": "https://suriota.com/industrial-engineering-automation/",
            "serviceType": "SCADA, PLC, HMI, control panel, automation engineering",
            "provider": { "@id": "https://suriota.com/#organization" },
            "areaServed": { "@type": "Country", "name": "Indonesia" }
          }
        },
        {
          "@type": "Offer",
          "itemOffered": {
            "@type": "Service",
            "@id": "https://suriota.com/surge-energy-mapping/#service",
            "name": "Renewable Energy & Water Treatment",
            "url": "https://suriota.com/surge-energy-mapping/",
            "serviceType": "Solar PV, renewable energy mapping, water treatment automation",
            "provider": { "@id": "https://suriota.com/#organization" },
            "areaServed": { "@type": "Country", "name": "Indonesia" }
          }
        }
      ]
    }
  ]
}
</script>
'''

payload = {
    "title": "SX / Service Hub OfferCatalog (Sitewide)",
    "status": "publish",
    "meta": {
        "_elementor_location": "elementor_head",
        "_elementor_priority": 3,
        "_elementor_code": CODE
    }
}

r = requests.post(BASE, auth=AUTH, json=payload, timeout=30)
print("Status:", r.status_code)
if r.status_code not in (200, 201):
    print(r.text[:600])
else:
    d = r.json()
    print("Created snippet ID:", d.get("id"))
    print("Slug:", d.get("slug"))
    print("Location:", d.get("meta",{}).get("_elementor_location"))
    print("Priority:", d.get("meta",{}).get("_elementor_priority"))
    print("Code length:", len(d.get("meta",{}).get("_elementor_code","")))
