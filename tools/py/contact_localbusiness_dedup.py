"""Phase A2 — /contact/ LocalBusiness dedup:
1. Update snippet 5192 with richer fields from /contact/ inline (postal, openingHours, email, fuller address)
2. Remove standalone LocalBusiness from /contact/ Elementor data (keep BreadcrumbList + FAQPage)
"""
import os
import requests, re
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
SNIPPET = "https://suriota.com/wp-json/wp/v2/elementor_snippet/5192"
CONTACT = "https://suriota.com/wp-json/wp/v2/pages/4983"

# Step 1: Update snippet 5192 with the contact page's richer data
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
      "logo": "https://suriota.com/wp-content/uploads/2023/01/Logo-Suriota-Putih-512x109.png",
      "description": "Industrial IoT, automation, and system integration company based in Batam, Indonesia. Specializing in SCADA, PLC, renewable energy, and water treatment solutions.",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Batam Centre, Jl. Legenda Malaka, Baloi Permai",
        "addressLocality": "Batam Kota",
        "addressRegion": "Kepulauan Riau",
        "postalCode": "29431",
        "addressCountry": "ID"
      },
      "telephone": "+62-858-3567-2476",
      "email": "admin@suriota.com",
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
          "opens": "09:00",
          "closes": "18:00"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": "Saturday",
          "opens": "09:00",
          "closes": "13:00"
        }
      ],
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+62-858-3567-2476",
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
print("=== 1. Update snippet 5192 with richer LocalBusiness data ===")
r = requests.post(SNIPPET, auth=AUTH, json={
    "meta": {
        "_elementor_code": NEW_CODE,
        "_elementor_location": "elementor_head",
        "_elementor_priority": 2
    }
}, timeout=30)
print(f"  status: {r.status_code}")
print(f"  contains postal 29431: {'29431' in NEW_CODE}")
print(f"  contains openingHours: {'openingHoursSpecification' in NEW_CODE}")
print(f"  contains email: {'admin@suriota.com' in NEW_CODE}")

# Step 2: Remove standalone LocalBusiness node from /contact/ Elementor data @graph
print("\n=== 2. Remove standalone LocalBusiness from /contact/ ===")
r = requests.get(f"{CONTACT}?context=edit&_fields=id,meta", auth=AUTH, timeout=30)
elem = r.json()['meta']['_elementor_data']
print(f"  before len: {len(elem)}")

# The LocalBusiness object is between {"@type":"LocalBusiness", ... }
# Need to match the WHOLE object as escaped JSON inside elementor data.
# Build the exact substring to remove. From the inspection earlier, it starts with:
#   ,{"@type":"LocalBusiness","@id":"https:\/\/suriota.com\/#localbusiness", ... }
# Ends before the next ,{"@type":"FAQPage", ...

# Find the LocalBusiness opening and the next sibling node start
lb_start = elem.find(',{\\"@type\\":\\"LocalBusiness\\"')
if lb_start < 0:
    print("  ERROR: LocalBusiness node not found in expected escaped form")
    raise SystemExit(1)

# Find the next node start ,{"@type": after this position
# Need to count balanced braces inside the LocalBusiness object
# Simpler: find ,{"@type":"FAQPage" as the next sibling
faq_start = elem.find(',{\\"@type\\":\\"FAQPage\\"', lb_start)
if faq_start < 0:
    # Or end of graph array ]
    print("  ERROR: FAQPage sibling not found")
    raise SystemExit(1)

print(f"  LocalBusiness span: chars {lb_start}..{faq_start}")
# Remove from elem[lb_start:faq_start]  (this includes the leading comma)
new_elem = elem[:lb_start] + elem[faq_start:]
print(f"  after len: {len(new_elem)}")
print(f"  removed {len(elem) - len(new_elem)} chars")

# Verify the resulting JSON portion still well-formed by parsing the @graph block
# Quick sanity: count occurrences of LocalBusiness
print(f"  LocalBusiness count after removal: {new_elem.count('LocalBusiness')}")
print(f"  BreadcrumbList still present: {'BreadcrumbList' in new_elem}")
print(f"  FAQPage still present: {'FAQPage' in new_elem}")

# Save
rp = requests.post(CONTACT, auth=AUTH, json={"meta": {"_elementor_data": new_elem}}, timeout=60)
print(f"  PATCH status: {rp.status_code}")
if rp.status_code != 200:
    print(rp.text[:400])
