from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width':1440,'height':900})
    page = ctx.new_page()
    page.goto('https://suriota.com/digital-transformation-consulting/', wait_until='networkidle', timeout=45000)

    # Find which element(s) contain em-dash
    locations = page.evaluate("""() => {
      const main = document.querySelector('main');
      if (!main) return [];
      const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT, null);
      const out = [];
      let n;
      while ((n = walker.nextNode())) {
        if (n.nodeValue && n.nodeValue.includes('\\u2014')) {
          const parent = n.parentElement;
          out.push({
            tag: parent ? parent.tagName : '?',
            cls: parent ? parent.className : '?',
            id: parent ? parent.id : '',
            snippet: n.nodeValue.trim().slice(0, 200)
          });
        }
      }
      return out;
    }""")
    for loc in locations:
        print(loc)
    ctx.close()
    b.close()
