(* code/coq/F28_singular_root.v

   The owner's eighteenth Coq file (22 November 2026), unchanged except for this header.  Standalone.
   WHAT IT PROVES: for f(X) = X^3 + A X + B with f'(r) = 3 r^2 + A, if p | f'(r) and p does not divide A, then p does not divide r
   (if p | r then p | 3 r^2, so p | A = f'(r) - 3 r^2).  No hypothesis on p (not even primality).  Correct and sound.
   WHY IT MATTERS: it is the nonvanishing input of the tangent equivalence of F28_tangent_character.v: at a double root r of the cubic mod p,
   p not dividing A gives p not dividing r, hence p not dividing 3r (p >= 5) and, with p | f(r), p not dividing B.  The combined theorem
   F28_nodal_split_criterion (all hypotheses discharged: prime p >= 5, p | f(r), p | f'(r), p not dividing A) is in F28_tangent_character.v. *)
From Coq Require Import ZArith.
From Coq Require Import Ring.

Open Scope Z_scope.

Definition F28_derivative (A r : Z) : Z :=
  3*r^2 + A.

Lemma F28_divide_product :
  forall p x y : Z,
    (p | x) ->
    (p | x*y).
Proof.
  intros p x y H.
  destruct H as [k Hk].
  exists (k*y).
  rewrite Hk.
  ring.
Qed.

Lemma F28_divide_difference :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x-y).
Proof.
  intros p x y Hx Hy.
  destruct Hx as [u Hu].
  destruct Hy as [v Hv].
  exists (u-v).
  rewrite Hu, Hv.
  ring.
Qed.

Theorem F28_singular_root_nonzero :
  forall p A r : Z,
    (p | F28_derivative A r) ->
    ~ (p | A) ->
    ~ (p | r).
Proof.
  intros p A r Hderivative Hnonzero Hr.

  assert (Hr2 : (p | r*r)).
  {
    apply F28_divide_product.
    exact Hr.
  }

  assert (Hthree : (p | 3*r^2)).
  {
    replace (3*r^2) with ((r*r)*3) by ring.
    apply F28_divide_product.
    exact Hr2.
  }

  apply Hnonzero.

  replace A with
    (F28_derivative A r - 3*r^2).
  - apply F28_divide_difference.
    + exact Hderivative.
    + exact Hthree.
  - unfold F28_derivative.
    ring.
Qed.

Check F28_singular_root_nonzero.
Print Assumptions F28_singular_root_nonzero.
