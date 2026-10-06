/-
Copyright (c) 2026 Arthur Freitas Ramos, David Barros Hulak,
Ruy Jose Guerra Barretto de Queiroz. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Arthur Freitas Ramos, David Barros Hulak, Ruy Jose Guerra Barretto de Queiroz
-/
module

public import Mathlib.Topology.Separation.Hausdorff
public import Mathlib.Topology.Connected.Clopen
public import Mathlib.Order.Zorn

/-!
Independent statement contracts for Bankston's non-cut point theorem.
Both removals in the first result are individual removals. The predicate in
the second result explicitly means membership and connectedness after removal.
The two proof holes are intentional; this module imports Mathlib alone.
-/

@[expose] public section

open Set

universe u

namespace NonCutPoints

variable {X : Type u} [tX : TopologicalSpace X]

/-- A point of a set whose individual removal leaves a connected set. -/
def IsNonCutPoint (C : Set X) (x : X) : Prop :=
  x ∈ C ∧ IsConnected (C \ {x})

theorem exists_two_noncut_points [t2X : T2Space X] {C : Set X}
    (hCcompact : IsCompact C) (hCconnected : IsConnected C) (hCnontrivial : C.Nontrivial) :
    ∃ x ∈ C, ∃ y ∈ C, x ≠ y ∧ IsConnected (C \ {x}) ∧ IsConnected (C \ {y}) := by
  sorry

theorem eq_of_contains_noncut_points [t2X : T2Space X] {C K : Set X}
    (hCcompact : IsCompact C) (hCconnected : IsConnected C)
    (_hKcompact : IsCompact K) (hKconnected : IsConnected K) (hKC : K ⊆ C)
    (hcontains : ∀ x, IsNonCutPoint C x → x ∈ K) : K = C := by
  sorry

end NonCutPoints
