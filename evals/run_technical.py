#!/usr/bin/env python3
"""Run deterministic contracts, regressions and actual Chromium/strict-QA integration.
No installation or external service calls. Visual release checks are separate.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--out',required=True)
p.add_argument('--node',required=True)
p.add_argument('--node-modules',required=True)
p.add_argument('--browsers',required=True)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
skill=root/'skills/cropmark'
out=Path(a.out).resolve()
if out.exists() and any(out.iterdir()):p.error('output directory must be new or empty')
out.mkdir(parents=True,exist_ok=True)
common=['--skill',str(skill),'--node',str(Path(a.node).resolve()),'--node-modules',str(Path(a.node_modules).resolve()),'--browsers',str(Path(a.browsers).resolve())]
commands=[('contracts',[sys.executable,str(root/'evals/test_contracts.py'),*common,'--out',str(out/'contracts')]),
          ('regressions',[sys.executable,str(root/'evals/test_regressions.py')]),
          ('html-integration',[sys.executable,str(root/'evals/test_html_v05.py'),*common,'--out',str(out/'html-integration')])]
results=[]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CM_SKILL=str(skill))
for name,argv in commands:
    result=subprocess.run(argv,cwd=root,env=env,capture_output=True,text=True,timeout=180)
    (out/(name+'.log')).write_text(result.stdout+result.stderr)
    evidence=out/name/'results.json'
    if evidence.exists():
        data=json.loads(evidence.read_text())
        count=data.get('tests_run',len(data.get('tests',[])))
    else:
        found=re.search(r'Ran (\d+) tests?',result.stderr)
        count=int(found.group(1)) if found else None
    results.append({'suite':name,'argv':argv,'exit_code':result.returncode,'tests':count})
    print(name, 'PASS' if result.returncode==0 else 'FAIL',count)
hashes={str(f.relative_to(skill)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(skill.rglob('*')) if f.is_file() and 'node_modules' not in f.parts and '__pycache__' not in f.parts}
report={'suites':results,'all_passed':all(r['exit_code']==0 for r in results),'skill_files':hashes,'visual_release_accepted':False}
(out/'results.json').write_text(json.dumps(report,indent=2))
raise SystemExit(0 if report['all_passed'] else 1)
