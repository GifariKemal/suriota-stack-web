"""Rewrite snippet 5192: merge LocalBusiness into AIOSEO #organization @graph node."""
import os
import requests, json
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
URL = "https://suriota.com/wp-json/wp/v2/elementor_snippet/5192"

NEW_CODE = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["Organization", "LocalBusiness"],
      "@id": "https://suriota.com/#organization",
      "name": "Suriota",
      "legalName": "PT Surya Inovasi Prioritas",
      "alternateName": "SURIOTA",
      "url": "https://suriota.com/",
      "description": "Industrial IoT, automation, and system integration company based in Batam, Indonesia. Specializing in SCADA, PLC, renewable energy, and water treatment solutions.",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Batam Centre",
        "addressLocality": "Batam",
        "addressRegion": "Kepulauan Riau",
        "postalCode": "29461",
        "addressCountry": "ID"
      },
      "telephone": "+62858-3567-2476",
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+62858-3567-2476",
        "contactType": "customer service",
        "areaServed": "ID",
        "availableLanguage": ["Indonesian", "English"]
      },
      "sameAs": [
        "https://www.instagram.com/Suriota.official",
        "https://linkedin.com/company/suriota"
      ],
      "areaServed": {
        "@type": "Country",
        "name": "Indonesia"
      },
      "knowsAbout": [
        "Industrial IoT",
        "Automation",
        "SCADA",
        "PLC",
        "Renewable Energy",
        "Water Treatment",
        "System Integration",
        "Modbus Gateway"
      ],
      "makesOffer": {
        "@id": "https://suriota.com/#service-catalog"
      }
    }
  ]
}
</script>
'''

payload = {
    "meta": {
        "_elementor_code": NEW_CODE,
        "_elementor_location": "elementor_head",
        "_elementor_priority": 2
    }
}

r = requests.post(URL, auth=AUTH, json=payload, timeout=30)
print("Status:", r.status_code)
if r.status_code != 200:
    print(r.text[:600])
else:
    d = r.json()
    code = d.get("meta", {}).get("_elementor_code", "")
    print("Code length:", len(code))
    print("Contains @id #organization:", "#organization" in code)
    print("Contains makesOffer #service-catalog:", "#service-catalog" in code)
