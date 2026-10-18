"""Portable-resource validation; does not evaluate aesthetic quality."""
from pathlib import Path
import hashlib
import json
import re
import sys


def resource_targets(text):
    """Read prose resource links, excluding fenced/inline commands and examples."""
    fence = None
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            if fence is None:
                fence = marker[1][0]
            elif marker[1][0] == fence:
                fence = None
            continue
        if fence or re.match(r'^(?: {4}|\t)', line):
            continue
        if re.search(r'\b(?:for example|e\.g\.|placeholder)\b', line, re.I):
            continue
        yield from re.findall(r'\]\(([^)]+)\)', line)
        for target in re.findall(r'`([^`]+)`', line):
            # A bare path is a resource. Spaces, flags, calls and shell syntax
            # identify commands or code rather than a required package file.
            if re.fullmatch(r'[\w./-]+\.(?:md|html|json|py)(?:#[\w-]+)?', target):
                if not Path(target.split('#')[0]).name.startswith('.'):
                    yield target


def resource_failures(skill):
    skill = skill.resolve()
    failures = []
    for page in skill.rglob('*.md'):
        for target in resource_targets(page.read_text()):
            target = target.removeprefix('<').removesuffix('>')
            if re.match(r'^[\w+.-]+:', target) or target.startswith('#'):
                continue
            name = target.split('#')[0]
            if not name:
                continue
            resolved = (page.parent / name).resolve()
            # Existing engine notes sometimes use skill-root-relative paths.
            if not name.startswith(('.', '/')) and not resolved.exists() and (skill / name).exists():
                resolved = (skill / name).resolve()
            # Bare script/data names in prose may describe generated metadata;
            # explicit paths and documentation filenames are resource references.
            if '/' not in name and Path(name).suffix in ('.py', '.json') and not resolved.exists():
                continue
            label = f'{page.relative_to(skill)}: {target}'
            if not resolved.is_relative_to(skill):
                failures.append(f'{label}: outside skill package')
            elif not resolved.is_file():
                failures.append(f'{label}: missing resource')
    return failures


def validate(root):
    skill = root / 'skills/cropmark'
    failures = resource_failures(skill)
    for path in skill.rglob('*.json'):
        try:
            json.loads(path.read_text())
        except ValueError as error:
            failures.append(f'{path}: {error}')
    atlas = json.loads((skill / 'refs/atlas.json').read_text())
    if len(atlas) != 21 or len({entry['id'] for entry in atlas}) != 21:
        failures.append('reference atlas needs 21 unique source IDs')
    base = root.parent / 'baselines/rc5'
    if base.exists():
        for folder in ['engines', 'fonts']:
            for path in (base / folder).rglob('*'):
                if path.is_file() and '__pycache__' not in path.parts:
                    candidate = skill / path.relative_to(base)
                    if not candidate.exists() or hashlib.sha256(path.read_bytes()).digest() != hashlib.sha256(candidate.read_bytes()).digest():
                        failures.append(f'rc5 changed: {candidate}')
    return failures


def main():
    failures = validate(Path(__file__).resolve().parents[1])
    print('\n'.join(failures) if failures else 'PASS: skill resources, JSON, atlas and available frozen renderer/font hashes')
    return int(bool(failures))


if __name__ == '__main__':
    sys.exit(main())
