#!/usr/bin/env python3
"""Independent validator for Phoenix proof-cycle JSON receipts."""
import argparse, hashlib, json
from datetime import datetime
from pathlib import Path

SCHEMA = "phoenix-proof-cycle/1.0"
GENESIS = "0" * 64
EVENTS = {"cycle.started", "scout.completed", "verifier.completed", "repair.applied", "verifier.recheck", "cycle.finished"}

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def object_hash(x):
    return digest(canonical(x))

def is_hash(x):
    return isinstance(x, str) and len(x) == 64 and all(c in "0123456789abcdef" for c in x)

def finding_errors(f):
    if not isinstance(f, dict):
        return ["finding must be an object"]
    errors = [f"{k} must be a non-empty string" for k in ("id", "title", "evidence") if not isinstance(f.get(k), str) or not f[k].strip()]
    if "confidence" in f and (isinstance(f["confidence"], bool) or not isinstance(f["confidence"], (int, float)) or not 0 <= f["confidence"] <= 1):
        errors.append("confidence must be a number in [0, 1]")
    return errors

def verify_ledger(ledger):
    if not isinstance(ledger, list) or not ledger:
        return False, "ledger must be a non-empty list"
    prev, prev_time = GENESIS, None
    for i, r in enumerate(ledger, 1):
        if not isinstance(r, dict) or r.get("sequence") != i:
            return False, f"invalid record or sequence at {i}"
        if r.get("schema") != SCHEMA or r.get("event") not in EVENTS or not isinstance(r.get("payload"), dict):
            return False, f"invalid schema, event, or payload at {i}"
        try:
            stamp = r.get("timestamp")
            dt = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            if dt.tzinfo is None or (prev_time is not None and dt < prev_time):
                return False, f"invalid timestamp order at {i}"
        except (TypeError, ValueError):
            return False, f"invalid timestamp at {i}"
        if r.get("previous_hash") != prev or not is_hash(r.get("hash")):
            return False, f"invalid chain link at {i}"
        body = {k:v for k,v in r.items() if k != "hash"}
        if digest(canonical(body)) != r["hash"]:
            return False, f"content hash mismatch at {i}"
        prev, prev_time = r["hash"], dt
    names = [r["event"] for r in ledger]
    clean = ["cycle.started", "scout.completed", "verifier.completed", "cycle.finished"]
    repaired = ["cycle.started", "scout.completed", "verifier.completed", "repair.applied", "verifier.recheck", "cycle.finished"]
    if names not in (clean, repaired):
        return False, "invalid lifecycle sequence"
    start, scout, initial = ledger[:3]
    if not isinstance(start["payload"].get("task"), str) or not start["payload"]["task"].strip():
        return False, "invalid task"
    sp, vp = scout["payload"], initial["payload"]
    h = sp.get("finding_sha256")
    if sp.get("source") != "deterministic-local-fixture" or sp.get("count") != 1 or not is_hash(h) or vp.get("finding_sha256") != h:
        return False, "Scout/verifier finding hash mismatch"
    if not isinstance(vp.get("valid"), bool) or not isinstance(vp.get("errors"), list) or not all(isinstance(e, str) for e in vp["errors"]):
        return False, "invalid initial verifier result"
    end = ledger[-1]["payload"]
    if end.get("status") not in ("PASS", "FAIL", "REPAIRED") or not is_hash(end.get("finding_sha256")):
        return False, "invalid terminal result"
    if names == clean:
        expected = "PASS" if vp["valid"] else "FAIL"
        if end["status"] != expected or end["finding_sha256"] != h:
            return False, "terminal result disagrees with initial verification"
    else:
        rp, re = ledger[3]["payload"], ledger[4]["payload"]
        after = rp.get("after_finding_sha256")
        if vp["valid"] or rp.get("repair_count") != 1 or rp.get("before_finding_sha256") != h or not is_hash(after) or re.get("finding_sha256") != after:
            return False, "invalid repair binding"
        if not isinstance(re.get("valid"), bool) or not isinstance(re.get("errors"), list) or not all(isinstance(e, str) for e in re["errors"]):
            return False, "invalid re-verification result"
        expected = "REPAIRED" if re["valid"] else "FAIL"
        if end["status"] != expected or end["finding_sha256"] != after:
            return False, "terminal result disagrees with re-verification"
    return True, f"verified {len(ledger)} events"

def verify_receipt(r):
    if not isinstance(r, dict):
        return False, "receipt must be an object"
    supplied = r.get("export_sha256")
    body = dict(r); body.pop("export_sha256", None)
    if not is_hash(supplied) or digest(canonical(body)) != supplied:
        return False, "export hash mismatch"
    if r.get("schema") != SCHEMA or r.get("status") not in ("PASS", "FAIL", "REPAIRED"):
        return False, "invalid schema or status"
    f, status = r.get("finding"), r["status"]
    if not isinstance(f, dict) or r.get("finding_sha256") != object_hash(f):
        return False, "finding hash mismatch"
    errors = finding_errors(f)
    if (status in ("PASS", "REPAIRED") and errors) or (status == "FAIL" and not errors):
        return False, "status disagrees with finding validation"
    b = r.get("evidence_boundary")
    keys = ("external_ai", "web_research", "bitcoin_anchor", "arweave_anchor", "ots_anchor")
    if not isinstance(b, dict) or any(not isinstance(b.get(k), bool) for k in keys):
        return False, "evidence boundary missing or malformed"
    if not isinstance(r.get("errors_before_repair"), list):
        return False, "pre-repair errors missing"
    ok, msg = verify_ledger(r.get("ledger"))
    if not ok: return False, msg
    end = r["ledger"][-1]
    if end["event"] != "cycle.finished" or end["payload"].get("status") != status or end["payload"].get("finding_sha256") != r["finding_sha256"]:
        return False, "ledger does not commit to exported status and finding"
    return True, f"receipt verified: {status}; {msg}"

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("receipt")
    a = p.parse_args()
    try: data = json.loads(Path(a.receipt).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"FAIL: cannot read receipt: {e}"); return 2
    ok, msg = verify_receipt(data)
    print(("PASS" if ok else "FAIL") + ": " + msg)
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
