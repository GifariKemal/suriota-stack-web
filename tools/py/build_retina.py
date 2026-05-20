import json

with open('current_retina.html','r',encoding='utf-8') as f:
    html = f.read()

# Font size increases for retina readability
replacements = [
    # H1 - bigger
    ('font-size:clamp(28px,5vw,42px)', 'font-size:clamp(32px,5vw,48px)'),
    
    # H2 section headings - bigger
    ('font-size:22px', 'font-size:24px'),
    
    # Body text - minimum 16px
    ('font-size:clamp(14px,2vw,16px)', 'font-size:clamp(15px,2vw,17px)'),
    
    # Position card titles
    ('font-size:14px;font-weight:700;color:#205B69;margin:0 0 6px', 'font-size:16px;font-weight:700;color:#205B69;margin:0 0 8px'),
    
    # Position card descriptions
    ('font-size:12px;color:#666;line-height:1.5', 'font-size:14px;color:#666;line-height:1.5'),
    
    # Tech stack badges
    ('font-size:12px;font-weight:600;padding:5px 12px', 'font-size:13px;font-weight:600;padding:6px 14px'),
    
    # Info pills
    ('font-size:12px;font-weight:600;padding:6px 14px', 'font-size:13px;font-weight:600;padding:7px 16px'),
    
    # Collapsible summary
    ('font-size:18px;font-weight:700', 'font-size:20px;font-weight:700'),
    
    # Collapsible badge
    ('font-size:12px;color:#3C7D47', 'font-size:13px;color:#3C7D47'),
    
    # List items in qualifications
    ('font-size:13px;line-height:1.7', 'font-size:15px;line-height:1.7'),
    
    # Document list
    ('font-size:13px;line-height:1.7', 'font-size:15px;line-height:1.7'),
    
    # Benefit card titles
    ('font-size:13px;font-weight:700', 'font-size:15px;font-weight:700'),
    
    # Benefit card descriptions
    ('font-size:12px;color:#666;line-height:1.4', 'font-size:14px;color:#666;line-height:1.4'),
    
    # CTA heading
    ('font-size:clamp(18px,3vw,26px)', 'font-size:clamp(20px,3vw,28px)'),
    
    # CTA body
    ('font-size:clamp(13px,1.5vw,15px)', 'font-size:clamp(14px,1.5vw,16px)'),
    
    # Step cards
    ('padding:6px 12px;border-radius:5px;font-size:12px', 'padding:8px 16px;border-radius:6px;font-size:14px'),
    
    # Main CTA button
    ('font-size:15px;font-weight:700;padding:12px 32px', 'font-size:16px;font-weight:700;padding:14px 36px'),
    
    # Kenapa SURIOTA paragraph
    ('font-size:14px;line-height:1.7', 'font-size:15px;line-height:1.7'),
    
    # Tech Stack heading
    ('font-size:15px;font-weight:700', 'font-size:16px;font-weight:700'),
]

for old, new in replacements:
    html = html.replace(old, new)

# Increase padding for cards
html = html.replace('padding:16px;text-align:center', 'padding:20px 16px;text-align:center')

# Increase gap for position cards
html = html.replace('display:flex;flex-wrap:wrap;gap:12px;', 'display:flex;flex-wrap:wrap;gap:16px;')

# Increase section margins
html = html.replace('margin:0 auto 24px;', 'margin:0 auto 32px;')
html = html.replace('margin:0 auto 32px;', 'margin:0 auto 36px;')

payload = {
    "jsonrpc": "2.0",
    "id": 131,
    "method": "tools/call",
    "params": {
        "name": "elementor-mcp-update-element",
        "arguments": {
            "post_id": 1127,
            "element_id": "fc46ef1",
            "settings": {
                "editor": html
            }
        }
    }
}

with open('u_retina.json','w',encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

print('Retina version created, length:', len(html))
