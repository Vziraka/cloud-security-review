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
