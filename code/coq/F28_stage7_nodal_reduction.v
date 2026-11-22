(* code/coq/F28_stage7_nodal_reduction.v

   The owner's fifty-first Coq file ("F.28 - Stage 7: algebraic nodal reduction certificate", 22 November 2026).  The text is the owner's, with ONE change: the import
   "From Stdlib Require Import ZArith Znumtheory Ring Lia." is written "From Coq Require Import ZArith Znumtheory Ring Lia." (CI compiles with Coq 8.20.1, which has no Stdlib prefix).
   Plus this header.  Standalone.
   DEFINITIONS: F28_multiplicative_invariant_criterion p A B := p | Delta (= -16(4A^3 + 27B^2)) and p not dividing c4 (= -48 A);  F28_ordinary_node p A B r := p | f(r), p | f'(r), p not dividing 3 r;
   F28_nodal_reduction_certificate := both.
   WHAT IT PROVES (read by hand): for the paper's model (A = 4 a c^3, B = -8 b c^5), prime p >= 5, p not dividing a, c, p | F = 4 a^3 + 27 b^2 c and any r with p | f(r), p | f'(r):
     F28_multiplicative_invariants: p | Delta and p not dividing c4 (c4 = -192 a c^3: p not dividing 192 = 2^6 * 3);   F28_A_nonzero: p not dividing A = 4 a c^3;
     F28_ordinary_node_from_singularity: p not dividing 3 r (p not dividing A and p | f'(r) give p not dividing r);
     F28_stage7_nodal_reduction: the certificate (invariant criterion AND ordinary node);
     F28_stage7_complete_certificate: the certificate AND p not dividing r AND the tangent cone at (1, 0) is nonzero.
   plus the translation identities f(r+u) = f(r) + f'(r) u + 3 r u^2 + u^3 and v^2 - f(r+u) = (v^2 - 3 r u^2) - u^3 - f(r) - f'(r) u (ring).
   It is the input that the Tate / Silverman statement needs ("p | Delta, p not dividing c4" = multiplicative reduction of a minimal model, node with tangent cone nonzero); that statement itself, and minimality, are NOT in Coq.
   Existence of r: F28_complete_arithmetic_bridge.v; class of 3r: F28_unconditional_bridge.v (50th file); composition held until the owner says so. *)

From Coq Require Import ZArith Znumtheory Ring Lia.

Open Scope Z_scope.

(* ====================================================== *)
(* F.28 - STAGE 7                                        *)
(* ALGEBRAIC NODAL REDUCTION CERTIFICATE                 *)
(* Complete standalone development                       *)
(* ====================================================== *)

(* ------------------------------------------------------ *)
(* 1. CURVE AND INVARIANTS                               *)
(* ------------------------------------------------------ *)

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

Definition F28_cubic (A B r : Z) : Z :=
  r^3 + A*r + B.

Definition F28_derivative (A r : Z) : Z :=
  3*r^2 + A.

Definition F28_tangent_cone (r u v : Z) : Z :=
  v^2 - 3*r*u^2.

Definition F28_multiplicative_invariant_criterion
  (p A B : Z) : Prop :=
  (p | F28_discriminant A B) /\
  ~ (p | F28_c4 A).

Definition F28_ordinary_node
  (p A B r : Z) : Prop :=
  (p | F28_cubic A B r) /\
  (p | F28_derivative A r) /\
  ~ (p | 3*r).

Definition F28_nodal_reduction_certificate
  (p A B r : Z) : Prop :=
  F28_multiplicative_invariant_criterion p A B /\
  F28_ordinary_node p A B r.

(* ------------------------------------------------------ *)
(* 2. ELEMENTARY DIVISIBILITY                            *)
(* ------------------------------------------------------ *)

Lemma F28_divide_mul :
  forall p x y : Z,
    (p | x) -> (p | x*y).
Proof.
  intros p x y H.
  destruct H as [k Hk].
  exists (k*y).
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

Lemma F28_prime_4_nonzero :
  forall p : Z,
    prime p ->
    5 <= p ->
    ~ (p | 4).
Proof.
  intros p Hp Hlarge.
  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }
  replace 4 with (2*2) by ring.
  apply F28_prime_product_nonzero.
  - exact Hp.
  - exact H2.
  - exact H2.
Qed.

Lemma F28_prime_3_nonzero :
  forall p : Z,
    5 <= p ->
    ~ (p | 3).
Proof.
  intros p Hlarge.
  apply F28_not_divide_small; lia.
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

(* ------------------------------------------------------ *)
(* 3. INVARIANT IDENTITIES                               *)
(* ------------------------------------------------------ *)

Theorem F28_c4_identity :
  forall a c : Z,
    F28_c4 (F28_A a c) =
    -192*a*c^3.
Proof.
  intros a c.
  unfold F28_c4, F28_A.
  ring.
Qed.

Theorem F28_c6_identity :
  forall b c : Z,
    F28_c6 (F28_B b c) =
    6912*b*c^5.
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
  unfold F28_discriminant.
  unfold F28_A, F28_B, F28_F.
  ring.
Qed.

Theorem F28_discriminant_vanishes :
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

(* ------------------------------------------------------ *)
(* 4. CORRECTED NONVANISHING OF A                        *)
(* ------------------------------------------------------ *)

Theorem F28_A_nonzero :
  forall p a c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    ~ (p | F28_A a c).
Proof.
  intros p a c Hp Hlarge Ha Hc.
  unfold F28_A.

  replace (4*a*c^3)
    with (4*(a*c^3)) by ring.

  apply F28_prime_product_nonzero.
  - exact Hp.
  - apply F28_prime_4_nonzero.
    + exact Hp.
    + exact Hlarge.
  - apply F28_prime_product_nonzero.
    + exact Hp.
    + exact Ha.
    + apply F28_prime_cube_nonzero.
      * exact Hp.
      * exact Hc.
Qed.

Theorem F28_c4_nonzero :
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

Theorem F28_multiplicative_invariants :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    F28_multiplicative_invariant_criterion
      p (F28_A a c) (F28_B b c).
Proof.
  intros p a b c Hp Hlarge Ha Hc HF.
  unfold F28_multiplicative_invariant_criterion.
  split.
  - apply F28_discriminant_vanishes.
    exact HF.
  - apply F28_c4_nonzero.
    + exact Hp.
    + exact Hlarge.
    + exact Ha.
    + exact Hc.
Qed.

(* ------------------------------------------------------ *)
(* 5. NONDEGENERATE SINGULAR ROOT                        *)
(* ------------------------------------------------------ *)

Theorem F28_derivative_root_nonzero :
  forall p A r : Z,
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | r).
Proof.
  intros p A r HA Hder Hr.

  assert (Hrr : (p | r*r)).
  {
    apply F28_divide_mul.
    exact Hr.
  }

  assert (Hthree : (p | 3*r^2)).
  {
    replace (3*r^2)
      with ((r*r)*3) by ring.
    apply F28_divide_mul.
    exact Hrr.
  }

  apply HA.

  replace A with
    ((3*r^2+A)+(-(3*r^2))) by ring.

  apply F28_divide_add.
  - exact Hder.
  - apply F28_divide_neg.
    exact Hthree.
Qed.

Theorem F28_three_root_nonzero :
  forall p A r : Z,
    prime p ->
    5 <= p ->
    ~ (p | A) ->
    (p | F28_derivative A r) ->
    ~ (p | 3*r).
Proof.
  intros p A r Hp Hlarge HA Hder.

  assert (H3 : ~ (p | 3)).
  {
    apply F28_prime_3_nonzero.
    exact Hlarge.
  }

  assert (Hr : ~ (p | r)).
  {
    exact
      (F28_derivative_root_nonzero
         p A r HA Hder).
  }

  exact
    (F28_prime_product_nonzero
       p 3 r Hp H3 Hr).
Qed.

Theorem F28_ordinary_node_from_singularity :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    F28_ordinary_node
      p (F28_A a c) (F28_B b c) r.
Proof.
  intros p a b c r Hp Hlarge Ha Hc Hf Hd.
  unfold F28_ordinary_node.

  split.
  - exact Hf.
  - split.
    + exact Hd.
    + apply F28_three_root_nonzero
        with (A := F28_A a c).
      * exact Hp.
      * exact Hlarge.
      * apply F28_A_nonzero.
        -- exact Hp.
        -- exact Hlarge.
        -- exact Ha.
        -- exact Hc.
      * exact Hd.
Qed.

(* ------------------------------------------------------ *)
(* 6. LOCAL TRANSLATION AT THE SINGULAR POINT           *)
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

Theorem F28_local_equation_identity :
  forall A B r u v : Z,
    v^2 - F28_cubic A B (r+u) =
    F28_tangent_cone r u v
    - u^3
    - F28_cubic A B r
    - F28_derivative A r*u.
Proof.
  intros A B r u v.
  unfold F28_tangent_cone.
  unfold F28_cubic, F28_derivative.
  ring.
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

(* ------------------------------------------------------ *)
(* 7. FINAL STAGE 7 CERTIFICATE                          *)
(* ------------------------------------------------------ *)

Theorem F28_stage7_nodal_reduction :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    F28_nodal_reduction_certificate
      p (F28_A a c) (F28_B b c) r.
Proof.
  intros p a b c r
         Hp Hlarge Ha Hc HF Hf Hd.

  unfold F28_nodal_reduction_certificate.
  split.
  - exact
      (F28_multiplicative_invariants
         p a b c Hp Hlarge Ha Hc HF).
  - exact
      (F28_ordinary_node_from_singularity
         p a b c r Hp Hlarge Ha Hc Hf Hd).
Qed.

(* ------------------------------------------------------ *)
(* 8. STRENGTHENED FINAL THEOREM                         *)
(* ------------------------------------------------------ *)

Theorem F28_stage7_complete_certificate :
  forall p a b c r : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (p | F28_cubic
           (F28_A a c) (F28_B b c) r) ->
    (p | F28_derivative (F28_A a c) r) ->
    F28_nodal_reduction_certificate
      p (F28_A a c) (F28_B b c) r
    /\
    ~ (p | r)
    /\
    ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p a b c r
         Hp Hlarge Ha Hc HF Hf Hd.

  assert (HA :
    ~ (p | F28_A a c)).
  {
    exact
      (F28_A_nonzero
         p a c Hp Hlarge Ha Hc).
  }

  assert (Hr : ~ (p | r)).
  {
    exact
      (F28_derivative_root_nonzero
         p (F28_A a c) r HA Hd).
  }

  assert (Hthree : ~ (p | 3*r)).
  {
    exact
      (F28_three_root_nonzero
         p (F28_A a c) r
         Hp Hlarge HA Hd).
  }

  split.
  - exact
      (F28_stage7_nodal_reduction
         p a b c r
         Hp Hlarge Ha Hc HF Hf Hd).
  - split.
    + exact Hr.
    + exact
        (F28_tangent_coefficient_nonzero
           p r Hthree).
Qed.

(* ------------------------------------------------------ *)
(* 9. COMPILER AND ASSUMPTION CHECKS                     *)
(* ------------------------------------------------------ *)

Check F28_c4_identity.
Check F28_c6_identity.
Check F28_discriminant_identity.
Check F28_A_nonzero.
Check F28_c4_nonzero.
Check F28_multiplicative_invariants.
Check F28_derivative_root_nonzero.
Check F28_three_root_nonzero.
Check F28_ordinary_node_from_singularity.
Check F28_cubic_translation_identity.
Check F28_local_equation_identity.
Check F28_stage7_nodal_reduction.
Check F28_stage7_complete_certificate.

Print Assumptions F28_A_nonzero.
Print Assumptions F28_stage7_nodal_reduction.
Print Assumptions F28_stage7_complete_certificate.
