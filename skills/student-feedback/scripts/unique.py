"""Per marker slide, print each deck's lines that are not shared template text.
usage: unique.py name=path [name=path ...]  (paths are Slides JSON dumps or answers.py 'all' dumps)"""
import json, re, sys, collections
def slides_of(path):
    raw = json.load(open(path)); slides = (raw.get('content') or raw).get('slides', [])
    out = []
    def texts(el):
        r = []
        sh = el.get('shape', {}).get('text')
        if sh: r.append(''.join(t.get('textRun', {}).get('content', '') for t in sh.get('textElements', [])))
        for row in el.get('table', {}).get('tableRows', []):
            for c in row.get('tableCells', []):
                if c.get('text'): r.append(''.join(x.get('textRun', {}).get('content', '') for x in c['text'].get('textElements', [])))
        for ch in el.get('elementGroup', {}).get('children', []): r += texts(ch)
        return r
    for s in slides:
        boxes = [t for el in s.get('pageElements', []) for t in texts(el)]
        out.append(boxes)
    return out
def key(boxes):
    m = re.findall(r'\[\[(?:NOTES|DRAFT|OPTIONAL|BANK):[^:\]]+:([^\]]+)\]\]', '\n'.join(boxes))
    return ' '.join(sorted(set(m)))
def lines(boxes):
    out = []
    for b in boxes:
        b = re.sub(r'\[\[[^\]]+\]\]', '', b)
        for l in re.split(r'[\n\v]+', b):
            l = re.sub(r'\s+', ' ', l).strip()
            if l: out.append(l)
    return out
decks = {}
for arg in sys.argv[1:]:
    name, path = arg.split('=', 1)
    decks[name] = {key(b): lines(b) for b in slides_of(path) if key(b)}
count = collections.Counter()
for d in decks.values():
    for k, ls in d.items():
        for l in set(ls): count[(k, l)] += 1
n = len(decks)
for name, d in decks.items():
    print(f'################ {name}')
    for k, ls in d.items():
        uniq = [l for l in ls if count[(k, l)] < max(2, n)] if n > 1 else ls
        if uniq:
            print(f'[{k}]'); [print('   ', l[:700]) for l in uniq]
