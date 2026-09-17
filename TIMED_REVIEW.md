# Timed assessment review

This is a scheduled second pass over the existing assessment, authorized by the
exercise owner. It preserves the earlier submission and commit history. Elapsed
schedule time includes intervals between runs; it is not a claim of continuous
hands-on effort. Deliberate faults will be labeled test exercises.

Start: 2026-09-17 20:10 UTC (16:10 America/New_York).
Target finish: 21:25 UTC (17:25 local), after 75 minutes.

| Stage | Earliest start UTC | Work and completion artifact |
| --- | --- | --- |
| 1 | 20:10 | Re-read guide and evidence; document requirements-to-deliverables checklist and review priorities; commit notes. |
| 2 | 20:25 | Review findings and technical answers against evidence, preserve resume background, improve specific gaps; commit meaningful revisions. |
| 3 | 20:45 | Introduce labeled faults in disposable local data; record expected and observed failures and diagnosis without publishing raw inputs; commit exercise notes/checks. |
| 4 | 21:00 | Correct disposable faults, rerun verification, improve remediation acceptance criteria based on review; commit verified changes. |
| 5 | 21:15 | Perform final requirement, publication and history review; prepare package. |
| Finish | 21:25 | Record actual completion, commit/push final report, verify remote HEAD and ZIP, pause scheduler and report links. |

Codex checks the saved checkpoint every five minutes and runs only the next due
incomplete stage. Actual start/finish times will be recorded below; delayed runs
will not be backdated. No live AWS changes are authorized by this exercise.

## Execution record

Scheduling setup: inspected repository status and existing scope notes; preserved
the clean baseline at commit `8ff1e5b`.

### Stage 1 — Requirements and evidence review

Started at 20:12:28 UTC, on the first scheduled wake-up after the 20:10 target.
Re-read the local challenge guide, all three source files, the main response and
the remediation plan. No source data or resume was added to Git.

| Requirement | Existing coverage | Second-pass review focus |
| --- | --- | --- |
| Five brief technical answers | Main response, Technical questions | Preserve resume-based background; distinguish recorded experience from proposed validation. |
| Review all three inputs together | F1–F6 use snapshot paths, control IDs and event references | Add a compact cross-source matrix so the relationships are easier to scan. |
| Prioritize material risks | Immediate root investigation, public RDP/runtime privilege and disabled detection precede scheduled corrections | Explain why the database migration is planned while containment starts immediately. |
| Separate facts from hypotheses | Each finding has confirmed observations and uncertainty | Tighten F2 title so network configuration is not mistaken for a verified listening RDP service. |
| Practical remediation with owners | Remediation table and database rollback gate | Make closure criteria distinguish incident escalation from actual incident resolution. |
| AWS, monitoring and compliance validation | Plan covers fresh state, functional tests, alert delivery and refreshed evidence | Retain historical gaps and ensure current PASS is not represented as period-wide effectiveness. |
| Assumptions and evidence requests | Seven owner questions and missing mutation-history caveat | Keep absent approvals and unprovided evidence attachments explicitly unresolved. |
| AI disclosure and handling | Main response records owner-authorized input inspection | Preserve the actual workflow; no claim of unaided work. |
| Readable named response and ZIP | Named Markdown response, public repository and earlier ZIP | Rebuild ZIP only after the scheduled final commit so it includes the redo. |

The six existing findings remain supported by the supplied evidence. Review
priorities are clarity and measurable closure, not inventing additional risks.
Two wording issues are queued for stage 2: the F2 heading overstates verified
reachability, and F1's closure table currently allows “escalated” to read as
equivalent to resolved. Neither changes the underlying observed evidence.

The 68-anchor verifier checks a fixed dataset, not corrected AWS posture. The
later fault exercise must show mismatched inputs being rejected and restored
reference inputs matching again; it must not call that a live remediation test.

Stage 1 completed at 20:13:21 UTC in commit `6a25fbb`.

### Stage 2 — Findings and response refinement

Started at 20:29:28 UTC, the first scheduled wake-up after the 20:25 target.
Added a six-row configuration/control/activity matrix, clarified why database
migration follows immediate containment, and corrected the RDP heading to describe
the observed rule rather than imply a successful connection test. Updated root
incident closure to require a documented disposition; escalation alone is no
longer listed as closure evidence.

Reviewed all five technical answers and retained their resume-based background.
Clarified the final disclosure so its verification limits do not contradict those
assigned-background statements. No unsupported past outcomes were added. Changes
are editorial clarifications based on already reviewed evidence, not new AWS
findings. Test-fault work remains scheduled for stage 3.

Stage 2 completed at 20:30:27 UTC in commit `f2faba4`.

### Stage 3 — Deliberate fault exercise

Started at 20:46:59 UTC. Created two separate disposable local copies of the
three source files outside the repository. These faults were deliberately
introduced for testing; they are not accidental mistakes or changes in AWS.

| Exercise fault | Expected behavior | Observed result | Diagnosis and next correction |
| --- | --- | --- | --- |
| Change E12's MFA flag to true in a copy | Reject the factual mismatch with exit 1 | 67/68 anchors matched; `MISMATCH: E12 mfa_used`; exit 1 | The altered sign-in fact no longer supports the report. Restore the original event bytes, not the verifier's expected value. |
| Append a duplicate control row in another copy | Reject ambiguous control identity with exit 2 | Input error; exit 2 | Duplicate IDs could otherwise overwrite evidence during dictionary construction. Restore the original CSV and retain the uniqueness check. |

Compared all original source bytes before and after the exercise: unchanged.
Faulty copies and detailed command logs remain only in the local work directory
for stage 4. No input copies are committed. The second error message is generic
by design; the known injection identifies the duplicate-ID cause in this test.
Neither result certifies live account security, and no report conclusions were
rewritten to accommodate deliberately false input.

Stage 3 completed at 20:47:56 UTC in commit `cdbd7d4`.

### Stage 4 — Correction and validation

Started at 21:04:29 UTC, the first scheduled wake-up after the 21:00 target.
Restored the original event-file bytes in the MFA exercise and original CSV bytes
in the duplicate-control exercise. Compared every file in both copies with the
originals: all matched byte for byte. Each restored copy returned exit 0 with
68/68 factual anchors matched. The existing eight regression checks also passed.

No verifier expectation was weakened to accept altered evidence. The local test
copies now contain the reference state; this is evidence-restoration testing,
not a claim that the scenario's AWS risks were remediated. Detailed before/after
test logs remain local.

Added measurable change-acceptance requirements to the remediation plan: agreed
baselines and thresholds, full-cycle job validation, timed alert acknowledgement,
data reconciliation, and approved RPO/RTO. Also made evidence-quality failures a
barrier to finding closure. Final publication review remains scheduled for stage 5.

Stage 4 completed at 21:05:22 UTC in commit `a476af0`.

### Stage 5 — Publication review

Started at 21:15:59 UTC. Checked the nine-file publication allowlist, all historical
Git paths, local Markdown link targets, Python syntax, common credential patterns
and whitespace. Confirmed six finding sections and five technical answers; the
technical-answer section is unchanged from the pre-redo baseline. The working
tree was clean at the start of the review.

Updated the verification record to include the ninth file and timed fault exercise,
and linked this review from the README. Reviewed actual commit timestamps for the
completed stages. Raw datasets, local fault copies, resume and checkpoint are
absent from Git history. Final ZIP regeneration and remote verification remain
scheduled for 21:25 UTC or the first wake-up thereafter.
