"""
Audit live ZH pages for remaining English content - v2 with correct URLs.
"""
import requests, re

PAGES = [
    (5450, 'https://suriota.com/zh/guanyu-women/', 'About'),
    (5451, 'https://suriota.com/zh/zidonghua/', 'Automation'),
    (5452, 'https://suriota.com/zh/dianqi-gongcheng/', 'Electrical'),
    (5453, 'https://suriota.com/zh/kezaisheng-nengyuan/', 'Renewable'),
    (5454, 'https://suriota.com/zh/anli/', 'Portfolio'),
    (5456, 'https://suriota.com/zh/modbus-gateway/', 'Modbus Gateway'),
    (5457, 'https://suriota.com/zh/shuichuli/', 'Water'),
    (5465, 'https://suriota.com/zh/lianxi/', 'Contact'),
    (5466, 'https://suriota.com/zh/yinsi-zhengce/', 'Privacy'),
    (5467, 'https://suriota.com/zh/fuwu-tiaokuan/', 'Terms'),
    (5468, 'https://suriota.com/zh/iot/', 'IoT'),
    (5469, 'https://suriota.com/zh/xitong-jicheng/', 'Integration'),
    (5470, 'https://suriota.com/zh/shuzihua-zixun/', 'Consulting'),
    (5471, 'https://suriota.com/zh/rengong-zhineng/', 'AI'),
    (5472, 'https://suriota.com/zh/shujufenxi/', 'Analytics'),
    (5473, 'https://suriota.com/zh/saas/', 'SaaS'),
]

# Regex to find English sentences (at least 3 consecutive English words)
en_sentence = re.compile(r'[A-Za-z][A-Za-z\s,\'\-]{2,}[A-Za-z]')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for pid, url, name in PAGES:
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        html = r.text

        # Remove script/style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.S)

        # Remove JSON-LD
        html = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html, flags=re.S)

        # Get visible text
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)

        # Find English sentences
        matches = en_sentence.findall(text)
        filtered = []
        for m in matches:
            m = m.strip()
            words = m.split()
            if len(words) >= 3:
                # Skip known technical terms / single words patterns
                skip_terms = ['SVG', 'viewBox', 'xmlns', 'path', 'rect', 'circle', 'line', 'polyline']
                if not any(s.lower() in m.lower() for s in skip_terms):
                    filtered.append(m)

        # Deduplicate
        filtered = list(dict.fromkeys(filtered))

        if filtered:
            print(f'\n=== {name} (Page {pid}) ===')
            print(f'URL: {url}')
            for m in filtered[:15]:
                print(f'  EN: {m}')
        else:
            print(f'OK: {name} (Page {pid}) - No English detected')

    except Exception as e:
        print(f'ERROR: {name} (Page {pid}): {e}')

print('\nDone.')
