"""Performance + switcher flicker diagnosis."""
import asyncio, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def measure_page(page, url):
    """Capture network timing + render metrics."""
    metrics = {'url': url, 'requests': 0, 'sizes': {}, 'slow_requests': []}
    big_requests = []

    page.on('response', lambda r: big_requests.append(r))

    t0 = time.time()
    resp = await page.goto(url, wait_until='networkidle', timeout=60000)
    t_load = time.time() - t0

    metrics['ttfb_ms'] = await page.evaluate('performance.timing.responseStart - performance.timing.requestStart')
    metrics['dom_content_loaded_ms'] = await page.evaluate('performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart')
    metrics['load_event_ms'] = await page.evaluate('performance.timing.loadEventEnd - performance.timing.navigationStart')
    metrics['transfer_size'] = await page.evaluate('performance.getEntriesByType("navigation")[0]?.transferSize || 0')
    metrics['encoded_size'] = await page.evaluate('performance.getEntriesByType("navigation")[0]?.encodedBodySize || 0')

    # Resource breakdown
    res_data = await page.evaluate('''() => {
        const res = performance.getEntriesByType('resource');
        const by_type = {};
        let total_size = 0;
        const big = [];
        res.forEach(r => {
            const type = r.initiatorType || 'other';
            if (!by_type[type]) by_type[type] = { count: 0, size: 0, duration: 0 };
            by_type[type].count++;
            by_type[type].size += r.transferSize || 0;
            by_type[type].duration += r.duration || 0;
            total_size += r.transferSize || 0;
            if ((r.duration || 0) > 500 || (r.transferSize || 0) > 200000) {
                big.push({
                    name: r.name.slice(-80),
                    duration: Math.round(r.duration),
                    size_kb: Math.round((r.transferSize || 0) / 1024),
                    type
                });
            }
        });
        return { by_type, total_size, big, total_count: res.length };
    }''')

    metrics['total_load_time'] = round(t_load * 1000)
    metrics['resource_summary'] = res_data['by_type']
    metrics['total_requests'] = res_data['total_count']
    metrics['total_transfer_kb'] = round(res_data['total_size'] / 1024)
    metrics['slow_or_heavy'] = res_data['big'][:10]
    metrics['cache_hit_header'] = resp.headers.get('cf-cache-status') if resp else None
    metrics['x_cache'] = resp.headers.get('x-cache') if resp else None

    return metrics


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})

        # 1) Performance — fresh load (no cache)
        print('=== PERFORMANCE — Homepage (fresh) ===')
        page = await ctx.new_page()
        m = await measure_page(page, 'https://suriota.com/?perf=' + str(int(time.time())))
        print(f"  TTFB         : {m['ttfb_ms']}ms")
        print(f"  DOMContentLoaded: {m['dom_content_loaded_ms']}ms")
        print(f"  Load event   : {m['load_event_ms']}ms")
        print(f"  Total wall   : {m['total_load_time']}ms")
        print(f"  Transfer     : {m['total_transfer_kb']} KB")
        print(f"  Requests     : {m['total_requests']}")
        print(f"  Cloudflare   : cf-cache-status={m['cache_hit_header']} x-cache={m['x_cache']}")
        print(f"  By type:")
        for typ, d in m['resource_summary'].items():
            print(f"    {typ:12} count={d['count']:3} size={round(d['size']/1024):4}KB dur_total={round(d['duration'])}ms")
        print(f"  Slow/heavy resources:")
        for r in m['slow_or_heavy']:
            print(f"    [{r['type']:8}] {r['duration']:4}ms {r['size_kb']:4}KB {r['name']}")
        await page.close()

        # 2) Performance — second hit (cached)
        print('\n=== PERFORMANCE — Homepage (second hit, cached) ===')
        page = await ctx.new_page()
        m2 = await measure_page(page, 'https://suriota.com/')
        print(f"  TTFB         : {m2['ttfb_ms']}ms")
        print(f"  DOMContentLoaded: {m2['dom_content_loaded_ms']}ms")
        print(f"  Load event   : {m2['load_event_ms']}ms")
        print(f"  Total wall   : {m2['total_load_time']}ms")
        print(f"  Cloudflare   : cf-cache-status={m2['cache_hit_header']}")
        await page.close()

        # 3) Switcher flicker investigation
        print('\n=== SWITCHER FLICKER ===')
        page = await ctx.new_page()
        # Track when sx-lang-switcher appears/disappears via MutationObserver
        await page.goto('https://suriota.com/', wait_until='domcontentloaded', timeout=30000)
        # Inject observer immediately
        observer_data = await page.evaluate('''() => new Promise((resolve) => {
            const events = [];
            const start = performance.now();
            const observer = new MutationObserver(muts => {
                muts.forEach(m => {
                    m.addedNodes.forEach(n => {
                        if (n.nodeType === 1 && (n.matches?.('.sx-lang-switcher') || n.querySelector?.('.sx-lang-switcher'))) {
                            events.push({ t: Math.round(performance.now() - start), type: 'ADD', target: n.tagName });
                        }
                    });
                    m.removedNodes.forEach(n => {
                        if (n.nodeType === 1 && (n.matches?.('.sx-lang-switcher') || n.querySelector?.('.sx-lang-switcher'))) {
                            events.push({ t: Math.round(performance.now() - start), type: 'REMOVE', target: n.tagName });
                        }
                    });
                });
            });
            observer.observe(document.body, { childList: true, subtree: true });

            setTimeout(() => {
                observer.disconnect();
                const sw = document.querySelector('.sx-lang-switcher');
                resolve({
                    events,
                    final_present: !!sw,
                    final_visible: sw ? getComputedStyle(sw).display !== 'none' : false,
                    final_opacity: sw ? getComputedStyle(sw).opacity : null,
                    final_position: sw ? {
                        position: getComputedStyle(sw).position,
                        top: getComputedStyle(sw).top,
                        bottom: getComputedStyle(sw).bottom,
                        right: getComputedStyle(sw).right,
                        left: getComputedStyle(sw).left,
                        zIndex: getComputedStyle(sw).zIndex
                    } : null
                });
            }, 5000);
        })''')
        print(f"  Mutation events: {len(observer_data['events'])}")
        for e in observer_data['events']:
            print(f"    t={e['t']}ms {e['type']} {e['target']}")
        print(f"  Final present: {observer_data['final_present']}")
        print(f"  Final visible: {observer_data['final_visible']} opacity={observer_data['final_opacity']}")
        print(f"  Final position: {observer_data['final_position']}")
        await page.close()

        # 4) Compare TTFB across pages
        print('\n=== TTFB comparison ===')
        for url, lbl in [
            ('https://suriota.com/', 'EN home'),
            ('https://suriota.com/id/beranda/', 'ID home'),
            ('https://suriota.com/about-us/', 'EN about'),
            ('https://suriota.com/portfolio/', 'EN portfolio'),
        ]:
            page = await ctx.new_page()
            t0 = time.time()
            try:
                resp = await page.goto(url + '?cb=' + str(int(time.time())), wait_until='domcontentloaded', timeout=30000)
                ttfb = await page.evaluate('performance.timing.responseStart - performance.timing.requestStart')
                wall = round((time.time() - t0) * 1000)
                cf = resp.headers.get('cf-cache-status', '?') if resp else '?'
                print(f"  {lbl:20} TTFB={ttfb:4}ms wall={wall:4}ms cf={cf}")
            except Exception as e:
                print(f"  {lbl}: ERR {e}")
            await page.close()

        await b.close()

asyncio.run(main())
