import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'art-direction'))
from score_blind import score


def fixture():
    labels = {f'H{i}': {'A': 'candidate', 'B': 'baseline', 'C': 'rc5'} for i in range(1, 7)}
    ratings = {}
    for group in labels:
        for pair, winner in [('AB', 'A'), ('AC', 'A'), ('BC', 'Empate')]:
            ratings[f'{group}-pair-{pair}'] = winner
        for label in 'ABC':
            ratings[f'{group}-quality-{label}'] = 'yes'
    return {'protocol': 'heldout-v1', 'human': True, 'ratings': ratings}, labels


class BlindGateTests(unittest.TestCase):
    def test_five_wins_and_five_approvals_suffice(self):
        ballot, labels = fixture()
        for pair in ['AB', 'AC']:
            ballot['ratings'][f'H6-pair-{pair}'] = 'Empate'
        ballot['ratings']['H6-quality-A'] = 'no'
        result = score(ballot, labels, technical_pass=True)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['wins'], {'baseline': 5, 'rc5': 5})
        self.assertEqual(result['quality_approved'], 5)

    def test_ties_and_neither_are_not_wins(self):
        ballot, labels = fixture()
        ballot['ratings']['H5-pair-AB'] = 'Empate'
        ballot['ratings']['H6-pair-AB'] = 'Ninguna'
        result = score(ballot, labels, technical_pass=True)
        self.assertEqual(result['status'], 'FAIL')
        self.assertEqual(result['wins']['baseline'], 4)

    def test_comparators_are_counted_separately(self):
        ballot, labels = fixture()
        ballot['ratings']['H5-pair-AC'] = 'C'
        ballot['ratings']['H6-pair-AC'] = 'C'
        result = score(ballot, labels, technical_pass=True)
        self.assertEqual(result['wins'], {'baseline': 6, 'rc5': 4})
        self.assertFalse(result['acceptance_gate_passed'])

    def test_blank_vote_stays_pending_even_if_export_claims_complete(self):
        ballot, labels = fixture()
        ballot['complete'] = True
        ballot['ratings']['H3-quality-B'] = ''
        result = score(ballot, labels, technical_pass=True)
        self.assertEqual(result['status'], 'PENDING')
        self.assertFalse(result['acceptance_gate_passed'])

    def test_human_votes_cannot_override_technical_failure(self):
        ballot, labels = fixture()
        self.assertEqual(score(ballot, labels, technical_pass=False)['status'], 'FAIL')

    def test_invalid_map_or_vote_is_rejected(self):
        ballot, labels = fixture()
        labels['H1']['B'] = 'candidate'
        with self.assertRaises(ValueError):
            score(ballot, labels, technical_pass=True)
        ballot, labels = fixture()
        ballot['ratings']['H1-pair-AB'] = 'C'
        with self.assertRaises(ValueError):
            score(ballot, labels, technical_pass=True)

    def test_anonymous_labels_do_not_fix_candidate_position(self):
        ballot, labels = fixture()
        for group in labels:
            labels[group] = {'A': 'rc5', 'B': 'candidate', 'C': 'baseline'}
            for pair, vote in [('AB', 'B'), ('AC', 'Empate'), ('BC', 'B')]:
                ballot['ratings'][f'{group}-pair-{pair}'] = vote
            ballot['ratings'][f'{group}-quality-A'] = 'no'
            ballot['ratings'][f'{group}-quality-C'] = 'no'
        result = score(ballot, labels, technical_pass=True)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['wins'], {'baseline': 6, 'rc5': 6})


if __name__ == '__main__':
    unittest.main()
