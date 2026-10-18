#!/usr/bin/env python3
"""Check declared layout relationships; never infer aesthetic quality from metadata.
Usage: python3 design_check.py contract.json [--out report.json]
Exit 0 = declared relationships passed; 1 = relationship failed; 2 = invalid input.
Coordinates are output pixels. Boxes are [left, top, right, bottom].
"""
import argparse
import json
import math
from pathlib import Path
import sys


def number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def vector(x, n, name):
    if not isinstance(x, list) or len(x) != n or not all(number(v) for v in x):
        raise ValueError(f'{name}: expected {n} finite numbers')
    return x


def positive(x, name, zero=False):
    if not number(x) or (x < 0 if zero else x <= 0):
        raise ValueError(f'{name}: expected a finite {"nonnegative" if zero else "positive"} number')
    return x


def reason(obj, key):
    if not isinstance(obj.get(key), str) or not obj[key].strip():
        raise ValueError(f'{key}: a nonempty visible-purpose explanation is required')


def check(data, root):
    if not isinstance(data, dict) or data.get('version') != 1:
        raise ValueError('version must be 1')
    frames = data.get('frames')
    if not isinstance(frames, list) or not frames:
        raise ValueError('frames must be a nonempty list')
    results, seen, frame_tokens = [], set(), []

    def record(ok, frame, rule, detail):
        results.append({'status': 'PASS' if ok else 'FAIL', 'frame': frame, 'rule': rule, 'detail': detail})

    for frame in frames:
        if not isinstance(frame, dict): raise ValueError('frame must be an object')
        fid = frame.get('id')
        if not isinstance(fid, str) or not fid or fid in seen: raise ValueError('unique nonempty frame id required')
        seen.add(fid)
        w, h = vector(frame.get('size'), 2, 'size')
        positive(w, 'width'); positive(h, 'height')
        margin = positive(frame.get('margin', 0), 'margin', zero=True)
        els = frame.get('elements')
        if not isinstance(els, list) or not els: raise ValueError(f'{fid}: elements must be nonempty')
        boxes = {}
        for el in els:
            if not isinstance(el, dict): raise ValueError('element must be an object')
            eid = el.get('id')
            if not isinstance(eid, str) or not eid or eid in boxes: raise ValueError('unique nonempty element id required')
            b = vector(el.get('box'), 4, f'{eid}.box')
            if b[2] <= b[0] or b[3] <= b[1]: raise ValueError('boxes must have positive area')
            boxes[eid] = b
            bleed = el.get('bleed', False)
            if not isinstance(bleed, bool): raise ValueError('bleed must be boolean')
            if bleed:
                reason(el, 'reason')
                record(True, fid, 'R08', f'{eid}: declared intentional bleed; requires visual inspection')
            else:
                record(b[0] >= margin and b[1] >= margin and b[2] <= w-margin and b[3] <= h-margin,
                       fid, 'R07', f'{eid}: content inside declared margin {margin}')
            if 'font_path' in el:
                if not isinstance(el['font_path'], str) or not el['font_path']: raise ValueError('font_path must be nonempty')
                record((root / el['font_path']).is_file(), fid, 'R03', f'{eid}: declared font file exists (not proof of loading)')

        def box(eid):
            if eid not in boxes: raise ValueError(f'unknown element {eid!r}')
            return boxes[eid]

        for group in frame.get('alignments', []):
            axis = group.get('axis')
            if axis not in ('left', 'right', 'top', 'bottom', 'center_x', 'center_y'): raise ValueError('invalid alignment axis')
            members = group.get('elements')
            if not isinstance(members, list) or len(members) < 2 or len(set(members)) != len(members): raise ValueError('alignment needs distinct elements')
            tol = positive(group.get('tolerance', 2), 'tolerance', zero=True)
            offsets = group.get('offsets', {})
            if not isinstance(offsets, dict) or any(k not in members or not number(v) for k, v in offsets.items()): raise ValueError('invalid optical offsets')
            if offsets: reason(group, 'reason')
            def coordinate(eid):
                a,b,c,d = box(eid)
                v = {'left':a,'right':c,'top':b,'bottom':d,'center_x':(a+c)/2,'center_y':(b+d)/2}[axis]
                return v-offsets.get(eid,0)
            coords = [coordinate(eid) for eid in members]
            record(max(coords)-min(coords) <= tol, fid, 'R05', f'{axis} alignment of {members}, tolerance {tol}')
        for group in frame.get('padding', []):
            outer = box(group.get('container'))
            children = group.get('children')
            if not isinstance(children, list) or not children: raise ValueError('padding needs children')
            cb = [box(eid) for eid in children]
            union = [min(b[0] for b in cb), min(b[1] for b in cb), max(b[2] for b in cb), max(b[3] for b in cb)]
            actual = [union[1]-outer[1], outer[2]-union[2], outer[3]-union[3], union[0]-outer[0]]
            expected = vector(group.get('expected'), 4, 'padding.expected (top,right,bottom,left)')
            if min(expected) < 0: raise ValueError('expected padding cannot be negative')
            tol = positive(group.get('tolerance', 2), 'tolerance', zero=True)
            record(all(abs(a-b) <= tol for a,b in zip(actual,expected)),fid,'R06',f'padding actual {actual}, expected {expected}')
        for group in frame.get('gaps', []):
            a, b = box(group.get('a')), box(group.get('b'))
            axis = group.get('axis')
            if axis not in ('x','y'): raise ValueError('gap axis must be x or y')
            minimum = positive(group.get('min'), 'gap.min', zero=True)
            overlap = group.get('allow_overlap', False)
            if not isinstance(overlap,bool): raise ValueError('allow_overlap must be boolean')
            gap = b[0]-a[2] if axis == 'x' else b[1]-a[3]
            if overlap:
                reason(group,'reason')
                record(True,fid,'R08',f'declared intentional overlap, measured gap {gap}; inspect readability')
            else: record(gap >= minimum,fid,'R07',f'{group["a"]} → {group["b"]}: gap {gap}, minimum {minimum}')
        tokens = frame.get('tokens',{})
        if not isinstance(tokens,dict): raise ValueError('tokens must be an object')
        frame_tokens.append((fid,tokens))
    shared = data.get('shared_tokens',[])
    if not isinstance(shared,list) or not all(isinstance(k,str) and k for k in shared): raise ValueError('shared_tokens must be names')
    for key in shared:
        if any(key not in t for _,t in frame_tokens): raise ValueError(f'missing shared token {key}')
        values=[t[key] for _,t in frame_tokens]
        record(all(v == values[0] for v in values),'set','R12',f'shared token {key}')
    return {'checks':results,'passed':all(r['status']=='PASS' for r in results),
            'scope':'declared metadata relationships only; no pixel inference, optical or aesthetic approval'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('contract',type=Path);p.add_argument('--out',type=Path)
    a=p.parse_args()
    try:
        report=check(json.loads(a.contract.read_text()),a.contract.resolve().parent)
        if a.out:
            a.out.parent.mkdir(parents=True,exist_ok=True)
            a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return 0 if report['passed'] else 1
    except (OSError,ValueError,TypeError,KeyError,AttributeError) as e:
        print(f'ERROR cropmark design contract: {e}',file=sys.stderr);return 2

if __name__=='__main__': raise SystemExit(main())
