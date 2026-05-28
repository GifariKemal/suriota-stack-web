import urllib.request
import json

req = urllib.request.Request('https://suriota.com/wp-json/aioseo/v1/')
resp = urllib.request.urlopen(req)
d = json.loads(resp.read().decode())
routes = d.get('routes', {})
for r in list(routes.keys())[:30]:
    print(r)
