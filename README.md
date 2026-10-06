# Non-cut points of Hausdorff continua

Every nontrivial compact connected subset `C` of a Hausdorff space contains distinct points `x` and `y` such that `C \ {x}` and `C \ {y}` are each connected. Removal is individual. A compact connected subset `K` of `C` containing every non-cut point of `C` equals `C`.

`Solution.lean` proves both results in 361 lines. It uses no metric, local connectedness, path connectedness, or ambient compactness assumption. `Challenge.lean` imports Mathlib alone and gives the two independent statement contracts with deliberate theorem holes. Its explicit predicate `IsNonCutPoint C x` means `x ∈ C ∧ IsConnected (C \ {x})`.

The source is Paul Bankston's [Metric Topology: A First Course](https://www.mscsnet.mu.edu/~paul/Paper/4450102text.pdf#page=91), Lecture 29, Propositions 29.1 and 29.3, printed pages 91 through 93. The proof first shows that adjoining a cut point to either open side gives a connected set. It then orients cuts toward a fixed side and proves that their tails nest. A point in the intersection of a chain of compact tails supplies a lower bound. Zorn's lemma gives a minimal tail, contradicted by a smaller tail. The cut sides themselves may be disconnected.

The exact pins are Lean `4.35.0-rc2` and Mathlib `065356127b1dc0016f66b7283ce0ce2c4055aa55`. The development depends on Mathlib alone and uses no proof source from the earlier topology projects.

For an ordinary dependency installation and strict verification, run:

```text
python3 scripts/verify.py --lake-build
```

The verifier compiles Solution afresh, compiles an isolated random-name Challenge using dependency paths alone, compares complete types and universe parameters, compares the explicit predicate's type and value, and audits transitive axioms. The CI workflow runs the same command. Local checks pass. Independent AI review approved the full mathematical scope and repeated the proof, contract, predicate, axiom, metadata and package checks. The approved proof bytes are unchanged. See `VERIFICATION.md` and `REVIEW.md` for exact scope and remaining limits. Publication belongs to the parent workflow.

The theorem concerns the structure of non-cut points in arbitrary Hausdorff continua. It provides a self-contained formal contribution for researchers in general topology and continuum theory. It formalizes a classical result; no mathematical novelty or source-author endorsement is claimed.
