# Work notes

## Scope

- Read the challenge guide and all three synthetic source files.
- Use the snapshot's 2026-09-01 09:00 UTC time as the assessment cutoff, not the
  workstation's current date. The event excerpt is incomplete by design.
- Review the intersection of configuration, control scope, and observed activity.
- Do not mistake a passed control for proof of unrelated controls, or an omitted
  event for proof that an action never occurred.
- Produce genuine incremental commits; do not invent a debugging history.
- The account owner states that they authored the exercise and authorizes AI
  inspection of its synthetic inputs. This departs from the published exercise's
  instruction prohibiting exposure of those inputs to AI, and will be disclosed.

## Initial observations

Root activity warrants urgent investigation without claiming an established
compromise. Public RDP and the attached application's wildcard policy form a
plausible high-impact attack path. GuardDuty, database encryption, access-review
evidence, and CloudTrail integrity require separate findings. Routine deployment
successes and intentional negative permission tests support preserving DeployRole.

## Correlation and review decisions

- Did not equate absent CloudTrail KMS configuration with absent encryption:
  the destination uses AES256. The concrete issue is disabled digest validation.
- Did not infer that root opened RDP or disabled GuardDuty: the excerpt contains
  no corresponding mutation events or causal link.
- Kept routine release approvals and narrow deployment permissions separate from
  application-role authorization and emergency support access.
- Checked RDS migration constraints in AWS documentation and made write handling
  and the post-cutover rollback limitation explicit.
- Read the supplied resume in Chrome. Replaced generic personal-answer examples
  with supported Terraform/Ansible and CI/CD experience; retained clear limits
  where no past IAM-reduction or audit-evidence case was documented.
- Compared 68 factual anchors with parsed inputs. Eight regression checks passed,
  including intentionally changed disposable inputs and malformed/missing data.
- Used Python's standard library only. No cloud provisioning, dependency install,
  scanner framework or automatic public-data fetch is needed for this exercise.
