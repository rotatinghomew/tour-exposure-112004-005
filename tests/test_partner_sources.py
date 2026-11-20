import csv
import json
from pathlib import Path
import unittest


RECORDS = Path(__file__).resolve().parents[1] / 'records'
SCHEMAS = {'venues.json': 'dict', 'observations.json': 'dict', 'booking_and_readback.json': 'dict',
           'zone_rollout.json': 'dict'}


class PartnerSourceTests(unittest.TestCase):
    def test_format(self):
        self.assertEqual({path.name for path in RECORDS.iterdir()}, set(SCHEMAS))
        for name, shape in SCHEMAS.items():
            with self.subTest(name=name), (RECORDS / name).open(encoding='utf-8', newline='') as source:
                if isinstance(shape, list):
                    rows = csv.DictReader(source)
                    self.assertEqual(rows.fieldnames, shape)
                    records = list(rows)
                    self.assertTrue(records)
                    self.assertTrue(all(None not in row and None not in row.values() for row in records))
                else:
                    records = json.load(source)
                    self.assertIsInstance(records, list if shape == 'list' else dict)
                    self.assertTrue(records)

    def test_rollout_references_capacity(self):
        layouts = json.loads((RECORDS / 'venues.json').read_text(encoding='utf-8'))
        handoffs = json.loads((RECORDS / 'zone_rollout.json').read_text(encoding='utf-8'))
        options = {row['id'] for row in layouts['options']}
        for row in handoffs['pending_rollouts']:
            self.assertIn(row['layout'], options)
            self.assertLess(row['window'][0], row['window'][1])
        for row in handoffs['staging_occupancy']:
            capacities = {(move[0], move[1]): move[4] for move in layouts['moves'][row['venue']]}
            self.assertGreaterEqual(capacities[row['from'], row['to']], row['blocked_units'])
