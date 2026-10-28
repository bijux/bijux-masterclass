#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'.progress.json'
modules=[]
for p in sorted(ROOT.glob('[0-9][0-9]-*/course-book/module-*/index.md')):
    num=int(p.parent.name.split('-')[1])
    title=p.read_text().splitlines()[0].split('—',1)[-1].strip()
    modules.append((num,title))
state={'done':[]} if not STATE.exists() else json.loads(STATE.read_text())
done=set(state.get('done',[]))
cmd=sys.argv[1] if len(sys.argv)>1 else 'show'
if cmd=='done':
    if len(sys.argv)!=3: raise SystemExit('usage: progress.py done MODULE_NUMBER')
    n=int(sys.argv[2]);
    if n not in {x for x,_ in modules}: raise SystemExit('unknown module')
    done.add(n); STATE.write_text(json.dumps({'done':sorted(done)},indent=2)+'\n')
elif cmd=='undo':
    n=int(sys.argv[2]); done.discard(n); STATE.write_text(json.dumps({'done':sorted(done)},indent=2)+'\n')
elif cmd=='reset':
    STATE.write_text('{"done": []}\n'); done=set()
elif cmd!='show': raise SystemExit('commands: show, done N, undo N, reset')
total=len(modules)
filled=round(len(done)/total*30)
print(f"[{'#'*filled}{'-'*(30-filled)}] {len(done)}/{total} modules ({len(done)/total:.0%})")
next_mod=next(((n,t) for n,t in modules if n not in done),None)
if next_mod: print(f'Next: {next_mod[0]:02d} — {next_mod[1]}')
else: print(f'All {total} modules marked complete.')
