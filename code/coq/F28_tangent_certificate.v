(* code/coq/F28_tangent_certificate.v

   The owner's forty-third Coq file (22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Znumtheory Ring." is written
   "From Coq Require Import ZArith Znumtheory Ring." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   It repeats the 42nd file (F28_tangent_arithmetic.v: tangent directions <-> certificate(3r), composition with certificate(3r) <-> certificate(ab), tangent cone -(3r) at (1, 0), nonvanishing)
   and adds, for f'(r) = 3 r^2 + A:
     F28_singular_root_nonzero: p not dividing A, p | f'(r) ==> p not dividing r   (A = (3 r^2 + A) - 3 r r; checked by hand);
     F28_three_root_nonzero: prime p not dividing 3, p not dividing A, p | f'(r) ==> p not dividing 3 r;
     F28_nondegenerate_tangent_certificate: the same hypotheses ==> p does not divide the tangent cone v^2 - 3 r u^2 at (u, v) = (1, 0)  (the node is not a cusp).
   The nonvanishing statements already exist in F28_tangent_cone.v (31st file) and F28_singular_root.v (19th file) with the hypothesis 5 <= p instead of ~(p | 3); nothing new mathematically.
   WHAT IT DOES NOT PROVE: Tate/Silverman (node = multiplicative reduction of the Weierstrass model), minimality. *)

From Coq Require Import ZArith Znumtheory Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: COMPLETE TANGENT CERTIFICATE       *)
(* ======================================== *)

Definition F28_square_certificate (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2-v^2).

Definition F28_rational_tangent_directions
  (p r : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | v^2-3*r*u^2).

Definition F28_tangent_cone (r u v : Z) : Z :=
  v^2-3*r*u^2.

Definition F28_derivative (A r : Z) : Z :=
  3*r^2+A.

(* ======================================== *)
(* DIVISIBILITY UNDER NEGATION              *)
(* ======================================== *)

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
(* TANGENT DIRECTIONS                       *)
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
  - intros [u [v [Hu Hv]]].
    exists u, v.
    split.
    + exact Hu.
    + replace (3*r*u^2-v^2)
        with (-(v^2-3*r*u^2)) by ring.
      apply F28_divide_neg.
      exact Hv.
  - intros [u [v [Hu Hv]]].
    exists u, v.
    split.
    + exact Hu.
    + replace (v^2-3*r*u^2)
        with (-(3*r*u^2-v^2)) by ring.
      apply F28_divide_neg.
      exact Hv.
Qed.

Theorem F28_tangent_arithmetic_equivalence :
  forall p r a b : Z,
    (F28_square_certificate p (3*r) <->
     F28_square_certificate p (a*b)) ->
    (F28_rational_tangent_directions p r <->
     F28_square_certificate p (a*b)).
Proof.
  intros p r a b Hbridge.
  split.
  - intro Htangent.
    apply (proj1 Hbridge).
    apply
      (proj1
        (F28_tangent_directions_certificate p r)).
    exact Htangent.
  - intro Hab.
    apply
      (proj2
        (F28_tangent_directions_certificate p r)).
    apply (proj2 Hbridge).
    exact Hab.
Qed.

(* ======================================== *)
(* TANGENT COEFFICIENT                      *)
(* ======================================== *)

Lemma F28_tangent_coefficient_identity :
  forall r : Z,
    F28_tangent_cone r 1 0 = -(3*r).
Proof.
  intro r.
  unfold F28_tangent_cone.
  ring.
Qed.

Theorem F28_tangent_coefficient_nonzero :
  forall p r : Z,
    ~ (p | 3*r) ->
    ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p r Hnonzero Hdiv.
  rewrite F28_tangent_coefficient_identity in Hdiv.
  apply Hnonzero.
  replace (3*r) with (-(-(3*r))) by ring.
  apply F28_divide_neg.
  exact Hdiv.
Qed.

(* ======================================== *)
(* SINGULAR ROOT NONVANISHING               *)
(* ======================================== *)

Theorem F28_singular_root_nonzero :
  forall p A r : Z,
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | r).
Proof.
  intros p A r HA Hder Hr.
  unfold F28_derivative in Hder.
  destruct Hder as [k Hk].
  destruct Hr as [j Hj].
  apply HA.
  exists (k-3*r*j).
  replace A with ((3*r^2+A)-3*r*r) by ring.
  rewrite Hk.
  rewrite Hj.
  ring.
Qed.

Theorem F28_three_root_nonzero :
  forall p A r : Z,
    prime p ->
    ~ (p | 3) ->
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | 3*r).
Proof.
  intros p A r Hp Hthree HA Hder Hproduct.
  assert (Hr : ~ (p | r)).
  {
    apply (F28_singular_root_nonzero p A r).
    - exact HA.
    - exact Hder.
  }
  assert (Hsplit : (p | 3) \/ (p | r)).
  {
    eapply prime_mult.
    - exact Hp.
    - exact Hproduct.
  }
  destruct Hsplit as [H3 | Hroot].
  - exact (Hthree H3).
  - exact (Hr Hroot).
Qed.

(* ======================================== *)
(* NONDEGENERATE TANGENT CERTIFICATE        *)
(* ======================================== *)

Theorem F28_nondegenerate_tangent_certificate :
  forall p A r : Z,
    prime p ->
    ~ (p | 3) ->
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p A r Hp H3 HA Hder.
  apply F28_tangent_coefficient_nonzero.
  apply (F28_three_root_nonzero p A r).
  - exact Hp.
  - exact H3.
  - exact HA.
  - exact Hder.
Qed.

(* ======================================== *)
(* FINAL TYPECHECKING                       *)
(* ======================================== *)

Check F28_square_certificate.
Check F28_rational_tangent_directions.
Check F28_tangent_directions_certificate.
Check F28_tangent_arithmetic_equivalence.
Check F28_singular_root_nonzero.
Check F28_three_root_nonzero.
Check F28_nondegenerate_tangent_certificate.

Print Assumptions F28_nondegenerate_tangent_certificate.
