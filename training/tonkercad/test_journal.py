import tempfile
import unittest
from pathlib import Path
from journal import record, review, accepted, search

class JournalTests(unittest.TestCase):
    def test_review_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = dict(task="flanged bracket", model="local", script="box({w:10,d:10,h:2})", scene="observed", printability="checked", status="candidate")
            ident = record(root, data)
            self.assertEqual(list(accepted(root)), [])
            review(root, ident, "accepted", "Verified dimensions")
            self.assertEqual(search(root, "bracket")[0]["id"], ident)
            review(root, ident, "rejected", "Fit failed")
            self.assertEqual(list(accepted(root)), [])
            failed = record(root, dict(data, status="failed"))
            with self.assertRaises(ValueError):
                review(root, failed, "accepted", "not valid")
            with self.assertRaises(ValueError):
                review(root, "../escape", "accepted", "no")

if __name__ == "__main__":
    unittest.main()
