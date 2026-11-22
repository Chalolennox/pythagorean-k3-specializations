(* code/coq/F28_tangent_product_square.v

   The owner's thirty-second Coq file (22 November 2026).  The text is the owner's, with ONE change: the three imports "From Stdlib Require Import ..." are written
   "From Coq Require Import ..." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   F28_tangent_square_identity: 864 B * 3 r - (72 r^2)^2 = 2592 r f(r) - 2592 r^2 f'(r) for f = x^3 + A x + B (ring; checked by hand: both sides equal 2592 B r - 5184 r^4);
   F28_tangent_product_square: p >= 5, p | f(r), p | f'(r) ==> certificate(p, 864 B * 3 r)  (witnesses u = 1, v = 72 r^2; ~(p | 1) from p >= 5 by a nia case split on the cofactor).
   Same statement as F28_tangent_product_certificate in F28_tangent_character.v with the hypothesis ~(p | 1) replaced by 5 <= p; nothing new mathematically.
   WHAT IT DOES NOT PROVE: the cancellation to (864 B / p) = (3 r / p) (F28_tangent_character.v, F28_large_prime_tangent.v). *)

From Coq Require Import ZArith.
From Coq Require Import Ring.
From Coq Require Import Lia.

Open Scope Z_scope.

Definition F28_cubic (A B x : Z) : Z :=
  x^3 + A*x + B.

Definition F28_derivative (A x : Z) : Z :=
  3*x^2 + A.

Definition F28_square_certificate (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2-v^2).

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

Lemma F28_not_divide_one :
  forall p : Z,
    5 <= p ->
    ~ (p | 1).
Proof.
  intros p Hlarge Hdiv.
  destruct Hdiv as [k Hk].
  destruct (Z_le_gt_dec 0 k) as [Hnonneg | Hneg].
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k. lia.
    + assert (1 <= k) by lia.
      nia.
  - assert (k <= -1) by lia.
    nia.
Qed.

(* ======================================== *)
(* EXACT TANGENT IDENTITY                   *)
(* ======================================== *)

Lemma F28_tangent_square_identity :
  forall A B r : Z,
    (864*B)*(3*r)-(72*r^2)^2 =
      2592*r*F28_cubic A B r
      -2592*r^2*F28_derivative A r.
Proof.
  intros A B r.
  unfold F28_cubic, F28_derivative.
  ring.
Qed.

(* ======================================== *)
(* MAIN SQUARE CERTIFICATE                  *)
(* ======================================== *)

Theorem F28_tangent_product_square :
  forall p A B r : Z,
    5 <= p ->
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    F28_square_certificate p ((864*B)*(3*r)).
Proof.
  intros p A B r Hlarge Hcubic Hder.

  unfold F28_square_certificate.
  exists 1.
  exists (72*r^2).

  split.
  - apply F28_not_divide_one.
    exact Hlarge.

  - replace
      ((864*B)*(3*r)*1^2-(72*r^2)^2)
      with
      (2592*r*F28_cubic A B r
       -2592*r^2*F28_derivative A r).
    2:{
      unfold F28_cubic, F28_derivative.
      ring.
    }

    apply F28_divide_difference.
    + replace
        (2592*r*F28_cubic A B r)
        with
        (F28_cubic A B r*(2592*r))
        by ring.
      apply F28_divide_product.
      exact Hcubic.

    + replace
        (2592*r^2*F28_derivative A r)
        with
        (F28_derivative A r*(2592*r^2))
        by ring.
      apply F28_divide_product.
      exact Hder.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_tangent_square_identity.
Check F28_tangent_product_square.

Print Assumptions F28_tangent_product_square.
