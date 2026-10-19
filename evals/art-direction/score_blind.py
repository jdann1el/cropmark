"""Score a user-supplied heldout-v1 ballot. Never infers blank votes or human authorship."""
import argparse
import json
from pathlib import Path


def score(ballot, labels, *, technical_pass):
    groups = [f'H{i}' for i in range(1, 7)]
    conditions = {'candidate', 'baseline', 'rc5'}
    if not isinstance(labels, dict) or set(labels) != set(groups):
        raise ValueError('identity map must contain exactly H1–H6')
    for mapping in labels.values():
        if (not isinstance(mapping, dict) or set(mapping) != set('ABC')
                or set(mapping.values()) != conditions):
            raise ValueError('each identity map must be a permutation of all three conditions')
    if not isinstance(ballot, dict) or ballot.get('protocol') != 'heldout-v1' or ballot.get('human') is not True:
        raise ValueError('expected the user-supplied heldout-v1 ballot')
    ratings = ballot.get('ratings')
    if not isinstance(ratings, dict):
        raise ValueError('ratings must be an object')
    missing = []
    for group in groups:
        for suffix, allowed in [
            ('pair-AB', {'A', 'B', 'Empate', 'Ninguna'}),
            ('pair-AC', {'A', 'C', 'Empate', 'Ninguna'}),
            ('pair-BC', {'B', 'C', 'Empate', 'Ninguna'}),
            *[(f'quality-{label}', {'yes', 'no'}) for label in 'ABC'],
        ]:
            key = f'{group}-{suffix}'
            value = ratings.get(key, '')
            if value == '':
                missing.append(key)
            elif not isinstance(value, str) or value not in allowed:
                raise ValueError(f'invalid vote: {key}')
    if missing:
        return {'status': 'PENDING', 'acceptance_gate_passed': False, 'missing': missing}

    wins = {'baseline': 0, 'rc5': 0}
    approved = []
    for group in groups:
        mapping = labels[group]
        candidate = next(k for k, v in mapping.items() if v == 'candidate')
        for comparator in wins:
            other = next(k for k, v in mapping.items() if v == comparator)
            pair = ''.join(sorted([candidate, other]))
            wins[comparator] += ratings[f'{group}-pair-{pair}'] == candidate
        if ratings[f'{group}-quality-{candidate}'] == 'yes':
            approved.append(group)
    families = {
        name: any(group in approved for group in members)
        for name, members in [('thumbnail', ['H1', 'H2']), ('carousel', ['H3', 'H4']), ('campaign', ['H5', 'H6'])]
    }
    passed = (technical_pass is True and min(wins.values()) >= 5
              and len(approved) >= 5 and all(families.values()))
    return {'status': 'PASS' if passed else 'FAIL', 'acceptance_gate_passed': passed,
            'wins': wins, 'quality_approved': len(approved), 'approved_cases': approved,
            'family_approved': families, 'technical_pass': technical_pass is True,
            'limits': 'Counts the supplied ballot only. Caller must verify human provenance and technical evidence; this script does not publish or merge.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ballot', type=Path)
    parser.add_argument('identity_map', type=Path)
    parser.add_argument('--technical-report', required=True, type=Path)
    args = parser.parse_args()
    try:
        ballot = json.loads(args.ballot.read_text())
        key = json.loads(args.identity_map.read_text())
        technical = json.loads(args.technical_report.read_text())
        technical_pass = (technical.get('technical_file_audit_pass') is True
                          and technical.get('completed_trials_audited') == 18)
        result = score(ballot, key['labels'], technical_pass=technical_pass)
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
