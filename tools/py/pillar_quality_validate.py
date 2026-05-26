"""Phase Q — Quality Validation for 15 pillar pages.

- Schema validation (structural; per @type required fields)
- SEO scorecard re-scoring on 5 EN pillars vs the SEO-AUDIT-2026-05-24.md baseline
- Schema validity check on ID + ZH pillars (no scoring; just JSON-LD parseability + types)

Outputs to audit/pillar-v2-snapshots/_tmp/pillar_quality.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from pillar_env import ROOT, assert_allowed

EN_URLS = {
    5554: "https://suriota.com/industrial-iot-system-integration/",
    5555: "https://suriota.com/ai-industrial-analytics/",
    5556: "https://suriota.com/digital-transformation-consulting/",
    5557: "https://suriota.com/industrial-engineering-automation/",
    5558: "https://suriota.com/surge-saas-platform/",
}
ID_URLS = {
    5566: "https://suriota.com/id/iot-industri-integrasi-sistem/",
    5567: "https://suriota.com/id/ai-analitik-industri/",
    5568: "https://suriota.com/id/konsultasi-transformasi-digital/",
    5569: "https://suriota.com/id/teknik-industri-otomasi/",
    5570: "https://suriota.com/id/platform-saas-surge/",
}
ZH_URLS = {
    5571: "https://suriota.com/zh/gongye-wulianwang-jicheng/",
    5572: "https://suriota.com/zh/ai-gongye-fenxi/",
    5573: "https://suriota.com/zh/shuzihua-zhuanxing-zixun/",
    5574: "https://suriota.com/zh/gongye-gongcheng-zidonghua/",
    5575: "https://suriota.com/zh/surge-saas-pingtai/",
}

PILLAR_SLUGS = [
    "industrial-iot-system-integration",
    "ai-industrial-analytics",
    "digital-transformation-consulting",
    "industrial-engineering-automation",
    "surge-saas-platform",
]

# Old baseline scores from SEO-AUDIT-2026-05-24.md
OLD_SCORES = {5554: 72, 5555: 74, 5556: 74, 5557: 74, 5558: 72}


def validate_schema_item(item: dict) -> list[str]:
    """Return a list of human-readable error strings for one parsed JSON-LD item."""
    errors: list[str] = []
    t = item.get("@type", "UNKNOWN")
    if isinstance(t, list):
        t_check = t
    else:
        t_check = [t]

    def need(keys: list[str]):
        for k in keys:
            if k not in item:
                errors.append(f"{t} missing required field: {k}")

    if "Service" in t_check:
        need(["name", "description", "provider", "serviceType"])
        # provider should have name + url
        provider = item.get("provider")
        if isinstance(provider, dict):
            for k in ("name", "url"):
                if k not in provider:
                    errors.append(f"Service.provider missing: {k}")
    if "SoftwareApplication" in t_check:
        need(["name", "applicationCategory", "operatingSystem", "offers"])
    if "Organization" in t_check:
        need(["name", "url"])
    if "WebSite" in t_check:
        need(["name", "url"])
    if "WebPage" in t_check:
        # WebPage flexible; just sanity-check url if present
        pass
    if "BreadcrumbList" in t_check:
        if "itemListElement" not in item:
            errors.append("BreadcrumbList missing itemListElement")
    return errors


def extract_ldjson(page) -> list[tuple[str, dict | list, list[str]]]:
    """Returns [(raw_text, parsed_or_None, errors)] per script tag."""
    blocks = page.locator('script[type="application/ld+json"]').all_text_contents()
    out = []
    for raw in blocks:
        raw = raw.strip()
        if not raw:
            continue
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as e:
            out.append((raw[:120], None, [f"INVALID JSON: {e}"]))
            continue
        items = parsed if isinstance(parsed, list) else [parsed]
        # Also handle "@graph" wrappers
        flat = []
        for it in items:
            if isinstance(it, dict) and "@graph" in it and isinstance(it["@graph"], list):
                flat.extend(it["@graph"])
            else:
                flat.append(it)
        errors = []
        for it in flat:
            if isinstance(it, dict):
                errors.extend(validate_schema_item(it))
        out.append((raw[:120], parsed, errors))
    return out


def get_main_text_and_counts(page):
    """Use document.querySelector('main') if available, else 'article', else 'body'."""
    text = page.evaluate(
        """
        () => {
          const el = document.querySelector('main') || document.querySelector('article') || document.body;
          return el ? el.innerText : '';
        }
        """
    )
    words = len([w for w in re.split(r"\s+", text) if w.strip()])
    # H1/H2/H3 scoped to main (or article or body)
    counts = page.evaluate(
        """
        () => {
          const el = document.querySelector('main') || document.querySelector('article') || document.body;
          if (!el) return {h1:0,h2:0,h3:0};
          return {
            h1: el.querySelectorAll('h1').length,
            h2: el.querySelectorAll('h2').length,
            h3: el.querySelectorAll('h3').length,
          };
        }
        """
    )
    return text, words, counts


def get_links(page, current_slug):
    data = page.evaluate(
        """
        () => {
          const el = document.querySelector('main') || document.querySelector('article') || document.body;
          if (!el) return [];
          return Array.from(el.querySelectorAll('a')).map(a => a.getAttribute('href') || '');
        }
        """
    )
    internal = 0
    external = 0
    cross_pillar = 0
    pillar_slugs = [s for s in PILLAR_SLUGS if s != current_slug]
    for href in data:
        if not href:
            continue
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
            continue
        if href.startswith("/") or "suriota.com" in href:
            internal += 1
            for ps in pillar_slugs:
                if ps in href:
                    cross_pillar += 1
                    break
        elif href.startswith("http"):
            external += 1
    return internal, external, cross_pillar


def get_meta(page):
    data = page.evaluate(
        """
        () => {
          const md = document.querySelector('meta[name="description"]');
          const vp = document.querySelector('meta[name="viewport"]');
          const og = Array.from(document.querySelectorAll('meta[property^="og:"]')).map(m => m.getAttribute('property'));
          const tw = Array.from(document.querySelectorAll('meta[name^="twitter:"]')).map(m => m.getAttribute('name'));
          const canonical = document.querySelector('link[rel="canonical"]');
          const hreflangs = Array.from(document.querySelectorAll('link[rel="alternate"][hreflang]')).map(l => l.getAttribute('hreflang'));
          return {
            title: document.title || '',
            meta_desc: md ? md.getAttribute('content') || '' : '',
            viewport: vp ? vp.getAttribute('content') || '' : '',
            og: og,
            tw: tw,
            canonical: canonical ? canonical.getAttribute('href') || '' : '',
            hreflangs: hreflangs,
          };
        }
        """
    )
    return data


def get_alt_coverage(page):
    data = page.evaluate(
        """
        () => {
          const el = document.querySelector('main') || document.querySelector('article') || document.body;
          if (!el) return {total:0, with_alt:0};
          const imgs = el.querySelectorAll('img');
          let with_alt = 0;
          imgs.forEach(i => { const a = (i.getAttribute('alt') || '').trim(); if (a) with_alt++; });
          return {total: imgs.length, with_alt};
        }
        """
    )
    if data["total"] == 0:
        return 100
    return round(100 * data["with_alt"] / data["total"])


def probe(url, pid, current_slug, score=True):
    """Probe one URL and return a dict of metrics."""
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=45000)
        except Exception as e:
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
            except Exception as e2:
                b.close()
                return {"pid": pid, "url": url, "error": f"{e2}"}
        # Reveal hidden content
        page.evaluate(
            "document.querySelectorAll('.sxp-reveal').forEach(el => el.classList.add('is-visible'));"
        )
        page.wait_for_timeout(400)

        text, words, counts = get_main_text_and_counts(page)
        internal, external, cross_pillar = get_links(page, current_slug)
        meta = get_meta(page)
        alt_pct = get_alt_coverage(page)
        ld = extract_ldjson(page)
        b.close()

    ld_types = []
    ld_errors_all: list[str] = []
    for raw, parsed, errors in ld:
        ld_errors_all.extend(errors)
        if parsed is None:
            continue
        items = parsed if isinstance(parsed, list) else [parsed]
        for it in items:
            if isinstance(it, dict):
                if "@graph" in it and isinstance(it["@graph"], list):
                    for g in it["@graph"]:
                        if isinstance(g, dict):
                            ld_types.append(g.get("@type", "?"))
                else:
                    ld_types.append(it.get("@type", "?"))

    result = {
        "pid": pid,
        "url": url,
        "words": words,
        "h1": counts["h1"],
        "h2": counts["h2"],
        "h3": counts["h3"],
        "internal": internal,
        "external": external,
        "cross_pillar": cross_pillar,
        "title": meta["title"],
        "title_len": len(meta["title"]),
        "meta_desc": meta["meta_desc"],
        "meta_len": len(meta["meta_desc"]),
        "og_count": len(meta["og"]),
        "tw_count": len(meta["tw"]),
        "canonical": meta["canonical"],
        "hreflangs": meta["hreflangs"],
        "viewport": meta["viewport"],
        "alt_pct": alt_pct,
        "ld_count": len(ld),
        "ld_types": ld_types,
        "ld_errors": ld_errors_all,
    }

    if score:
        # Same axes/thresholds as SEO-AUDIT-2026-05-24.md
        s_content = 25 if words >= 1500 else (15 if words >= 1000 else (10 if words >= 600 else 5))
        s_headings = 10 if counts["h1"] == 1 and counts["h2"] >= 3 else 5
        s_internal = 15 if internal >= 10 else (10 if internal >= 5 else 5)
        s_cross = 10 if cross_pillar >= 3 else (5 if cross_pillar >= 1 else 0)
        has_service = "Service" in ld_types or "SoftwareApplication" in ld_types
        s_schema = 15 if has_service and len(ld_types) >= 2 else (10 if has_service else 5)
        title_ok = 35 <= result["title_len"] <= 65
        meta_ok = 100 <= result["meta_len"] <= 180
        s_meta = 10 if title_ok and meta_ok else (7 if title_ok or meta_ok else 3)
        s_og = 5 if len(meta["og"]) >= 6 and len(meta["tw"]) >= 3 else 3
        s_alt = round(alt_pct / 20)
        s_mobile = 5 if "width=device-width" in meta["viewport"] else 2
        s_a11y = 5  # baseline maintained — verified Phase D

        breakdown = {
            "content": s_content,
            "headings": s_headings,
            "internal": s_internal,
            "cross_pillar": s_cross,
            "schema": s_schema,
            "meta": s_meta,
            "og_tw": s_og,
            "alt": s_alt,
            "mobile": s_mobile,
            "a11y": s_a11y,
        }
        result["score"] = sum(breakdown.values())
        result["breakdown"] = breakdown
        result["old_score"] = OLD_SCORES.get(pid)
    return result


def main():
    assert_allowed(5554)  # sanity-check scope lock
    out: dict = {"en": [], "id": [], "zh": []}

    print("=== EN pillars (full scoring) ===")
    for i, (pid, url) in enumerate(EN_URLS.items()):
        slug = PILLAR_SLUGS[i]
        print(f"  probing {pid} {url}")
        r = probe(url, pid, slug, score=True)
        out["en"].append(r)
        if "score" in r:
            print(f"    -> {r.get('score')}  words={r.get('words')}  ld_types={r.get('ld_types')}  errors={len(r.get('ld_errors', []))}")

    print("\n=== ID pillars (schema-only validity) ===")
    for i, (pid, url) in enumerate(ID_URLS.items()):
        slug = PILLAR_SLUGS[i]
        print(f"  probing {pid} {url}")
        r = probe(url, pid, slug, score=False)
        out["id"].append(r)
        print(f"    -> ld_types={r.get('ld_types')}  errors={len(r.get('ld_errors', []))}")

    print("\n=== ZH pillars (schema-only validity) ===")
    for i, (pid, url) in enumerate(ZH_URLS.items()):
        slug = PILLAR_SLUGS[i]
        print(f"  probing {pid} {url}")
        r = probe(url, pid, slug, score=False)
        out["zh"].append(r)
        print(f"    -> ld_types={r.get('ld_types')}  errors={len(r.get('ld_errors', []))}")

    out_dir = ROOT / "audit" / "pillar-v2-snapshots" / "_tmp"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "pillar_quality.json"
    out_file.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    # Summary
    en_scores = [r["score"] for r in out["en"] if "score" in r]
    if en_scores:
        avg = sum(en_scores) / len(en_scores)
        print(f"\nEN average: {avg:.1f}/100 (old baseline 73.2)")
    print(f"Wrote: {out_file}")


if __name__ == "__main__":
    main()
