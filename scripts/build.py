"""Build the HTML entry point and CSV exports from the preserved final spec."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = json.loads((ROOT / 'specs/dashboard.vl.json').read_text())
panels = spec['vconcat']
tables = {
    'recent_immigrants_by_citizenship.csv': panels[0]['hconcat'][0]['data']['values'],
    'recent_immigrants_age_by_citizenship.csv': panels[0]['hconcat'][1]['data']['values'],
    'recent_immigrants_housing_tenure.csv': panels[1]['hconcat'][0]['data']['values'],
    'recent_immigrants_rent_by_citizenship.csv': panels[1]['hconcat'][1]['layer'][1]['data']['values'],
}
(ROOT / 'data').mkdir(exist_ok=True)
for filename, rows in tables.items():
    with (ROOT / 'data' / filename).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

# Keep the original renderer versions and embedded data; improve the HTML wrapper.
original = (ROOT / 'originals/visualization.html').read_text()
page = original.replace('<html>', '<html lang="en">').replace('<head>', '''<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ireland Census Visualisation | James McClatchie</title>
  <style>body { margin: 24px; font-family: system-ui, sans-serif; } #vis { overflow-x: auto; }</style>''').replace('<div id="vis"/>', '<div id="vis"></div>')
start = page.index('const spec = ') + len('const spec = ')
end = page.index(';\n    vegaEmbed', start)
page = page[:start] + json.dumps(spec, ensure_ascii=False, indent=2) + page[end:]
(ROOT / 'index.html').write_text(page, encoding='utf-8')
print('Built index.html and four CSV exports.')
