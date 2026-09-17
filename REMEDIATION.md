# Remediation and post-change validation

These are proposed owner actions, not executed changes. Time targets start when
the review is received. Incident findings can accelerate the schedule. Preserve
original evidence before changes where feasible, without delaying containment.

| Order | Target and owner | Action and operational safeguards | Evidence required to close |
| --- | --- | --- | --- |
| F1 | Immediately; Security Operations, account custodian, incident lead | Verify root activity through a trusted channel; preserve raw audit and identity records; secure credentials/recovery and contain unauthorized access under the incident plan. Escalate suspected compromise to leadership; involve privacy/legal if data exposure is suspected. | Root activity attributable or escalated; current MFA/credential posture checked; persistence and session review recorded; root-use alert received and acknowledged. An alert test must not create an unnecessary real root login. |
| F2 network | Same day; Platform Operations, vendor and application owner | Capture rules/sessions, verify private support access, revoke internet RDP and investigate sessions. Retain public HTTPS and required feed/DB paths. Do not terminate or reimage the host before preserving needed evidence. | Fresh rules plus authorized external/private connection tests; no new public RDP connection; private support works; host listener/firewall verified; application/feeds healthy. Existing connections reviewed separately. |
| F3 | Same day, alongside containment; Security Operations | Restore GuardDuty in the represented region; inventory all intended account/region coverage and protection plans. Preserve earlier findings and establish the disabled interval. | Detector enabled and health checked; a marked sample finding reaches the security queue and on-call acknowledgement; test routing filters and failure handling. A sample validates routing, not effectiveness of every detection source. |
| F2 IAM | Start same day, staged over 1–3 days; Application Engineering with Security Operations | Map workload dependencies, including scheduled feeds; review effective policies and use a narrowed policy on a canary. Keep a reviewed, time-limited recovery path and expand only specifically justified permissions if a job fails. | Required telemetry and full operational-cycle jobs work; unauthorized actions fail in simulation or disposable test resources; production error/latency/denial metrics remain acceptable; owner approval recorded. Never test deletion against real production resources. |
| F4 | Plan within 1 business day; migration window agreed with Database Operations and service owner | Rehearse encrypted copy/restore and KMS access; agree write freeze or separately tested replication; migrate during an approved window. Keep source restricted for a bounded recovery period. | New DB reports encrypted storage and intended key, private networking, TLS and baseline backup/Multi-AZ settings; reconciled data and application writes succeed; encrypted backup restore tested; RPO/RTO measured. |
| F5 | Within 3 business days; Security Operations | Enable log digests; separately review access separation, retention and any KMS requirement. Test any key-policy change before rollout to avoid blocking delivery. | Fresh S3/CloudWatch delivery without errors, expected events present, new digest chain validated with CloudTrail validation tooling, missing historical coverage documented. |
| F6 | Within 5 business days; Security Operations and compliance owner | Reconcile current identity/access population, obtain dated approvals, and track removals. Request SEC-184, SEC-191 and SEC-193 acceptance criteria; create/link tickets for other findings. | Completed current review plus approval/removal evidence; fresh control evaluations tied to exact resources and timestamps; historical gaps retained, not overwritten. |

## Database cutover and rollback gate

Snapshot encryption is a copy-and-restore process to a new instance, not an
in-place toggle. Rehearse restore duration, KMS permissions, application credentials,
parameter/subnet/security groups, extensions, monitoring and connection behavior.
For the simplest migration, obtain an approved write outage, stop writers, create
the final snapshot, encrypt its copy, restore and reconcile data before cutover.
If that outage exceeds business tolerance, design/test a replication alternative
before setting the date; do not imply a stale snapshot preserves later writes.

Before writes resume on the target, rollback can return the endpoint to the
unchanged source after checks. After target writes start, rollback requires data
reconciliation or a tested reverse-replication plan; switching back blindly loses
data. The business owner accepts this gate. Remove old unencrypted copies only
after the agreed retention and incident-preservation requirements are satisfied.
[AWS snapshot-copy guidance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CopySnapshot.html).

## Validation across AWS, monitoring and compliance

1. Capture scoped, timestamped fresh AWS API results after changes. For IAM include
   trust/inline/managed policies and applicable organization restrictions; for
   networking include attachments, routes, NACLs, IPv4/IPv6 rules and host controls.
   For the DB check instance and backup encryption separately. Record resource IDs,
   collector identity and collection failures in the restricted evidence store.
2. Pair configuration assertions with functional tests. Policy simulation assists
   but does not prove live permissions; canary jobs exercise real dependencies.
   Include the overnight feed and operations tasks, not just a web health check.
   [AWS simulator limitations](https://docs.aws.amazon.com/IAM/latest/APIReference/API_SimulatePrincipalPolicy.html).
3. Confirm fresh management-event delivery in every intended region. Enable
   digest generation, wait for a new interval and run `aws cloudtrail validate-logs`
   for that interval with an authorized read identity; review invalid/missing
   results. Check alert delivery, recipient acknowledgement and escalation using
   labeled safe test events. Retain test IDs/times and any coverage gaps.
   [AWS log validation procedure](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-cli.html).
4. Refresh the relevant compliance evidence and tests. Link before/after state,
   approval, change ticket, functional results and owner signoff. Separate current
   configuration compliance from operating effectiveness across the review period.
   Ask the control owner to accept closure; never overwrite failed historical
   evidence or report an unperformed test as passing.

## Escalation and release gates

Unexplained root activity remains with the incident lead until resolved; signs of
persistence, log tampering or unauthorized data access expand investigation scope.
Compliance labels alone do not determine whether an incident is reportable.
Security and business owners jointly approve risky containment or an exception
that affects service availability. Every exception needs a reason, compensating
control, named owner and expiration; reopening public RDP or restoring wildcard
permissions indefinitely is not the default rollback.
