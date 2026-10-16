import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from phoenix_proof_cycle import run_cycle
from phoenix_receipt_contract import canonical, digest, verify_ledger, verify_receipt

def reseal(receipt):
    previous = "0" * 64
    for index, record in enumerate(receipt["ledger"], 1):
        record["sequence"] = index
        record["previous_hash"] = previous
        record.pop("hash", None)
        record["hash"] = digest(canonical(record))
        previous = record["hash"]
    receipt.pop("export_sha256", None)
    receipt["export_sha256"] = digest(canonical(receipt))
    return receipt

class ReceiptContractTests(unittest.TestCase):
    def test_clean_receipt(self):
        receipt = run_cycle("contract clean")
        self.assertEqual(receipt["status"], "PASS")
        self.assertTrue(verify_receipt(receipt)[0])

    def test_repaired_receipt(self):
        receipt = run_cycle("contract repair", inject_defect=True)
        self.assertEqual(receipt["status"], "REPAIRED")
        self.assertTrue(verify_receipt(receipt)[0])

    def test_failed_receipt(self):
        receipt = run_cycle("contract failure", inject_defect=True, repair=False)
        self.assertEqual(receipt["status"], "FAIL")
        self.assertTrue(verify_receipt(receipt)[0])

    def test_export_tampering_rejected(self):
        receipt = run_cycle("tamper export")
        receipt["finding"]["title"] = "changed"
        self.assertFalse(verify_receipt(receipt)[0])

    def test_rehashed_export_cannot_hide_finding_tamper(self):
        receipt = run_cycle("tamper finding")
        receipt["finding"]["title"] = "changed"
        receipt.pop("export_sha256", None)
        receipt["export_sha256"] = digest(canonical(receipt))
        self.assertFalse(verify_receipt(receipt)[0])

    def test_ledger_tampering_rejected(self):
        receipt = run_cycle("tamper ledger")
        receipt["ledger"][0]["payload"]["task"] = "changed"
        self.assertFalse(verify_ledger(receipt["ledger"])[0])

    def test_rehashed_invalid_lifecycle_rejected(self):
        receipt = run_cycle("bad lifecycle")
        receipt["ledger"][1]["event"] = "cycle.finished"
        reseal(receipt)
        ok, message = verify_receipt(receipt)
        self.assertFalse(ok)
        self.assertIn("lifecycle", message)

    def test_rehashed_bad_timestamp_rejected(self):
        receipt = run_cycle("bad timestamp")
        receipt["ledger"][0]["timestamp"] = "not-a-time"
        reseal(receipt)
        self.assertFalse(verify_receipt(receipt)[0])

    def test_evidence_boundary_required(self):
        receipt = run_cycle("boundary")
        del receipt["evidence_boundary"]["bitcoin_anchor"]
        receipt.pop("export_sha256", None)
        receipt["export_sha256"] = digest(canonical(receipt))
        self.assertFalse(verify_receipt(receipt)[0])

    def test_status_mismatch_rejected(self):
        receipt = run_cycle("status mismatch")
        receipt["status"] = "FAIL"
        receipt.pop("export_sha256", None)
        receipt["export_sha256"] = digest(canonical(receipt))
        self.assertFalse(verify_receipt(receipt)[0])

    def test_schema_mismatch_rejected(self):
        receipt = run_cycle("schema mismatch")
        receipt["schema"] = "unknown"
        receipt.pop("export_sha256", None)
        receipt["export_sha256"] = digest(canonical(receipt))
        self.assertFalse(verify_receipt(receipt)[0])

    def test_malformed_root_rejected(self):
        self.assertFalse(verify_receipt([])[0])
        self.assertFalse(verify_ledger({})[0])

    def test_terminal_finding_binding(self):
        receipt = run_cycle("binding")
        self.assertEqual(receipt["ledger"][-1]["payload"]["finding_sha256"], receipt["finding_sha256"])
        self.assertTrue(verify_receipt(receipt)[0])

if __name__ == "__main__":
    unittest.main(verbosity=2)
