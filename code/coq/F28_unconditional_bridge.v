(* code/coq/F28_unconditional_bridge.v

   The owner's fiftieth Coq file ("F.28 - Stage 6: unconditional arithmetic bridge", 22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Znumtheory Ring Lia."
   is written "From Coq Require Import ZArith Znumtheory Ring Lia." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone.
   KEY RESULT, for EVERY integer r that is a double root mod p of the paper's model (p | r^3 + A r + B and p | 3 r^2 + A, A = 4 a c^3, B = -8 b c^5), prime p >= 5, p not dividing c:
     F28_singular_linear_identity: 3 f(r) - r f'(r) = 2 A r + 3 B = 8 c^3 (a r - 3 b c^2)  (ring; checked by hand);
     F28_singular_linear_relation: p | a r - 3 b c^2  (cancel the factor 8 c^3: p does not divide 8 (= 2*2*2) nor c^3);
     F28_square_class_identity: (3r)(ab) - (3bc)^2 = 3b (a r - 3 b c^2)  (ring), hence F28_singular_square_relation: p | (3r)(ab) - (3bc)^2;
     F28_square_transfer / F28_square_class_equivalence: prime p, p not dividing x, y, p | x y - z^2 ==> (certificate(x) <-> certificate(y))  (witnesses x u, z v; y (xu)^2 - (zv)^2 = (xy - z^2)(x u^2) + (x u^2 - v^2) z^2, checked by hand);
     F28_unconditional_square_bridge: p not dividing 3r, ab ==> (certificate(3r) <-> certificate(ab));
     F28_unconditional_split_node / _nonsplit_node / F28_stage6_arithmetic_complete: the same with "split node certificate" (p not dividing 3r and rational tangent directions) <-> certificate(ab) and the nonsplit version.
   WHY IT MATTERS: it holds for any double root r, not only for the candidate root 24 b c^5 u of earlier files (F28_complete_arithmetic_bridge.v), so no uniqueness of the double root is needed and the 'bridge' hypothesis of
   F28_stage6_certificate.v is discharged: for the paper's model, at ANY double root mod p the node is split iff ab is a square class mod p (p not dividing 3r, ab; p not dividing ab holds for a primitive triple by F28_main_arithmetic).
   WHAT IT DOES NOT PROVE: existence of the double root (F28_complete_arithmetic_bridge.v / F28_specialized_singular_root.v), the Tate/Silverman identification of this node with split multiplicative reduction of the minimal model,
   root numbers, the parametrization; "split node" is defined by tangent slopes.  Files are standalone; composition is held until the owner says so. *)

From Coq Require Import ZArith Znumtheory Ring Lia.

Open Scope Z_scope.

(* ==================================================== *)
(* F.28 - STAGE 6: UNCONDITIONAL ARITHMETIC BRIDGE      *)
(* ==================================================== *)

Definition F28_F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_cubic (A B r : Z) : Z :=
  r^3 + A*r + B.

Definition F28_derivative (A r : Z) : Z :=
  3*r^2 + A.

Definition F28_tangent_cone (r u v : Z) : Z :=
  v^2 - 3*r*u^2.

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

(* ==================================================== *)
(* 1. DIVISIBILITY LEMMAS                              *)
(* ==================================================== *)

Lemma F28_divide_neg :
  forall p x : Z,
    (p | x) -> (p | -x).
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
  destruct Hx as [kx Hkx].
  destruct Hy as [ky Hky].
  exists (kx+ky).
  rewrite Hkx, Hky.
  ring.
Qed.

Lemma F28_divide_mul :
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

Lemma F28_divide_sub :
  forall p x y : Z,
    (p | x) ->
    (p | y) ->
    (p | x-y).
Proof.
  intros p x y Hx Hy.
  replace (x-y) with (x+(-y)) by ring.
  apply F28_divide_add.
  - exact Hx.
  - apply F28_divide_neg.
    exact Hy.
Qed.

Lemma F28_not_divide_small :
  forall p n : Z,
    0 < n ->
    n < p ->
    ~ (p | n).
Proof.
  intros p n Hpos Hbound Hdiv.
  destruct Hdiv as [k Hk].
  destruct (Z_lt_ge_dec k 0) as [Hneg | Hnonneg].
  - nia.
  - destruct (Z.eq_dec k 0) as [Hzero | Hnonzero].
    + subst k. nia.
    + assert (Hpositive : 1 <= k) by lia.
      nia.
Qed.

Lemma F28_prime_product_nonzero :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    ~ (p | x*y).
Proof.
  intros p x y Hp Hx Hy Hxy.
  apply prime_mult in Hxy; [|exact Hp].
  destruct Hxy as [Hleft | Hright].
  - exact (Hx Hleft).
  - exact (Hy Hright).
Qed.

Lemma F28_prime_cancel :
  forall p x y : Z,
    prime p ->
    ~ (p | x) ->
    (p | x*y) ->
    (p | y).
Proof.
  intros p x y Hp Hx Hxy.
  apply prime_mult in Hxy; [|exact Hp].
  destruct Hxy as [Hleft | Hright].
  - exfalso.
    exact (Hx Hleft).
  - exact Hright.
Qed.

Lemma F28_cube_nonzero :
  forall p x : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | x^3).
Proof.
  intros p x Hp Hx.
  replace (x^3) with (x*(x*x)) by ring.
  apply F28_prime_product_nonzero.
  - exact Hp.
  - exact Hx.
  - apply F28_prime_product_nonzero.
    + exact Hp.
    + exact Hx.
    + exact Hx.
Qed.

Lemma F28_eight_nonzero :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 8).
Proof.
  intros p Hp Hlarge.
  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }
  replace 8 with (2*(2*2)) by ring.
  apply F28_prime_product_nonzero.
  - exact Hp.
  - exact H2.
  - apply F28_prime_product_nonzero.
    + exact Hp.
    + exact H2.
    + exact H2.
Qed.

(* ==================================================== *)
(* 2. SINGULAR ROOT IMPLIES ar = 3bc^2 MOD p          *)
(* ==================================================== *)

Theorem F28_singular_linear_identity :
  forall a b c r : Z,
    3*F28_cubic
        (F28_A a c) (F28_B b c) r
    - r*F28_derivative (F28_A a c) r
    =
    8*c^3*(a*r-3*b*c^2).
Proof.
  intros a b c r.
  unfold F28_cubic, F28_derivative.
  unfold F28_A, F28_B.
  ring.
Qed.

Theorem F28_singular_linear_relation :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | c) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    (p | a*r-3*b*c^2).
Proof.
  intros p a b c r Hp Hlarge Hc Hf Hd.

  assert (Hlinear :
    (p | 3*F28_cubic
             (F28_A a c) (F28_B b c) r
          - r*F28_derivative (F28_A a c) r)).
  {
    apply F28_divide_sub.
    - replace
        (3*F28_cubic
             (F28_A a c) (F28_B b c) r)
        with
        (F28_cubic
             (F28_A a c) (F28_B b c) r*3)
        by ring.
      apply F28_divide_mul.
      exact Hf.
    - replace
        (r*F28_derivative (F28_A a c) r)
        with
        (F28_derivative (F28_A a c) r*r)
        by ring.
      apply F28_divide_mul.
      exact Hd.
  }

  rewrite F28_singular_linear_identity
    in Hlinear.

  assert (H8 : ~ (p | 8)).
  {
    exact (F28_eight_nonzero p Hp Hlarge).
  }

  assert (Hcube : ~ (p | c^3)).
  {
    exact (F28_cube_nonzero p c Hp Hc).
  }

  assert (Hfactor : ~ (p | 8*c^3)).
  {
    apply F28_prime_product_nonzero.
    - exact Hp.
    - exact H8.
    - exact Hcube.
  }

  replace
    (8*c^3*(a*r-3*b*c^2))
    with
    ((8*c^3)*(a*r-3*b*c^2))
    in Hlinear by ring.

  exact
    (F28_prime_cancel
       p (8*c^3) (a*r-3*b*c^2)
       Hp Hfactor Hlinear).
Qed.

(* ==================================================== *)
(* 3. THE CRUCIAL SQUARE IDENTITY                     *)
(* ==================================================== *)

Theorem F28_square_class_identity :
  forall a b c r : Z,
    (3*r)*(a*b) - (3*b*c)^2 =
    3*b*(a*r-3*b*c^2).
Proof.
  intros a b c r.
  ring.
Qed.

Theorem F28_singular_square_relation :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | c) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    (p | (3*r)*(a*b)-(3*b*c)^2).
Proof.
  intros p a b c r Hp Hlarge Hc Hf Hd.

  rewrite F28_square_class_identity.

  replace
    (3*b*(a*r-3*b*c^2))
    with
    ((a*r-3*b*c^2)*(3*b))
    by ring.

  apply F28_divide_mul.

  exact
    (F28_singular_linear_relation
       p a b c r Hp Hlarge Hc Hf Hd).
Qed.

(* ==================================================== *)
(* 4. SQUARE-CLASS TRANSFER                           *)
(* ==================================================== *)

Lemma F28_square_transfer :
  forall p x y z : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    (p | x*y-z^2) ->
    F28_square_certificate p x ->
    F28_square_certificate p y.
Proof.
  intros p x y z Hp Hx Hy Hrelation Hsquare.
  destruct Hsquare as [u [v [Hu Heq]]].

  assert (Hxu : ~ (p | x*u)).
  {
    apply F28_prime_product_nonzero.
    - exact Hp.
    - exact Hx.
    - exact Hu.
  }

  exists (x*u), (z*v).
  split.
  - exact Hxu.
  - assert (Hfirst :
        (p | (x*y-z^2)*(x*u^2))).
    {
      apply F28_divide_mul.
      exact Hrelation.
    }

    assert (Hsecond :
        (p | (x*u^2-v^2)*z^2)).
    {
      apply F28_divide_mul.
      exact Heq.
    }

    assert (Hsum :
        (p |
          (x*y-z^2)*(x*u^2)
          + (x*u^2-v^2)*z^2)).
    {
      apply F28_divide_add.
      - exact Hfirst.
      - exact Hsecond.
    }

    replace
      (y*(x*u)^2-(z*v)^2)
      with
      ((x*y-z^2)*(x*u^2)
       + (x*u^2-v^2)*z^2)
      by ring.

    exact Hsum.
Qed.

Theorem F28_square_class_equivalence :
  forall p x y z : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | y) ->
    (p | x*y-z^2) ->
    (F28_square_certificate p x <->
     F28_square_certificate p y).
Proof.
  intros p x y z Hp Hx Hy Hrelation.

  assert (Hreverse : (p | y*x-z^2)).
  {
    replace (y*x-z^2) with (x*y-z^2)
      by ring.
    exact Hrelation.
  }

  split.
  - intro Hsquare.
    exact
      (F28_square_transfer
         p x y z Hp Hx Hy Hrelation Hsquare).
  - intro Hsquare.
    exact
      (F28_square_transfer
         p y x z Hp Hy Hx Hreverse Hsquare).
Qed.

(* ==================================================== *)
(* 5. TANGENT DIRECTIONS                              *)
(* ==================================================== *)

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
      replace
        (-(3*r*u^2-v^2))
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
      replace
        (F28_tangent_cone r u v)
        with (-(3*r*u^2-v^2))
        by (unfold F28_tangent_cone; ring).
      exact Hsquare.
Qed.

(* ==================================================== *)
(* 6. UNCONDITIONAL ARITHMETIC BRIDGE                  *)
(* ==================================================== *)

Theorem F28_unconditional_square_bridge :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | c) ->
    ~ (p | 3*r) ->
    ~ (p | a*b) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    (F28_square_certificate p (3*r) <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b c r
         Hp Hlarge Hc Hthree Hab Hf Hd.

  assert (Hrelation :
    (p | (3*r)*(a*b)-(3*b*c)^2)).
  {
    exact
      (F28_singular_square_relation
         p a b c r Hp Hlarge Hc Hf Hd).
  }

  exact
    (F28_square_class_equivalence
       p (3*r) (a*b) (3*b*c)
       Hp Hthree Hab Hrelation).
Qed.

(* ==================================================== *)
(* 7. UNCONDITIONAL SPLIT-NODE CRITERION               *)
(* ==================================================== *)

Theorem F28_unconditional_split_node :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | c) ->
    ~ (p | 3*r) ->
    ~ (p | a*b) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    (F28_split_node_certificate p r <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b c r
         Hp Hlarge Hc Hthree Hab Hf Hd.

  pose proof
    (F28_unconditional_square_bridge
       p a b c r
       Hp Hlarge Hc Hthree Hab Hf Hd)
    as Hbridge.

  pose proof
    (F28_tangent_square_equivalence p r)
    as Htangent.

  unfold F28_split_node_certificate.

  split.
  - intros [_ Hdirections].
    apply (proj1 Hbridge).
    apply (proj1 Htangent).
    exact Hdirections.
  - intro Hsquare.
    split.
    + exact Hthree.
    + apply (proj2 Htangent).
      apply (proj2 Hbridge).
      exact Hsquare.
Qed.

(* ==================================================== *)
(* 8. UNCONDITIONAL NONSPLIT CRITERION                 *)
(* ==================================================== *)

Theorem F28_unconditional_nonsplit_node :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | c) ->
    ~ (p | 3*r) ->
    ~ (p | a*b) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    (F28_nonsplit_node_certificate p r <->
     ~ F28_square_certificate p (a*b)).
Proof.
  intros p a b c r
         Hp Hlarge Hc Hthree Hab Hf Hd.

  pose proof
    (F28_unconditional_square_bridge
       p a b c r
       Hp Hlarge Hc Hthree Hab Hf Hd)
    as Hbridge.

  pose proof
    (F28_tangent_square_equivalence p r)
    as Htangent.

  unfold F28_nonsplit_node_certificate.

  split.
  - intros [_ Hnot].
    intro Hsquare.
    apply Hnot.
    apply (proj2 Htangent).
    apply (proj2 Hbridge).
    exact Hsquare.
  - intro Hnot.
    split.
    + exact Hthree.
    + intro Hdirections.
      apply Hnot.
      apply (proj1 Hbridge).
      apply (proj1 Htangent).
      exact Hdirections.
Qed.

(* ==================================================== *)
(* 9. FINAL COMBINED THEOREM                           *)
(* ==================================================== *)

Theorem F28_stage6_arithmetic_complete :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | c) ->
    ~ (p | 3*r) ->
    ~ (p | a*b) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    (F28_split_node_certificate p r <->
     F28_square_certificate p (a*b))
    /\
    (F28_nonsplit_node_certificate p r <->
     ~ F28_square_certificate p (a*b)).
Proof.
  intros p a b c r
         Hp Hlarge Hc Hthree Hab Hf Hd.

  split.
  - exact
      (F28_unconditional_split_node
         p a b c r
         Hp Hlarge Hc Hthree Hab Hf Hd).
  - exact
      (F28_unconditional_nonsplit_node
         p a b c r
         Hp Hlarge Hc Hthree Hab Hf Hd).
Qed.

(* ==================================================== *)
(* 10. CI CHECKS                                      *)
(* ==================================================== *)

Check F28_singular_linear_identity.
Check F28_singular_linear_relation.
Check F28_square_class_identity.
Check F28_singular_square_relation.
Check F28_square_transfer.
Check F28_square_class_equivalence.
Check F28_tangent_square_equivalence.
Check F28_unconditional_square_bridge.
Check F28_unconditional_split_node.
Check F28_unconditional_nonsplit_node.
Check F28_stage6_arithmetic_complete.

Print Assumptions F28_unconditional_square_bridge.
Print Assumptions F28_stage6_arithmetic_complete.
