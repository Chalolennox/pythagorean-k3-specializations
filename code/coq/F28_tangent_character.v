(* code/coq/F28_tangent_character.v

   The owner's seventeenth Coq file (22 November 2026), which supersedes the sixteenth (it contains its two theorems and adds the equivalence):
   everything before the line "ADDED IN REVIEW" is the owner's text unchanged except for this header.  A standalone compilation unit about a general
   cubic Y^2 = f(X) = X^3 + A X + B (for the integral model of the paper A = 4 a c^3, B = -8 b c^5), with -c6 = 864 B.
   WHAT IT PROVES: if r is a double root of f modulo p (p | f(r) and p | f'(r)), then -c6 * (3r) = 864 B * 3r is a square certificate mod p
   (u = 1, v = 72 r^2); the identity behind it, 864 B (3r) - (72 r^2)^2 = 2592 r f(r) - 2592 r^2 f'(r), I checked by hand (both sides equal
   2592 B r - 5184 r^4).  F28_tangent_character_equivalence: for a prime p not dividing 864 B and 3 r, (-c6 is a certificate) <-> (3r is a
   certificate).  Geometrically: at the node (r, 0) the tangent slopes squared are f''(r)/2 = 3r, so the node is split iff 3r is a square mod p:
   the split criterion (-c6/p) = (3r/p) = +1 in certificate form, derived from the local geometry rather than from the (a, b, c) family.
   WHAT IT DOES NOT PROVE: the existence of the double root r from p | Delta (that needs the factorization of the cubic mod p), and the identification
   of "split" with "3r is a square" (Tate/Silverman).  The hypothesis ~ (p | 1) is redundant for a prime p; the added part removes it. *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Ring.

Open Scope Z_scope.

Definition F28_cubic (A B x : Z) : Z :=
  x^3 + A*x + B.

Definition F28_derivative (A x : Z) : Z :=
  3*x^2 + A.

Definition F28_minus_c6 (B : Z) : Z :=
  864*B.

Definition F28_square_certificate (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2 - v^2).

(* ======================================== *)
(* DIVISIBILITY                             *)
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
  destruct Hx as [u Hu].
  destruct Hy as [v Hv].
  exists (u+v).
  rewrite Hu, Hv.
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

Lemma F28_nonzero_product :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    ~ (p | x*y).
Proof.
  intros p x y Hp Hnx Hny Hxy.
  pose proof
    (F28_prime_product_split p x y Hp Hxy)
    as Hsplit.
  destruct Hsplit as [Hx | Hy].
  - exact (Hnx Hx).
  - exact (Hny Hy).
Qed.

(* ======================================== *)
(* COMPILED TANGENT CERTIFICATE             *)
(* ======================================== *)

Theorem F28_tangent_polynomial_identity :
  forall A B r : Z,
    F28_minus_c6 B * (3*r) - (72*r^2)^2 =
    2592*r*F28_cubic A B r
    -2592*r^2*F28_derivative A r.
Proof.
  intros A B r.
  unfold F28_minus_c6, F28_cubic, F28_derivative.
  ring.
Qed.

Theorem F28_tangent_product_certificate :
  forall p A B r : Z,
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    ~ (p | 1) ->
    F28_square_certificate
      p (F28_minus_c6 B * (3*r)).
Proof.
  intros p A B r Hcubic Hderivative Hunit.
  unfold F28_square_certificate.

  exists 1.
  exists (72*r^2).

  split.
  - exact Hunit.
  - destruct Hcubic as [k Hk].
    destruct Hderivative as [m Hm].

    exists (2592*r*k - 2592*r^2*m).

    unfold F28_minus_c6.
    unfold F28_cubic in Hk.
    unfold F28_derivative in Hm.

    assert (Hidentity :
      864*B*(3*r)*1^2 - (72*r^2)^2 =
      2592*r*(r^3+A*r+B)
      -2592*r^2*(3*r^2+A)).
    {
      ring.
    }

    rewrite Hidentity.
    rewrite Hk.
    rewrite Hm.
    ring.
Qed.

(* ======================================== *)
(* CERTIFICATE CANCELLATION                 *)
(* ======================================== *)

Theorem F28_certificate_cancel :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    F28_square_certificate p (x*y) ->
    F28_square_certificate p x ->
    F28_square_certificate p y.
Proof.
  intros p x y Hp Hnx Hxy Hx.

  destruct Hxy as
    [u [v [Hnu Hxyuv]]].

  destruct Hx as
    [r [s [Hnr Hxrs]]].

  unfold F28_square_certificate.

  exists (x*u*r).
  exists (v*s).

  split.

  - assert (Hnur : ~ (p | u*r)).
    {
      apply (F28_nonzero_product p u r).
      + exact Hp.
      + exact Hnu.
      + exact Hnr.
    }

    replace (x*u*r)
      with (x*(u*r)) by ring.

    apply (F28_nonzero_product p x (u*r)).
    + exact Hp.
    + exact Hnx.
    + exact Hnur.

  - replace
      (y*(x*u*r)^2-(v*s)^2)
      with
      ((x*y*u^2-v^2)*(x*r^2)
       +v^2*(x*r^2-s^2))
      by ring.

    apply F28_divide_sum.

    + apply F28_divide_product.
      exact Hxyuv.

    + replace
        (v^2*(x*r^2-s^2))
        with
        ((x*r^2-s^2)*v^2)
        by ring.

      apply F28_divide_product.
      exact Hxrs.
Qed.

(* ======================================== *)
(* MAIN TANGENT CHARACTER EQUIVALENCE       *)
(* ======================================== *)

Theorem F28_tangent_character_equivalence :
  forall p A B r : Z,
    prime p ->
    ~ (p | 1) ->
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    ~ (p | F28_minus_c6 B) ->
    ~ (p | 3*r) ->
    (F28_square_certificate p (F28_minus_c6 B)
     <->
     F28_square_certificate p (3*r)).
Proof.
  intros p A B r
    Hp Hunit Hcubic Hderivative Hnc6 Hnr.

  pose proof
    (F28_tangent_product_certificate
       p A B r Hcubic Hderivative Hunit)
    as Hproduct.

  split.

  - intro Hc6.
    apply
      (F28_certificate_cancel
         p (F28_minus_c6 B) (3*r)).
    + exact Hp.
    + exact Hnc6.
    + exact Hproduct.
    + exact Hc6.

  - intro Htangent.

    assert (Hreverse :
      F28_square_certificate
        p ((3*r)*F28_minus_c6 B)).
    {
      replace
        ((3*r)*F28_minus_c6 B)
        with
        (F28_minus_c6 B*(3*r))
        by ring.
      exact Hproduct.
    }

    apply
      (F28_certificate_cancel
         p (3*r) (F28_minus_c6 B)).
    + exact Hp.
    + exact Hnr.
    + exact Hreverse.
    + exact Htangent.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_tangent_product_certificate.
Check F28_certificate_cancel.
Check F28_tangent_character_equivalence.

Print Assumptions F28_tangent_product_certificate.
Print Assumptions F28_tangent_character_equivalence.

(* ======================================== *)
(* ADDED IN REVIEW (22 November 2026): the equivalence without the redundant hypothesis *)
(* ======================================== *)

From Coq Require Import Lia.

Lemma F28_prime_not_divide_1 :
  forall p : Z,
    prime p ->
    ~ (p | 1).
Proof.
  intros p Hp H1.
  pose proof (prime_ge_2 p Hp) as Hge.
  destruct (Z.divide_1_r p H1) as [E | E]; lia.
Qed.

Theorem F28_tangent_split_equivalence :
  forall p A B r : Z,
    prime p ->
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    ~ (p | 864*B) ->
    ~ (p | 3*r) ->
    (F28_square_certificate p (864*B)
     <-> F28_square_certificate p (3*r)).
Proof.
  intros p A B r Hp Hcubic Hderivative Hn864 Hn3r.
  exact (F28_tangent_character_equivalence p A B r Hp
           (F28_prime_not_divide_1 p Hp) Hcubic Hderivative Hn864 Hn3r).
Qed.

Print Assumptions F28_tangent_split_equivalence.
