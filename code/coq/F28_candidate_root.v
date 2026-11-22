(* code/coq/F28_candidate_root.v

   The owner's twenty-fourth Coq file (22 November 2026), unchanged except for this header.  Standalone (ZArith, Ring only; no primality needed).
   For f(X) = X^3 + A X + B, Delta = -4 A^3 - 27 B^2, candidate root r = -3 B u:
     F28_candidate_derivative_identity: f'(r) = -u^2 Delta - A (2 A u - 1)(2 A u + 1);
     F28_candidate_cubic_identity:      f(r) = B u^3 Delta - (2 A u - 1)(A (-3B) u (2 A u + 1) + B ((2 A u)^2 + 2 A u + 1))
   (both ring identities, checked by hand; they are the specializations of the transport identities of F28_root_transport.v), and
     F28_candidate_is_singular: p | Delta and p | 2 A u - 1  ==>  p | f(r) and p | f'(r)   (for ANY integer p, u).
   WHAT IT DOES NOT PROVE: that such a u exists.  That is Bezout (p prime, p not dividing 2A), done in F28_large_prime_tangent.v
   (F28_double_root_exists); the hypothesis p | 2 A u - 1 here is exactly the inverse relation produced there.  Compare F28_root_transport.v:
   the same identities written with the definition F28_candidate_root; the two files are consistent. *)

From Coq Require Import ZArith.
From Coq Require Import Ring.

Open Scope Z_scope.

Definition F28_cubic (A B x : Z) : Z :=
  x^3 + A*x + B.

Definition F28_derivative (A x : Z) : Z :=
  3*x^2 + A.

Definition F28_discriminant (A B : Z) : Z :=
  -4*A^3 - 27*B^2.

Definition F28_root_numerator (B : Z) : Z :=
  -3*B.

Definition F28_root_denominator (A : Z) : Z :=
  2*A.

Definition F28_candidate_root (B u : Z) : Z :=
  F28_root_numerator B*u.

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
  destruct Hy as [m Hm].
  exists (k+m).
  rewrite Hk, Hm.
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
  destruct Hy as [m Hm].
  exists (k-m).
  rewrite Hk, Hm.
  ring.
Qed.

(* ======================================== *)
(* CANDIDATE DERIVATIVE IDENTITY            *)
(* ======================================== *)

Theorem F28_candidate_derivative_identity :
  forall A B u : Z,
    F28_derivative A
      (F28_candidate_root B u)
    =
    -u^2*F28_discriminant A B
    - A*
      (F28_root_denominator A*u-1)*
      (F28_root_denominator A*u+1).
Proof.
  intros A B u.
  unfold F28_candidate_root.
  unfold F28_derivative.
  unfold F28_root_numerator.
  unfold F28_root_denominator.
  unfold F28_discriminant.
  ring.
Qed.

(* ======================================== *)
(* CANDIDATE CUBIC IDENTITY                 *)
(* ======================================== *)

Theorem F28_candidate_cubic_identity :
  forall A B u : Z,
    F28_cubic A B
      (F28_candidate_root B u)
    =
    B*u^3*F28_discriminant A B
    -
    (F28_root_denominator A*u-1)*
    (A*(F28_root_numerator B)*u*
       (F28_root_denominator A*u+1)
     + B*
       ((F28_root_denominator A*u)^2
        + F28_root_denominator A*u+1)).
Proof.
  intros A B u.
  unfold F28_candidate_root.
  unfold F28_cubic.
  unfold F28_root_numerator.
  unfold F28_root_denominator.
  unfold F28_discriminant.
  ring.
Qed.

(* ======================================== *)
(* DERIVATIVE DIVISIBILITY                  *)
(* ======================================== *)

Theorem F28_candidate_derivative_divisible :
  forall p A B u : Z,
    (p | F28_discriminant A B) ->
    (p | F28_root_denominator A*u-1) ->
    (p | F28_derivative A
           (F28_candidate_root B u)).
Proof.
  intros p A B u HD Hinv.

  rewrite F28_candidate_derivative_identity.

  apply F28_divide_difference.

  - replace
      (-u^2*F28_discriminant A B)
      with
      (F28_discriminant A B*(-u^2))
      by ring.
    apply F28_divide_product.
    exact HD.

  - replace
      (A*(F28_root_denominator A*u-1)*
       (F28_root_denominator A*u+1))
      with
      ((F28_root_denominator A*u-1)*
       (A*(F28_root_denominator A*u+1)))
      by ring.
    apply F28_divide_product.
    exact Hinv.
Qed.

(* ======================================== *)
(* CUBIC DIVISIBILITY                       *)
(* ======================================== *)

Theorem F28_candidate_cubic_divisible :
  forall p A B u : Z,
    (p | F28_discriminant A B) ->
    (p | F28_root_denominator A*u-1) ->
    (p | F28_cubic A B
           (F28_candidate_root B u)).
Proof.
  intros p A B u HD Hinv.

  rewrite F28_candidate_cubic_identity.

  apply F28_divide_difference.

  - replace
      (B*u^3*F28_discriminant A B)
      with
      (F28_discriminant A B*(B*u^3))
      by ring.
    apply F28_divide_product.
    exact HD.

  - apply F28_divide_product.
    exact Hinv.
Qed.

(* ======================================== *)
(* SINGULAR ROOT CONSTRUCTION               *)
(* ======================================== *)

Theorem F28_candidate_is_singular :
  forall p A B u : Z,
    (p | F28_discriminant A B) ->
    (p | F28_root_denominator A*u-1) ->
    (p | F28_cubic A B
           (F28_candidate_root B u))
    /\
    (p | F28_derivative A
           (F28_candidate_root B u)).
Proof.
  intros p A B u HD Hinv.
  split.

  - apply F28_candidate_cubic_divisible.
    + exact HD.
    + exact Hinv.

  - apply F28_candidate_derivative_divisible.
    + exact HD.
    + exact Hinv.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_candidate_derivative_divisible.
Check F28_candidate_cubic_divisible.
Check F28_candidate_is_singular.

Print Assumptions F28_candidate_is_singular.
