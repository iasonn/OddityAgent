import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import time
import uuid

ROOT = Path(os.environ.get("ODDITY_TRAINING_DIR", str(Path.home() / ".oddityagent" / "training" / "tonkercad")))
ID = re.compile(r"^[a-f0-9]{32}$")

def record(root, data):
    for key in ("task", "model", "script", "scene", "printability"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError("Missing nonempty field: " + key)
    if data.get("status") not in ("candidate", "failed"):
        raise ValueError("Initial status must be candidate or failed")
    allowed = ("task", "model", "script", "scene", "printability", "status", "corrections", "reference", "images", "tags")
    clean = {key: data[key] for key in allowed if key in data}
    clean.update(id=uuid.uuid4().hex, created=time.time(), script_sha256=hashlib.sha256(data["script"].encode()).hexdigest())
    root.mkdir(parents=True, exist_ok=True)
    save(root, clean)
    return clean["id"]

def save(root, item):
    file = root / (item["id"] + ".json")
    temp = root / (item["id"] + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temp.open("x", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        os.replace(temp, file)
    finally:
        temp.unlink(missing_ok=True)

def review(root, ident, decision, note):
    if not ID.fullmatch(ident):
        raise ValueError("Invalid run ID")
    if not note.strip():
        raise ValueError("A human assessment is required")
    item = json.loads((root / (ident + ".json")).read_text(encoding="utf-8"))
    if item["status"] == "failed" and decision == "accepted":
        raise ValueError("Record corrected execution as a new candidate")
    item.update(status=decision, review_note=note, reviewed=time.time())
    save(root, item)

def accepted(root):
    for f in sorted(root.glob("*.json")):
        item = json.loads(f.read_text(encoding="utf-8"))
        if item.get("status") == "accepted" and item.get("review_note"):
            yield item

def search(root, query):
    words = set(re.findall(r"\w+", query.lower()))
    matches = []
    for item in accepted(root):
        corpus = " ".join([item["task"], str(item.get("tags", [])), str(item.get("corrections", ""))])
        score = len(words & set(re.findall(r"\w+", corpus.lower())))
        if score:
            matches.append((score, item))
    return [item for _, item in sorted(matches, key=lambda x: -x[0])[:5]]

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record"); r.add_argument("file", type=Path)
    r = sub.add_parser("review"); r.add_argument("id"); r.add_argument("decision", choices=["accepted", "rejected"]); r.add_argument("note")
    r = sub.add_parser("search"); r.add_argument("query")
    sub.add_parser("export")
    a = p.parse_args()
    if a.cmd == "record": print(record(ROOT, json.loads(a.file.read_text(encoding="utf-8"))))
    elif a.cmd == "review": review(ROOT, a.id, a.decision, a.note)
    elif a.cmd == "search": print(json.dumps(search(ROOT, a.query), ensure_ascii=False, indent=2))
    else:
        for item in accepted(ROOT):
            print(json.dumps({"messages": [{"role":"user","content":item["task"]},{"role":"assistant","content":item["script"]}], "run_id":item["id"]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
