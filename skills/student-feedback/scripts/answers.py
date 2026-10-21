"""Print each slide's text boxes; flag response slides (NOTES/DRAFT markers) and their non-boilerplate text."""
import json, re, sys
raw = json.load(open(sys.argv[1]))
slides = (raw.get('content') or raw).get('slides', [])
BOILER = {'your answer — then your revision', 'your first answer', 'your revised answer',
          'think first. discuss with a partner. then write.', 'your reasoning and revision',
          'write privately first. discuss after your first answer is recorded.'}
def texts(el):
    out = []
    sh = el.get('shape', {}).get('text')
    if sh:
        out.append(''.join(t.get('textRun', {}).get('content', '') for t in sh.get('textElements', [])))
    for row in el.get('table', {}).get('tableRows', []):
        for cell in row.get('tableCells', []):
            t = cell.get('text')
            if t: out.append(''.join(x.get('textRun', {}).get('content', '') for x in t.get('textElements', [])))
    for ch in el.get('elementGroup', {}).get('children', []):
        out += texts(ch)
    return out
mode = sys.argv[2] if len(sys.argv) > 2 else 'answers'
prev_prompt = ''
for i, s in enumerate(slides, 1):
    boxes = [t.strip() for el in s.get('pageElements', []) for t in texts(el) if t.strip()]
    joined = '\n'.join(boxes)
    marks = re.findall(r'\[\[(?:NOTES|DRAFT|OPTIONAL|BANK):[^\]]+\]\]', joined)
    if mode == 'all':
        print(f'--- slide {i}'); print(joined[:1500]); continue
    if not marks:
        prev_prompt = re.sub(r'\s+', ' ', joined)[:420]
        continue
    student = [b for b in boxes if b.lower() not in BOILER and not re.fullmatch(r'(\[\[[^\]]+\]\]\s*)+', b)
               and not b.lower().startswith('critical aspect:')]
    print(f'=== slide {i} {" ".join(sorted(set(m.split(":")[2].rstrip("]") for m in marks if m.count(":")>=2)))}')
    print('  PROMPT:', prev_prompt)
    for b in student:
        print('  >>', re.sub(r'\s+', ' ', b)[:900])
