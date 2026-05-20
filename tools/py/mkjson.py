import json

with open('internship_content.html', 'r', encoding='utf-8') as f:
    html = f.read()

payload = {
    "jsonrpc": "2.0",
    "id": 63,
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

with open('u4.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

print("OK, html len:", len(html))
