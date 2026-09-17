# AWS security and control review

Assessment work product for Ensizziyo Ziraka (`Vziraka`). Based on the synthetic
[Cloud Security Engineer Challenge](https://github.com/ConsensioHealth/Cloud_Security_Engineer_Challenge).

Scope: review the supplied AWS snapshot, control export, and event excerpt;
prioritize findings; propose safe remediation and measurable validation.
No live AWS deployment or production changes are part of this review.

Start with [Ensizziyo Ziraka's response](Ensizziyo_Ziraka_Response.md) for the six
prioritized findings, evidence references, five technical answers and AI disclosure.
Then read the [remediation and validation plan](REMEDIATION.md).

The [verification record](VERIFICATION.md) describes executed local checks and
their limits. [Work notes](WORK_NOTES.md) record review decisions. No fix has been
applied to an AWS account. The source data and original resume are not included;
selected synthetic facts are cited to make the reasoning reviewable.

The [timed second-pass review](TIMED_REVIEW.md) records scheduled stages, actual
execution times, editorial refinements and the deliberate fault/correction exercise.

## Reproduce the factual checks

Python 3.10+ and its standard library are sufficient. Obtain the three exercise
files through an approved channel and keep them together outside this repository.
The scripts do not download, upload or call AWS. Run from an approved local working
directory: tests make temporary copies there and remove them when finished.

```sh
python /path/to/cloud-security-review/verify_evidence.py /path/to/exercise-files
python /path/to/cloud-security-review/test_verify_evidence.py /path/to/exercise-files
```

On Windows, quote paths containing spaces. The verifier returns 0 for matching
anchors, 1 for differences and 2 for missing/malformed inputs. A match confirms
selected statements about this fixed dataset, **not a secure AWS environment**.
The scripts are intentionally specific to the original exercise, including event
line numbers. A different dataset requires review, not automatic acceptance.

## Provenance

The requesting owner states that they authored the exercise and authorized AI
inspection of its synthetic data. The [disclosure](Ensizziyo_Ziraka_Response.md#ai-use-and-verification)
records this exception to the published AI-data restriction and how outputs were
checked. Resume-based statements are distinguished from proposed methods where
the source does not establish a specific past result. Git history reflects actual
stages of work.
