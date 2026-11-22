(* code/coq/F28_tangent_cone.v

   The owner's thirty-first Coq file (22 November 2026).  The text is the owner's, with ONE change: the four imports "From Stdlib Require Import ..." are written
   "From Coq Require Import ..." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   For f(x) = x^3 + A x + B and a double root r mod p (p | f'(r) = 3 r^2 + A):
     F28_singular_root_nonzero: p | f'(r), p not dividing A ==> p not dividing r  (A = f'(r) - 3 r^2);
     F28_large_prime_not_divide_three: prime p >= 5 does not divide 3;
     F28_tangent_coefficient_nonzero: prime p >= 5, p | f'(r), p not dividing A ==> p not dividing 3 r  (the tangent-cone coefficient is nonzero: the node is nondegenerate);
     F28_cubic_translation: f(r + U) = f(r) + f'(r) U + U^2 (U + 3 r)  (exact, ring; checked by hand: expand (r+U)^3 + A (r+U) + B).
   Meaning: modulo p, f(r+U) = U^2 (U + 3r) when p | f(r), p | f'(r): a double root with U^2 times a nonzero linear factor, i.e. the singular point of Y^2 = f(X) is
   a node (distinct tangent directions Y^2 = 3r U^2), split iff 3r is a square mod p.  The first and the third statements already appear in F28_tangent_character.v /
   F28_singular_root.v / F28_large_prime_tangent.v; the translation identity is new to the repository.  WHAT IT DOES NOT PROVE: the Tate/Silverman statement that this
   node means multiplicative reduction, nor the minimality of the model. *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Ring.
From Coq Require Import Lia.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: NONDEGENERATE TANGENT CONE         *)
(* ======================================== *)

Definition F28_cubic (A B x : Z) : Z :=
  x^3 + A*x + B.

Definition F28_derivative (A x : Z) : Z :=
  3*x^2 + A.

Definition F28_tangent_coefficient (r : Z) : Z :=
  3*r.

(* ======================================== *)
(* DIVISIBILITY HELPERS                     *)
(* ======================================== *)

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
  destruct Hx as [k Hk].
  destruct Hy as [l Hl].
  exists (k-l).
  rewrite Hk, Hl.
  ring.
Qed.

Lemma F28_prime_product_split :
  forall p x y : Z,
    prime p ->
    (p | x*y) ->
    (p | x) \/ (p | y).
Proof.
  intros p x y Hp Hxy.
  eapply prime_mult; eauto.
Qed.

(* ======================================== *)
(* SINGULAR ROOT IS NONZERO                 *)
(* ======================================== *)

Theorem F28_singular_root_nonzero :
  forall p A r : Z,
    (p | F28_derivative A r) ->
    ~ (p | A) ->
    ~ (p | r).
Proof.
  intros p A r Hder HnotA Hr.

  assert (Hsquare : (p | r*r)).
  {
    apply F28_divide_product.
    exact Hr.
  }

  assert (Hterm : (p | 3*r^2)).
  {
    replace (3*r^2) with ((r*r)*3) by ring.
    apply F28_divide_product.
    exact Hsquare.
  }

  apply HnotA.

  replace A with
    (F28_derivative A r - 3*r^2).
  2:{
    unfold F28_derivative.
    ring.
  }

  apply F28_divide_difference.
  - exact Hder.
  - exact Hterm.
Qed.

(* ======================================== *)
(* LARGE PRIME DOES NOT DIVIDE THREE        *)
(* ======================================== *)

Lemma F28_large_prime_not_divide_three :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 3).
Proof.
  intros p Hp Hlarge Hdiv.
  destruct Hdiv as [k Hk].

  destruct (Z_le_gt_dec 0 k) as [Hnonneg | Hneg].
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k.
      lia.
    + assert (1 <= k) by lia.
      nia.
  - assert (k <= -1) by lia.
    nia.
Qed.

(* ======================================== *)
(* NONZERO TANGENT COEFFICIENT              *)
(* ======================================== *)

Theorem F28_tangent_coefficient_nonzero :
  forall p A r : Z,
    prime p ->
    5 <= p ->
    (p | F28_derivative A r) ->
    ~ (p | A) ->
    ~ (p | F28_tangent_coefficient r).
Proof.
  intros p A r Hp Hlarge Hder HnotA Htangent.

  unfold F28_tangent_coefficient in Htangent.

  destruct
    (F28_prime_product_split p 3 r Hp Htangent)
    as [Hthree | Hr].
  - apply (F28_large_prime_not_divide_three p).
    + exact Hp.
    + exact Hlarge.
    + exact Hthree.
  - apply (F28_singular_root_nonzero p A r).
    + exact Hder.
    + exact HnotA.
    + exact Hr.
Qed.

(* ======================================== *)
(* EXACT CUBIC TRANSLATION                  *)
(* ======================================== *)

Theorem F28_cubic_translation :
  forall A B r U : Z,
    F28_cubic A B (r+U) =
      F28_cubic A B r
      + F28_derivative A r*U
      + U^2*(U+F28_tangent_coefficient r).
Proof.
  intros A B r U.
  unfold F28_cubic,
    F28_derivative,
    F28_tangent_coefficient.
  ring.
Qed.

(* ======================================== *)
(* FINAL CHECKS                             *)
(* ======================================== *)

Check F28_singular_root_nonzero.
Check F28_tangent_coefficient_nonzero.
Check F28_cubic_translation.

Print Assumptions F28_singular_root_nonzero.
Print Assumptions F28_tangent_coefficient_nonzero.
Print Assumptions F28_cubic_translation.
