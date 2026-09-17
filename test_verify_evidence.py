"""Exercise success, mismatch and invalid-input paths using disposable copies.

Run: python test_verify_evidence.py /path/to/local/exercise/files
"""

import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python test_verify_evidence.py SOURCE_DIRECTORY")
    source = Path(sys.argv[1])
    names = ("aws_security_snapshot.json", "secureframe_control_status.csv", "cloud_activity_events.jsonl")
    originals = {name: (source / name).read_bytes() for name in names}
    script = Path(__file__).with_name("verify_evidence.py")
    # Copies contain exercise data: keep this directory on an approved local disk.
    with tempfile.TemporaryDirectory(prefix="evidence-test-", dir=Path.cwd()) as temp:
        target = Path(temp)

        def reset():
            for name, content in originals.items():
                (target / name).write_bytes(content)

        def expect(code, label):
            result = subprocess.run([sys.executable, str(script), str(target)],
                                    capture_output=True, text=True, check=False)
            if result.returncode != code:
                raise AssertionError(f"{label}: expected exit {code}, got {result.returncode}")
            print(f"PASS: {label}")

        reset()
        expect(0, "original evidence matches")
        snapshot = json.loads(originals[names[0]])
        snapshot["guardduty"]["enabled"] = True
        (target / names[0]).write_text(json.dumps(snapshot), encoding="utf-8")
        expect(1, "changed security fact rejected")
        snapshot["guardduty"]["enabled"] = 0
        (target / names[0]).write_text(json.dumps(snapshot), encoding="utf-8")
        expect(1, "integer zero is not accepted as boolean false")
        del snapshot["guardduty"]["enabled"]
        (target / names[0]).write_text(json.dumps(snapshot), encoding="utf-8")
        expect(2, "missing required field rejected")
        reset()
        (target / names[2]).write_text("invalid JSON\n", encoding="utf-8")
        expect(2, "malformed event rejected")
        reset()
        rows = originals[names[1]].decode("utf-8-sig").splitlines()
        (target / names[1]).write_text("\n".join(rows + [rows[1]]) + "\n", encoding="utf-8")
        expect(2, "duplicate control ID rejected")
        reset()
        events = originals[names[2]].decode("utf-8-sig").splitlines()
        (target / names[2]).write_text("\n".join(events[:11] + ["{}"] + events[11:]) + "\n", encoding="utf-8")
        expect(2, "shifted event-line citation rejected")
        reset()
        (target / names[0]).unlink()
        expect(2, "missing source file rejected")
    print("8 checks passed; temporary source copies removed.")


if __name__ == "__main__":
    main()
