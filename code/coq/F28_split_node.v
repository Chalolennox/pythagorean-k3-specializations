(* code/coq/F28_split_node.v

   The owner's forty-fourth Coq file (22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Znumtheory Ring." is written
   "From Coq Require Import ZArith Znumtheory Ring." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   It contains the 42nd and 43rd files and adds (everything read by hand):
     F28_cubic_translation_identity: f(r + u) = f(r) + f'(r) u + 3 r u^2 + u^3;
     F28_curve_translation_identity: (Y^2 - f(X)) at (r + u, v) = (v^2 - u^3 - 3 r u^2) - f(r) - f'(r) u;
     F28_singular_translation: p | f(r), p | f'(r) ==> (p | curve equation at (r + u, v) <-> p | v^2 - u^3 - 3 r u^2)   (the curve near a double root reads V^2 = U^3 + 3 r U^2 mod p);
     F28_translated_tangent_identity: v^2 - u^3 - 3 r u^2 = (v^2 - 3 r u^2) - u^3;
     F28_split_node p r := F28_rational_tangent_directions p r  (a DEFINITION of "split node": rational tangent directions of the node), F28_nonsplit_node its negation;
     F28_split_node_arithmetic / F28_nonsplit_node_arithmetic: if certificate(3 r) <-> certificate(ab) then split node <-> certificate(ab), nonsplit <-> not certificate(ab);
     F28_singular_node_classification: prime p not dividing 3 and A, double root r, certificate(3r) <-> certificate(ab) ==> the tangent cone at (1, 0) is nonzero, and split <-> certificate(ab), nonsplit <-> not certificate(ab).
   NOTE: "split node" here is defined by rational tangent directions of the local equation, which is the geometric definition; that a Weierstrass model with such a node at p has split multiplicative reduction
   (and minimality, Tate/Silverman VII.1) is NOT proved in Coq.  Combined with F28_complete_arithmetic_bridge.v (40th): for the paper's model the node at p is split iff ab is a square class mod p. *)

From Coq Require Import ZArith Znumtheory Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: DEFINITIONS                        *)
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

Definition F28_cubic (A B x : Z) : Z :=
  x^3+A*x+B.

Definition F28_derivative (A r : Z) : Z :=
  3*r^2+A.

Definition F28_curve_equation (A B x y : Z) : Z :=
  y^2-F28_cubic A B x.

Definition F28_translated_equation
  (r u v : Z) : Z :=
  v^2-u^3-3*r*u^2.

(* ======================================== *)
(* DIVISIBILITY HELPERS                     *)
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

Lemma F28_divide_add :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x+y).
Proof.
  intros p x y Hx Hy.
  destruct Hx as [k Hk].
  destruct Hy as [j Hj].
  exists (k+j).
  rewrite Hk.
  rewrite Hj.
  ring.
Qed.

Lemma F28_divide_mul :
  forall p x y : Z,
    (p | x) ->
    (p | x*y).
Proof.
  intros p x y Hx.
  destruct Hx as [k Hk].
  exists (k*y).
  rewrite Hk.
  ring.
Qed.

Lemma F28_divide_sub :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x-y).
Proof.
  intros p x y Hx Hy.
  apply F28_divide_add.
  - exact Hx.
  - replace (x-y-x) with (-y) by ring.
    apply F28_divide_neg.
    exact Hy.
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
(* NONDEGENERACY                            *)
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
(* NEW: EXACT TRANSLATION IDENTITY          *)
(* ======================================== *)

Theorem F28_cubic_translation_identity :
  forall A B r u : Z,
    F28_cubic A B (r+u) =
      F28_cubic A B r
      + F28_derivative A r*u
      + 3*r*u^2
      + u^3.
Proof.
  intros A B r u.
  unfold F28_cubic.
  unfold F28_derivative.
  ring.
Qed.

(* ======================================== *)
(* NEW: EQUATION TRANSLATION                *)
(* ======================================== *)

Theorem F28_curve_translation_identity :
  forall A B r u v : Z,
    F28_curve_equation A B (r+u) v =
      F28_translated_equation r u v
      - F28_cubic A B r
      - F28_derivative A r*u.
Proof.
  intros A B r u v.
  unfold F28_curve_equation.
  unfold F28_translated_equation.
  rewrite F28_cubic_translation_identity.
  ring.
Qed.

(* ======================================== *)
(* NEW: SINGULAR REDUCTION                  *)
(* ======================================== *)

Theorem F28_singular_translation :
  forall p A B r u v : Z,
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    ((p | F28_curve_equation A B (r+u) v) <->
     (p | F28_translated_equation r u v)).
Proof.
  intros p A B r u v Hroot Hder.

  assert (Hlinear :
    (p | F28_derivative A r*u)).
  {
    apply F28_divide_mul.
    exact Hder.
  }

  split.

  - intro Hcurve.
    replace (F28_translated_equation r u v)
      with
      (F28_curve_equation A B (r+u) v
       + F28_cubic A B r
       + F28_derivative A r*u).
    + apply F28_divide_add.
      * apply F28_divide_add.
        -- exact Hcurve.
        -- exact Hroot.
      * exact Hlinear.
    + rewrite F28_curve_translation_identity.
      ring.

  - intro Htranslated.
    rewrite F28_curve_translation_identity.
    apply F28_divide_sub.
    + apply F28_divide_sub.
      * exact Htranslated.
      * exact Hroot.
    + exact Hlinear.
Qed.

(* ======================================== *)
(* NEW: TANGENT CONE IDENTITY               *)
(* ======================================== *)

Theorem F28_translated_tangent_identity :
  forall r u v : Z,
    F28_translated_equation r u v =
      F28_tangent_cone r u v-u^3.
Proof.
  intros r u v.
  unfold F28_translated_equation.
  unfold F28_tangent_cone.
  ring.
Qed.

(* ======================================== *)
(* NEW: SPLIT NODE CERTIFICATE              *)
(* ======================================== *)

Definition F28_split_node (p r : Z) : Prop :=
  F28_rational_tangent_directions p r.

Definition F28_nonsplit_node (p r : Z) : Prop :=
  ~ F28_split_node p r.

Theorem F28_split_node_arithmetic :
  forall p r a b : Z,
    (F28_square_certificate p (3*r) <->
     F28_square_certificate p (a*b)) ->
    (F28_split_node p r <->
     F28_square_certificate p (a*b)).
Proof.
  intros p r a b Hbridge.
  unfold F28_split_node.
  apply F28_tangent_arithmetic_equivalence.
  exact Hbridge.
Qed.

Theorem F28_nonsplit_node_arithmetic :
  forall p r a b : Z,
    (F28_square_certificate p (3*r) <->
     F28_square_certificate p (a*b)) ->
    (F28_nonsplit_node p r <->
     ~ F28_square_certificate p (a*b)).
Proof.
  intros p r a b Hbridge.
  unfold F28_nonsplit_node.
  split.
  - intros Hnonsplit Hab.
    apply Hnonsplit.
    apply (proj2
      (F28_split_node_arithmetic p r a b Hbridge)).
    exact Hab.
  - intros Hnotab Hsplit.
    apply Hnotab.
    apply (proj1
      (F28_split_node_arithmetic p r a b Hbridge)).
    exact Hsplit.
Qed.

(* ======================================== *)
(* NEW: COMBINED ALGEBRAIC CLASSIFICATION   *)
(* ======================================== *)

Theorem F28_singular_node_classification :
  forall p A B r a b : Z,
    prime p ->
    ~ (p | 3) ->
    ~ (p | A) ->
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    (F28_square_certificate p (3*r) <->
     F28_square_certificate p (a*b)) ->
    (~ (p | F28_tangent_cone r 1 0)) /\
    (F28_split_node p r <->
     F28_square_certificate p (a*b)) /\
    (F28_nonsplit_node p r <->
     ~ F28_square_certificate p (a*b)).
Proof.
  intros p A B r a b Hp H3 HA Hroot Hder Hbridge.

  split.
  - apply (F28_nondegenerate_tangent_certificate
      p A r).
    + exact Hp.
    + exact H3.
    + exact HA.
    + exact Hder.

  - split.
    + apply F28_split_node_arithmetic.
      exact Hbridge.
    + apply F28_nonsplit_node_arithmetic.
      exact Hbridge.
Qed.

(* ======================================== *)
(* FINAL TYPECHECKING                       *)
(* ======================================== *)

Check F28_cubic_translation_identity.
Check F28_curve_translation_identity.
Check F28_singular_translation.
Check F28_translated_tangent_identity.
Check F28_split_node_arithmetic.
Check F28_nonsplit_node_arithmetic.
Check F28_singular_node_classification.

Print Assumptions F28_singular_node_classification.
Print Assumptions F28_singular_translation.
