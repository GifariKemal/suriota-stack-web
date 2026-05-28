---
name: Suriota Page & Widget IDs Reference
description: Elementor post IDs and key widget IDs for suriota.com pages — for direct MCP operations
type: reference
originSessionId: 587198fb-6cea-4b87-a692-d8a6e5ea6255
---
## Page (Post) IDs

| Page | post_id |
|---|---|
| Homepage | 12 |
| About Us | 29 |
| Desain Grafis | 33 |
| Automation | 35 |
| Electrical | 37 |
| Renewable Energy | 39 |
| Teknologi Informasi | 41 |
| Tentang | 376 |
| Portfolio | 839 |
| Modbus Gateway | 934 |
| Waste Water Loger | 929 |
| Water Treatment | 945 |
| Internship | 1127 |
| SURGE-Energy Mapping | 1542 |
| SURGE-Vessel Tracking | 1546 |
| SURGE-Water Analytic | 1547 |
| ISO-M485 SERIES | 1740 |
| THM-30MD | 1741 |
| PM1611-WD | 1742 |
| RS-485 Surge Protector | 1765 |

## Service Pages Widget IDs (Common Structure — 4 pages share template)

Each service page has hero section + content section with these widget types:

### Electrical (37)
- Hero section: `00f6628` | column: `79d8e7b`
- Content section: `ca0248d` | column: `6082bbf`
- H1: `bc67178` "Electrical Services"
- Subtitle: `ae7cdea`
- Hero button: `969e246`
- **v4 Industries chips: `4561f38`**
- Main H2: `5657cca`
- Intro text-editor: `fd54486`
- Mid heading: `3610c37`
- **v4 Why Us cards: `290817d`**
- Our Services H2: `c1444ed`
- Service grid: `619a2e4`
- Workflow: `e5c63a1`
- FAQ H2: `d9a4a89`
- FAQ accordion: `cc40fb4`
- CTA H2: `a74c0c1`
- CTA button: `6ee0147`
- Portfolio H2: `0182c56`
- Portfolio list: `ee5d5de`
- **v4 JSON-LD: `36fdeef`**

### Automation (35)
- Hero section: `e4d0856` | column: `c48a432`
- Content section: `4c2bb21` | column: `f66ff98`
- H1: `5bccd9c` | Subtitle: `b11aad7` | Hero button: `4cdc231`
- **v4 Industries: `997c12e`**
- Main H2: `b15f302` | Intro: `43fbe4f` | Mid heading: `3c0ca08`
- **v4 Why Us: `4bee829`**
- Our Services: `063f531` | Service grid: `ba7be46` | Workflow: `5f1ebd4`
- FAQ H2: `8081432` | Accordion: `af5b3ec`
- CTA H2: `fd16c61` | Button: `08b621f`
- Portfolio: `8773388` / `2e6fd0f`
- **v4 JSON-LD: `720c669`**

### Water Treatment (945)
- Hero section: `e4d0856` | column: `c48a432` (same ID as Auto — different post)
- Content section: `5b96134` | column: `f46fd5d`
- H1: `5bccd9c` | Subtitle: `3bec8b7` | Hero button: `30d4be1`
- **v4 Industries: `51b42e7`**
- Main H2: `f1309a5` | Intro: `ebc466a` | Mid heading: `af4eae9`
- **v4 Why Us: `0948521`**
- Our Services: `f3ea095` | Service grid: `5c68286` | Workflow: `d6e57ae`
- FAQ H2: `a735eb5` | Accordion: `3a4c61c`
- CTA H2: `5df88d8` | Button: `28786ca`
- Portfolio: `8ffbc83` / `c084596`
- **v4 JSON-LD: `82ae13c`**

### Renewable Energy (39)
- Hero section: `d238b21` | column: `cb90971`
- Content section: `299c0aa` | column: `0cb51ce`
- H1: `cd9e45a` | Subtitle: `2416991` | Hero button: `c4c2078`
- **v4 Industries: `19fcca0`**
- Main H2: `9b2e3e3` | Intro: `6d5d0a1` | Mid heading: `4911eff`
- **v4 Why Us: `890145e`**
- Our Services: `38d3726` | Service grid: `5fb162f` | Workflow: `90634a3`
- FAQ H2: `0fa67be` | Accordion: `2bf99bb`
- CTA H2: `cbc70bf` | Button: `de36f6e`
- Portfolio: `6e0b966` / `8192ccb`
- **v4 JSON-LD: `8225123`**

## About Us (29) — Active Widgets After Cleanup

Section structure (Stats Bar + 5 Services REMOVED — moved to Homepage):
- `d2056c4` Hero section
- `9d8606c` Visi/Misi section → widget `ab865ca`
- `323e173` Siapa SURIOTA section → widget `8ef5419` (contains extended JSON-LD)
- `738eb59` CIPTA Core Values section → widget `7b714f7`
- `692d54a` CTA section → H2 `c82dbe6`, paragraph + buttons `6274048`

Hero widgets: H1 `2f1b2e7`, subtitle `eecf593`, divider `b4e9f0f`

## Homepage (12) — Key Widgets

- Hero section: `e916bb8` (padding now 60/40)
- Hero column: `2365a25b`
- H1: `1696de30` "Next Gen. Industrial Partner"
- Hero intro: `223ff102`
- 5 SX service cards: `3f586b9` (NEW, replaced 4-column icon-boxes)
- Bottom intro: `47520221`
- Social icons: `208da1c7` (has WA `wa.me/6285835672476`)
- Free Consultation button: `3f160523`
- Stats Bar text-editor: `50680e6` (inside section inserted at position 1)
- "Products" sub-eyebrow: `ec7caec`
- "Trusted By" sub-eyebrow: `2b673f7` (column `5c2c373` now dark callout `#0E3942`)
- "Portfolio" sub-eyebrow: `362468c`

## Portfolio (839) — Key Widget
- Hero H1: `6ab2ba6` "Portfolio"
- Main content text-editor: `13eb8f6` (contains everything inline)

## Internship (1127) — Key Widget
- Single text-editor: `fc46ef1` (entire page content inline)
