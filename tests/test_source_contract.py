import csv
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / "records"


class SourceContract(unittest.TestCase):
    def test_export_shape(self):
        self.assertEqual({path.name for path in ROOT.iterdir()}, set(EXPECTED))
        for name, contract in EXPECTED.items():
            with self.subTest(source=name):
                path = ROOT / name
                if path.suffix == ".csv":
                    with path.open(encoding="utf-8", newline="") as source:
                        reader = csv.DictReader(source)
                        self.assertEqual(reader.fieldnames, contract)
                        rows = list(reader)
                    self.assertTrue(rows)
                    self.assertTrue(all(None not in row and None not in row.values() for row in rows))
                else:
                    body = json.loads(path.read_text(encoding="utf-8"))
                    self.assertIsInstance(body, list if contract == "list" else dict)
                    self.assertTrue(body)

    def test_related_export_records(self):
        for name, value in SEQUENCE.items():
            with self.subTest(source=name):
                path = ROOT / name
                if path.suffix == ".csv":
                    with path.open(encoding="utf-8", newline="") as source:
                        cells = {cell for row in csv.reader(source) for cell in row}
                else:
                    rows = json.loads(path.read_text(encoding="utf-8"))
                    cells = {item for row in rows for item in row.values() if isinstance(item, str)}
                self.assertIn(value, cells)


EXPECTED = {'groups.csv': ['group', 'school', 'timezone', 'students', 'languages'], 'available.csv': ['rule', 'group', 'from', 'through', 'weekday', 'start_local', 'end_local'], 'sessions.csv': ['id', 'host_tz', 'start_local', 'offset', 'duration', 'languages', 'hosts'], 'invites.csv': ['seq', 'group', 'session', 'kind', 'state'], 'changes.json': 'list', 'contract.json': 'dict'}
SEQUENCE = {'sessions.csv': 's2', 'invites.csv': 'makeup', 'changes.json': 'clock_note'}
