"""Check selected report anchors against local exercise files; no network calls.

Exit 0 means the anchors match, NOT that the environment is secure.
Exit 1 means an anchor differs; exit 2 means inputs could not be checked.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path


# Exact reference-dataset assertions, not a general AWS scanner or policy engine.
SNAPSHOT_CHECKS = [
    ("/generated_at", "2026-09-01T09:00:00Z"),
    ("/iam_roles/0/role_name", "DeployRole"),
    ("/iam_roles/0/managed_policy_arns", []),
    ("/iam_roles/0/trust_policy/Statement/0/Condition/StringEquals/ci.example.com:aud", "sts.amazonaws.com"),
    ("/iam_roles/0/trust_policy/Statement/0/Condition/StringEquals/ci.example.com:sub", "repo:platform/clinical-api:environment:production"),
    ("/iam_roles/1/role_name", "ProdAppRole"),
    ("/iam_roles/1/inline_policies/0/document/Statement/0", {"Effect": "Allow", "Action": "*", "Resource": "*"}),
    ("/security_groups/0/group_id", "sg-app-prod"),
    ("/security_groups/0/ingress_rules/1/protocol", "tcp"),
    ("/security_groups/0/ingress_rules/1/from_port", 3389),
    ("/security_groups/0/ingress_rules/1/to_port", 3389),
    ("/security_groups/0/ingress_rules/1/cidr_ipv4", "0.0.0.0/0"),
    ("/security_groups/0/attached_resources/0/iam_role", "ProdAppRole"),
    ("/security_groups/0/attached_resources/0/route_to_internet_gateway", True),
    ("/security_groups/0/attached_resources/0/network_acl_allows_ingress_tcp_ports", [443, 8443, 3389]),
    ("/security_groups/0/attached_resources/0/network_acl_allows_established_return_traffic", True),
    ("/security_groups/0/attached_resources/0/imds_http_tokens", "required"),
    ("/security_groups/0/attached_resources/0/ebs_encrypted", True),
    ("/security_groups/1/ingress_rules/0/source_group_id", "sg-app-prod"),
    ("/rds_instances/0/storage_encrypted", False),
    ("/rds_instances/0/kms_key_id", None),
    ("/rds_instances/0/publicly_accessible", False),
    ("/rds_instances/0/parameter_overrides/rds.force_ssl", "1"),
    ("/rds_instances/0/backup_retention_days", 7),
    ("/rds_instances/0/restore_test_result", "passed"),
    ("/guardduty/enabled", False),
    ("/guardduty/alert_route_configured", True),
    ("/cloudtrail/is_logging", True),
    ("/cloudtrail/is_multi_region_trail", True),
    ("/cloudtrail/enable_log_file_validation", False),
    ("/cloudtrail/kms_key_id", None),
    ("/cloudtrail/last_delivery_error", None),
    ("/cloudtrail/event_selectors", [{"read_write_type": "All", "include_management_events": True}]),
    ("/s3_buckets/1/default_encryption/sse_algorithm", "AES256"),
    ("/kms_keys/0/rotation_enabled", True),
]
CONTROL_CHECKS = [
    ("CC6.1", "test_status", "FAIL"),
    ("CC6.1", "evidence_period_end", "2026-04-30"),
    ("CC6.1", "remediation_ticket", "SEC-184"),
    ("CC6.7", "test_status", "FAIL"),
    ("CC6.7", "remediation_ticket", "SEC-193"),
    ("CC7.2", "test_status", "FAIL"),
    ("CC7.2", "remediation_ticket", "SEC-191"),
    ("CC6.2", "test_status", "PASS"),
    ("CC6.3", "test_status", "PASS"),
    ("CC6.6", "test_status", "PASS"),
    ("CC7.1", "test_status", "PASS"),
    ("CC7.3", "test_status", "PASS"),
    ("CC8.1", "test_status", "PASS"),
    ("A1.2", "test_status", "PASS"),
    ("A1.3", "test_status", "PASS"),
]
EVENT_CHECKS = [
    (8, "event_name", "PutLogEvents"),
    (9, "event_name", "DeleteRepository"),
    (9, "outcome", "AccessDenied"),
    (11, "principal", "ProdAppRole"),
    (11, "event_name", "PutLogEvents"),
    (12, "event_time_utc", "2026-08-29T02:14:37Z"),
    (12, "event_name", "ConsoleLogin"),
    (12, "principal", "root"),
    (12, "outcome", "Success"),
    (12, "mfa_used", False),
    (13, "event_time_utc", "2026-08-29T02:16:37Z"),
    (13, "event_name", "GetAccountSummary"),
    (13, "principal", "root"),
    (14, "event_name", "DescribeDBSnapshots"),
    (18, "event_name", "TerminateEnvironment"),
    (18, "outcome", "AccessDenied"),
    (23, "event_name", "PutLogEvents"),
    (24, "event_name", "GetTrailStatus"),
]


def pointer(document, path):
    for key in path.lstrip("/").split("/"):
        key = key.replace("~1", "/").replace("~0", "~")
        document = document[int(key)] if isinstance(document, list) else document[key]
    return document


def verify(directory):
    names = ("aws_security_snapshot.json", "secureframe_control_status.csv", "cloud_activity_events.jsonl")
    raw = [(directory / name).read_bytes() for name in names]
    snapshot = json.loads(raw[0].decode("utf-8-sig"))
    rows = list(csv.DictReader(raw[1].decode("utf-8-sig").splitlines()))
    controls = {row["control_id"]: row for row in rows}
    if len(controls) != len(rows):
        raise ValueError("duplicate control IDs")
    # Keep physical line numbering; blank or malformed lines are input errors.
    events = [json.loads(line) for line in raw[2].decode("utf-8-sig").splitlines()]
    checks = [(f"S {path}", pointer(snapshot, path), expected) for path, expected in SNAPSHOT_CHECKS]
    checks += [(f"C {cid}/{field}", controls[cid][field], expected) for cid, field, expected in CONTROL_CHECKS]
    checks += [(f"E{line} {field}", events[line - 1][field], expected) for line, field, expected in EVENT_CHECKS]
    failures = [label for label, actual, expected in checks
                if type(actual) is not type(expected) or actual != expected]
    print(f"Anchors matched: {len(checks) - len(failures)}/{len(checks)}")
    print(f"Inputs: {len(rows)} controls; {len(events)} events")
    for label in failures:
        print(f"MISMATCH: {label}")
    for name, content in zip(names, raw):
        print(f"SHA256 {name}: {hashlib.sha256(content).hexdigest()}")
    print("Offline anchor check only; no AWS posture or remediation certification.")
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_directory", type=Path, help="Local directory containing the three original exercise files")
    args = parser.parse_args()
    try:
        return verify(args.source_directory)
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        # Do not print source values, parser excerpts or local paths on failure.
        print("INPUT ERROR: files are missing, malformed, duplicated, or lack required fields.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
