(* code/coq/F28_stage5_certificate.v

   The owner's forty-eighth Coq file ("F.28 - complete standalone Stage 5", 22 November 2026).  The text is the owner's, with ONE change: the import "From Stdlib Require Import ZArith Znumtheory Ring Lia."
   is written "From Coq Require Import ZArith Znumtheory Ring Lia." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).  Plus this header.  Standalone; it contains the 46th and 47th files.
   New in this file (everything read by hand):
     F28_divide_opp_iff: p | x <-> p | -x;
     F28_tangent_square_equivalence: rational tangent directions (u not 0, p | v^2 - 3 r u^2) <-> certificate(3 r);
     F28_square_root_nonzero: prime p not dividing x and certificate(x) ==> u, v with p not dividing u, v and p | x u^2 - v^2  (v is nonzero because p | v would give p | x u^2);
     F28_split_node_certificate p r := p not dividing 3 r AND rational tangent directions;  F28_split_node_square_criterion: for p not dividing 3 r, split node certificate <-> certificate(3 r);
     F28_stage5_certificate: prime p >= 5, p not dividing a, c, p | F, p | f'(r) (A = 4 a c^3) ==> invariant certificate (p | Delta, p not dividing c4) AND p not dividing r AND p not dividing 3 r
       AND (split node certificate <-> certificate(3 r)).
   The Stage 4 part is the 47th file.  Together with F28_complete_arithmetic_bridge.v (40th: some double root r with certificate(3r) <-> certificate(ab)) this says: at the node, split iff ab is a square class mod p.
   WHAT IT DOES NOT PROVE: that the node of the model at p IS (split) multiplicative reduction and the model is minimal (Silverman VII.1.1/Tate); the definition of "split node" here is by rational tangent directions;
   existence of r, root numbers, the parametrization.  Composition with the other files is held until the owner says so. *)

From Coq Require Import ZArith Znumtheory Ring Lia.

Open Scope Z_scope.

(* ================================================= *)
(* F.28 - COMPLETE STANDALONE STAGE 5                *)
(* ================================================= *)

(* ================================================= *)
(* 1. ELLIPTIC CURVE INVARIANTS                      *)
(* ================================================= *)

Definition F28_F (a b c : Z) : Z :=
  4*a^3 + 27*b^2*c.

Definition F28_A (a c : Z) : Z :=
  4*a*c^3.

Definition F28_B (b c : Z) : Z :=
  -8*b*c^5.

Definition F28_c4 (A : Z) : Z :=
  -48*A.

Definition F28_c6 (B : Z) : Z :=
  -864*B.

Definition F28_discriminant (A B : Z) : Z :=
  -16*(4*A^3 + 27*B^2).

Definition F28_invariant_certificate
  (p A B : Z) : Prop :=
  (p | F28_discriminant A B) /\
  ~ (p | F28_c4 A).

Definition F28_derivative (A x : Z) : Z :=
  3*x^2 + A.

Definition F28_tangent_cone (r u v : Z) : Z :=
  v^2 - 3*r*u^2.

(* ================================================= *)
(* 2. BASIC NUMBER THEORY                           *)
(* ================================================= *)

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

Lemma F28_prime_square_nonzero :
  forall p x : Z,
    prime p ->
    ~ (p | x) ->
    ~ (p | x*x).
Proof.
  intros p x Hp Hx.
  apply F28_prime_product_nonzero.
  - exact Hp.
  - exact Hx.
  - exact Hx.
Qed.

Lemma F28_prime_cube_nonzero :
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
  - apply F28_prime_square_nonzero.
    + exact Hp.
    + exact Hx.
Qed.

Lemma F28_prime_192_nonzero :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 192).
Proof.
  intros p Hp Hlarge.

  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }

  assert (H3 : ~ (p | 3)).
  {
    apply F28_not_divide_small; lia.
  }

  replace 192 with
    (2*(2*(2*(2*(2*(2*3)))))) by ring.

  repeat
    (apply F28_prime_product_nonzero;
      [exact Hp | exact H2 |]).

  exact H3.
Qed.

(* ================================================= *)
(* 3. INVARIANT IDENTITIES                          *)
(* ================================================= *)

Theorem F28_c4_identity :
  forall a c : Z,
    F28_c4 (F28_A a c) = -192*a*c^3.
Proof.
  intros a c.
  unfold F28_c4, F28_A.
  ring.
Qed.

Theorem F28_c6_identity :
  forall b c : Z,
    F28_c6 (F28_B b c) = 6912*b*c^5.
Proof.
  intros b c.
  unfold F28_c6, F28_B.
  ring.
Qed.

Theorem F28_discriminant_identity :
  forall a b c : Z,
    F28_discriminant
      (F28_A a c) (F28_B b c) =
    -1024*c^9*F28_F a b c.
Proof.
  intros a b c.
  unfold F28_discriminant, F28_A, F28_B, F28_F.
  ring.
Qed.

Theorem F28_large_prime_c4_nonzero :
  forall p a c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    ~ (p | F28_c4 (F28_A a c)).
Proof.
  intros p a c Hp Hlarge Ha Hc.
  rewrite F28_c4_identity.

  replace (-192*a*c^3)
    with ((-192)*(a*c^3)) by ring.

  apply F28_prime_product_nonzero.
  - exact Hp.
  - intro Hneg.
    apply (F28_prime_192_nonzero p Hp Hlarge).
    destruct Hneg as [k Hk].
    exists (-k).
    nia.
  - apply F28_prime_product_nonzero.
    + exact Hp.
    + exact Ha.
    + apply F28_prime_cube_nonzero.
      * exact Hp.
      * exact Hc.
Qed.

Theorem F28_F_divides_discriminant :
  forall p a b c : Z,
    (p | F28_F a b c) ->
    (p | F28_discriminant
           (F28_A a c) (F28_B b c)).
Proof.
  intros p a b c HF.
  rewrite F28_discriminant_identity.
  destruct HF as [k Hk].
  exists ((-1024*c^9)*k).
  rewrite Hk.
  ring.
Qed.

Theorem F28_large_prime_reduction_certificate :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    F28_invariant_certificate
      p (F28_A a c) (F28_B b c).
Proof.
  intros p a b c Hp Hlarge Ha Hc HF.
  unfold F28_invariant_certificate.
  split.
  - apply F28_F_divides_discriminant.
    exact HF.
  - apply F28_large_prime_c4_nonzero.
    + exact Hp.
    + exact Hlarge.
    + exact Ha.
    + exact Hc.
Qed.

(* ================================================= *)
(* 4. DIVISIBILITY OPERATIONS                       *)
(* ================================================= *)

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

Lemma F28_divide_neg :
  forall p x : Z,
    (p | x) ->
    (p | -x).
Proof.
  intros p x Hx.
  destruct Hx as [k Hk].
  exists (-k).
  rewrite Hk.
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

(* ================================================= *)
(* 5. STAGE 4: NONDEGENERATE SINGULAR ROOT          *)
(* ================================================= *)

Theorem F28_singular_root_nonzero :
  forall p A r : Z,
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | r).
Proof.
  intros p A r HA Hder Hr.
  unfold F28_derivative in Hder.

  assert (Hrr : (p | r*r)).
  {
    apply F28_divide_mul.
    exact Hr.
  }

  assert (Hthree : (p | 3*r^2)).
  {
    replace (3*r^2) with ((r*r)*3) by ring.
    exact (F28_divide_mul p (r*r) 3 Hrr).
  }

  assert (Hnegative : (p | -(3*r^2))).
  {
    apply F28_divide_neg.
    exact Hthree.
  }

  apply HA.
  replace A with ((3*r^2+A)+(-(3*r^2))) by ring.
  apply F28_divide_add.
  - exact Hder.
  - exact Hnegative.
Qed.

Theorem F28_three_root_nonzero :
  forall p A r : Z,
    prime p ->
    5 <= p ->
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | 3*r).
Proof.
  intros p A r Hp Hlarge HA Hder Hthree.

  assert (H3 : ~ (p | 3)).
  {
    apply F28_not_divide_small; lia.
  }

  assert (Hr : ~ (p | r)).
  {
    exact (F28_singular_root_nonzero p A r HA Hder).
  }

  exact
    (F28_prime_product_nonzero
       p 3 r Hp H3 Hr Hthree).
Qed.

Theorem F28_tangent_coefficient_identity :
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

Theorem F28_nondegenerate_singular_root :
  forall p A r : Z,
    prime p ->
    5 <= p ->
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | r) /\
    ~ (p | 3*r) /\
    ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p A r Hp Hlarge HA Hder.

  assert (Hr : ~ (p | r)).
  {
    exact (F28_singular_root_nonzero p A r HA Hder).
  }

  assert (Hthree : ~ (p | 3*r)).
  {
    exact
      (F28_three_root_nonzero
         p A r Hp Hlarge HA Hder).
  }

  split.
  - exact Hr.
  - split.
    + exact Hthree.
    + exact
        (F28_tangent_coefficient_nonzero
           p r Hthree).
Qed.

Theorem F28_stage4_certificate :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (p | F28_derivative (F28_A a c) r) ->
    F28_invariant_certificate
      p (F28_A a c) (F28_B b c)
    /\
    ~ (p | r)
    /\
    ~ (p | 3*r)
    /\
    ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p a b c r Hp Hlarge Ha Hc HF Hder.

  assert (Hinv :
    F28_invariant_certificate
      p (F28_A a c) (F28_B b c)).
  {
    exact
      (F28_large_prime_reduction_certificate
         p a b c Hp Hlarge Ha Hc HF).
  }

  assert (HA : ~ (p | F28_A a c)).
  {
    intro Hbad.

    assert (Hc4 : (p | F28_c4 (F28_A a c))).
    {
      unfold F28_c4.
      replace (-48*F28_A a c)
        with (F28_A a c*(-48)) by ring.
      apply F28_divide_mul.
      exact Hbad.
    }

    exact
      (F28_large_prime_c4_nonzero
         p a c Hp Hlarge Ha Hc Hc4).
  }

  pose proof
    (F28_nondegenerate_singular_root
       p (F28_A a c) r Hp Hlarge HA Hder)
    as Hnode.

  destruct Hnode as [Hr [Hthree Htangent]].

  split.
  - exact Hinv.
  - split.
    + exact Hr.
    + split.
      * exact Hthree.
      * exact Htangent.
Qed.

(* ================================================= *)
(* 6. STAGE 5: SQUARE CERTIFICATE                  *)
(* ================================================= *)

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

(* ================================================= *)
(* 7. SIGN REVERSAL OF DIVISIBILITY                *)
(* ================================================= *)

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

(* ================================================= *)
(* 8. TANGENT CONE AND SQUARE CERTIFICATE          *)
(* ================================================= *)

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
    + apply (proj2
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
    + apply (proj1
        (F28_divide_opp_iff
          p (3*r*u^2-v^2))) in Hsquare.
      replace (F28_tangent_cone r u v)
        with (-(3*r*u^2-v^2))
        by (unfold F28_tangent_cone; ring).
      exact Hsquare.
Qed.

(* ================================================= *)
(* 9. NONZERO SQUARE HAS NONZERO ROOT              *)
(* ================================================= *)

Theorem F28_square_root_nonzero :
  forall p x : Z,
    prime p ->
    ~ (p | x) ->
    F28_square_certificate p x ->
    exists u v : Z,
      ~ (p | u) /\
      ~ (p | v) /\
      (p | x*u^2-v^2).
Proof.
  intros p x Hp Hx Hsquare.
  destruct Hsquare as [u [v [Hu Heq]]].

  assert (Hv : ~ (p | v)).
  {
    intro Hbad.

    assert (Hvv : (p | v^2)).
    {
      replace (v^2) with (v*v) by ring.
      exact (F28_divide_mul p v v Hbad).
    }

    assert (Hneg : (p | -(v^2))).
    {
      exact (F28_divide_neg p (v^2) Hvv).
    }

    assert (Hxuu : (p | x*u^2)).
    {
      replace (x*u^2)
        with ((x*u^2-v^2)+v^2) by ring.
      apply F28_divide_add.
      - exact Heq.
      - exact Hvv.
    }

    assert (Hx_not : ~ (p | x*u^2)).
    {
      replace (x*u^2) with (x*(u*u)) by ring.
      apply F28_prime_product_nonzero.
      - exact Hp.
      - exact Hx.
      - apply F28_prime_square_nonzero.
        + exact Hp.
        + exact Hu.
    }

    exact (Hx_not Hxuu).
  }

  exists u, v.
  split.
  - exact Hu.
  - split.
    + exact Hv.
    + exact Heq.
Qed.

(* ================================================= *)
(* 10. STAGE 5 SPLIT-NODE ARITHMETIC CERTIFICATE    *)
(* ================================================= *)

Definition F28_split_node_certificate
  (p r : Z) : Prop :=
  ~ (p | 3*r) /\
  F28_rational_tangent_directions p r.

Theorem F28_split_node_square_criterion :
  forall p r : Z,
    ~ (p | 3*r) ->
    (F28_split_node_certificate p r <->
     F28_square_certificate p (3*r)).
Proof.
  intros p r Hnonzero.
  unfold F28_split_node_certificate.
  split.
  - intros [_ Htangent].
    apply (proj1
      (F28_tangent_square_equivalence p r)).
    exact Htangent.
  - intro Hsquare.
    split.
    + exact Hnonzero.
    + apply (proj2
        (F28_tangent_square_equivalence p r)).
      exact Hsquare.
Qed.

(* ================================================= *)
(* 11. STAGE 4 + STAGE 5 COMBINATION                *)
(* ================================================= *)

Theorem F28_stage5_certificate :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (p | F28_derivative (F28_A a c) r) ->
    F28_invariant_certificate
      p (F28_A a c) (F28_B b c)
    /\
    ~ (p | r)
    /\
    ~ (p | 3*r)
    /\
    (F28_split_node_certificate p r <->
     F28_square_certificate p (3*r)).
Proof.
  intros p a b c r Hp Hlarge Ha Hc HF Hder.

  pose proof
    (F28_stage4_certificate
       p a b c r Hp Hlarge Ha Hc HF Hder)
    as Hstage4.

  destruct Hstage4 as
    [Hinv [Hr [Hthree Htangent]]].

  split.
  - exact Hinv.
  - split.
    + exact Hr.
    + split.
      * exact Hthree.
      * exact
          (F28_split_node_square_criterion
             p r Hthree).
Qed.

(* ================================================= *)
(* 12. FINAL CHECKS FOR CI                         *)
(* ================================================= *)

Check F28_large_prime_reduction_certificate.
Check F28_stage4_certificate.

Check F28_divide_opp_iff.
Check F28_tangent_square_equivalence.
Check F28_square_root_nonzero.
Check F28_split_node_square_criterion.
Check F28_stage5_certificate.

Print Assumptions F28_stage5_certificate.
Print Assumptions F28_tangent_square_equivalence.
Print Assumptions F28_square_root_nonzero.
