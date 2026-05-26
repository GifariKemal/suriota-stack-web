"""Build FAQPage JSON-LD schema widgets from existing FAQ widget HTML.

Reads `design-system/components/{lang}/p{N}-faq.html` for each pillar/lang
and emits `design-system/components/{lang}/p{N}-faqschema.html` containing
a single <script type="application/ld+json"> FAQPage block whose Q&A text
matches the visible FAQ exactly (Google policy requirement).
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPONENTS = ROOT / "design-system" / "components"

LANGS = [("", ""), ("id/", "id"), ("zh/", "zh")]
PILLARS = [1, 2, 3, 4, 5]

# Question is inside the first <span> child of the .sxp-faq__btn button.
BTN_RE = re.compile(
    r'<button[^>]*class="sxp-faq__btn"[^>]*>\s*<span>(.+?)</span>',
    re.S,
)
# Answer paragraph inside the panel div.
PANEL_RE = re.compile(
    r'<div[^>]*class="sxp-faq__panel"[^>]*>\s*<p class="sxp-body"[^>]*>(.+?)</p>',
    re.S,
)


def _clean(text: str) -> str:
    """Strip inline HTML tags, decode entities, collapse whitespace."""
    # Drop inline tags (e.g. <a>, <strong>) but keep their inner text.
    no_tags = re.sub(r"<[^>]+>", "", text)
    decoded = html.unescape(no_tags)
    return re.sub(r"\s+", " ", decoded).strip()


def extract(faq_path: Path) -> list[tuple[str, str]]:
    raw = faq_path.read_text(encoding="utf-8")
    questions = [_clean(q) for q in BTN_RE.findall(raw)]
    answers = [_clean(a) for a in PANEL_RE.findall(raw)]
    if len(questions) != len(answers):
        raise ValueError(
            f"{faq_path}: question/answer count mismatch "
            f"({len(questions)} vs {len(answers)})"
        )
    return list(zip(questions, answers))


def build_schema(pairs: list[tuple[str, str]]) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in pairs
        ],
    }
    body = json.dumps(schema, indent=2, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{body}\n</script>\n'


def main() -> None:
    summary: list[str] = []
    for lang_dir, lang_label in LANGS:
        for n in PILLARS:
            src = COMPONENTS / lang_dir / f"p{n}-faq.html"
            if not src.exists():
                summary.append(f"SKIP {lang_label or 'en'} P{n}: missing {src}")
                continue
            pairs = extract(src)
            out = COMPONENTS / lang_dir / f"p{n}-faqschema.html"
            out.write_text(build_schema(pairs), encoding="utf-8")
            summary.append(
                f"OK   {lang_label or 'en':>2} P{n}: {len(pairs)} Q&A -> {out.relative_to(ROOT)}"
            )
    print("\n".join(summary))


if __name__ == "__main__":
    main()
