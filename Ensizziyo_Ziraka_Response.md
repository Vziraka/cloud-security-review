# AWS security and control review

Prepared for Ensizziyo Ziraka. Assessment cutoff: **2026-09-01 09:00 UTC**.
This is a review of synthetic evidence, not a live account audit. Recommended
changes and validation steps below have **not** been executed against AWS.

## Decision

Investigate the root session immediately, restrict internet-facing administrative
access, and restore threat detection. The combination of public RDP and a runtime
role with unrestricted identity-policy permissions creates the most concerning
configuration risk. Plan database encryption as a controlled migration rather
than an emergency in-place change. Preserve working deployment, backup, and
logging paths throughout remediation.

Priorities are response targets proposed for this exercise: **P1** means act
immediately or the same day; **P2** means assign an owner now and complete a
scheduled correction. No confirmed breach is established by these materials.

The database gap is serious, but the export shows private networking and enforced
TLS, while correcting storage encryption requires a migration with availability
and data-loss risks. Start its plan immediately while containing the exposed
administrative path and investigating privileged activity. Evidence of active
data access or compromise would change this ordering.

## Evidence notation

- **S**: `aws_security_snapshot.json`; paths use zero-based JSON array indexes.
- **C**: `secureframe_control_status.csv`; references use its unique `control_id`.
- **E**: `cloud_activity_events.jsonl`; references use one-based physical line
  numbers, UTC timestamps, and event names.

References identify the original exercise data without republishing whole files.
The local verifier checks selected factual anchors; it does not establish that
the exports are authentic, exhaustive, or representative of the live account.

## Findings in priority order

| Finding | Configuration evidence | Control evidence | Activity evidence and limit |
| --- | --- | --- | --- |
| F1 Root sign-in | Current root MFA configuration is not supplied | CC8.1 approval scope covers routine releases only | E12–E13 show root login without MFA and follow-up activity; authorization remains unknown |
| F2 RDP and runtime privilege | World-open 3389 rule, public host routing, wildcard runtime policy | CC6.6 excludes app ingress; CC6.1 review is stale | E8/E11/E23 show telemetry use, not the full access requirement; no causative change event |
| F3 Detection disabled | GuardDuty disabled; route still configured | CC7.2 FAIL / SEC-191 | No disabling event supplied; E24 corroborates separate CloudTrail collection |
| F4 Database encryption | Storage unencrypted; DB private and SSL enforced | CC6.7 FAIL / SEC-193; A1.2/A1.3 address backup/restore | E14 describes a completed backup, not proof of encryption |
| F5 Log integrity | Digest validation off; delivery active; destination uses AES256 | CC7.3 PASS explicitly excludes integrity | E10/E24 support delivery status, not tamper resistance |
| F6 Access review | Broad runtime grant makes current approval especially important | CC6.1 FAIL / SEC-184; evidence ends April 30 | Workload activity cannot substitute for dated access approval |

### F1 — P1 — Unexplained root sign-in without MFA

**Confirmed:** E12 records a successful root `ConsoleLogin` at
2026-08-29 02:14:37 UTC with `mfa_used=false` from an address described as unseen
in the preceding 30 days. E13 records `GetAccountSummary` two minutes later from
the same principal and source. These are materially different from the
noninteractive workload events with `mfa_used=null`.

**Impact and uncertainty:** Root access can have account-wide consequences.
Treat this as a suspected identity incident pending verification, not proof of
account takeover, malicious changes, or data loss. The excerpt does not establish
whether MFA is enrolled today, who used the account, or whether this session
caused any other finding. C/CC8.1 only samples routine application releases;
its PASS does not approve root use.

**Action:** Security Operations should engage the account custodian and incident
lead immediately, preserve the original sign-in/session records, and verify a
business justification through a trusted channel. If unauthorized or unexplained,
secure root credentials and recovery channels, review MFA and root access keys,
and investigate persistence, privilege changes, and resource activity across
regions. Avoid assuming a password reset invalidates every existing session.
Use the incident process and AWS Support as needed to establish containment.
[AWS root-user guidance](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html).

### F2 — P1 — Public RDP rule on a host with excessive runtime permissions

**Confirmed:** S `/security_groups/0/ingress_rules/1` allows TCP/3389 from
`0.0.0.0/0`. Its attached running Windows host has a public IP, an internet-gateway
route, and NACL settings allowing that port and return traffic. The host uses
`ProdAppRole`; S `/iam_roles/1/inline_policies/0/document/Statement/0` grants
`Action="*"`, `Resource="*"`, with no condition. The role description says it
writes application telemetry. E8, E11 and E23 show `PutLogEvents`, including a
scheduled feed, but cannot define the complete workload permission requirement.

**Impact and uncertainty:** The AWS network configuration permits an internet
path to RDP. A listening service and host-firewall rule still need verification;
`host_firewall_profile="managed"` does not prove the port is blocked. Host
compromise could expose the attached role's credentials and greatly expand the
blast radius. Effective authorization may be constrained by unprovided SCPs,
boundaries, or other denies; the identity policy itself is demonstrably excessive.
IMDSv2, patch compliance and healthy endpoint protection are useful protections,
but do not remove this risk.

**Action:** Platform Operations and Application Engineering should remove the
world-open administrative rule after establishing a tested private support path
(for example, SSM where prerequisites are met), preserving incident evidence and
essential service access. Review existing support sessions as well as the rule;
do not assume editing a stateful rule instantly ends every existing connection.
Build a runtime allowlist from application configuration, owners, and a full
operational cycle, then canary it. Do not copy DeployRole permissions onto the
application or grant the deployment role administrator rights.

**Control context:** C/CC6.6 covers private database ingress only. C/CC7.1 covers
patching and endpoint protection. Neither PASS clears application ingress or IAM
authorization. C/CC6.1's stale review increases uncertainty about approval of the
runtime policy. No rule-change or policy-change event is supplied.

### F3 — P1 — GuardDuty detection is disabled

**Confirmed:** S `/guardduty/enabled=false`; C/CC7.2 fails at 08:25 UTC and tracks
SEC-191. An alert destination and route remain configured, but a configured route
cannot compensate for a disabled detector. CloudTrail remains active: S
`/cloudtrail/is_logging=true`, recent successful deliveries, and E24 agree with
C/CC7.3's collection PASS.

**Impact and uncertainty:** GuardDuty coverage is absent in the represented
region. The disabled interval and status of other regions/accounts are unknown;
the evidence does not establish it was disabled during the root login or by root.
CloudTrail collection and endpoint protection provide partial evidence sources,
not equivalent detection coverage.

**Action:** Security Operations should preserve the configuration and change
history, restore the detector, check regional/account coverage, and test the
notification path through queue receipt and on-call acknowledgement. Investigate
the gap using retained telemetry; do not assume re-enablement backfills missed
detections. [AWS GuardDuty suspension behavior](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_suspend-disable.html).

### F4 — P2 — Database storage lacks encryption at rest

**Confirmed:** S `/rds_instances/0/storage_encrypted=false` and `kms_key_id=null`;
the data classification is regulated health data in the scenario. C/CC6.7 fails
and tracks SEC-193. The database is private and enforces SSL. Backups and restore
testing pass C/A1.2 and C/A1.3, with supporting backup activity in E14; neither
proves encryption at rest.

**Impact and uncertainty:** This is an at-rest protection gap for sensitive data,
not evidence of public database access or a breach. Review snapshot copies and
backup destinations individually; their encryption cannot all be inferred from
this snapshot. Whether the supplied KMS key is suitable requires its actual
policy, grants, ownership and recovery requirements, not only an approved label.

**Action:** Database Operations should schedule an encrypted snapshot-copy and
restore migration to a new DB instance, with Security Operations reviewing KMS
access and Application Engineering owning cutover tests. Encryption cannot simply
be toggled on for this existing unencrypted instance. Agree downtime/RPO, freeze
writes for a final consistent snapshot or separately design and test replication,
then validate the new database before resuming traffic. Keep old copies restricted
under a documented retention/incident-preservation decision.
[AWS PostgreSQL encryption migration](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/encrypt-an-existing-amazon-rds-for-postgresql-db-instance.html).

### F5 — P2 — Audit collection works, but digest integrity is disabled

**Confirmed:** S `/cloudtrail/enable_log_file_validation=false`. The trail logs
multi-region management events and successfully delivers to S3 and CloudWatch.
C/CC7.3 explicitly excludes integrity and key-management settings. The destination
bucket uses `AES256` encryption; the trail has no KMS key. This is **not** plaintext
log storage, and the available evidence does not make customer-managed KMS a
mandatory control requirement.

**Impact and uncertainty:** Digest-based tamper detection is missing. There is
no evidence that logs were altered. Versioning and 400-day retention help, but
do not establish immutability or protect against every privileged deletion.
The selectors show management events; object-level S3 data-event coverage is not
demonstrated. The trail's name does not prove organization-wide coverage.

**Action:** Security Operations should enable digest generation and explicitly
validate a subsequent delivery interval, preserving the known historical gap.
Evaluate stronger retention/access separation and KMS against the actual policy;
test delivery permissions before any encryption change. Decide data-event scope
from investigation and data-access needs rather than turning on every event type.
Enabling validation produces digests; it does not itself run validation or create
digests for the period when disabled.
[AWS integrity validation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html),
[digest gaps](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-digest-file-structure.html).

### F6 — P2 — Access-review evidence is out of date

**Confirmed:** C/CC6.1 fails, with SEC-184 open. The test ran on September 1 but
the latest completed review covers only April 30. A recent test execution does
not refresh the underlying evidence. The broad ProdAppRole grant in F2 is a
concrete reason to prioritize the workload population in the review.

**Impact and uncertainty:** Current access approvals cannot be demonstrated.
This establishes an evidence gap; it does not prove that no newer review happened
elsewhere or that every permission is unauthorized. Request the actual quarterly
schedule, complete population and approvals before judging the full period.

**Action:** Security Operations should obtain a reconciled current population,
named reviewer decisions, dated approvals and removal tickets. Separate removal
of unnecessary access from collection of missing paperwork. Record any historical
gap and compensating review; do not backdate approval or mark the failed period
as passing because today's access is corrected.

## Controls to preserve and conclusions to avoid

DeployRole is scoped to a specific OIDC audience/subject, one image repository,
and one existing environment. E4–E7 and E21–E23 show successful releases and
application health; E9 and E18 explicitly identify intentional destructive-action
negative tests returning AccessDenied. Those denials are expected, not deployment
failures or proof of an attacker. Upstream ECR authentication is described
separately, so no additional token permission for DeployRole is justified here.

Both S3 buckets have public-access blocks and no public policy; the build bucket
has KMS encryption. Public HTTPS/443 is intentional. Internal 8443 is scoped to
the VPC CIDR; ask about required callers before narrowing it. The private DB's
application-SG-only ingress, TLS, Multi-AZ, backups and restore test are meaningful
protections. KMS rotation and EBS encryption are enabled. These findings do not
justify disruptive replacement of working controls.

## Assumptions and unanswered questions

1. Treat resource names and addresses as synthetic labels; do not probe them.
   Confirm the full account/region/resource inventory and export provenance.
2. Account custodian: who used root, why, with what approval, and are raw identity,
   session, MFA and recovery-channel records consistent with E12–E13?
3. Platform/vendor owner: is RDP listening, what does the host firewall permit,
   which support sessions exist, and when should the temporary exception expire?
4. Application owner: what credentials, scheduled jobs, log streams and AWS calls
   are actually required? Obtain full policies, boundaries, SCPs and dependencies.
5. Security Operations: when did detection/integrity settings change, who approved
   them, what telemetry spans the interval, and who receives/acknowledges alerts?
6. Database/business owner: what downtime, RPO/RTO, retention, data classification
   and key ownership apply? What snapshots or replicas exist outside this export?
7. Compliance owner: provide actual evidence files, control definitions, review
   cadence, exception approvals and issue closure criteria. The CSV filenames
   are references; the referenced PDFs and reports were not supplied or reviewed.

The excerpt does not contain `AuthorizeSecurityGroupIngress`, `PutRolePolicy`,
`UpdateDetector` or `UpdateTrail` changes explaining these gaps. Retrieve full
audit/configuration history and change tickets before asserting chronology or
causality. Do not infer absence of compromise from a short, mostly routine log.

## Technical questions

Experience statements are drawn from the supplied resume. Where it does not
document a specific incident, audit deliverable, or validation result, the answer
identifies the proposed method rather than inventing a past outcome.

**1. Securing an AWS environment.** At SAP NS2, I implemented a three-layer
Terraform architecture for a regulated AWS environment, covering networking,
identity and compute with explicit remote-state contracts. I also automated a
public/private EC2 deployment with Ansible: a TLS-enabled NGINX reverse proxy,
SSH tunneling to a private Apache host, CloudWatch alarms and validation tests,
with the public host restricted to a single operator IP. These are implementation
examples; my resume does not document an inherited-resource cleanup incident.
For a cleanup, I would trace routes, security groups, instance profiles and owner
dependencies, remove unjustified access incrementally, and compare functional
and denied-access tests before and after each change.

**2. Reviewing AWS access.** My reusable Terraform infrastructure project includes
least-privilege IAM, and my ECS delivery pipeline uses OIDC instead of static AWS
credentials. The resume does not identify a particular existing role I reduced
or its before/after policy. For that review, I would combine code and owner input
with a full operational cycle of activity, scope actions to required resources,
and canary the policy using required-job tests and safe out-of-scope negative
tests. Simulation would support, rather than replace, real workload validation.

**3. Compliance evidence.** My closest relevant experience is engineering in a
FedRAMP-aligned environment at SAP NS2; my resume does not establish that I owned
a SOC 2/HIPAA audit or a particular auditor evidence request. A concrete related
artifact I built was an offline-safe pre-commit template with six local checks
and a verification checklist for restricted-network repositories. For a change-
control evidence request, I would provide versioned configuration, check results
and approvals tied to the review period, verify their coverage, and track missing
approvals or periods as gaps instead of backdating evidence.

**4. A previously passing control now fails.** I would compare the exact resource,
rule version, evaluation time and evidence period with a fresh read of AWS state
and the related configuration-change event. I would check authorization,
propagation delay and collector health to distinguish exposure from stale evidence,
contain confirmed material risk, and preserve both the prior and current results.
The record would include actor, time, approval, impacted scope, root cause or open
hypothesis, remediation owner and a fresh control test; this dataset does not
itself contain the hypothetical configuration-change event.

**5. CI/CD.** I built an ECS Fargate pipeline with GitHub Actions, Jest tests,
Docker builds and Trivy scanning that fails builds on HIGH/CRITICAL CVEs. It uses
OIDC with no static AWS credentials, pushes to ECR, deploys staging automatically,
and requires manual production approval; production releases also generate a
stakeholder summary with rollback instructions. In a separate Kubernetes project,
I implemented Prometheus/Grafana and Alertmanager routing for error-rate, latency
and crash-loop alerts. The resume does not establish that this monitoring was
integrated into the ECS pipeline or provide a particular release's safety evidence;
for that release I would retain tests, scans, image digest, approval, deployment
health and post-deployment metrics before declaring it safe.

## AI use and verification

OpenAI Codex inspected the guide, synthetic inputs and the supplied resume,
drafted the responses and plan, wrote local evidence checks, and organized the
Git commits. The requesting account owner stated that they authored the exercise
and authorized direct AI inspection of the synthetic inputs as an exception to
the published input-handling restriction. The source files are excluded from
this public repository.

Verification consists of comparisons against parsed source fields, control rows
and event locations; negative tests of the evidence verifier; and review of
AWS documentation for remediation constraints. This verification was performed
by Codex, not independently by a human or in a live AWS account. No live fix,
incident resolution or audit acceptance is claimed. Personal experience statements
use the assigned resume background and have not been independently verified.
See [verification](VERIFICATION.md) for executed checks and limitations, and
[the change plan](REMEDIATION.md) for proposed post-change validation.
