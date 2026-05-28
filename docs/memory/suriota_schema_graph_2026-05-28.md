---
name: suriota-schema-graph-architecture-2026-05-28
description: "Live JSON-LD entity graph on suriota.com — Organization+LocalBusiness merge, OfferCatalog hub, per-pillar Service @id linking"
metadata: 
  node_type: memory
  type: project
  originSessionId: 632eaef5-07d2-4ba1-8394-c8327af57fa1
---

## Sitewide nodes (every page)

| Node | @id | Source | Notes |
|---|---|---|---|
| Organization+LocalBusiness | `https://suriota.com/#organization` | AIOSEO @graph **+** snippet 5192 (same @id, merged by parsers) | AIOSEO emits minimal Organization; snippet 5192 adds LocalBusiness fields (address, phone, contactPoint, areaServed, knowsAbout) |
| WebSite | `https://suriota.com/#website` | AIOSEO | publisher → #organization |
| BreadcrumbList | `https://suriota.com/#breadcrumblist` | AIOSEO | per page |
| WebPage | `https://suriota.com/#webpage` | AIOSEO | per page |
| OfferCatalog | `https://suriota.com/#service-catalog` | snippet 5639 (sitewide) | itemListElement: 5 Service refs |

## Per-pillar Service nodes (inline JSON-LD)

@id = `https://suriota.com/{en-slug}/#service` (shared across EN/ID/ZH language variants — they describe the same Service entity).

| Pillar | EN slug | EN id | ID id | ZH id | has @id? |
|---|---|---|---|---|---|
| IoT & System Integration | industrial-iot-system-integration | 5554 | 5566 | 5571 | ✓ |
| SCADA Automation | industrial-engineering-automation | 5557 | 5569 | 5574 | ✓ |
| Modbus Gateway | suriota-modbus-gateway | 934 | (n/a) | (n/a) | ✗ no Service block |
| SaaS Monitoring | surge-saas-platform | 5558 | 5570 | (?) | ✗ no Service block (has SoftwareApplication + FAQPage instead) |
| Renewable Energy | surge-energy-mapping | 1542 | (?) | (?) | ✗ no Service block |

**Out of scope** in 2026-05-28 task: adding Service JSON-LD to 3 pillars that lack it. The OfferCatalog #service-catalog already declares all 5 services with name/url/provider/areaServed/serviceType, so the entity graph is complete at the catalog level — pillars 934, 1542, 5558 just don't have per-page Service rich-result data.

## How merging works

JSON-LD parsers (Google, Bing) merge nodes with the same @id across multiple `<script type="application/ld+json">` blocks on the same page. Our LocalBusiness snippet 5192 and AIOSEO Organization both use `@id=https://suriota.com/#organization` → Google sees ONE entity with `@type: ["Organization","LocalBusiness"]` and merged property set.

Same applies cross-page: per-pillar Service @id is identical across EN/ID/ZH variants → Google treats them as the SAME Service in different languages. This is the recommended schema.org pattern for multilingual sites.

## Verification commands

```bash
# Homepage @graph dump
curl -s https://suriota.com/ | python -c "import sys,re,json; html=sys.stdin.read(); [print(json.dumps(json.loads(b), indent=2, ensure_ascii=False)) for b in re.findall(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', html, re.DOTALL)]"

# Per-page Service @id check
curl -s https://suriota.com/industrial-iot-system-integration/ | grep -oP '"@id"\s*:\s*"[^"]*#service[^"]*"'
```

## Deployment record (2026-05-28)

1. Snippet 5192 — rewritten with @graph wrapper, @id=#organization, @type=[Organization,LocalBusiness], makesOffer→#service-catalog
2. Snippet 5639 — created, sitewide OfferCatalog with 5 Service refs
3. Pages 5554, 5557 (EN), 5566, 5569 (ID), 5571, 5574 (ZH) — inline Service JSON-LD updated with @id and provider→#organization ref
4. Elementor cache flushed via Playwright admin session (Tools → Clear Files & Data)
5. Live verified all 6 pillar URLs (EN/ID/ZH × IoT+SCADA) emit @id + provider ref

## What's next (future tasks)

- Optionally add inline Service JSON-LD to pillars 934/1542/5558 so each pillar has per-page Service rich-result data
- Validate with Google Rich Results Test on /industrial-iot-system-integration/
- Consider moving snippet 5192 LocalBusiness data into AIOSEO's Organization Schema Settings (would let us delete snippet 5192 entirely)
