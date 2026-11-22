(* code/coq/F28_candidate_root_relation.v

   The owner's thirty-fifth Coq file (22 November 2026), sent twice with identical text.  The text is the owner's, with ONE change: the import line "From Stdlib Require Import ZArith Ring."
   is written "From Coq Require Import ZArith Ring." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone (no primality used).
   For the paper's model A = 4 a c^3, B = -8 b c^5 and the candidate root r = -3 B u = 24 b c^5 u:
     F28_candidate_root_identity: a^2 (3 r) - (3c)^2 (a b) = (2 A u - 1) * 9 a b c^2  (ring; checked by hand: 72 a^2 b c^5 u - 9 a b c^2 = 9 a b c^2 (8 a c^3 u - 1));
     F28_candidate_root_relation: p | 2 A u - 1 ==> p | a^2 (3 r) - (3c)^2 (ab);   F28_inverse_gives_arithmetic_root: the existential form.
   Hence modulo p the class of 3r is that of ab (3 r a^2 = ab (3c)^2).  WHAT IT DOES NOT PROVE: the passage from the relation to the character (F28_square_scaling.v,
   F28_root_arithmetic_equivalence, F28_candidate_root_class), nor that EVERY double root has this class (the double root is unique mod p when p does not divide A; not proved in Coq; the
   theorems F28_discriminant_split_criterion / F28_specialized_singular_root produce a root, not named as the candidate root: not composed yet). *)

From Coq Require Import ZArith Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: SINGULAR ROOT ARITHMETIC RELATION  *)
(* ======================================== *)

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_candidate_root (b c u : Z) : Z :=
  -3*F28_B b c*u.

(* ======================================== *)
(* DIVISIBILITY UNDER MULTIPLICATION        *)
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

(* ======================================== *)
(* EXACT ARITHMETIC IDENTITY                *)
(* ======================================== *)

Theorem F28_candidate_root_identity :
  forall a b c u : Z,
    a^2*(3*F28_candidate_root b c u)
      -(3*c)^2*(a*b)
    =
    (2*F28_A a c*u-1)*(9*a*b*c^2).
Proof.
  intros a b c u.
  unfold F28_candidate_root, F28_A, F28_B.
  ring.
Qed.

(* ======================================== *)
(* MODULAR CONSEQUENCE                      *)
(* ======================================== *)

Theorem F28_candidate_root_relation :
  forall p a b c u : Z,
    (p | 2*F28_A a c*u-1) ->
    (p |
      a^2*(3*F28_candidate_root b c u)
      -(3*c)^2*(a*b)).
Proof.
  intros p a b c u Hinverse.

  rewrite F28_candidate_root_identity.

  apply F28_divide_product.
  exact Hinverse.
Qed.

(* ======================================== *)
(* EXISTENTIAL FORM                         *)
(* ======================================== *)

Theorem F28_inverse_gives_arithmetic_root :
  forall p a b c : Z,
    (exists u : Z,
      (p | 2*F28_A a c*u-1)) ->
    exists r : Z,
      (p | a^2*(3*r)-(3*c)^2*(a*b)).
Proof.
  intros p a b c Hinverse.
  destruct Hinverse as [u Hu].

  exists (F28_candidate_root b c u).

  apply F28_candidate_root_relation.
  exact Hu.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_candidate_root_identity.
Check F28_candidate_root_relation.
Check F28_inverse_gives_arithmetic_root.

Print Assumptions F28_inverse_gives_arithmetic_root.
