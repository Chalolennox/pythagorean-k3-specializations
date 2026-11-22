(* code/coq/F28_candidate_singular.v

   The owner's thirty-eighth Coq file (22 November 2026).  The text is the owner's, with ONE change: the import line "From Stdlib Require Import ZArith Ring." is written "From Coq Require Import ZArith Ring."
   (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone (no primality).
   F28_candidate_singular: p | F(a,b,c) and p | 2 A u - 1 (A = 4 a c^3) ==> for r = -3 B u = 24 b c^5 u (B = -8 b c^5): p | r^3 + A r + B and p | 3 r^2 + A.
   Built from: Delta = -64 c^9 F (ring), the two candidate identities (ring; the same as in F28_candidate_root.v with B, A generic), and the divisibility steps.  Checked by hand.
   It is the specialization of F28_candidate_is_singular (F28_candidate_root.v) to the paper's model with the hypothesis p | F in place of p | Delta. *)

From Coq Require Import ZArith Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: SINGULARITY OF THE CANDIDATE ROOT  *)
(* ======================================== *)

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_F (a b c : Z) : Z :=
  4*a^3+27*b^2*c.

Definition F28_cubic (A B x : Z) : Z :=
  x^3+A*x+B.

Definition F28_derivative (A x : Z) : Z :=
  3*x^2+A.

Definition F28_discriminant (A B : Z) : Z :=
  -4*A^3-27*B^2.

Definition F28_candidate_root (b c u : Z) : Z :=
  -3*F28_B b c*u.

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

Lemma F28_divide_sum :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x+y).
Proof.
  intros p x y Hx Hy.
  destruct Hx as [k Hk].
  destruct Hy as [l Hl].
  exists (k+l).
  rewrite Hk, Hl.
  ring.
Qed.

Lemma F28_divide_neg :
  forall p x : Z,
    (p | x) ->
    (p | -x).
Proof.
  intros p x H.
  destruct H as [k Hk].
  exists (-k).
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
  apply F28_divide_sum.
  - exact Hx.
  - apply F28_divide_neg.
    exact Hy.
Qed.

(* ======================================== *)
(* DISCRIMINANT SPECIALIZATION              *)
(* ======================================== *)

Lemma F28_discriminant_identity :
  forall a b c : Z,
    F28_discriminant
      (F28_A a c) (F28_B b c)
    =
    -64*c^9*F28_F a b c.
Proof.
  intros a b c.
  unfold F28_discriminant, F28_A, F28_B, F28_F.
  ring.
Qed.

Lemma F28_F_divides_discriminant :
  forall p a b c : Z,
    (p | F28_F a b c) ->
    (p |
      F28_discriminant
        (F28_A a c) (F28_B b c)).
Proof.
  intros p a b c HF.
  rewrite F28_discriminant_identity.

  replace (-64*c^9*F28_F a b c)
    with (F28_F a b c*(-64*c^9))
    by ring.

  apply F28_divide_product.
  exact HF.
Qed.

(* ======================================== *)
(* EXACT DERIVATIVE IDENTITY                *)
(* ======================================== *)

Lemma F28_candidate_derivative_identity :
  forall A B u : Z,
    F28_derivative A (-3*B*u)
    =
    -(u^2)*F28_discriminant A B
    -A*((2*A*u-1)*(2*A*u+1)).
Proof.
  intros A B u.
  unfold F28_derivative, F28_discriminant.
  ring.
Qed.

(* ======================================== *)
(* EXACT CUBIC IDENTITY                     *)
(* ======================================== *)

Lemma F28_candidate_cubic_identity :
  forall A B u : Z,
    F28_cubic A B (-3*B*u)
    =
    B*F28_discriminant A B*u^3
    -(2*A*u-1)*
      (A*(-3*B)*u*(2*A*u+1)
       +B*((2*A*u)^2+2*A*u+1)).
Proof.
  intros A B u.
  unfold F28_cubic, F28_discriminant.
  ring.
Qed.

(* ======================================== *)
(* SINGULARITY: DERIVATIVE                  *)
(* ======================================== *)

Theorem F28_candidate_derivative_zero :
  forall p A B u : Z,
    (p | F28_discriminant A B) ->
    (p | 2*A*u-1) ->
    (p | F28_derivative A (-3*B*u)).
Proof.
  intros p A B u HD Hu.

  rewrite F28_candidate_derivative_identity.

  apply F28_divide_difference.

  - replace
      (-(u^2)*F28_discriminant A B)
      with
      (F28_discriminant A B*(-u^2))
      by ring.
    apply F28_divide_product.
    exact HD.

  - replace
      (A*((2*A*u-1)*(2*A*u+1)))
      with
      ((2*A*u-1)*(A*(2*A*u+1)))
      by ring.
    apply F28_divide_product.
    exact Hu.
Qed.

(* ======================================== *)
(* SINGULARITY: CUBIC                       *)
(* ======================================== *)

Theorem F28_candidate_cubic_zero :
  forall p A B u : Z,
    (p | F28_discriminant A B) ->
    (p | 2*A*u-1) ->
    (p | F28_cubic A B (-3*B*u)).
Proof.
  intros p A B u HD Hu.

  rewrite F28_candidate_cubic_identity.

  apply F28_divide_difference.

  - replace
      (B*F28_discriminant A B*u^3)
      with
      (F28_discriminant A B*(B*u^3))
      by ring.
    apply F28_divide_product.
    exact HD.

  - apply F28_divide_product.
    exact Hu.
Qed.

(* ======================================== *)
(* INTEGRATED SPECIALIZED SINGULARITY       *)
(* ======================================== *)

Theorem F28_candidate_singular :
  forall p a b c u : Z,
    (p | F28_F a b c) ->
    (p | 2*F28_A a c*u-1) ->
    let r := F28_candidate_root b c u in
      (p | F28_cubic (F28_A a c) (F28_B b c) r)
      /\
      (p | F28_derivative (F28_A a c) r).
Proof.
  intros p a b c u HF Hu.
  simpl.

  assert (HD :
    (p |
      F28_discriminant
        (F28_A a c) (F28_B b c))).
  {
    apply F28_F_divides_discriminant.
    exact HF.
  }

  unfold F28_candidate_root.

  split.

  - apply F28_candidate_cubic_zero.
    + exact HD.
    + exact Hu.

  - apply F28_candidate_derivative_zero.
    + exact HD.
    + exact Hu.
Qed.

(* ======================================== *)
(* FINAL VERIFICATION                       *)
(* ======================================== *)

Check F28_discriminant_identity.
Check F28_candidate_derivative_identity.
Check F28_candidate_cubic_identity.
Check F28_candidate_singular.

Print Assumptions F28_candidate_singular.
