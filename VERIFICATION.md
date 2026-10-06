# Desktop verification

Both selected non-cut-point statements pass local Lean verification at Lean `4.35.0-rc2` and Mathlib `065356127b1dc0016f66b7283ce0ce2c4055aa55`. Solution has 361 lines and no admissions or new axioms. Challenge is 1,612 bytes and contains two intentional statement holes; it imports Mathlib alone and compiles without Solution.

| Check | Result | Private evidence |
| --- | --- | --- |
| Fresh Solution compilation with warnings as errors | Passed locally and repeated independently | `verification.json`; independent review receipts |
| Random-name Challenge using dependency paths alone | Passed, with two deliberate-hole warnings | `verification.json` |
| Complete theorem types and universe parameters | Byte-identical raw representations in separate processes | `verification.json` |
| Explicit non-cut predicate type and value | Byte-identical raw representations | `verification.json` |
| Transitive theorem axioms | Only `propext`, `Classical.choice`, `Quot.sound` | `verification.json` |
| Predicate axioms | None, confirmed independently | `verification.json`; independent review receipts |
| Independent AI mathematical and package review | Approved full scope and reviewed source snapshot | `evidence/independent-review/review-decision.json` |
| Official v0.4 JSON Schema | Passed; three invalid controls rejected | `evidence/schema-validation.json` |
| Pinned intake metadata validators | Passed with a duplicate-rejecting JSON decoder | `formalization-validation.json` |
| Copied dependency provenance | 9 pinned clean source trees; 12,642 matching copied files | `evidence/dependency-byte-provenance.json` |
| Complete tracked Mathlib scan | 9,123 Lean files; 211 reviewed candidates; no equivalent target located | `evidence/complete-mathlib-search.json` |

The final verification stage took 42.05 seconds. A Windows Job Object restricted the full process group to one CPU, 3 GiB of committed memory and a 3,600-second timeout. Lean used one worker and its 3,072 MiB internal cap. Peak job commit was 2,401,804,288 bytes; peak sampled aggregate RSS was 754,872,320 bytes. No owned processes remained, and the start/end source hashes match. The exact compiler binary hash, commands, source hashes, resource samples and cleanup appear in the private receipt.

Dependency objects came from a permitted pinned cache. Every copied source and complete artifact family is byte-identical to that cache. Exact manifest revisions and clean tracked source trees were checked. Dependency objects were not rebuilt here. The provenance stage has a separate stable-source receipt.

The official schema and intake rule files have verified Git blob identities. Metadata is JSON-form YAML. PowerShell `Test-Json` checks the full official schema and rejects an invalid relationship, a thin wrapper missing its substantive source and a negative admission count. The pinned Python validators run unchanged with a duplicate-rejecting JSON decoder substituted at their YAML decoding boundary. These checks cover this exact JSON document; general YAML parsing was not tested. No denied installation or shared-ownership bypass was used.

The private archive retains failed attempts. Initial Lean passes required equality rewriting, subtype instance names and lint corrections. Two early verifier runs mishandled the predicate's empty axiom list; the final parser accepts the explicitly reported absence of axioms. A dependency-copy attempt detected draft creation during the stage and was repeated with stable source. Only the final passing receipts support the result.

Independent AI review approved both full-scope non-cut-point statements, the exposed predicate and the reviewed 16-file public source snapshot. The reviewer checked the mathematical argument and independently repeated strict compilation, an isolated dependency-only Challenge, exact theorem types and universes, predicate type and value, a literal predicate check, and transitive axioms. The reviewer also verified the exact JSON metadata against the official schema and intake validators, source requirements, dependency byte provenance, the duplicate assessment, archive integrity and public privacy whitelist. No mathematical or local Lean proof blocker was found. The original proof receipts and independent decision record the pre-refresh metadata hash. Post-review metadata/schema checks and the refresh receipt connect the new reader prose and metadata to the unchanged approved source, without a repeat proof build. A clean dependency rebuild, ordinary Lake build, GitHub Actions execution, hosted Comparator, NanoDa and con-ron independent kernel replay, and human mathematical review remain unrun. CI is defined. The desktop task makes no public repository change or registry submission. The public publication archive has an explicit 16-file whitelist; the private review archive includes exact source and evidence and excludes cached binaries and transfer helpers.
