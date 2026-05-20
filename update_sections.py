import json

sections = [
    {
        "id": 103,
        "element_id": "11ed93e",
        "name": "Hero Section",
        "settings": {
            "padding": {"unit": "px", "top": "10", "right": "0", "bottom": "10", "left": "0", "isLinked": False},
            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
        }
    },
    {
        "id": 104,
        "element_id": "dd5da11",
        "name": "Poster Section",
        "settings": {
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
        }
    },
    {
        "id": 105,
        "element_id": "170400c",
        "name": "Main Content Section",
        "settings": {
            "padding": {"unit": "px", "top": "10", "right": "0", "bottom": "10", "left": "0", "isLinked": False},
            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
        }
    }
]

for s in sections:
    payload = {
        "jsonrpc": "2.0",
        "id": s["id"],
        "method": "tools/call",
        "params": {
            "name": "elementor-mcp-update-element",
            "arguments": {
                "post_id": 1127,
                "element_id": s["element_id"],
                "settings": s["settings"]
            }
        }
    }
    with open(f'section_{s["element_id"]}.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    print(f"Created: section_{s['element_id']}.json")
