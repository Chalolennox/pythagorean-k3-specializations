(* code/coq/F28_square_class_cancellation.v

   The owner's thirty-third Coq file (22 November 2026).  The text is the owner's, with ONE change: the three imports "From Stdlib Require Import ..." are written
   "From Coq Require Import ..." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   F28_certificate_cancel: prime p, p not dividing x, certificate(x y), certificate(x) ==> certificate(y)  (witnesses x u r, v s; checked by hand:
   y (x u r)^2 - (v s)^2 = (x y u^2 - v^2)(x r^2) + v^2 (x r^2 - s^2));
   F28_product_square_equivalence: prime p, p not dividing x, y, certificate(x y) ==> (certificate(x) <-> certificate(y));
   F28_tangent_character_equivalence: prime p, p not dividing 864 B, 3 r, certificate(864 B * 3 r) ==> (certificate(864 B) <-> certificate(3 r)).
   The same three statements as in F28_certificate.v / F28_tangent_character.v (cancellation, product equivalence, tangent equivalence); nothing new mathematically.
   Together with F28_tangent_product_square.v (the certificate of the product from p | f(r), p | f'(r)) this is the file-level decomposition of
   F28_tangent_character_equivalence; the assembled statement is in F28_large_prime_tangent.v (F28_large_prime_tangent_character). *)

From Coq Require Import ZArith.
From Coq Require Import Znumtheory.
From Coq Require Import Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: SQUARE-CLASS CANCELLATION          *)
(* ======================================== *)

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
  intros p x y Hp Hx Hy Hxy.
  destruct
    (F28_prime_product_split p x y Hp Hxy)
    as [Hpx | Hpy].
  - exact (Hx Hpx).
  - exact (Hy Hpy).
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

  destruct Hxy as [u [v [Hnu Hxyuv]]].
  destruct Hx as [r [s [Hnr Hxrs]]].

  unfold F28_square_certificate.

  exists (x*u*r).
  exists (v*s).

  split.
  - assert (Hnur : ~ (p | u*r)).
    {
      apply (F28_nonzero_product p u r).
      - exact Hp.
      - exact Hnu.
      - exact Hnr.
    }

    replace (x*u*r) with (x*(u*r)) by ring.

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
    + replace (v^2*(x*r^2-s^2))
        with ((x*r^2-s^2)*v^2)
        by ring.
      apply F28_divide_product.
      exact Hxrs.
Qed.

(* ======================================== *)
(* SQUARE-CLASS EQUIVALENCE                 *)
(* ======================================== *)

Theorem F28_product_square_equivalence :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    F28_square_certificate p (x*y) ->
    (F28_square_certificate p x <->
     F28_square_certificate p y).
Proof.
  intros p x y Hp Hnx Hny Hxy.

  split.
  - intro Hx.
    apply (F28_certificate_cancel p x y).
    + exact Hp.
    + exact Hnx.
    + exact Hxy.
    + exact Hx.

  - intro Hy.

    assert (Hyx : F28_square_certificate p (y*x)).
    {
      replace (y*x) with (x*y) by ring.
      exact Hxy.
    }

    apply (F28_certificate_cancel p y x).
    + exact Hp.
    + exact Hny.
    + exact Hyx.
    + exact Hy.
Qed.

(* ======================================== *)
(* APPLICATION TO TANGENT COEFFICIENT       *)
(* ======================================== *)

Theorem F28_tangent_character_equivalence :
  forall p B r : Z,
    prime p ->
    ~ (p | 864*B) ->
    ~ (p | 3*r) ->
    F28_square_certificate p ((864*B)*(3*r)) ->
    (F28_square_certificate p (864*B) <->
     F28_square_certificate p (3*r)).
Proof.
  intros p B r Hp HB Hr Hproduct.

  apply (F28_product_square_equivalence
    p (864*B) (3*r)).
  - exact Hp.
  - exact HB.
  - exact Hr.
  - exact Hproduct.
Qed.

(* ======================================== *)
(* FINAL CHECKS                             *)
(* ======================================== *)

Check F28_certificate_cancel.
Check F28_product_square_equivalence.
Check F28_tangent_character_equivalence.

Print Assumptions F28_tangent_character_equivalence.
