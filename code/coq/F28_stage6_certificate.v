(* code/coq/F28_stage6_certificate.v

   The owner's forty-ninth Coq file ("F.28 - Stage 6", 22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Znumtheory Ring Lia." is written
   "From Coq Require Import ZArith Znumtheory Ring Lia." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   WHAT IT PROVES (read by hand): the rational-tangent-directions <-> certificate(3 r) equivalence (as in the 48th file); with the hypothesis F28_square_class_bridge p a b r := (certificate(3 r) <-> certificate(a b)):
     F28_stage6_tangent_arithmetic: rational tangent directions <-> certificate(ab) (by tauto from the two equivalences);
     F28_stage6_split_node / F28_stage6_nonsplit_node: for p not dividing 3 r: split node certificate <-> certificate(ab); nonsplit node certificate (p not dividing 3r and no rational directions) <-> not certificate(ab);
     the cubic and curve translation identities: f(r+u) = f(r) + f'(r) u + 3 r u^2 + u^3; v^2 - f(r+u) = (v^2 - (u^3 + 3 r u^2)) - f(r) - f'(r) u; v^2 - (u^3 + 3 r u^2) = (v^2 - 3 r u^2) - u^3 (ring);
     F28_stage6_combined_certificate: given the invariant certificate, p | f(r), p | f'(r), p not dividing 3 r and the bridge: invariant certificate AND (split <-> certificate(ab)) AND (nonsplit <-> not certificate(ab)).
   NOTE (fidelity): the "combined certificate" ASSUMES the invariant certificate and the square-class bridge as hypotheses (and ignores p | f(r), p | f'(r), p >= 5 in the proof): it is packaging of the 48th file's statements with
   the bridge supplied by F28_complete_arithmetic_bridge.v (40th file), not an independent derivation.  The nonsplit definition is by tangent slopes; identification with nonsplit multiplicative reduction
   (and minimality) is Tate/Silverman, not in Coq. *)

From Coq Require Import ZArith Znumtheory Ring Lia.

Open Scope Z_scope.

(* ====================================================== *)
(* F.28 - STAGE 6                                        *)
(* STANDALONE ARITHMETIC AND SPLIT-NODE BRIDGE            *)
(* ====================================================== *)

(* ------------------------------------------------------ *)
(* 1. CURVE DATA                                         *)
(* ------------------------------------------------------ *)

Definition F28_F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_c4 (A : Z) : Z :=
  -48*A.

Definition F28_discriminant (A B : Z) : Z :=
  -16*(4*A^3 + 27*B^2).

Definition F28_derivative (A r : Z) : Z :=
  3*r^2 + A.

Definition F28_cubic (A B r : Z) : Z :=
  r^3 + A*r + B.

Definition F28_tangent_cone (r u v : Z) : Z :=
  v^2 - 3*r*u^2.

Definition F28_invariant_certificate
  (p A B : Z) : Prop :=
  (p | F28_discriminant A B) /\
  ~ (p | F28_c4 A).

(* ------------------------------------------------------ *)
(* 2. SQUARE AND TANGENT CERTIFICATES                    *)
(* ------------------------------------------------------ *)

Definition F28_square_certificate
  (p x : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | x*u^2-v^2).

Definition F28_rational_tangent_directions
  (p r : Z) : Prop :=
  exists u v : Z,
    ~ (p | u) /\
    (p | F28_tangent_cone r u v).

Definition F28_split_node_certificate
  (p r : Z) : Prop :=
  ~ (p | 3*r) /\
  F28_rational_tangent_directions p r.

Definition F28_nonsplit_node_certificate
  (p r : Z) : Prop :=
  ~ (p | 3*r) /\
  ~ F28_rational_tangent_directions p r.

(* ------------------------------------------------------ *)
(* 3. DIVISIBILITY UNDER NEGATION                        *)
(* ------------------------------------------------------ *)

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

Lemma F28_divide_opp_iff :
  forall p x : Z,
    (p | x) <-> (p | -x).
Proof.
  intros p x.
  split.
  - intro H.
    exact (F28_divide_neg p x H).
  - intro H.
    replace x with (-(-x)) by ring.
    exact (F28_divide_neg p (-x) H).
Qed.

(* ------------------------------------------------------ *)
(* 4. VERIFIED STAGE 5 ALGEBRAIC CRITERION               *)
(* ------------------------------------------------------ *)

Theorem F28_tangent_square_equivalence :
  forall p r : Z,
    F28_rational_tangent_directions p r <->
    F28_square_certificate p (3*r).
Proof.
  intros p r.
  unfold F28_rational_tangent_directions.
  unfold F28_square_certificate.
  split.
  - intros [u [v [Hu Hcone]]].
    exists u, v.
    split.
    + exact Hu.
    + apply
        (proj2
          (F28_divide_opp_iff
             p (3*r*u^2-v^2))).
      replace (-(3*r*u^2-v^2))
        with (F28_tangent_cone r u v)
        by (unfold F28_tangent_cone; ring).
      exact Hcone.
  - intros [u [v [Hu Hsquare]]].
    exists u, v.
    split.
    + exact Hu.
    + apply
        (proj1
          (F28_divide_opp_iff
             p (3*r*u^2-v^2))) in Hsquare.
      replace (F28_tangent_cone r u v)
        with (-(3*r*u^2-v^2))
        by (unfold F28_tangent_cone; ring).
      exact Hsquare.
Qed.

(* ------------------------------------------------------ *)
(* 5. STAGE 6: EXPLICIT SQUARE-CLASS BRIDGE              *)
(* ------------------------------------------------------ *)

Definition F28_square_class_bridge
  (p a b r : Z) : Prop :=
  F28_square_certificate p (3*r) <->
  F28_square_certificate p (a*b).

Theorem F28_stage6_tangent_arithmetic :
  forall p a b r : Z,
    F28_square_class_bridge p a b r ->
    (F28_rational_tangent_directions p r <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b r Hbridge.
  unfold F28_square_class_bridge in Hbridge.
  pose proof
    (F28_tangent_square_equivalence p r)
    as Htangent.
  tauto.
Qed.

(* ------------------------------------------------------ *)
(* 6. SPLIT NODE                                        *)
(* ------------------------------------------------------ *)

Theorem F28_stage6_split_node :
  forall p a b r : Z,
    ~ (p | 3*r) ->
    F28_square_class_bridge p a b r ->
    (F28_split_node_certificate p r <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b r Hnonzero Hbridge.
  unfold F28_split_node_certificate.
  pose proof
    (F28_stage6_tangent_arithmetic
       p a b r Hbridge)
    as Hcriterion.
  split.
  - intros [_ Htangent].
    apply (proj1 Hcriterion).
    exact Htangent.
  - intro Hsquare.
    split.
    + exact Hnonzero.
    + apply (proj2 Hcriterion).
      exact Hsquare.
Qed.

(* ------------------------------------------------------ *)
(* 7. NONSPLIT NODE                                     *)
(* ------------------------------------------------------ *)

Theorem F28_stage6_nonsplit_node :
  forall p a b r : Z,
    ~ (p | 3*r) ->
    F28_square_class_bridge p a b r ->
    (F28_nonsplit_node_certificate p r <->
     ~ F28_square_certificate p (a*b)).
Proof.
  intros p a b r Hnonzero Hbridge.
  unfold F28_nonsplit_node_certificate.
  pose proof
    (F28_stage6_tangent_arithmetic
       p a b r Hbridge)
    as Hcriterion.
  split.
  - intros [_ Hnot].
    intro Hsquare.
    apply Hnot.
    apply (proj2 Hcriterion).
    exact Hsquare.
  - intro Hnot.
    split.
    + exact Hnonzero.
    + intro Htangent.
      apply Hnot.
      apply (proj1 Hcriterion).
      exact Htangent.
Qed.

(* ------------------------------------------------------ *)
(* 8. TRANSLATION OF THE CUBIC                          *)
(* ------------------------------------------------------ *)

Theorem F28_cubic_translation_identity :
  forall A B r u : Z,
    F28_cubic A B (r+u) =
    F28_cubic A B r +
    F28_derivative A r*u +
    3*r*u^2 + u^3.
Proof.
  intros A B r u.
  unfold F28_cubic, F28_derivative.
  ring.
Qed.

(* ------------------------------------------------------ *)
(* 9. TRANSLATED CURVE EQUATION                         *)
(* ------------------------------------------------------ *)

Theorem F28_curve_translation_identity :
  forall A B r u v : Z,
    v^2 - F28_cubic A B (r+u) =
    (v^2 - (u^3+3*r*u^2)) -
    F28_cubic A B r -
    F28_derivative A r*u.
Proof.
  intros A B r u v.
  rewrite F28_cubic_translation_identity.
  ring.
Qed.

(* ------------------------------------------------------ *)
(* 10. TRANSLATED TANGENT CONE                          *)
(* ------------------------------------------------------ *)

Theorem F28_translated_tangent_identity :
  forall r u v : Z,
    v^2 - (u^3+3*r*u^2) =
    F28_tangent_cone r u v - u^3.
Proof.
  intros r u v.
  unfold F28_tangent_cone.
  ring.
Qed.

(* ------------------------------------------------------ *)
(* 11. COMBINED STAGE 6 CERTIFICATE                     *)
(* ------------------------------------------------------ *)

Theorem F28_stage6_combined_certificate :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    F28_invariant_certificate
      p (F28_A a c) (F28_B b c) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    ~ (p | 3*r) ->
    F28_square_class_bridge p a b r ->
    F28_invariant_certificate
      p (F28_A a c) (F28_B b c)
    /\
    (F28_split_node_certificate p r <->
     F28_square_certificate p (a*b))
    /\
    (F28_nonsplit_node_certificate p r <->
     ~ F28_square_certificate p (a*b)).
Proof.
  intros p a b c r Hp Hlarge
         Hinv Hcubic Hder Hnonzero Hbridge.
  split.
  - exact Hinv.
  - split.
    + exact
        (F28_stage6_split_node
           p a b r Hnonzero Hbridge).
    + exact
        (F28_stage6_nonsplit_node
           p a b r Hnonzero Hbridge).
Qed.

(* ------------------------------------------------------ *)
(* 12. CI CHECKS                                        *)
(* ------------------------------------------------------ *)

Check F28_tangent_square_equivalence.
Check F28_stage6_tangent_arithmetic.
Check F28_stage6_split_node.
Check F28_stage6_nonsplit_node.
Check F28_cubic_translation_identity.
Check F28_curve_translation_identity.
Check F28_translated_tangent_identity.
Check F28_stage6_combined_certificate.

Print Assumptions F28_stage6_combined_certificate.
Print Assumptions F28_stage6_split_node.
Print Assumptions F28_stage6_nonsplit_node.
