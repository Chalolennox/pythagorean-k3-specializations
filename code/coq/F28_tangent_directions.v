(* code/coq/F28_tangent_directions.v

   The owner's forty-first Coq file (22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Ring." is written "From Coq Require Import ZArith Ring."
   (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   F28_cubic_translation: f(r + u) = f(r) + f'(r) u + u^2 (u + 3 r) (ring; checked by hand);
   F28_singular_cubic_factorization: p | f(r), p | f'(r) ==> p | f(r + u) - u^2 (u + 3 r)  (so near a double root the curve Y^2 = f(X) reads Y^2 = U^2 (U + 3 r) modulo p);
   F28_tangent_cone_identity: v^2 - u^2 (u + 3 r) = (v^2 - 3 r u^2) - u^3  (the cone Y^2 = 3 r U^2 is the part of lowest degree);
   F28_rational_tangent_directions p r := exists u v, p not dividing u, p | v^2 - 3 r u^2   (a rational tangent direction v/u of the node, with v^2 = 3 r u^2);
   F28_tangent_directions_certificate: rational tangent directions <-> certificate(3 r)  (sign flip).
   MEANING: it gives the geometric meaning of "split": the node at (r, 0) has rational tangent directions iff 3r is a square mod p (the certificate), i.e. the definition of split in terms of tangent
   slopes becomes exactly the character used in the earlier files.  WHAT IT DOES NOT PROVE: that a node of this kind is multiplicative reduction of the Weierstrass model, nor minimality (Tate/Silverman);
   the translation identity already appears in F28_tangent_cone.v (31st file). *)

From Coq Require Import ZArith Ring.

Open Scope Z_scope.

Definition F28_cubic (A B x : Z) : Z :=
  x^3 + A*x + B.

Definition F28_derivative (A x : Z) : Z :=
  3*x^2 + A.

Definition F28_square_certificate (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2-v^2).

Definition F28_rational_tangent_directions
  (p r : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | v^2-3*r*u^2).

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

(* ======================================== *)
(* CUBIC TRANSLATION                        *)
(* ======================================== *)

Theorem F28_cubic_translation :
  forall A B r u : Z,
    F28_cubic A B (r+u)
    =
    F28_cubic A B r
    +F28_derivative A r*u
    +u^2*(u+3*r).
Proof.
  intros A B r u.
  unfold F28_cubic, F28_derivative.
  ring.
Qed.

(* ======================================== *)
(* SINGULAR CUBIC FACTORIZATION             *)
(* ======================================== *)

Theorem F28_singular_cubic_factorization :
  forall p A B r u : Z,
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    (p |
      F28_cubic A B (r+u)
      -u^2*(u+3*r)).
Proof.
  intros p A B r u Hroot Hder.

  replace
    (F28_cubic A B (r+u)-u^2*(u+3*r))
    with
    (F28_cubic A B r
     +F28_derivative A r*u).
  2:{
    rewrite F28_cubic_translation.
    ring.
  }

  apply F28_divide_sum.
  - exact Hroot.
  - apply F28_divide_product.
    exact Hder.
Qed.

(* ======================================== *)
(* TANGENT CONE IDENTITY                    *)
(* ======================================== *)

Theorem F28_tangent_cone_identity :
  forall r u v : Z,
    v^2-u^2*(u+3*r)
    =
    (v^2-3*r*u^2)-u^3.
Proof.
  intros r u v.
  ring.
Qed.

(* ======================================== *)
(* TANGENT DIRECTIONS AND CERTIFICATES      *)
(* ======================================== *)

Theorem F28_tangent_directions_certificate :
  forall p r : Z,
    F28_rational_tangent_directions p r <->
    F28_square_certificate p (3*r).
Proof.
  intros p r.
  unfold F28_rational_tangent_directions.
  unfold F28_square_certificate.

  split.

  - intros [u [v [Hnonzero Hdiv]]].
    exists u, v.
    split.
    + exact Hnonzero.
    + replace
        (3*r*u^2-v^2)
        with
        (-(v^2-3*r*u^2))
        by ring.
      apply F28_divide_neg.
      exact Hdiv.

  - intros [u [v [Hnonzero Hdiv]]].
    exists u, v.
    split.
    + exact Hnonzero.
    + replace
        (v^2-3*r*u^2)
        with
        (-(3*r*u^2-v^2))
        by ring.
      apply F28_divide_neg.
      exact Hdiv.
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_cubic_translation.
Check F28_singular_cubic_factorization.
Check F28_tangent_cone_identity.
Check F28_tangent_directions_certificate.

Print Assumptions F28_tangent_directions_certificate.
