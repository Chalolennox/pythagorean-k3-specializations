(* code/coq/F28_stage13_multiplicative_reduction.v

   STAGE 13.  NOT an owner file: written in review by Claude (a language model; no human check), at the owner's request ("go ahead").  Standalone.  Compiled only by CI (Coq 8.20.1); read by hand beforehand, no local Coq.
   THIS IS THE COMPOSITION: the first file that assembles the standalone files into one development, as the owner allowed.  Nothing is changed in the blocks copied.
   HOW IT IS BUILT: (1) the whole text of my Stage 8a file (F28_stage8a_reduced_model.v: the owner's 51st file, blocks of the 50th and 40th files, and the 8a section: integer minimality, existence of a double root, singular points of the reduced curve y^2 = f(x)
   mod p, uniqueness, node, split criterion), its closing Check/Print lines dropped; (2) blocks copied UNCHANGED from the owner's 56th file (F28_stage12_inverses.v, which contains files 52-55): the factorization certificate (Stage 8), the normalization
   t |-> (t^2 - 2r, t(t^2 - 3r)) and its map into the reduced curve (Stage 9), the two branches above the node (Stage 10), the square-class bridge (Stage 11) and inverse elimination via Bezout (Stage 12); (3) a section "NEW IN STAGE 13" which is mine.
   WHAT THE NEW SECTION PROVES, for prime p >= 5, p not dividing a, b, c, p | F = 4 a^3 + 27 b^2 c, F nonzero, A = 4 a c^3, B = -8 b c^5:
     F28_valuation_bound: if n^4 C = m^4 C' (u = m/n a rational scaling of coordinates, C = c4, C' = c4') and p does not divide C, then every power of p dividing m divides n, i.e. v_p(u) <= 0 (induction on the exponent; F28_ppow p k = p^k);
       F28_scaling_minimal p A: the statement of this for C = c4 = -48 A; F28_scaling_minimal_model: it holds for the model (p >= 5, p not dividing a, c).  Together with Delta = u^12 Delta' (not formalised) this is minimality of the model at p.
     F28_discriminant_nonzero: Delta = -1024 c^9 F is nonzero when c is nonzero (p does not divide c) and F is nonzero: the curve is an elliptic curve over Q.
     F28_multiplicative_reduction p A B := F28_scaling_minimal p A and F28_node_reduction p A B (a singular point (x, 0) of the reduced curve exists and at every singular point p does not divide 3x); F28_split_multiplicative / F28_nonsplit_multiplicative add
       "the tangent directions are (not) rational over F_p" at every singular point.  This is Silverman's definition of the reduction type (Ch. VII, section 1, Prop. VII.5.1), used as the DEFINITION, on integer representatives mod p.
     F28_model_multiplicative_reduction: the model has multiplicative reduction at p;  F28_model_split_multiplicative_iff / F28_model_nonsplit_multiplicative_iff: it is split iff F28_square_certificate p (a b) (a b a nonzero square mod p), nonsplit iff not.
     F28_square_certificate_to_mod / F28_square_mod_to_certificate / F28_branches_iff_tangent_directions: at a node with p not dividing 3r the two branches of the normalization exist iff the tangent cone v^2 - 3 r u^2 has rational directions.
     F28_stage13_multiplicative_reduction: all of this in one theorem: p | Delta, p not dividing c4, Delta nonzero, multiplicative reduction, the factorization certificate and the normalization map at every singular point, branches iff tangent directions, branches iff ab a square
       mod p, split iff ab square class, nonsplit iff not.
   WHAT IT DOES NOT PROVE (explicitly): there is no construction of Q_p or of a p-adic valuation on Q (valuations enter only through F28_ppow and divisibility of integers); Delta = u^12 Delta' and the Weierstrass change-of-variables formulas are not formalised;
   that this reduction type of the reduced curve is "multiplicative reduction of the elliptic curve over Q_p" is the DEFINITION used, not derived from Tate's algorithm or the Neron model; THE LOCAL ROOT NUMBER (Stage 14: w_p = -1 split multiplicative, +1 nonsplit,
   Rohrlich) is a cited theorem, NOT in Coq, so w_p = -(ab/p) is not proved; the facts that F nonzero and p not dividing a, b, c hold for a Pythagorean specialization and that c is a perfect square on the family are not here (hypotheses). *)

From Coq Require Import
  ZArith Znumtheory Zgcd_alt Ring Lia.

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


(* ====================================================== *)
(* BLOCKS COPIED UNCHANGED FROM THE 50TH FILE (F28_unconditional_bridge.v) *)
(* ====================================================== *)

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

(* ====================================================== *)
(* BLOCK COPIED UNCHANGED FROM THE 40TH FILE (F28_complete_arithmetic_bridge.v) *)
(* ====================================================== *)

Lemma F28_prime_inverse :
  forall p s : Z,
    prime p ->
    ~ (p | s) ->
    exists u : Z, (p | s*u-1).
Proof.
  intros p s Hp Hnotdiv.

  assert (Hgcd : Z.gcd p s = 1).
  {
    apply Zis_gcd_gcd.
    - lia.
    - apply prime_rel_prime.
      + exact Hp.
      + exact Hnotdiv.
  }

  pose proof
    (Z.gcd_bezout p s 1 Hgcd) as Hbezout.

  unfold Z.Bezout in Hbezout.
  destruct Hbezout as [k [u Hidentity]].

  exists u.
  exists (-k).
  rewrite <- Hidentity.
  ring.
Qed.

(* ====================================================== *)
(* NEW IN STAGE 8a (written in review by Claude)          *)
(* ====================================================== *)

(* ------------------------------------------------------ *)
(* 8a.1  ELEMENTARY MINIMALITY CRITERION                  *)
(* ------------------------------------------------------ *)

(* An integral change of Weierstrass coordinates with scaling
   factor u multiplies c4 by u^4: c4 = u^4 * c4'.  If p does not
   divide c4 then p cannot divide u. *)

Theorem F28_unit_scaling :
  forall p C u C' : Z,
    ~ (p | C) ->
    C = u^4*C' ->
    ~ (p | u).
Proof.
  intros p C u C' HC Heq Hu.
  apply HC.
  rewrite Heq.
  destruct Hu as [k Hk].
  exists (k^4*p^3*C').
  rewrite Hk.
  ring.
Qed.

Theorem F28_model_scaling_unit :
  forall p a c u C' : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    F28_c4 (F28_A a c) = u^4*C' ->
    ~ (p | u).
Proof.
  intros p a c u C' Hp Hlarge Ha Hc Heq.
  apply (F28_unit_scaling p (F28_c4 (F28_A a c)) u C').
  - exact (F28_c4_nonzero p a c Hp Hlarge Ha Hc).
  - exact Heq.
Qed.

(* ------------------------------------------------------ *)
(* 8a.2  EXISTENCE OF A DOUBLE ROOT (GENERAL A, B)        *)
(* ------------------------------------------------------ *)

Lemma F28_double_root_general :
  forall p A B u m : Z,
    prime p ->
    5 <= p ->
    ~ (p | A) ->
    (p | 4*A^3 + 27*B^2) ->
    2*A*u - 1 = m*p ->
    (p | F28_cubic A B (-3*B*u)) /\
    (p | F28_derivative A (-3*B*u)).
Proof.
  intros p A B u m Hp Hlarge HA HD Hm.

  assert (H3 : ~ (p | 3)).
  {
    apply F28_not_divide_small; lia.
  }

  assert (H4 : ~ (p | 4)).
  {
    exact (F28_prime_4_nonzero p Hp Hlarge).
  }

  assert (HAA : ~ (p | A*A)).
  {
    exact (F28_prime_square_nonzero p A Hp HA).
  }

  assert (H4AA : ~ (p | 4*(A*A))).
  {
    exact (F28_prime_product_nonzero p 4 (A*A) Hp H4 HAA).
  }

  assert (Hu : 2*A*u = m*p+1).
  {
    rewrite <- Hm.
    ring.
  }

  assert (Hid :
    4*(A*A)*(3*(-3*B*u)^2+A) =
    (4*A^3+27*B^2) + p*(27*B^2*(2*m+m^2*p))).
  {
    replace (4*(A*A)*(3*(-3*B*u)^2+A))
      with (4*A^3+27*B^2*(2*A*u)^2) by ring.
    rewrite Hu.
    ring.
  }

  assert (Hdiv :
    (p | 4*(A*A)*(3*(-3*B*u)^2+A))).
  {
    rewrite Hid.
    apply F28_divide_add.
    - exact HD.
    - exact
        (F28_divide_mul p p
           (27*B^2*(2*m+m^2*p))
           (Z.divide_refl p)).
  }

  assert (Hder : (p | 3*(-3*B*u)^2+A)).
  {
    exact
      (F28_prime_cancel p (4*(A*A))
         (3*(-3*B*u)^2+A) Hp H4AA Hdiv).
  }

  assert (Hid2 :
    3*((-3*B*u)^3 + A*(-3*B*u) + B) =
    (3*(-3*B*u)^2+A)*(-3*B*u) + p*(-3*B*m)).
  {
    replace (3*((-3*B*u)^3 + A*(-3*B*u) + B))
      with ((3*(-3*B*u)^2+A)*(-3*B*u)
            + 3*B*(1 - 2*A*u)) by ring.
    replace (1 - 2*A*u) with (-(m*p)).
    - ring.
    - rewrite Hu.
      ring.
  }

  assert (H3f :
    (p | 3*((-3*B*u)^3 + A*(-3*B*u) + B))).
  {
    rewrite Hid2.
    apply F28_divide_add.
    - exact
        (F28_divide_mul p (3*(-3*B*u)^2+A)
           (-3*B*u) Hder).
    - exact
        (F28_divide_mul p p (-3*B*m)
           (Z.divide_refl p)).
  }

  split.
  - exact
      (F28_prime_cancel p 3
         ((-3*B*u)^3 + A*(-3*B*u) + B)
         Hp H3 H3f).
  - exact Hder.
Qed.

Lemma F28_discriminant_quartic_identity :
  forall a b c : Z,
    4*(F28_A a c)^3 + 27*(F28_B b c)^2 =
    64*c^9*F28_F a b c.
Proof.
  intros a b c.
  unfold F28_A, F28_B, F28_F.
  ring.
Qed.

Theorem F28_double_root_exists :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    exists r : Z,
      (p | F28_cubic (F28_A a c) (F28_B b c) r) /\
      (p | F28_derivative (F28_A a c) r).
Proof.
  intros p a b c Hp Hlarge Ha Hc HF.

  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }

  assert (HA : ~ (p | F28_A a c)).
  {
    exact (F28_A_nonzero p a c Hp Hlarge Ha Hc).
  }

  assert (H2A : ~ (p | 2*F28_A a c)).
  {
    exact
      (F28_prime_product_nonzero
         p 2 (F28_A a c) Hp H2 HA).
  }

  assert (HD :
    (p | 4*(F28_A a c)^3 + 27*(F28_B b c)^2)).
  {
    rewrite F28_discriminant_quartic_identity.
    destruct HF as [k Hk].
    exists (64*c^9*k).
    rewrite Hk.
    ring.
  }

  destruct
    (F28_prime_inverse p (2*F28_A a c) Hp H2A)
    as [u [m Hm]].

  exists (-3*F28_B b c*u).

  exact
    (F28_double_root_general
       p (F28_A a c) (F28_B b c) u m
       Hp Hlarge HA HD Hm).
Qed.

(* ------------------------------------------------------ *)
(* 8a.3  THE REDUCED CURVE OVER F_p, AFFINE SINGULAR POINTS *)
(* ------------------------------------------------------ *)

(* A point (x, y) of the reduced curve y^2 = f(x) over F_p is
   singular when it lies on the curve, d/dy (y^2 - f) = 2 y
   vanishes and d/dx (y^2 - f) = - f'(x) vanishes (the sign is
   irrelevant for divisibility).  Points are integer
   representatives; everything is read mod p. *)

Definition F28_reduced_singular
  (p A B x y : Z) : Prop :=
  (p | y^2 - F28_cubic A B x) /\
  (p | 2*y) /\
  (p | F28_derivative A x).

Lemma F28_reduced_singular_split :
  forall p A B x y : Z,
    prime p ->
    5 <= p ->
    F28_reduced_singular p A B x y ->
    (p | y) /\
    (p | F28_cubic A B x) /\
    (p | F28_derivative A x).
Proof.
  intros p A B x y Hp Hlarge Hsing.
  destruct Hsing as [Hcurve [Hy2 Hder]].

  assert (H2 : ~ (p | 2)).
  {
    apply F28_not_divide_small; lia.
  }

  assert (Hy : (p | y)).
  {
    exact (F28_prime_cancel p 2 y Hp H2 Hy2).
  }

  assert (Hysq : (p | y^2)).
  {
    replace (y^2) with (y*y) by ring.
    exact (F28_divide_mul p y y Hy).
  }

  assert (Hf : (p | F28_cubic A B x)).
  {
    replace (F28_cubic A B x)
      with (y^2 - (y^2 - F28_cubic A B x))
      by ring.
    exact (F28_divide_sub p _ _ Hysq Hcurve).
  }

  split.
  - exact Hy.
  - split.
    + exact Hf.
    + exact Hder.
Qed.

Lemma F28_reduced_singular_intro :
  forall p A B x : Z,
    (p | F28_cubic A B x) ->
    (p | F28_derivative A x) ->
    F28_reduced_singular p A B x 0.
Proof.
  intros p A B x Hf Hder.
  unfold F28_reduced_singular.
  split.
  - replace (0^2 - F28_cubic A B x)
      with (-(F28_cubic A B x)) by ring.
    exact (F28_divide_neg p _ Hf).
  - split.
    + exists 0.
      ring.
    + exact Hder.
Qed.

(* ------------------------------------------------------ *)
(* 8a.4  THE SINGULAR POINT IS UNIQUE MOD p               *)
(* ------------------------------------------------------ *)

Theorem F28_reduced_singular_unique :
  forall p a b c x1 y1 x2 y2 : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    F28_reduced_singular
      p (F28_A a c) (F28_B b c) x1 y1 ->
    F28_reduced_singular
      p (F28_A a c) (F28_B b c) x2 y2 ->
    (p | x1 - x2) /\ (p | y1) /\ (p | y2).
Proof.
  intros p a b c x1 y1 x2 y2
         Hp Hlarge Ha Hc S1 S2.

  destruct
    (F28_reduced_singular_split
       p (F28_A a c) (F28_B b c) x1 y1
       Hp Hlarge S1)
    as [Hy1 [Hf1 Hd1]].

  destruct
    (F28_reduced_singular_split
       p (F28_A a c) (F28_B b c) x2 y2
       Hp Hlarge S2)
    as [Hy2 [Hf2 Hd2]].

  pose proof
    (F28_singular_linear_relation
       p a b c x1 Hp Hlarge Hc Hf1 Hd1)
    as L1.

  pose proof
    (F28_singular_linear_relation
       p a b c x2 Hp Hlarge Hc Hf2 Hd2)
    as L2.

  split.
  - apply (F28_prime_cancel p a (x1-x2) Hp Ha).
    replace (a*(x1-x2))
      with ((a*x1-3*b*c^2) - (a*x2-3*b*c^2))
      by ring.
    exact (F28_divide_sub p _ _ L1 L2).
  - split.
    + exact Hy1.
    + exact Hy2.
Qed.

(* ------------------------------------------------------ *)
(* 8a.5  THE SINGULAR POINT IS A NODE (NONDEGENERATE CONE) *)
(* ------------------------------------------------------ *)

Theorem F28_reduced_singular_node :
  forall p a b c x y : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    F28_reduced_singular
      p (F28_A a c) (F28_B b c) x y ->
    ~ (p | x) /\
    ~ (p | 3*x) /\
    ~ (p | F28_tangent_cone x 1 0).
Proof.
  intros p a b c x y Hp Hlarge Ha Hc Hsing.

  destruct
    (F28_reduced_singular_split
       p (F28_A a c) (F28_B b c) x y
       Hp Hlarge Hsing)
    as [Hy [Hf Hd]].

  assert (HA : ~ (p | F28_A a c)).
  {
    exact (F28_A_nonzero p a c Hp Hlarge Ha Hc).
  }

  assert (Hr : ~ (p | x)).
  {
    exact
      (F28_derivative_root_nonzero
         p (F28_A a c) x HA Hd).
  }

  assert (Hthree : ~ (p | 3*x)).
  {
    exact
      (F28_three_root_nonzero
         p (F28_A a c) x Hp Hlarge HA Hd).
  }

  split.
  - exact Hr.
  - split.
    + exact Hthree.
    + exact
        (F28_tangent_coefficient_nonzero
           p x Hthree).
Qed.

(* ------------------------------------------------------ *)
(* 8a.6  SPLIT / NONSPLIT NODE OF THE REDUCED CURVE       *)
(* ------------------------------------------------------ *)

Theorem F28_reduced_node_split_criterion :
  forall p a b c x y : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    F28_reduced_singular
      p (F28_A a c) (F28_B b c) x y ->
    (F28_split_node_certificate p x <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b c x y Hp Hlarge Ha Hb Hc Hsing.

  assert (Hab : ~ (p | a*b)).
  {
    exact (F28_prime_product_nonzero p a b Hp Ha Hb).
  }

  destruct
    (F28_reduced_singular_split
       p (F28_A a c) (F28_B b c) x y
       Hp Hlarge Hsing)
    as [Hy [Hf Hd]].

  destruct
    (F28_reduced_singular_node
       p a b c x y Hp Hlarge Ha Hc Hsing)
    as [Hr [Hthree Htangent]].

  exact
    (F28_unconditional_split_node
       p a b c x
       Hp Hlarge Hc Hthree Hab Hf Hd).
Qed.

(* ------------------------------------------------------ *)
(* 8a.7  THE STAGE 8a MODEL THEOREM                       *)
(* ------------------------------------------------------ *)

Theorem F28_stage8a_reduction_model :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    F28_multiplicative_invariant_criterion
      p (F28_A a c) (F28_B b c)
    /\
    (forall u C' : Z,
       F28_c4 (F28_A a c) = u^4*C' ->
       ~ (p | u))
    /\
    (exists x : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x 0)
    /\
    (forall x1 y1 x2 y2 : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x1 y1 ->
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x2 y2 ->
       (p | x1 - x2) /\ (p | y1) /\ (p | y2))
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       ~ (p | x) /\
       ~ (p | 3*x) /\
       ~ (p | F28_tangent_cone x 1 0))
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       (F28_split_node_certificate p x <->
        F28_square_certificate p (a*b))).
Proof.
  intros p a b c Hp Hlarge Ha Hb Hc HF.

  assert (H1 :
    F28_multiplicative_invariant_criterion
      p (F28_A a c) (F28_B b c)).
  {
    exact
      (F28_multiplicative_invariants
         p a b c Hp Hlarge Ha Hc HF).
  }

  assert (H2 :
    forall u C' : Z,
      F28_c4 (F28_A a c) = u^4*C' ->
      ~ (p | u)).
  {
    intros u C' Heq.
    exact
      (F28_model_scaling_unit
         p a c u C' Hp Hlarge Ha Hc Heq).
  }

  assert (H3 :
    exists x : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x 0).
  {
    destruct
      (F28_double_root_exists
         p a b c Hp Hlarge Ha Hc HF)
      as [r [Hf Hd]].
    exists r.
    exact
      (F28_reduced_singular_intro
         p (F28_A a c) (F28_B b c) r Hf Hd).
  }

  assert (H4 :
    forall x1 y1 x2 y2 : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x1 y1 ->
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x2 y2 ->
      (p | x1 - x2) /\ (p | y1) /\ (p | y2)).
  {
    intros x1 y1 x2 y2 S1 S2.
    exact
      (F28_reduced_singular_unique
         p a b c x1 y1 x2 y2
         Hp Hlarge Ha Hc S1 S2).
  }

  assert (H5 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      ~ (p | x) /\
      ~ (p | 3*x) /\
      ~ (p | F28_tangent_cone x 1 0)).
  {
    intros x y S.
    exact
      (F28_reduced_singular_node
         p a b c x y Hp Hlarge Ha Hc S).
  }

  assert (H6 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      (F28_split_node_certificate p x <->
       F28_square_certificate p (a*b))).
  {
    intros x y S.
    exact
      (F28_reduced_node_split_criterion
         p a b c x y
         Hp Hlarge Ha Hb Hc S).
  }

  exact (conj H1 (conj H2 (conj H3 (conj H4 (conj H5 H6))))).
Qed.


(* ====================================================== *)
(* BLOCKS COPIED UNCHANGED FROM THE 56TH FILE (F28_stage12_inverses.v): STAGES 8-12 *)
(* ====================================================== *)

Definition F28_factor (r x : Z) : Z := (x-r)^2*(x+2*r).

Theorem F28_factor_difference :
  forall A B r x : Z,
    F28_cubic A B x - F28_factor r x =
    F28_derivative A r*(x-r) + F28_cubic A B r.
Proof.
  intros A B r x.
  unfold F28_cubic, F28_derivative, F28_factor. ring.
Qed.

Theorem F28_simple_root_factor :
  forall r : Z, F28_factor r (-2*r) = 0.
Proof.
  intro r. unfold F28_factor. ring.
Qed.

Theorem F28_root_difference :
  forall r : Z, r - (-2*r) = 3*r.
Proof.
  intro r. ring.
Qed.

Theorem F28_derivative_difference :
  forall A r : Z,
    F28_derivative A (-2*r) - F28_derivative A r = (3*r)*(3*r).
Proof.
  intros A r. unfold F28_derivative. ring.
Qed.

Theorem F28_singular_factorization :
  forall p A B r x : Z,
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    (p | F28_cubic A B x - F28_factor r x).
Proof.
  intros p A B r x Hf Hd.
  destruct Hf as [kf Hkf].
  destruct Hd as [kd Hkd].
  rewrite F28_factor_difference.
  exists (kd*(x-r)+kf).
  rewrite Hkd, Hkf. ring.
Qed.

Theorem F28_second_root_on_cubic :
  forall p A B r : Z,
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    (p | F28_cubic A B (-2*r)).
Proof.
  intros p A B r Hf Hd.
  pose proof (F28_singular_factorization p A B r (-2*r) Hf Hd)
    as Hfactor.
  rewrite F28_simple_root_factor in Hfactor.
  replace (F28_cubic A B (-2*r)-0)
    with (F28_cubic A B (-2*r)) in Hfactor by ring.
  exact Hfactor.
Qed.

Theorem F28_distinct_roots_mod_p :
  forall p r : Z, ~ (p | 3*r) -> ~ (p | r-(-2*r)).
Proof.
  intros p r Hthree.
  rewrite F28_root_difference. exact Hthree.
Qed.

Theorem F28_simple_root_derivative_nonzero :
  forall p A r : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | F28_derivative A r) ->
    ~ (p | F28_derivative A (-2*r)).
Proof.
  intros p A r Hp Hthree Hd Hbad.
  destruct Hd as [kd Hkd].
  destruct Hbad as [ks Hks].
  assert (Hsquare : (p | (3*r)*(3*r))).
  {
    exists (ks-kd).
    rewrite <- (F28_derivative_difference A r).
    rewrite Hks, Hkd. ring.
  }
  assert (Hnot : ~ (p | (3*r)*(3*r))).
  {
    apply F28_prime_product_nonzero.
    - exact Hp.
    - exact Hthree.
    - exact Hthree.
  }
  exact (Hnot Hsquare).
Qed.

Theorem F28_tangent_nonzero :
  forall p r : Z,
    ~ (p | 3*r) -> ~ (p | F28_tangent_cone r 1 0).
Proof.
  intros p r Hthree Hbad.
  rewrite F28_tangent_coefficient_identity in Hbad.
  apply Hthree.
  replace (3*r) with (-(-(3*r))) by ring.
  apply F28_divide_neg. exact Hbad.
Qed.

Definition F28_factorization_certificate (p A B r : Z) : Prop :=
  (forall x : Z, (p | F28_cubic A B x - F28_factor r x)) /\
  (p | F28_cubic A B r) /\
  (p | F28_derivative A r) /\
  ~ (p | r-(-2*r)) /\
  (p | F28_cubic A B (-2*r)) /\
  ~ (p | F28_derivative A (-2*r)) /\
  ~ (p | F28_tangent_cone r 1 0).

Theorem F28_stage8_factorization :
  forall p A B r : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    F28_factorization_certificate p A B r.
Proof.
  intros p A B r Hp Hthree Hf Hd.
  unfold F28_factorization_certificate.
  repeat split.
  - intro x.
    exact (F28_singular_factorization p A B r x Hf Hd).
  - exact Hf.
  - exact Hd.
  - exact (F28_distinct_roots_mod_p p r Hthree).
  - exact (F28_second_root_on_cubic p A B r Hf Hd).
  - exact (F28_simple_root_derivative_nonzero p A r Hp Hthree Hd).
  - exact (F28_tangent_nonzero p r Hthree).
Qed.

Definition F28_norm_x (r t : Z) : Z := t^2 - 2*r.

Definition F28_norm_y (r t : Z) : Z := t*(t^2 - 3*r).

Definition F28_node_equation (r x y : Z) : Z :=
  y^2 - F28_factor r x.

Theorem F28_stage9_parametrization :
  forall r t : Z,
    F28_node_equation r (F28_norm_x r t) (F28_norm_y r t) = 0.
Proof.
  intros r t.
  unfold F28_node_equation, F28_norm_x, F28_norm_y, F28_factor.
  ring.
Qed.

Theorem F28_stage9_reduced_model_parametrization :
  forall p A B r t : Z,
    (p | F28_cubic A B r) ->
    (p | F28_derivative A r) ->
    (p | F28_norm_y r t ^ 2 -
         F28_cubic A B (F28_norm_x r t)).
Proof.
  intros p A B r t Hf Hd.
  pose proof
    (F28_singular_factorization
       p A B r (F28_norm_x r t) Hf Hd) as Hdiff.
  destruct Hdiff as [k Hk].
  exists (-k).
  pose proof (F28_stage9_parametrization r t) as Hparam.
  unfold F28_node_equation in Hparam.
  replace (F28_norm_y r t ^ 2 -
           F28_cubic A B (F28_norm_x r t))
    with ((F28_norm_y r t ^ 2 - F28_factor r (F28_norm_x r t))
          - (F28_cubic A B (F28_norm_x r t)
             - F28_factor r (F28_norm_x r t))) by ring.
  rewrite Hparam, Hk.
  ring.
Qed.

Definition F28_square_mod (p z : Z) : Prop :=
  exists t : Z, (p | t^2 - z).

Definition F28_split_branches (p r : Z) : Prop :=
  exists t : Z,
    (p | F28_norm_x r t - r) /\
    (p | F28_norm_y r t) /\
    ~ (p | t).

Theorem F28_stage10_node_x_identity :
  forall r t : Z,
    F28_norm_x r t - r = t^2 - 3*r.
Proof.
  intros r t. unfold F28_norm_x. ring.
Qed.

Theorem F28_stage10_node_y_identity :
  forall r t : Z,
    F28_norm_y r t = t*(t^2-3*r).
Proof.
  intros r t. unfold F28_norm_y. reflexivity.
Qed.

Theorem F28_stage10_square_gives_node :
  forall p r t : Z,
    (p | t^2 - 3*r) ->
    (p | F28_norm_x r t - r) /\
    (p | F28_norm_y r t).
Proof.
  intros p r t H.
  split.
  - rewrite F28_stage10_node_x_identity. exact H.
  - rewrite F28_stage10_node_y_identity.
    destruct H as [k Hk].
    exists (t*k). rewrite Hk. ring.
Qed.

Theorem F28_stage10_square_nonzero :
  forall p r t : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | t^2 - 3*r) ->
    ~ (p | t).
Proof.
  intros p r t Hp Hr Hsquare Ht.
  apply Hr.
  destruct Hsquare as [k Hk].
  destruct Ht as [j Hj].
  exists (p*j*j-k).
  rewrite Hj in Hk.
  nia.
Qed.

Theorem F28_stage10_split_iff_square :
  forall p r : Z,
    prime p ->
    ~ (p | 3*r) ->
    (F28_split_branches p r <-> F28_square_mod p (3*r)).
Proof.
  intros p r Hp Hr.
  split.
  - intros [t [Hx [Hy Ht]]].
    exists t.
    rewrite <- F28_stage10_node_x_identity.
    exact Hx.
  - intros [t Hsquare].
    exists t.
    destruct (F28_stage10_square_gives_node p r t Hsquare)
      as [Hx Hy].
    repeat split.
    + exact Hx.
    + exact Hy.
    + exact (F28_stage10_square_nonzero p r t Hp Hr Hsquare).
Qed.

Definition F28_congr (p x y : Z) : Prop := (p | x-y).

Lemma F28_congr_refl : forall p x, F28_congr p x x.
Proof.
  intros p x. unfold F28_congr.
  replace (x-x) with 0 by ring.
  exists 0. ring.
Qed.

Lemma F28_congr_sym : forall p x y,
  F28_congr p x y -> F28_congr p y x.
Proof.
  intros p x y H. unfold F28_congr in *.
  destruct H as [k Hk]. exists (-k).
  replace (y-x) with (-(x-y)) by ring.
  rewrite Hk. ring.
Qed.

Lemma F28_congr_trans : forall p x y z,
  F28_congr p x y -> F28_congr p y z -> F28_congr p x z.
Proof.
  intros p x y z H1 H2. unfold F28_congr in *.
  destruct H1 as [k Hk]. destruct H2 as [l Hl].
  exists (k+l).
  replace (x-z) with ((x-y)+(y-z)) by ring.
  rewrite Hk, Hl. ring.
Qed.

Lemma F28_congr_mul : forall p x x' y y',
  F28_congr p x x' -> F28_congr p y y' ->
  F28_congr p (x*y) (x'*y').
Proof.
  intros p x x' y y' H1 H2. unfold F28_congr in *.
  destruct H1 as [k Hk]. destruct H2 as [l Hl].
  exists (k*y+x'*l).
  replace (x*y-x'*y') with ((x-x')*y+x'*(y-y')) by ring.
  rewrite Hk, Hl. ring.
Qed.

Lemma F28_congr_square : forall p x y,
  F28_congr p x y -> F28_congr p (x^2) (y^2).
Proof.
  intros p x y H.
  replace (x^2) with (x*x) by ring.
  replace (y^2) with (y*y) by ring.
  apply F28_congr_mul; exact H.
Qed.

Theorem F28_stage11_product_square :
  forall p a b c r : Z,
    (p | a*r - 3*b*c^2) ->
    F28_congr p ((3*r)*(a*b)) ((3*b*c)^2).
Proof.
  intros p a b c r H.
  unfold F28_congr.
  destruct H as [k Hk].
  exists (3*b*k).
  replace ((3*r)*(a*b)-(3*b*c)^2)
    with ((3*b)*(a*r-3*b*c^2)) by ring.
  rewrite Hk. ring.
Qed.

Theorem F28_stage11_square_transfer :
  forall p z y s w : Z,
    F28_congr p (z*y) (s^2) ->
    F28_congr p (z*w) 1 ->
    F28_square_mod p z ->
    F28_square_mod p y.
Proof.
  intros p z y s w Hprod Hinv [t Ht].
  exists (s*w*t).
  unfold F28_square_mod in *.
  assert (Htz : F28_congr p (t^2) z).
  { unfold F28_congr. exact Ht. }
  assert (Hsqprod : F28_congr p (s^2) (z*y)).
  { apply F28_congr_sym. exact Hprod. }
  assert (Hleft :
    F28_congr p ((s^2)*(w^2)*(t^2)) ((z*y)*(w^2)*z)).
  {
    apply F28_congr_mul.
    - apply F28_congr_mul.
      + exact Hsqprod.
      + apply F28_congr_refl.
    - exact Htz.
  }
  assert (Hinv2 : F28_congr p ((z*w)^2) 1).
  {
    replace 1 with (1^2) by ring.
    apply F28_congr_square. exact Hinv.
  }
  assert (Hright : F28_congr p (y*((z*w)^2)) y).
  {
    replace y with (y*1) at 2 by ring.
    apply F28_congr_mul.
    - apply F28_congr_refl.
    - exact Hinv2.
  }
  assert (Hfinal : F28_congr p ((s*w*t)^2) y).
  {
    eapply F28_congr_trans.
    - replace ((s*w*t)^2) with ((s^2)*(w^2)*(t^2)) by ring.
      exact Hleft.
    - replace ((z*y)*(w^2)*z) with (y*((z*w)^2)) by ring.
      exact Hright.
  }
  unfold F28_congr in Hfinal.
  exact Hfinal.
Qed.

Theorem F28_stage11_split_to_ab :
  forall p a b c r w : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | a*r-3*b*c^2) ->
    (p | (3*r)*w-1) ->
    F28_split_branches p r ->
    F28_square_mod p (a*b).
Proof.
  intros p a b c r w Hp Hr Hbridge Hinv Hsplit.
  apply (F28_stage11_square_transfer
           p (3*r) (a*b) (3*b*c) w).
  - exact (F28_stage11_product_square p a b c r Hbridge).
  - unfold F28_congr. exact Hinv.
  - apply (proj1 (F28_stage10_split_iff_square p r Hp Hr)).
    exact Hsplit.
Qed.

Theorem F28_stage11_ab_to_split :
  forall p a b c r w : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | a*r-3*b*c^2) ->
    (p | (a*b)*w-1) ->
    F28_square_mod p (a*b) ->
    F28_split_branches p r.
Proof.
  intros p a b c r w Hp Hr Hbridge Hinv Hsquare.
  apply (proj2 (F28_stage10_split_iff_square p r Hp Hr)).
  apply (F28_stage11_square_transfer
           p (a*b) (3*r) (3*b*c) w).
  - unfold F28_congr.
    replace ((a*b)*(3*r)-(3*b*c)^2)
      with ((3*r)*(a*b)-(3*b*c)^2) by ring.
    exact (F28_stage11_product_square p a b c r Hbridge).
  - unfold F28_congr. exact Hinv.
  - exact Hsquare.
Qed.

Theorem F28_stage11_split_iff_ab :
  forall p a b c r w1 w2 : Z,
    prime p ->
    ~ (p | 3*r) ->
    (p | a*r-3*b*c^2) ->
    (p | (3*r)*w1-1) ->
    (p | (a*b)*w2-1) ->
    (F28_split_branches p r <-> F28_square_mod p (a*b)).
Proof.
  intros p a b c r w1 w2 Hp Hr Hbridge Hinv1 Hinv2.
  split.
  - apply (F28_stage11_split_to_ab p a b c r w1
             Hp Hr Hbridge Hinv1).
  - apply (F28_stage11_ab_to_split p a b c r w2
             Hp Hr Hbridge Hinv2).
Qed.

Lemma F28_stage12_inverse_from_bezout :
  forall p z : Z,
    Bezout p z 1 -> exists w : Z, (p | z*w-1).
Proof.
  intros p z Hbez.
  destruct Hbez as [u v Huv].
  exists v.
  exists (-u).
  nia.
Qed.

Lemma F28_stage12_inverse_prime :
  forall p z : Z,
    prime p -> ~ (p | z) ->
    exists w : Z, (p | z*w-1).
Proof.
  intros p z Hp Hnz.
  apply F28_stage12_inverse_from_bezout.
  apply rel_prime_bezout.
  apply prime_rel_prime; assumption.
Qed.

Theorem F28_stage12_split_iff_ab :
  forall p a b c r : Z,
    prime p ->
    ~ (p | 3*r) ->
    ~ (p | a*b) ->
    (p | a*r-3*b*c^2) ->
    (F28_split_branches p r <-> F28_square_mod p (a*b)).
Proof.
  intros p a b c r Hp Hr Hab Hbridge.
  destruct (F28_stage12_inverse_prime p (3*r) Hp Hr)
    as [w1 Hw1].
  destruct (F28_stage12_inverse_prime p (a*b) Hp Hab)
    as [w2 Hw2].
  exact (F28_stage11_split_iff_ab
           p a b c r w1 w2 Hp Hr Hbridge Hw1 Hw2).
Qed.

(* ====================================================== *)
(* NEW IN STAGE 13 (written in review by Claude)          *)
(* ====================================================== *)

(* ------------------------------------------------------ *)
(* 13.1  VALUATION FORM OF THE MINIMALITY CRITERION       *)
(* ------------------------------------------------------ *)

(* F28_ppow p k = p^k, for a natural number k. *)

Fixpoint F28_ppow (p : Z) (k : nat) : Z :=
  match k with
  | O => 1
  | S k' => p * F28_ppow p k'
  end.

Lemma F28_ppow_pos :
  forall p : Z,
    1 < p ->
    forall k : nat,
      0 < F28_ppow p k.
Proof.
  intros p Hp k.
  induction k as [|k IH].
  - simpl. lia.
  - simpl.
    apply Z.mul_pos_pos.
    + lia.
    + exact IH.
Qed.

Lemma F28_prime_divides_fourth :
  forall p x : Z,
    prime p ->
    (p | x^4) ->
    (p | x).
Proof.
  intros p x Hp H.
  replace (x^4) with (x*(x*(x*x))) in H by ring.
  destruct (prime_mult p Hp x (x*(x*x)) H) as [H1 | H2].
  - exact H1.
  - destruct (prime_mult p Hp x (x*x) H2) as [H3 | H4].
    + exact H3.
    + destruct (prime_mult p Hp x x H4) as [H5 | H6].
      * exact H5.
      * exact H6.
Qed.

(* One step of the induction: n^4 C = m^4 C', p not dividing C,
   q | n and p q | m give p q | n.  Here u = m/n is the scaling
   factor of a change of coordinates, C = c4 and C' = c4'. *)

Lemma F28_valuation_step :
  forall p C m n C' q : Z,
    prime p ->
    ~ (p | C) ->
    0 < q ->
    n^4*C = m^4*C' ->
    (q | n) ->
    (p*q | m) ->
    (p*q | n).
Proof.
  intros p C m n C' q Hp HC Hq Heq Hqn Hpqm.
  destruct Hqn as [n' Hn].
  destruct Hpqm as [m' Hm].

  assert (Hq4 : q^4 <> 0).
  {
    assert (Hpos : 0 < q^4).
    {
      apply Z.pow_pos_nonneg; lia.
    }
    lia.
  }

  assert (Hmul :
    q^4*(n'^4*C) = q^4*(p^4*m'^4*C')).
  {
    transitivity (n^4*C).
    - rewrite Hn. ring.
    - rewrite Heq. rewrite Hm. ring.
  }

  assert (Hred : n'^4*C = p^4*m'^4*C').
  {
    exact
      (proj1
        (Z.mul_cancel_l
           (n'^4*C) (p^4*m'^4*C') (q^4) Hq4)
        Hmul).
  }

  assert (Hdiv : (p | C*n'^4)).
  {
    exists (p^3*m'^4*C').
    replace (C*n'^4) with (n'^4*C) by ring.
    rewrite Hred.
    ring.
  }

  assert (Hn4 : (p | n'^4)).
  {
    exact (F28_prime_cancel p C (n'^4) Hp HC Hdiv).
  }

  destruct (F28_prime_divides_fourth p n' Hp Hn4)
    as [j Hj].
  exists j.
  rewrite Hn.
  rewrite Hj.
  ring.
Qed.

(* v_p(m) <= v_p(n): every power of p dividing m divides n. *)

Lemma F28_valuation_bound :
  forall p C m n C' : Z,
    prime p ->
    ~ (p | C) ->
    n^4*C = m^4*C' ->
    forall k : nat,
      (F28_ppow p k | m) ->
      (F28_ppow p k | n).
Proof.
  intros p C m n C' Hp HC Heq k.

  assert (Hgt : 1 < p).
  {
    destruct Hp as [Hg _].
    exact Hg.
  }

  induction k as [|k IH].
  - simpl.
    intro H.
    apply Z.divide_1_l.
  - intro Hm.
    simpl in Hm.
    assert (Hqm : (F28_ppow p k | m)).
    {
      destruct Hm as [m' Hm'].
      exists (m'*p).
      rewrite Hm'.
      ring.
    }
    exact
      (F28_valuation_step
         p C m n C' (F28_ppow p k)
         Hp HC (F28_ppow_pos p Hgt k) Heq
         (IH Hqm) Hm).
Qed.

(* ------------------------------------------------------ *)
(* 13.2  REDUCTION TYPE OF AN INTEGRAL MODEL AT p         *)
(*       (Silverman, Ch. VII, section 1, used as the      *)
(*        definition; a model, not Q_p)                   *)
(* ------------------------------------------------------ *)

(* Minimality, in valuation form: a change of coordinates with
   rational scaling u = m/n and c4 = u^4 c4' (c4' an integer)
   has v_p(u) <= 0.  Then Delta = u^12 Delta' gives
   v_p(Delta') = v_p(Delta) - 12 v_p(u) >= v_p(Delta), so no
   change of coordinates lowers the discriminant valuation.
   The last step (Delta = u^12 Delta', valuations of Delta) is
   not formalised here. *)

Definition F28_scaling_minimal (p A : Z) : Prop :=
  forall m n C' : Z,
    n^4*F28_c4 A = m^4*C' ->
    forall k : nat,
      (F28_ppow p k | m) ->
      (F28_ppow p k | n).

(* A node of the reduced curve: a singular point exists, and at
   every singular point (x, y) the tangent cone v^2 - 3 x u^2 is
   nondegenerate (p does not divide 3x). *)

Definition F28_node_reduction (p A B : Z) : Prop :=
  (exists x : Z, F28_reduced_singular p A B x 0) /\
  (forall x y : Z,
     F28_reduced_singular p A B x y ->
     ~ (p | 3*x)).

Definition F28_multiplicative_reduction (p A B : Z) : Prop :=
  F28_scaling_minimal p A /\
  F28_node_reduction p A B.

Definition F28_split_multiplicative (p A B : Z) : Prop :=
  F28_multiplicative_reduction p A B /\
  (forall x y : Z,
     F28_reduced_singular p A B x y ->
     F28_rational_tangent_directions p x).

Definition F28_nonsplit_multiplicative (p A B : Z) : Prop :=
  F28_multiplicative_reduction p A B /\
  (forall x y : Z,
     F28_reduced_singular p A B x y ->
     ~ F28_rational_tangent_directions p x).

Theorem F28_scaling_minimal_model :
  forall p a c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    F28_scaling_minimal p (F28_A a c).
Proof.
  intros p a c Hp Hlarge Ha Hc.
  unfold F28_scaling_minimal.
  intros m n C' Heq k.
  exact
    (F28_valuation_bound
       p (F28_c4 (F28_A a c)) m n C'
       Hp
       (F28_c4_nonzero p a c Hp Hlarge Ha Hc)
       Heq k).
Qed.

(* ------------------------------------------------------ *)
(* 13.3  THE DISCRIMINANT IS NONZERO                      *)
(* ------------------------------------------------------ *)

Theorem F28_discriminant_nonzero :
  forall p a b c : Z,
    prime p ->
    ~ (p | c) ->
    F28_F a b c <> 0 ->
    F28_discriminant (F28_A a c) (F28_B b c) <> 0.
Proof.
  intros p a b c Hp Hc HF Hzero.
  rewrite F28_discriminant_identity in Hzero.

  assert (Hc0 : c <> 0).
  {
    intro H0.
    apply Hc.
    rewrite H0.
    exists 0.
    ring.
  }

  assert (Hc9 : c^9 <> 0).
  {
    apply Z.pow_nonzero.
    - exact Hc0.
    - lia.
  }

  assert (H1024 : -1024*c^9 <> 0).
  {
    intro H.
    apply Z.mul_eq_0 in H.
    destruct H as [H | H].
    - lia.
    - exact (Hc9 H).
  }

  apply Z.mul_eq_0 in Hzero.
  destruct Hzero as [H | H].
  - exact (H1024 H).
  - exact (HF H).
Qed.

(* ------------------------------------------------------ *)
(* 13.4  MULTIPLICATIVE REDUCTION OF THE MODEL            *)
(* ------------------------------------------------------ *)

Theorem F28_model_multiplicative_reduction :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    F28_multiplicative_reduction
      p (F28_A a c) (F28_B b c).
Proof.
  intros p a b c Hp Hlarge Ha Hc HF.
  unfold F28_multiplicative_reduction.
  split.
  - exact
      (F28_scaling_minimal_model
         p a c Hp Hlarge Ha Hc).
  - unfold F28_node_reduction.
    split.
    + destruct
        (F28_double_root_exists
           p a b c Hp Hlarge Ha Hc HF)
        as [r [Hf Hd]].
      exists r.
      exact
        (F28_reduced_singular_intro
           p (F28_A a c) (F28_B b c) r Hf Hd).
    + intros x y Hsing.
      exact
        (proj1
          (proj2
            (F28_reduced_singular_node
               p a b c x y
               Hp Hlarge Ha Hc Hsing))).
Qed.

Theorem F28_model_split_multiplicative_iff :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (F28_split_multiplicative
       p (F28_A a c) (F28_B b c) <->
     F28_square_certificate p (a*b)).
Proof.
  intros p a b c Hp Hlarge Ha Hb Hc HF.

  pose proof
    (F28_model_multiplicative_reduction
       p a b c Hp Hlarge Ha Hc HF)
    as Hmult.

  pose proof Hmult as Hmult0.
  unfold F28_multiplicative_reduction in Hmult.
  unfold F28_node_reduction in Hmult.
  destruct Hmult as [Hmin [[x Hx] Hthree]].

  unfold F28_split_multiplicative.
  split.
  - intros [_ Hdir].
    assert (Hsc : F28_split_node_certificate p x).
    {
      unfold F28_split_node_certificate.
      split.
      - exact (Hthree x 0 Hx).
      - exact (Hdir x 0 Hx).
    }
    exact
      (proj1
        (F28_reduced_node_split_criterion
           p a b c x 0
           Hp Hlarge Ha Hb Hc Hx)
        Hsc).
  - intro Hsq.
    split.
    + exact Hmult0.
    + intros x' y' Hsing.
      pose proof
        (F28_reduced_node_split_criterion
           p a b c x' y'
           Hp Hlarge Ha Hb Hc Hsing)
        as Hcrit.
      pose proof (proj2 Hcrit Hsq) as Hsc.
      unfold F28_split_node_certificate in Hsc.
      exact (proj2 Hsc).
Qed.

Theorem F28_model_nonsplit_multiplicative_iff :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    (F28_nonsplit_multiplicative
       p (F28_A a c) (F28_B b c) <->
     ~ F28_square_certificate p (a*b)).
Proof.
  intros p a b c Hp Hlarge Ha Hb Hc HF.

  pose proof
    (F28_model_multiplicative_reduction
       p a b c Hp Hlarge Ha Hc HF)
    as Hmult.

  pose proof Hmult as Hmult0.
  unfold F28_multiplicative_reduction in Hmult.
  unfold F28_node_reduction in Hmult.
  destruct Hmult as [Hmin [[x Hx] Hthree]].

  unfold F28_nonsplit_multiplicative.
  split.
  - intros [_ Hnot] Hsq.
    apply (Hnot x 0 Hx).
    pose proof
      (F28_reduced_node_split_criterion
         p a b c x 0
         Hp Hlarge Ha Hb Hc Hx)
      as Hcrit.
    pose proof (proj2 Hcrit Hsq) as Hsc.
    unfold F28_split_node_certificate in Hsc.
    exact (proj2 Hsc).
  - intro Hnot.
    split.
    + exact Hmult0.
    + intros x' y' Hsing Hdir.
      apply Hnot.
      pose proof
        (F28_reduced_node_split_criterion
           p a b c x' y'
           Hp Hlarge Ha Hb Hc Hsing)
        as Hcrit.
      apply (proj1 Hcrit).
      unfold F28_split_node_certificate.
      split.
      * exact (Hthree x' y' Hsing).
      * exact Hdir.
Qed.

(* ------------------------------------------------------ *)
(* 13.5  BRANCHES OF THE NORMALIZATION = TANGENT DIRECTIONS *)
(* ------------------------------------------------------ *)

Lemma F28_square_certificate_to_mod :
  forall p z : Z,
    prime p ->
    F28_square_certificate p z ->
    F28_square_mod p z.
Proof.
  intros p z Hp Hcert.
  unfold F28_square_certificate in Hcert.
  destruct Hcert as [u [v [Hu Hc]]].
  destruct (F28_prime_inverse p u Hp Hu) as [w Hw].
  destruct Hc as [k Hk].
  destruct Hw as [l Hl].
  exists (v*w).
  exists (-w^2*k + z*(u*w+1)*l).
  assert (E :
    (-w^2*k + z*(u*w+1)*l)*p =
    -w^2*(k*p) + z*(u*w+1)*(l*p)) by ring.
  rewrite E.
  rewrite <- Hk.
  rewrite <- Hl.
  ring.
Qed.

Lemma F28_square_mod_to_certificate :
  forall p z : Z,
    5 <= p ->
    F28_square_mod p z ->
    F28_square_certificate p z.
Proof.
  intros p z Hlarge Hmod.
  destruct Hmod as [t Ht].
  unfold F28_square_certificate.
  exists 1, t.
  split.
  - apply F28_not_divide_small; lia.
  - replace (z*1^2 - t^2) with (-(t^2 - z)) by ring.
    exact (F28_divide_neg p _ Ht).
Qed.

Theorem F28_branches_iff_tangent_directions :
  forall p r : Z,
    prime p ->
    5 <= p ->
    ~ (p | 3*r) ->
    (F28_split_branches p r <->
     F28_rational_tangent_directions p r).
Proof.
  intros p r Hp Hlarge Hr.
  pose proof
    (F28_stage10_split_iff_square p r Hp Hr) as H1.
  pose proof
    (F28_tangent_square_equivalence p r) as H2.
  pose proof
    (F28_square_certificate_to_mod p (3*r) Hp) as H3.
  pose proof
    (F28_square_mod_to_certificate p (3*r) Hlarge) as H4.
  tauto.
Qed.

(* ------------------------------------------------------ *)
(* 13.6  THE STAGE 13 THEOREM                             *)
(* ------------------------------------------------------ *)

Theorem F28_stage13_multiplicative_reduction :
  forall p a b c : Z,
    prime p ->
    5 <= p ->
    ~ (p | a) ->
    ~ (p | b) ->
    ~ (p | c) ->
    (p | F28_F a b c) ->
    F28_F a b c <> 0 ->
    (p | F28_discriminant (F28_A a c) (F28_B b c))
    /\
    ~ (p | F28_c4 (F28_A a c))
    /\
    F28_discriminant (F28_A a c) (F28_B b c) <> 0
    /\
    F28_multiplicative_reduction
      p (F28_A a c) (F28_B b c)
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       F28_factorization_certificate
         p (F28_A a c) (F28_B b c) x)
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       forall t : Z,
         (p | F28_norm_y x t ^ 2 -
              F28_cubic (F28_A a c) (F28_B b c)
                (F28_norm_x x t)))
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       (F28_split_branches p x <->
        F28_rational_tangent_directions p x))
    /\
    (forall x y : Z,
       F28_reduced_singular
         p (F28_A a c) (F28_B b c) x y ->
       (F28_split_branches p x <->
        F28_square_mod p (a*b)))
    /\
    (F28_split_multiplicative
       p (F28_A a c) (F28_B b c) <->
     F28_square_certificate p (a*b))
    /\
    (F28_nonsplit_multiplicative
       p (F28_A a c) (F28_B b c) <->
     ~ F28_square_certificate p (a*b)).
Proof.
  intros p a b c Hp Hlarge Ha Hb Hc HF HF0.

  assert (Hab : ~ (p | a*b)).
  {
    exact (F28_prime_product_nonzero p a b Hp Ha Hb).
  }

  assert (H1 :
    (p | F28_discriminant (F28_A a c) (F28_B b c))).
  {
    exact (F28_discriminant_vanishes p a b c HF).
  }

  assert (H2 : ~ (p | F28_c4 (F28_A a c))).
  {
    exact (F28_c4_nonzero p a c Hp Hlarge Ha Hc).
  }

  assert (H3 :
    F28_discriminant (F28_A a c) (F28_B b c) <> 0).
  {
    exact (F28_discriminant_nonzero p a b c Hp Hc HF0).
  }

  assert (H4 :
    F28_multiplicative_reduction
      p (F28_A a c) (F28_B b c)).
  {
    exact
      (F28_model_multiplicative_reduction
         p a b c Hp Hlarge Ha Hc HF).
  }

  assert (H5 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      F28_factorization_certificate
        p (F28_A a c) (F28_B b c) x).
  {
    intros x y Hsing.
    destruct
      (F28_reduced_singular_split
         p (F28_A a c) (F28_B b c) x y
         Hp Hlarge Hsing)
      as [Hy [Hf Hd]].
    destruct
      (F28_reduced_singular_node
         p a b c x y Hp Hlarge Ha Hc Hsing)
      as [Hx [Hthree Htan]].
    exact
      (F28_stage8_factorization
         p (F28_A a c) (F28_B b c) x
         Hp Hthree Hf Hd).
  }

  assert (H6 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      forall t : Z,
        (p | F28_norm_y x t ^ 2 -
             F28_cubic (F28_A a c) (F28_B b c)
               (F28_norm_x x t))).
  {
    intros x y Hsing t.
    destruct
      (F28_reduced_singular_split
         p (F28_A a c) (F28_B b c) x y
         Hp Hlarge Hsing)
      as [Hy [Hf Hd]].
    exact
      (F28_stage9_reduced_model_parametrization
         p (F28_A a c) (F28_B b c) x t Hf Hd).
  }

  assert (H7 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      (F28_split_branches p x <->
       F28_rational_tangent_directions p x)).
  {
    intros x y Hsing.
    destruct
      (F28_reduced_singular_node
         p a b c x y Hp Hlarge Ha Hc Hsing)
      as [Hx [Hthree Htan]].
    exact
      (F28_branches_iff_tangent_directions
         p x Hp Hlarge Hthree).
  }

  assert (H8 :
    forall x y : Z,
      F28_reduced_singular
        p (F28_A a c) (F28_B b c) x y ->
      (F28_split_branches p x <->
       F28_square_mod p (a*b))).
  {
    intros x y Hsing.
    destruct
      (F28_reduced_singular_split
         p (F28_A a c) (F28_B b c) x y
         Hp Hlarge Hsing)
      as [Hy [Hf Hd]].
    destruct
      (F28_reduced_singular_node
         p a b c x y Hp Hlarge Ha Hc Hsing)
      as [Hx [Hthree Htan]].
    exact
      (F28_stage12_split_iff_ab
         p a b c x Hp Hthree Hab
         (F28_singular_linear_relation
            p a b c x Hp Hlarge Hc Hf Hd)).
  }

  assert (H9 :
    F28_split_multiplicative
      p (F28_A a c) (F28_B b c) <->
    F28_square_certificate p (a*b)).
  {
    exact
      (F28_model_split_multiplicative_iff
         p a b c Hp Hlarge Ha Hb Hc HF).
  }

  assert (H10 :
    F28_nonsplit_multiplicative
      p (F28_A a c) (F28_B b c) <->
    ~ F28_square_certificate p (a*b)).
  {
    exact
      (F28_model_nonsplit_multiplicative_iff
         p a b c Hp Hlarge Ha Hb Hc HF).
  }

  exact
    (conj H1
      (conj H2
        (conj H3
          (conj H4
            (conj H5
              (conj H6
                (conj H7
                  (conj H8
                    (conj H9 H10))))))))).
Qed.

(* ------------------------------------------------------ *)
(* COMPILER AND ASSUMPTION CHECKS                         *)
(* ------------------------------------------------------ *)

Check F28_valuation_bound.
Check F28_scaling_minimal_model.
Check F28_discriminant_nonzero.
Check F28_model_multiplicative_reduction.
Check F28_model_split_multiplicative_iff.
Check F28_model_nonsplit_multiplicative_iff.
Check F28_branches_iff_tangent_directions.
Check F28_stage13_multiplicative_reduction.

Print Assumptions F28_stage13_multiplicative_reduction.
