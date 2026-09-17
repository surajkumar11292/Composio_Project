import json

with open('data/apps_research.json', 'r', encoding='utf-8') as f:
    apps = json.load(f)

print('Total apps:', len(apps))
print()

for app in apps:
    issues = []
    if 'simulation' in app.get('raw_notes','').lower():
        issues.append('MOCK raw_notes')
    if 'fallback' in app.get('raw_notes','').lower():
        issues.append('FALLBACK in raw_notes')
    if not app.get('evidence_urls'):
        issues.append('NO evidence_urls')
    if 'example.com' in str(app.get('docs_url','')):
        issues.append('FAKE docs_url')
    if not app.get('auth_methods'):
        issues.append('NO auth_methods')
    if not app.get('docs_url'):
        issues.append('NO docs_url')
    if not app.get('category'):
        issues.append('NO category')
    if not app.get('buildability'):
        issues.append('NO buildability')
    for ev in app.get('evidence_urls', []):
        if 'example.com' in ev:
            issues.append('FAKE evidence_url: ' + ev)

    name = app['name']
    auth = ','.join(app.get('auth_methods', []))
    tier = app.get('access_tier', '')
    verdict = app.get('buildability', '')
    ev_count = len(app.get('evidence_urls', []))
    status = 'PASS' if not issues else 'FAIL: ' + ', '.join(issues)
    print(f"  [{status}] {name}")
    print(f"         auth={auth} | tier={tier} | verdict={verdict} | evidence_urls={ev_count}")
    print()

print('--- REQUIRED FIELDS CHECK ---')
required = ['id','name','category','auth_methods','access_tier','docs_url','api_type','has_mcp_server','buildability','evidence_urls','raw_notes']
for app in apps:
    missing = [f for f in required if not app.get(f) and app.get(f) != False]
    if missing:
        print(f"MISSING in {app['name']}: {missing}")
    else:
        print(f"  {app['name']}: all required fields present")
