(* code/coq/F28_tangent_arithmetic.v

   The owner's forty-second Coq file (22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Ring." is written "From Coq Require Import ZArith Ring."
   (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   F28_tangent_directions_certificate: rational tangent directions of the node <-> certificate(3 r) (same as in F28_tangent_directions.v, 41st file);
   F28_tangent_arithmetic_equivalence: if certificate(3 r) <-> certificate(a b) then rational tangent directions <-> certificate(a b)  (composition of two equivalences; trivial, checked by hand);
   F28_tangent_coefficient_identity: the tangent cone v^2 - 3 r u^2 at (u, v) = (1, 0) equals -(3 r)  (ring);
   F28_tangent_coefficient_nonzero: p not dividing 3 r ==> p not dividing the tangent cone at (1, 0)  (the cone is not identically zero: the node is not a cusp).
   Used together with the 40th file (F28_complete_arithmetic_bridge: some double root r with certificate(3 r) <-> certificate(ab)): the node's tangent directions are rational iff ab is a square class mod p.
   WHAT IT DOES NOT PROVE: the Tate/Silverman statement that this is multiplicative reduction of the Weierstrass model, nor minimality; the statements are about the local equation Y^2 = f(X) near the node. *)

From Coq Require Import ZArith Ring.

Open Scope Z_scope.

(* ======================================== *)
(* F.28: TANGENT CONE AND SQUARE CLASSES    *)
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

  - intros [u [v [Hnonzero Hdiv]]].
    exists u, v.
    split.
    + exact Hnonzero.
    + replace
        (3*r*u^2-v^2)
        with (-(v^2-3*r*u^2))
        by ring.
      apply F28_divide_neg.
      exact Hdiv.

  - intros [u [v [Hnonzero Hdiv]]].
    exists u, v.
    split.
    + exact Hnonzero.
    + replace
        (v^2-3*r*u^2)
        with (-(3*r*u^2-v^2))
        by ring.
      apply F28_divide_neg.
      exact Hdiv.
Qed.

(* ======================================== *)
(* ARITHMETIC COMPOSITION                   *)
(* ======================================== *)

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
(* EXACT TANGENT COEFFICIENT IDENTITY       *)
(* ======================================== *)

Lemma F28_tangent_coefficient_identity :
  forall r : Z,
    F28_tangent_cone r 1 0 = -(3*r).
Proof.
  intro r.
  unfold F28_tangent_cone.
  ring.
Qed.

(* ======================================== *)
(* NONDEGENERACY                            *)
(* ======================================== *)

Theorem F28_tangent_coefficient_nonzero :
  forall p r : Z,
    ~ (p | 3*r) ->
    ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p r Hnonzero Hdiv.

  rewrite F28_tangent_coefficient_identity in Hdiv.

  assert (Hpositive : (p | 3*r)).
  {
    replace (3*r) with (-(-(3*r))) by ring.
    apply F28_divide_neg.
    exact Hdiv.
  }

  exact (Hnonzero Hpositive).
Qed.

(* ======================================== *)
(* VERIFICATION                             *)
(* ======================================== *)

Check F28_tangent_directions_certificate.
Check F28_tangent_arithmetic_equivalence.
Check F28_tangent_coefficient_identity.
Check F28_tangent_coefficient_nonzero.

Print Assumptions F28_tangent_coefficient_nonzero.
